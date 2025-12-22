# Stability AI Conservative Upscale with boto3

This project demonstrates how to successfully invoke the Stability AI Conservative Upscale model using boto3 and Amazon Bedrock.

## Model Information
- **Model ID**: `stability.stable-conservative-upscale-v1:0`
- **Inference Profile**: `us.stability.stable-conservative-upscale-v1:0` (Required!)
- **Available Regions**: us-east-1, us-east-2, us-west-2
- **Purpose**: Upscales images 20-40x while preserving quality

## Files Created

1. **`requirements.txt`** - Python dependencies
2. **`create_test_image.py`** - Creates a sample test image
3. **`stability_upscale.py`** - Main implementation script
4. **`complete_demo.py`** - Comprehensive demonstration with full documentation
5. **`README.md`** - This documentation file

## Key Steps to Success

### 1. Research & Discovery
- Searched AWS documentation for Stability AI models
- Found the model in the supported models list
- Discovered that direct model invocation is not supported

### 2. Inference Profile Requirement
- **Critical**: Must use inference profile `us.stability.stable-conservative-upscale-v1:0`
- Cannot invoke the model directly with `stability.stable-conservative-upscale-v1:0`
- Found this by listing available inference profiles with AWS CLI

### 3. Dependencies Installation
```bash
pip install boto3 pillow
```

### 4. Image Requirements
- Input image: 64x64 to 1 megapixel
- Supported formats: JPEG, PNG, WebP
- Must be base64 encoded for API call
- Aspect ratio: 1:2.5 to 2.5:1

### 5. Required Parameters
- **`image`**: Base64 encoded image data
- **`prompt`**: Description of desired output (required)
- **`creativity`**: 0.1-0.5 (default 0.35, controls enhancement level)
- **`output_format`**: jpeg, png, or webp

## Usage

### Quick Start
```bash
python complete_demo.py
```

### Basic Usage
```python
import boto3
import base64
import json
from PIL import Image
import io

# Initialize client
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# Prepare image
with open("input.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# Parameters
params = {
    "image": image_base64,
    "prompt": "High-quality upscaled version with enhanced details",
    "creativity": 0.30,
    "output_format": "png"
}

# Invoke model
response = bedrock.invoke_model(
    modelId="us.stability.stable-conservative-upscale-v1:0",
    body=json.dumps(params)
)

# Process response
result = json.loads(response["body"].read())
image_data = base64.b64decode(result["images"][0])
Image.open(io.BytesIO(image_data)).save("upscaled.png")
```

## Results Achieved

- ✅ Successfully invoked the model
- ✅ Upscaled 200x200 image to 3112x3112 (15.6x scale factor)
- ✅ Generated high-quality PNG output
- ✅ Preserved image quality with conservative upscaling

## Troubleshooting

### Common Issues

1. **ValidationException: on-demand throughput isn't supported**
   - **Solution**: Use inference profile `us.stability.stable-conservative-upscale-v1:0` instead of direct model ID

2. **Image size errors**
   - **Solution**: Ensure image is between 64x64 and 1 megapixel

3. **Missing prompt**
   - **Solution**: Always include a descriptive prompt parameter

## AWS CLI Commands Used

```bash
# Check AWS credentials
aws sts get-caller-identity

# List available inference profiles
aws bedrock list-inference-profiles --region us-east-1

# Check regional availability
aws bedrock list-foundation-models --region us-east-1
```

## Architecture

```
Input Image (200x200) 
    ↓ (base64 encode)
Amazon Bedrock Runtime API
    ↓ (invoke_model)
Stability AI Conservative Upscale
    ↓ (inference profile)
Output Image (3112x3112)
    ↓ (base64 decode)
Saved PNG File
```

## Cost Considerations

- Conservative Upscale is part of Stability AI Image Services
- Pricing is per image processed
- Check AWS Bedrock pricing for current rates

## Next Steps

- Try different creativity values (0.1-0.5)
- Test with different image sizes and formats
- Explore other Stability AI Image Services (Creative Upscale, Fast Upscale)
- Implement batch processing for multiple images
