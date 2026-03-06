"""Step 4: Reproduce via LangChain — JPEG bytes with data:image/webp;base64 URL.
This simulates a customer passing a JPEG image with a wrong webp media type declaration.
"""
import base64, io
from PIL import Image
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage

# Create real 8x8 JPEG
img = Image.new("RGB", (8, 8), color=(100, 150, 200))
buf = io.BytesIO()
img.save(buf, format="JPEG")
jpeg_b64 = base64.b64encode(buf.getvalue()).decode()

MODEL_ID = "eu.anthropic.claude-haiku-4-5-20251001-v1:0"
REGION = "eu-central-1"
model = ChatBedrockConverse(model=MODEL_ID, region_name=REGION, max_tokens=50)

def test_langchain(media_type, label):
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    data_url = f"data:{media_type};base64,{jpeg_b64}"
    msg = HumanMessage(content=[
        {"type": "text", "text": "Describe this image."},
        {"type": "image_url", "image_url": {"url": data_url}},
    ])
    try:
        resp = model.invoke([msg])
        print(f"  SUCCESS: {resp.content[:100] if isinstance(resp.content, str) else resp.content}")
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")

# Test 1: MISMATCH — JPEG bytes declared as webp via data URL
test_langchain("image/webp", "MISMATCH: JPEG bytes + data:image/webp via LangChain")

# Test 2: CONTROL — JPEG bytes declared correctly
test_langchain("image/jpeg", "CONTROL: JPEG bytes + data:image/jpeg via LangChain")
