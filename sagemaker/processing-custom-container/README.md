# SageMaker Processing with Custom Container for Anomaly Detection

This example demonstrates how to run anomaly detection using SageMaker Processing with a custom Docker container. The solution implements region-level breach detection using the RRCF (Robust Random Cut Forest) algorithm.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Synthetic     │    │   SageMaker      │    │  Output Data    │
│   Data Gen      │───▶│   Processing     │───▶│  (S3 Bucket)    │
│                 │    │   Job            │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Custom Docker   │
                       │  Container       │
                       │  (ECR)           │
                       └──────────────────┘
```

## Features

- **Self-Contained**: Generates synthetic data automatically - no external files needed
- **Custom Docker Container**: Uses Python 3.10 with scientific computing libraries
- **Anomaly Detection**: Implements RRCF algorithm for breach detection
- **SageMaker Integration**: Fully compatible with SageMaker Processing jobs
- **Scalable Processing**: Handles large datasets with parallel processing
- **End-to-End Workflow**: From data generation to production deployment

## Prerequisites

- AWS CLI configured with appropriate permissions
- Docker installed and running
- Python 3.8+ with Jupyter notebook support
- SageMaker execution role with ECR and S3 permissions

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/virgilio-murillo/aws-samples.git
   cd aws-samples/sagemaker/processing-custom-container
   ```

2. **Run the complete workflow**:
   Open `anomaly-detection-processing.ipynb` and execute all cells sequentially.
   
   **That's it!** The notebook will:
   - Generate synthetic data automatically
   - Test the algorithm locally
   - Build and test Docker container
   - Deploy to SageMaker Processing
   - Download and verify results

## What the Notebook Does

### Step 1: Generate Synthetic Data
- Creates 6,018 rows of realistic data matching the original structure
- Ensures sufficient data for the target analysis date (2025-11-08)
- No external files or manual data preparation needed

### Step 2: Local Testing
- Installs required dependencies automatically
- Runs anomaly detection algorithm locally
- Generates breach detection results

### Step 3: Docker Container
- Builds multi-architecture container for SageMaker
- Tests container locally with synthetic data
- Verifies output format and results

### Step 4: SageMaker Processing
- Creates ECR repository and pushes container
- Sets up S3 bucket and uploads data
- Creates and monitors processing job
- Downloads final results

## Data Structure

The synthetic data includes these columns:
- `marketplace_set`: Market identifier (string)
- `marketplace_id`: Numeric market ID (int64)
- `snapshot_week`: Analysis date (datetime)
- `sortability`: Product classification (string)
- `iog_type`: Fulfillment type (string)
- `destination_zip_assigned_region`: Geographic region (string)
- `inregion_units`: Regional unit count (int64)
- `total_units`: Total unit count (int64)
- `metric_new`: Performance metric (float64)

## Output Format

The processing generates breach detection results with:
- `breach`: Binary anomaly indicator (0/1)
- `anomaly_score`: RRCF algorithm score
- `Impact`: Calculated business impact
- All original input columns preserved

## Local Testing Only

If you want to test just the algorithm without SageMaker:

```bash
# Install dependencies
pip install pandas joblib numpy rrcf scipy pyarrow swifter

# Run the processing script directly
python standalone_region_training_test.py --dataset_date "2025-11-08" --output_path "./output"
```

## Cost Optimization

- Uses `ml.m5.large` instances by default (adjust based on data size)
- Processing job runs only when needed
- Automatic cleanup of temporary resources
- Synthetic data eliminates data transfer costs

## Security

- IAM roles follow least privilege principle
- ECR repositories use private access
- S3 buckets created with appropriate permissions
- No sensitive data required

## Troubleshooting

**Notebook cells fail**: Ensure all cells are run in sequence from top to bottom.

**Docker build fails**: Ensure Docker Desktop is running and you have sufficient disk space.

**ECR push fails**: Check AWS credentials and ECR permissions.

**Processing job fails**: Check CloudWatch logs for detailed error messages.

**Output validation fails**: Verify the synthetic data generation completed successfully.

## Files Structure

```
├── anomaly-detection-processing.ipynb  # Main self-contained notebook
├── Dockerfile                         # Container definition
├── requirements.txt                   # Python dependencies
├── standalone_region_training_test.py # Processing script
└── README.md                          # This file
```

## Contributing

Please read the main repository's contributing guidelines before submitting pull requests.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
