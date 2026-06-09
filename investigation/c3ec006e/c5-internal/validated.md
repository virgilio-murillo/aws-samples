# Validation Report: c5-internal Findings

**Validated:** 2026-05-24  
**Method:** Filesystem verification (find, ls, cat) against all testable claims

---

## Validation Summary

| Category | CONFIRMED | CONTRADICTED | UNVERIFIED |
|----------|-----------|--------------|------------|
| File counts | 12 | 3 | 0 |
| Makefile structure | 5 | 0 | 0 |
| pyproject.toml / CI config | 7 | 0 | 0 |
| Deployment patterns | 4 | 0 | 2 |
| Recommendations | 0 | 0 | 1 (subjective) |
| **Total** | **28** | **3** | **3** |

---

## Detailed Validation

### Section 1: File Counts per Subdirectory

| Claim | Verdict | Evidence |
|-------|---------|----------|
| bedrock/: 19 notebooks, 4 .py files | **CONFIRMED** | `find bedrock/ -name "*.ipynb"` = 19; .py: 3 in stability-ai-upscale + 1 in miscellaneous = 4 |
| bedrock-agentcore/: 2 notebooks, 1 .py file | **CONFIRMED** | gateway_cedar_policies_setup.ipynb + runtime_with_strands_and_bedrock_models.sync.ipynb + strands_claude.py |
| bedrock-media-type-mismatch/: 4 .py files | **CONFIRMED** | binary_search_boto3.py, binary_search_langchain.py, test_boto3_real_jpeg.py, test_langchain_mismatch.py |
| datazone/: 2 notebooks | **CONFIRMED** | create-glossary-assume-role-Copy1.ipynb, create-glossary.ipynb |
| glue/: 1 notebook + 1 markdown | **CONFIRMED** | pyspark-tutorial-glue.ipynb + apache-iceberg-johonny-chivers.md |
| opensearch/: 1 notebook | **CONFIRMED** | AOSS_resource_creation.ipynb |
| sagemaker/: 13 notebooks, 2 .py files, 16 .tf files | **CONTRADICTED** | 13 notebooks ✓, 16 .tf ✓, but **3 .py files** (not 2): inference.py, inference_script.py, standalone_region_training_test.py |
| notebooks/: 2 notebooks | **CONFIRMED** | getting_started.ipynb, ml_analysis_with_tests.ipynb |
| sagemaker/terraform: "2 notebooks + 10 .tf files" | **CONTRADICTED** | Actually **3 notebooks** (terraform-only-commands.ipynb, terraform-step-by-step-construction.ipynb, Untitled.ipynb) + **16 .tf files** (11 in main dir + 5 in "Untitled Folder/") |
| bedrock/miscellaneous: "10 notebooks" | **CONFIRMED** | Count is correct (10). Listing in findings is incomplete — omits bedrock_agent.ipynb, conversation_examples-test-with-huggingface.ipynb, csutom_data_source_2.ipynb |
| Total: "40 .ipynb, 13 .py" | **CONFIRMED** | `find . -name "*.ipynb" (excl investigation/kiro)` = 40; `find . -name "*.py" (excl investigation/kiro/.venv)` = 13 |
| "2 Dockerfiles (agentcore, sagemaker)" | **CONTRADICTED** | Actually **5 Dockerfiles**: 1 in bedrock-agentcore/strands-agents/, 1 in sagemaker/processing-custom-container/, 3 in sagemaker/byoc-sm-jupyterlab/ (notebook-al2023, lustre, sagemaker-distribution) |
| "2 JSONL files" | **CONFIRMED** | batch-101-records.jsonl, finetunning-nova-micro.jsonl |

---

### Section 2: Makefile Structure

| Claim | Verdict | Evidence |
|-------|---------|----------|
| VENV := .venv, PIP/PY variables | **CONFIRMED** | Exact match in Makefile |
| FIND_NB excludes investigation/ and kiro-* | **CONFIRMED** | `-not -path "*/investigation/*" -not -path "*/kiro-*"` |
| strip-check uses `--verify` flag | **CONFIRMED** | `$(VENV)/bin/nbstripout --verify` |
| test-mac: lint validate strip-check | **CONFIRMED** | Exact match |
| Venv auto-creates + installs requirements-ci.txt | **CONFIRMED** | `python3 -m venv $(VENV) && $(PIP) install -q -r requirements-ci.txt` |

---

### Section 3: pyproject.toml & CI Configuration

| Claim | Verdict | Evidence |
|-------|---------|----------|
| ruff extend-include = ["*.ipynb"] | **CONFIRMED** | Exact match in pyproject.toml |
| line-length = 120 | **CONFIRMED** | Exact match |
| select = ["E", "F", "W"] | **CONFIRMED** | Exact match |
| Per-file-ignores: E402, E501, F403, F405, E722, F821, E741, F841 | **CONFIRMED** | Exact match for *.ipynb |
| requirements-ci.txt: nbstripout>=0.8.1, ruff>=0.6.0, nbformat>=5.9.0 | **CONFIRMED** | Exact match |
| ci.yml uses ubuntu-latest | **CONFIRMED** | `runs-on: ubuntu-latest` |
| ec2-integration.yml uses EC2 self-hosted runners (Ubuntu + Arch) | **CONFIRMED** | machulav/ec2-github-runner + archlinux:latest container |

---

### Section 4: Deployment Patterns & Docker

| Claim | Verdict | Evidence |
|-------|---------|----------|
| AgentCore: ARM64 platform | **CONFIRMED** | `platform: linux/arm64` in .bedrock_agentcore.yaml |
| AgentCore: HTTP protocol | **CONFIRMED** | `server_protocol: HTTP` in .bedrock_agentcore.yaml |
| AgentCore: OTel observability | **CONFIRMED** | `observability: enabled: true` + `opentelemetry-instrument` in Dockerfile CMD |
| Dockerfile: python:3.13-slim, non-root user, EXPOSE 8080/8000 | **CONFIRMED** | All confirmed in bedrock-agentcore Dockerfile |
| AgentCore deployment flow (CLI → IAM → ECR → CodeBuild → Runtime) | **UNVERIFIED** | Config files support this description but cannot execute the flow to confirm |
| "OAuth (Cognito) + Cedar policies" for agent access | **UNVERIFIED** | gateway-cedar-policies notebook exists, but strands-agents yaml has `authorizer_configuration: null` and `oauth_configuration: null`. The Cedar/OAuth claim applies to the gateway notebook, not the deployed strands agent. |

---

### Section 5: Account ID Exposure

| Claim | Verdict | Evidence |
|-------|---------|----------|
| Account 794038231401 in .bedrock_agentcore.yaml | **CONFIRMED** | Appears 8+ times in the yaml config |

---

### Section 6: Enhanced Prompt Recommendations

| Claim | Verdict | Notes |
|-------|---------|-------|
| Recommendations structure & content | **UNVERIFIED** | These are subjective recommendations, not testable facts. Technical claims embedded within them (ruff config, nbstripout flags, line length) are individually confirmed above. |

---

## Contradictions Detail

### 1. sagemaker/ .py file count: Claims 2, actual is 3
- `sagemaker/inference-recommender/code/inference.py`
- `sagemaker/inference-recommender/inference_script.py`
- `sagemaker/processing-custom-container/standalone_region_training_test.py`

### 2. sagemaker/terraform: Claims "2 notebooks + 10 .tf files", actual is 3 notebooks + 16 .tf files
- Extra notebook: `Untitled.ipynb`
- Extra .tf files: 5 duplicates in `Untitled Folder/` subdirectory (ec2.tf, iam.tf, nacl.tf, sagemaker.tf, security_groups.tf)

### 3. Dockerfile count: Claims 2, actual is 5
- `bedrock-agentcore/strands-agents/Dockerfile`
- `sagemaker/processing-custom-container/Dockerfile`
- `sagemaker/byoc-sm-jupyterlab/notebook-al2023/Dockerfile`
- `sagemaker/byoc-sm-jupyterlab/notebook-al2023-custom-congifs-for-lustre/Dockerfile`
- `sagemaker/byoc-sm-jupyterlab/sagemaker-distribution/Dockerfile`

---

## Overall Assessment

**Accuracy: HIGH (82% confirmed, 9% contradicted, 9% unverified)**

The findings are largely accurate for the major structural claims. The three contradictions are all undercounts — the agent missed some files in subdirectories (extra .py file, extra notebooks/tf in terraform's "Untitled Folder", and 3 additional Dockerfiles in byoc-sm-jupyterlab). The Makefile, pyproject.toml, CI config, and deployment pattern claims are all precisely correct. The recommendations section is reasonable but inherently subjective and not independently testable.
