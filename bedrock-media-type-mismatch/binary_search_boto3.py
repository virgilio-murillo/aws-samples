"""Step 5b: Binary search boto3 versions with raw boto3 (no langchain).
Tests whether the mismatch error is server-side (all versions fail)
or client-side (only newer versions fail).
"""
import subprocess, sys

VENV_DIR = "./kiro-test/venv_boto3"
VENV_PIP = f"{VENV_DIR}/bin/pip"
VENV_PYTHON = f"{VENV_DIR}/bin/python"

# Create a separate venv for boto3-only testing
subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
subprocess.run([VENV_PIP, "install", "--upgrade", "pip", "-q"], capture_output=True)
subprocess.run([VENV_PIP, "install", "Pillow", "-q"], capture_output=True)

# Wide range: ~2 months ago to now
VERSIONS = ["1.36.0", "1.38.0", "1.40.0", "1.41.0", "1.42.0", "1.42.30", "1.42.62"]

TEST_SCRIPT = '''
import io, struct, boto3
from importlib.metadata import version as pkg_version
from PIL import Image

print(f"boto3={pkg_version('boto3')}, botocore={pkg_version('botocore')}")

img = Image.new("RGB", (8, 8), color=(100, 150, 200))
buf = io.BytesIO()
img.save(buf, format="JPEG")
jpeg_bytes = buf.getvalue()

client = boto3.client("bedrock-runtime", region_name="eu-central-1")
try:
    resp = client.converse(
        modelId="eu.anthropic.claude-haiku-4-5-20251001-v1:0",
        messages=[{"role": "user", "content": [
            {"text": "Describe this image."},
            {"image": {"format": "webp", "source": {"bytes": jpeg_bytes}}}
        ]}],
        inferenceConfig={"maxTokens": 50}
    )
    print("RESULT:SUCCESS")
except Exception as e:
    err = str(e)
    if "media type" in err.lower() or "webp" in err.lower():
        print("RESULT:MISMATCH_ERROR")
    else:
        print(f"RESULT:OTHER_ERROR:{err[:200]}")
'''

results = []
for ver in VERSIONS:
    print(f"\nTesting boto3=={ver}")
    install = subprocess.run(
        [VENV_PIP, "install", f"boto3=={ver}", "-q", "--force-reinstall"],
        capture_output=True, text=True, timeout=120
    )
    if install.returncode != 0:
        print(f"  INSTALL FAILED: {install.stderr[-200:]}")
        results.append((ver, "INSTALL_FAILED"))
        continue

    test = subprocess.run(
        [VENV_PYTHON, "-c", TEST_SCRIPT],
        capture_output=True, text=True, timeout=60
    )
    output = test.stdout.strip()
    print(f"  {output}")
    
    for line in output.split("\n"):
        if line.startswith("RESULT:"):
            results.append((ver, line.split(":", 1)[1]))
            break
    else:
        results.append((ver, f"UNKNOWN:{test.stderr[-150:]}"))

print(f"\n{'='*60}")
print("BOTO3 BINARY SEARCH SUMMARY:")
print(f"{'Version':<15} {'Result'}")
print("-" * 50)
for ver, result in results:
    print(f"{ver:<15} {result}")
