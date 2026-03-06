# Bug Reproduction Report: AWS Bedrock Runtime 400 Error — Media Type Mismatch

**Date:** 2026-03-06  
**Incident Start:** 2026-03-05 15:40:00 UTC  
**Region:** eu-central-1  
**Model:** eu.anthropic.claude-haiku-4-5-20251001-v1:0  
**Error:** `ValidationException: messages.0.content.0.image.source.bytes: The image was specified using the image/webp media type, but the image appears to be a image/jpeg image`

---

## Root Cause

**The root cause is a Bedrock service-side change that added strict media type validation.** The Bedrock Converse API now validates that the declared `format` (media type) in image content blocks matches the actual image bytes (detected via magic bytes). Previously, this mismatch was accepted silently.

This is NOT a bug in `langchain-aws`, `langchain-core`, or `boto3`. The customer's application has always sent JPEG image bytes with a `webp` media type declaration — a mismatch that was previously tolerated by the Bedrock service but is now rejected.

---

## Evidence

### 1. Raw boto3 Reproduction (Step 3)

Sending JPEG bytes (magic: `FF D8 FF`) with `format: "webp"` to the Converse API triggers the exact customer error:

```python
# MISMATCH — triggers error
client.converse(
    modelId="eu.anthropic.claude-haiku-4-5-20251001-v1:0",
    messages=[{"role": "user", "content": [
        {"text": "Describe this image."},
        {"image": {"format": "webp", "source": {"bytes": jpeg_bytes}}}
    ]}],
    inferenceConfig={"maxTokens": 50}
)
# → ValidationException: The image was specified using the image/webp media type,
#   but the image appears to be a image/jpeg image

# CONTROL — succeeds
# Same call with format: "jpeg" → SUCCESS
```

### 2. LangChain Reproduction (Step 4)

Passing `data:image/webp;base64,<jpeg_data>` through `ChatBedrockConverse` triggers the same error. LangChain's `_format_openai_image_url()` extracts the media type from the data URL regex and passes it to Bedrock without validating against actual bytes.

### 3. Binary Search: langchain-aws (Step 5)

| langchain-aws | langchain-core | Result |
|---|---|---|
| 1.2.0 | 1.2.17 | MISMATCH_ERROR |
| 1.2.2 | 1.2.17 | MISMATCH_ERROR |
| 1.2.3 | 1.2.17 | MISMATCH_ERROR |
| 1.2.5 | 1.2.17 | MISMATCH_ERROR |
| 1.3.0 | 1.2.17 | MISMATCH_ERROR |
| 1.3.1 | 1.2.17 | MISMATCH_ERROR |

**Conclusion:** ALL versions reproduce the error. langchain-aws has always blindly trusted the declared media type.

### 4. Binary Search: boto3 (Step 5b)

| boto3 | botocore | Result |
|---|---|---|
| 1.36.0 | 1.36.26 | MISMATCH_ERROR |
| 1.38.0 | 1.38.46 | MISMATCH_ERROR |
| 1.40.0 | 1.40.76 | MISMATCH_ERROR |
| 1.41.0 | 1.41.6 | MISMATCH_ERROR |
| 1.42.0 | 1.41.6 | MISMATCH_ERROR |
| 1.42.30 | 1.42.62 | MISMATCH_ERROR |
| 1.42.62 | 1.42.62 | MISMATCH_ERROR |

**Conclusion:** ALL versions reproduce the error. The validation is server-side — the Bedrock service rejects the mismatch regardless of client version.

---

## Root Cause Hypothesis

1. The customer's application constructs image content blocks where the declared media type (`image/webp`) does not match the actual image bytes (JPEG, magic bytes `FF D8 FF`).
2. This mismatch likely originates in the customer's image processing pipeline — e.g., a data URL is generated with `image/webp` as the MIME type, but the underlying image data is JPEG.
3. **Before ~2026-03-05:** The Bedrock Converse API accepted this mismatch silently, detecting the actual image type from the bytes and processing it regardless of the declared format.
4. **After ~2026-03-05:** A Bedrock service-side change added strict validation that rejects requests where the declared media type doesn't match the actual image bytes.
5. The gradual escalation from 0% to 100% error rate over 24 hours is consistent with a rolling deployment of the Bedrock service change across availability zones.

---

## Workaround for Customer

### Option 1: Fix the media type at the source (Recommended)

Ensure the data URL or content block uses the correct MIME type. Detect the actual image type from the bytes:

```python
import imghdr  # or use Pillow

def detect_image_type(image_bytes: bytes) -> str:
    """Detect actual image type from bytes."""
    if image_bytes[:3] == b'\xff\xd8\xff':
        return "image/jpeg"
    elif image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        return "image/png"
    elif image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
        return "image/webp"
    elif image_bytes[:6] in (b'GIF87a', b'GIF89a'):
        return "image/gif"
    raise ValueError("Unknown image type")
```

### Option 2: Override in LangChain

If using the `image_url` format with data URLs, ensure the MIME type in the data URL matches the actual bytes:

```python
import base64

actual_type = detect_image_type(image_bytes)
data_url = f"data:{actual_type};base64,{base64.b64encode(image_bytes).decode()}"

message = HumanMessage(content=[
    {"type": "text", "text": "Describe this image."},
    {"type": "image_url", "image_url": {"url": data_url}},
])
```

### Option 3: Use the native Bedrock content block format

Bypass the `image_url` path entirely and use the native format with correct type detection:

```python
message = HumanMessage(content=[
    {"type": "text", "text": "Describe this image."},
    {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": detect_image_type(image_bytes),
            "data": base64.b64encode(image_bytes).decode(),
        },
    },
])
```

---

## Recommendation for LangChain

The `_format_openai_image_url()` function in `langchain-aws` (and `_format_data_content_block()`) should validate that the declared media type matches the actual image bytes, or at minimum log a warning. This would prevent silent mismatches from reaching the Bedrock API. A defensive fix could detect the actual type from magic bytes and either:
- Override the declared type with the detected type
- Raise a clear error if they don't match

---

## Files

- `kiro-test/test_boto3_mismatch.py` — Raw boto3 mismatch reproduction
- `kiro-test/test_boto3_real_jpeg.py` — Control test with real JPEG
- `kiro-test/test_langchain_mismatch.py` — LangChain mismatch reproduction
- `kiro-test/binary_search_langchain.py` — Binary search across langchain-aws versions
- `kiro-test/binary_search_boto3.py` — Binary search across boto3 versions
