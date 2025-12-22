import boto3
import base64
import json
from PIL import Image
import io

def upscale_image_with_stability_ai():
    """
    Invoke Stability AI Conservative Upscale model using boto3
    """
    # Configuration
    region = "us-east-1"
    model_id = "us.stability.stable-conservative-upscale-v1:0"  # Using inference profile
    input_image_path = "test_input.jpg"
    output_image_path = "upscaled_output.png"
    
    # Initialize Bedrock client
    bedrock = boto3.client("bedrock-runtime", region_name=region)
    
    try:
        # Read and encode the input image
        with open(input_image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Prepare the request parameters
        params = {
            "image": image_base64,
            "prompt": "A high-quality upscaled version of this image with enhanced details",
            "creativity": 0.30,
            "output_format": "png"
        }
        
        # Convert parameters to JSON
        request_body = json.dumps(params)
        
        print(f"Invoking model: {model_id}")
        print(f"Region: {region}")
        print(f"Input image: {input_image_path}")
        
        # Invoke the model
        response = bedrock.invoke_model(
            modelId=model_id,
            body=request_body
        )
        
        # Parse the response
        model_response = json.loads(response["body"].read())
        
        # Extract the base64 image data
        base64_image_data = model_response["images"][0]
        
        if not base64_image_data:
            raise ValueError("No image data found in model response.")
        
        # Decode and save the image
        image_data = base64.b64decode(base64_image_data)
        image = Image.open(io.BytesIO(image_data))
        image.save(output_image_path)
        
        print(f"Successfully saved upscaled image to: {output_image_path}")
        print(f"Original image size: {Image.open(input_image_path).size}")
        print(f"Upscaled image size: {image.size}")
        
        # Print response metadata
        if "seeds" in model_response:
            print(f"Seeds used: {model_response['seeds']}")
        if "finish_reasons" in model_response:
            print(f"Finish reasons: {model_response['finish_reasons']}")
            
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = upscale_image_with_stability_ai()
    if success:
        print("\n✅ Successfully invoked Stability AI Conservative Upscale model!")
    else:
        print("\n❌ Failed to invoke the model.")
