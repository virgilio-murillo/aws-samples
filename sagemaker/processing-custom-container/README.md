# SageMaker Processing with Custom Container for Anomaly Detection

This example demonstrates how to run anomaly detection using SageMaker Processing with a custom Docker container. The solution implements region-level breach detection using the RRCF (Robust Random Cut Forest) algorithm.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Input Data    │    │   SageMaker      │    │  Output Data    │
│   (S3 Bucket)   │───▶│   Processing     │───▶│  (S3 Bucket)    │
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

- **Custom Docker Container**: Uses Python 3.10 with scientific computing libraries
- **Anomaly Detection**: Implements RRCF algorithm for breach detection
- **SageMaker Integration**: Fully compatible with SageMaker Processing jobs
- **Scalable Processing**: Handles large datasets with parallel processing
- **End-to-End Workflow**: From local testing to production deployment

## Prerequisites

- AWS CLI configured with appropriate permissions
- Docker installed and running
- Python 3.8+ with required libraries
- SageMaker execution role with ECR and S3 permissions

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aws-samples/aws-samples.git
   cd aws-samples/sagemaker/processing-custom-container
   ```

2. **Run the complete workflow**:
   Open `anomaly-detection-processing.ipynb` and execute all cells sequentially.

## Input Data Format

The processing script expects a Parquet file with the following columns:
- `snapshot_week`: Date column (datetime)
- `marketplace_set`: String identifier
- `cohort`: String identifier for grouping
- `inregion_units`: Integer count
- `total_units`: Integer count
- Additional columns as required by the algorithm

## Output Format

The processing job generates a Parquet file with breach detection results:
- `breach`: Binary indicator (0/1) for anomaly detection
- `anomaly_score`: Numerical score from RRCF algorithm
- `Impact`: Calculated impact metric
- All original input columns preserved

## Files Structure

```
├── anomaly-detection-processing.ipynb  # Main notebook with complete workflow
├── Dockerfile                         # Container definition
├── requirements.txt                   # Python dependencies
├── standalone_region_training_test.py # Processing script
└── README.md                          # This file
```

## Local Testing

Test the Docker container locally before deploying:

```bash
# Build the container
docker buildx build --platform linux/amd64 -t sagemaker-processing-test .

# Test with sample data
mkdir -p test-input test-output
cp your-data.parquet ./test-input/data.parquet

docker run --rm \
  -v $(pwd)/test-input:/opt/ml/processing/input \
  -v $(pwd)/test-output:/opt/ml/processing/output \
  sagemaker-processing-test \
  --dataset_date "2025-11-08" --output_path "/opt/ml/processing/output"
```

## SageMaker Processing Job

The notebook automatically:
1. Creates ECR repository and pushes the Docker image
2. Creates S3 bucket and uploads input data
3. Creates and monitors the SageMaker processing job
4. Downloads and validates the results

## Cost Optimization

- Uses `ml.m5.large` instances by default (adjust based on data size)
- Processing job runs only when needed
- Automatic cleanup of temporary resources

## Security

- IAM roles follow least privilege principle
- ECR repositories use private access
- S3 buckets created with appropriate permissions

## Troubleshooting

**Docker build fails**: Ensure Docker Desktop is running and you have sufficient disk space.

**ECR push fails**: Check AWS credentials and ECR permissions.

**Processing job fails**: Check CloudWatch logs for detailed error messages.

**Output validation fails**: Verify input data format matches expected schema.

## Contributing

Please read the main repository's contributing guidelines before submitting pull requests.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
