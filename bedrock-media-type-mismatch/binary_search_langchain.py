"""Step 5: Binary search langchain-aws versions.
Tests whether the mismatch error reproduces across different versions.
If ALL versions reproduce it → server-side Bedrock change.
If only newer versions → client-side langchain change.
"""
import subprocess, sys, json

VENV_PIP = "./kiro-test/venv/bin/pip"
VENV_PYTHON = "./kiro-test/venv/bin/python"

# Versions to test (binary search range)
VERSIONS = ["1.2.0", "1.2.2", "1.2.3", "1.2.5", "1.3.0", "1.3.1"]

TEST_SCRIPT = '''
import base64, io, sys
from PIL import Image

img = Image.new("RGB", (8, 8), color=(100, 150, 200))
buf = io.BytesIO()
img.save(buf, format="JPEG")
jpeg_b64 = base64.b64encode(buf.getvalue()).decode()

from importlib.metadata import version as pkg_version
print(f"langchain-aws={pkg_version('langchain-aws')}, langchain-core={pkg_version('langchain-core')}")

from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage

model = ChatBedrockConverse(
    model="eu.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="eu-central-1", max_tokens=50
)
data_url = f"data:image/webp;base64,{jpeg_b64}"
msg = HumanMessage(content=[
    {"type": "text", "text": "Describe this image."},
    {"type": "image_url", "image_url": {"url": data_url}},
])
try:
    resp = model.invoke([msg])
    print("RESULT:SUCCESS")
except Exception as e:
    err = str(e)
    if "media type" in err.lower() or "webp" in err.lower():
        print(f"RESULT:MISMATCH_ERROR")
    else:
        print(f"RESULT:OTHER_ERROR:{err[:200]}")
'''

results = []
for ver in VERSIONS:
    print(f"\n{'='*60}")
    print(f"Testing langchain-aws=={ver}")
    
    # Install specific version
    install = subprocess.run(
        [VENV_PIP, "install", f"langchain-aws=={ver}", "-q", "--force-reinstall"],
        capture_output=True, text=True, timeout=120
    )
    if install.returncode != 0:
        print(f"  INSTALL FAILED: {install.stderr[-200:]}")
        results.append({"version": ver, "result": "INSTALL_FAILED"})
        continue
    
    # Also ensure Pillow is installed
    subprocess.run([VENV_PIP, "install", "Pillow", "-q"], capture_output=True, timeout=60)
    
    # Run test
    test = subprocess.run(
        [VENV_PYTHON, "-c", TEST_SCRIPT],
        capture_output=True, text=True, timeout=60
    )
    output = test.stdout.strip()
    print(f"  Output: {output}")
    
    # Parse result
    for line in output.split("\n"):
        if line.startswith("RESULT:"):
            result = line.split(":", 1)[1]
            results.append({"version": ver, "result": result})
            break
    else:
        results.append({"version": ver, "result": f"UNKNOWN:{test.stderr[-200:]}"})

print(f"\n{'='*60}")
print("SUMMARY:")
print(f"{'Version':<15} {'Result'}")
print("-" * 50)
for r in results:
    print(f"{r['version']:<15} {r['result']}")
