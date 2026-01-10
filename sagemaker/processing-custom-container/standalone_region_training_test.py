#!/usr/bin/env python3
"""
Standalone script for region-level breach detection model training and inference.
Test version with local paths.
"""

import argparse
import glob
import os
import logging
import numpy as np
import pandas as pd
import rrcf
from joblib import Parallel, delayed

# Constants
NONE_VALUE = "None"
PATH_SEPARATOR = "/"
ANY_WILD_CARD = "*"
PARQUET_EXTENSION = ".parquet"
IRIS_REGION_LEVEL_BREACH_OUTPUT_FILENAME = "iris_region_breach_output"
MIN_DATA_DATE = '2025-01-01'
NUM_TREES = 100
MAX_TREE_SIZE = 256
MIN_GROUP_COUNT = 12
CUM_PERC_THRESHOLD = 0.99
IMPACT_MULTIPLIER = 10000
BATCH_SIZE = 20
NUM_JOBS = 40

# Logger setup
logger = logging.Logger("IRIS")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
stream.setFormatter(formatter)
logger.addHandler(stream)

def get_metric(num, denom):
    """Calculate a metric based on numerator and denominator."""
    return num / denom if denom != 0 else 0

def prepare_region_data(df):
    """Prepare data for region analysis."""
    logger.info(f"Input dataframe shape for region data preparation: {df.shape}")
    df_model = df[df['snapshot_week'] >= MIN_DATA_DATE].reset_index(drop=True)
    logger.info(f"After filtering by MIN_DATA_DATE ({MIN_DATA_DATE}): {df_model.shape}")
    
    df_model['Region'] = df_model['destination_zip_assigned_region'].str.replace(r'^US\.', '', regex=True)
    
    df_final = df_model.groupby(['marketplace_set', 'snapshot_week', 'Region', 'iog_type', 'sortability'])[
        ['inregion_units', 'total_units']].sum().reset_index()
    
    df_final['iris'] = df_final.apply(lambda x: get_metric(x['inregion_units'], x['total_units']), axis=1)
    df_final['cohort'] = df_final['Region'] + '_' + df_final['iog_type'] + '_' + df_final['sortability']
    
    logger.info(f"Final prepared dataframe shape: {df_final.shape}")
    logger.info('Data Preparation for Region completed')
    return df_final

def get_latest_data(preprocessed_df, dataset_date):
    """Get the latest data for analysis."""
    logger.info(f"Getting latest data for dataset_date: {dataset_date}")
    raw_df = preprocessed_df[['snapshot_week', 'marketplace_set', 'cohort', 'inregion_units', 'total_units']]
    grouped_df = raw_df.groupby(['snapshot_week', 'marketplace_set', 'cohort']).sum().reset_index()
    grouped_df['IRIS'] = grouped_df.apply(lambda x: get_metric(x['inregion_units'], x['total_units']), axis=1)
    logger.info(f"Grouped dataframe shape: {grouped_df.shape}")

    group_count = grouped_df.groupby(['cohort'])['snapshot_week'].nunique().reset_index()
    group_count.columns = ['cohort', 'group_count']
    logger.info(f"Group count dataframe shape: {group_count.shape}")

    merged_df = grouped_df.merge(group_count, on='cohort', how='left').reset_index(drop=True)
    df_with_subcat_count = merged_df[~(merged_df['cohort'].isin(['Unknown']))].reset_index(drop=True)
    logger.info(f"After removing Unknown cohorts: {df_with_subcat_count.shape}")
    
    recent_df = df_with_subcat_count[df_with_subcat_count['snapshot_week'].astype(str) == dataset_date].sort_values(by=['cohort', 'total_units'])
    recent_df = recent_df.drop_duplicates(subset=['cohort'], keep='last')
    logger.info(f"Recent dataframe before group count filter: {recent_df.shape}")
    
    final_recent_df = recent_df[recent_df['group_count'] > MIN_GROUP_COUNT].reset_index(drop=True)
    logger.info(f"Final recent dataframe after MIN_GROUP_COUNT filter ({MIN_GROUP_COUNT}): {final_recent_df.shape}")

    logger.info("Recent week data consolidation completed")
    return final_recent_df, df_with_subcat_count

def get_processed_data(recent_df, df_with_subcat_count):
    """Process data for model training."""
    logger.info(f"Processing data - recent_df shape: {recent_df.shape}, df_with_subcat_count shape: {df_with_subcat_count.shape}")
    
    top_df = recent_df[['cohort', 'total_units']].groupby('cohort').sum().reset_index()
    top_df = top_df.sort_values('total_units', ascending=False).reset_index(drop=True)
    top_df['cum_units'] = top_df['total_units'].cumsum()
    top_df['cum_perc'] = top_df['cum_units'] / top_df['total_units'].sum()
    logger.info(f"Top dataframe shape: {top_df.shape}")

    filtered_cohorts = top_df[top_df['cum_perc'] < CUM_PERC_THRESHOLD]['cohort']
    logger.info(f"Number of cohorts after CUM_PERC_THRESHOLD filter ({CUM_PERC_THRESHOLD}): {len(filtered_cohorts)}")
    
    filtered_df = df_with_subcat_count[df_with_subcat_count['cohort'].isin(filtered_cohorts)].reset_index(drop=True)
    logger.info(f"Filtered dataframe shape: {filtered_df.shape}")

    processed_df = filtered_df[['snapshot_week', 'cohort', 'IRIS']].drop_duplicates().copy()
    processed_df['snapshot_date'] = pd.to_datetime(processed_df['snapshot_week'])
    processed_df = processed_df.sort_values(['cohort', 'snapshot_date']).reset_index(drop=True)
    logger.info(f"Processed dataframe before diff calculation: {processed_df.shape}")

    processed_df['diffs'] = processed_df['IRIS'].diff()
    processed_df.loc[processed_df['cohort'] != processed_df['cohort'].shift(1), 'diffs'] = np.nan
    processed_df = processed_df.dropna()
    logger.info(f"Processed dataframe after diff calculation and dropna: {processed_df.shape}")

    median_iris = processed_df.groupby('cohort')['IRIS'].median().reset_index()
    median_iris.columns = ['cohort', 'median_IRIS']
    processed_df = processed_df.merge(median_iris, on='cohort', how='left')
    logger.info(f"Final processed dataframe shape: {processed_df.shape}")

    logger.info("Processing data completed")
    return processed_df

def train_rrcf_for_group(group_data):
    """Train Robust Random Cut Forest (RRCF) model for anomaly detection on group data."""
    cohort_name = group_data['cohort'].iloc[0] if not group_data.empty else 'Unknown'
    logger.info(f"Training RRCF for cohort: {cohort_name}, data points: {len(group_data)}")
    
    num_trees = NUM_TREES
    tree_size = min(MAX_TREE_SIZE, len(group_data))
    logger.info(f"Using {num_trees} trees with max size {tree_size}")

    forest = []
    for _ in range(num_trees):
        tree = rrcf.RCTree()
        forest.append(tree)

    points = group_data[['IRIS', 'diffs']].values
    anomaly_scores = pd.Series(0.0, index=group_data.index)
    logger.info(f"Processing {len(points)} data points")

    for index, point in enumerate(points):
        for tree in forest:
            if len(tree.leaves) > tree_size:
                tree.forget_point(index - tree_size)
            tree.insert_point(point, index=index)
            score = tree.codisp(index)
            anomaly_scores.iloc[index] += score / num_trees

    group_data['anomaly_score'] = anomaly_scores
    median_value = group_data['IRIS'].median()
    threshold = group_data['anomaly_score'].median()
    logger.info(f"Median IRIS: {median_value:.4f}, Anomaly threshold: {threshold:.4f}")
    
    anomalies = group_data[(group_data['anomaly_score'] > threshold) & (group_data['diffs'] < 0)]
    logger.info(f"Found {len(anomalies)} anomalies")

    latest_week = group_data['snapshot_date'].max()
    group_data['breach'] = 0
    if not anomalies.empty:
        breach_indices = group_data[
            (group_data['snapshot_date'] == latest_week) &
            (group_data['IRIS'] < median_value) &
            (group_data['anomaly_score'] > threshold)
            ].index
        group_data.loc[breach_indices, 'breach'] = 1
        logger.info(f"Marked {len(breach_indices)} breaches for latest week")
    else:
        logger.info("No breaches detected for latest week")

    return group_data

def process_group(process_df, group):
    """Process a single cohort group by filtering data and training RRCF model."""
    group_data = process_df[process_df['cohort'] == group].reset_index(drop=True)
    logger.info(f'Processing cohort: {group}, Cohort size: {len(group_data)} records')
    return train_rrcf_for_group(group_data)

def get_predictions(process_df, cohorts):
    """Generate predictions using parallel processing."""
    logger.info(f"Starting parallel processing for {len(cohorts)} cohorts using {NUM_JOBS} jobs")
    results = Parallel(n_jobs=NUM_JOBS, batch_size=BATCH_SIZE)(delayed(process_group)(process_df, cohort) for cohort in cohorts)
    final_results = pd.concat(results).reset_index(drop=True)
    logger.info(f"Completed parallel processing, final results shape: {final_results.shape}")
    return final_results

def get_breach_data(final_anomalies, recent_df, cohorts, df, dataset_date):
    """Get breach data for reporting."""
    logger.info(f"Generating breach data for {len(cohorts)} cohorts")
    
    latest_date = final_anomalies['snapshot_date'].max()
    logger.info(f"Latest date in anomalies: {latest_date}")
    
    breach_status = final_anomalies[final_anomalies['snapshot_date'] == latest_date].reset_index(drop=True)
    final_data = breach_status[['cohort', 'median_IRIS', 'anomaly_score', 'breach']]
    logger.info(f"Breach status data shape: {breach_status.shape}")

    recent_df['Bridge_Units'] = recent_df['total_units'] - recent_df['inregion_units']
    recent_df['Total_MP'] = df[df['snapshot_week'].astype(str) == dataset_date]['total_units'].sum()
    recent_df['Impact'] = (recent_df['Bridge_Units'] / recent_df['Total_MP']) * IMPACT_MULTIPLIER
    logger.info(f"Calculated impact metrics, Total_MP: {recent_df['Total_MP'].iloc[0] if not recent_df.empty else 0}")

    final_breach_df = recent_df[recent_df['cohort'].isin(cohorts)].reset_index(drop=True)
    result = final_breach_df.merge(final_data, on='cohort').reset_index(drop=True)
    logger.info(f"Final breach data shape: {result.shape}")
    
    return result

def process_mp_set_region(mp_set: str, dataset_date: str, df: pd.DataFrame) -> pd.DataFrame:
    """Process region level data for a marketplace set."""
    logger.info(f"Processing Region Level - marketplace_set: {mp_set}")
    preprocessed_region_level_df = prepare_region_data(df)

    logger.info(f"Region Level: Processed region level dataframe shape: {preprocessed_region_level_df.shape}")

    recent_df, df_with_subcat_count = get_latest_data(preprocessed_region_level_df, dataset_date)
    logger.info(f"Region Level: Recent dataframe shape: {recent_df.shape}")

    processed_df = get_processed_data(recent_df, df_with_subcat_count)
    logger.info(f"Region Level: Processed dataframe shape: {processed_df.shape}")

    cohorts = processed_df['cohort'].unique()
    logger.info(f"Region Level: Number of cohorts: {len(cohorts)}")

    final_anomalies = get_predictions(processed_df, cohorts)
    final_data = get_breach_data(final_anomalies, recent_df, cohorts, df, dataset_date)
    logger.info(f"Completed region-level breach detection for marketplace_set: {mp_set}")
    return final_data

def train_inference_region_level():
    """Execute region-level breach detection model training and inference."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_date", dest="dataset_date", type=str, default=NONE_VALUE)
    parser.add_argument("--input_path", dest="input_path", type=str, default="./input")
    parser.add_argument("--output_path", dest="output_path", type=str, default="./output")
    args, _ = parser.parse_known_args()
    logger.info(f"Running region-level breach model for dataset date: {args.dataset_date}")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_path, exist_ok=True)
    
    # Hardcoded input file path
    input_file_path = "/opt/ml/processing/input/data.parquet"
    output_file_path = "/opt/ml/processing/output/" + IRIS_REGION_LEVEL_BREACH_OUTPUT_FILENAME + PARQUET_EXTENSION

    df = pd.read_parquet(input_file_path)
    logger.info(f"Input dataframe shape: {df.shape}")

    mp_set_list = df["marketplace_set"].unique()
    breach_output_df = pd.DataFrame()

    for mp_set in mp_set_list:
        mp_set_df = df[df["marketplace_set"] == mp_set].reset_index(drop=True)
        logger.info(f"Running for marketplace set: {mp_set} with {mp_set_df.shape[0]} records")
        mp_set_breach_df = process_mp_set_region(mp_set, args.dataset_date, mp_set_df)
        breach_output_df = pd.concat([breach_output_df, mp_set_breach_df])

    logger.info(f"Output dataframe shape: {breach_output_df.shape}")
    breach_output_df.to_parquet(output_file_path, index=False)
    logger.info("Completed processing all marketplace sets")

if __name__ == "__main__":
    train_inference_region_level()