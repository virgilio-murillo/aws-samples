"""Step 3b: Control test with a real JPEG image."""
import boto3
from PIL import Image
import io

# Create a real 8x8 JPEG in memory
img = Image.new("RGB", (8, 8), color=(100, 150, 200))
buf = io.BytesIO()
img.save(buf, format="JPEG")
jpeg_bytes = buf.getvalue()
print(f"Downloaded {len(jpeg_bytes)} bytes, magic: {jpeg_bytes[:3].hex()}")

MODEL_ID = "eu.anthropic.claude-haiku-4-5-20251001-v1:0"
client = boto3.client("bedrock-runtime", region_name="eu-central-1")

def call_converse(fmt, image_bytes, label):
    print(f"\nTEST: {label}")
    try:
        resp = client.converse(
            modelId=MODEL_ID,
            messages=[{"role": "user", "content": [
                {"text": "Describe this image in one sentence."},
                {"image": {"format": fmt, "source": {"bytes": image_bytes}}}
            ]}],
            inferenceConfig={"maxTokens": 50}
        )
        print(f"  SUCCESS: {resp['output']['message']['content'][0]['text'][:100]}")
    except Exception as e:
        print(f"  ERROR: {e}")

call_converse("webp", jpeg_bytes, "MISMATCH: real JPEG + webp format")
call_converse("jpeg", jpeg_bytes, "CONTROL: real JPEG + jpeg format")
