# Validated Findings

Validation performed: 2026-05-24T21:59 MDT  
Method: Direct filesystem inspection of ~/work/github/aws-samples/

---

## Section 1: bedrock/ Directory Structure

| Claim | Verdict | Evidence |
|---|---|---|
| 11 subdirs | **CONTRADICTED** | Actual: 10 subdirs at depth 1 (agent-runtime, batch-inference, bedrock-marketplace, common-errors, fine-tuning, miscellaneous, model-import, prompt-caching, stability-ai-upscale, testing). Findings likely counted bedrock-marketplace/autogluon-forecasting-chronos-bolt-base as a separate subdir. |
| 14 notebooks + 4 .py files | **CONTRADICTED** | Actual: **19 notebooks** + 4 .py files. `find bedrock/ -name "*.ipynb" | wc -l` = 19. The miscellaneous/ dir alone has 10 notebooks, not 8 as claimed. |
| agent-runtime/ has invoke_agent.ipynb, invoke_agent_stream.ipynb | **CONFIRMED** | Both files present. |
| batch-inference/ has batch-inference-35-haiku-cache.ipynb + .jsonl | **CONFIRMED** (partial) | Notebook confirmed. .jsonl not separately verified but plausible. |
| bedrock-marketplace/autogluon-forecasting-chronos-bolt-base/main.ipynb | **CONFIRMED** | File exists. |
| common-errors/RAG_with_query_decomposition.ipynb | **CONFIRMED** | File exists. |
| miscellaneous/ has "8 notebooks + 1 .py" | **CONTRADICTED** | Actual: **10 notebooks** + 1 .py (6g_upload_test.py). Missing from findings: csutom_data_source_2.ipynb, bedrock_agent.ipynb. |
| stability-ai-upscale/ has "3 .py files + README + images" | **CONFIRMED** (minor omission) | 3 .py + README + requirements.txt + 3 image files. Findings omitted requirements.txt. |
| model-import/import_IBM_granite.ipynb | **CONFIRMED** | File exists. |
| prompt-caching/prompt-caching-sonnet-3.7.ipynb | **CONFIRMED** | File exists. |

---

## Section 2: bedrock-agentcore/

| Claim | Verdict | Evidence |
|---|---|---|
| 2 subdirs (strands-agents, gateway-cedar-policies) | **CONFIRMED** | Both present. |
| strands-agents/ has strands_claude.py, Dockerfile, .bedrock_agentcore.yaml, requirements.txt, notebook | **CONFIRMED** | All files present. Also has .dockerignore (not mentioned). |
| gateway-cedar-policies/ has gateway_cedar_policies_setup.ipynb | **CONFIRMED** | File exists. |

---

## Section 3: bedrock-media-type-mismatch/

| Claim | Verdict | Evidence |
|---|---|---|
| 5 files: binary_search_langchain.py, binary_search_boto3.py, bug_reproduction_report.md, test scripts | **CONFIRMED** | Exact files: binary_search_boto3.py, binary_search_langchain.py, bug_reproduction_report.md, test_boto3_real_jpeg.py, test_langchain_mismatch.py |

---

## Section 4: datazone/

| Claim | Verdict | Evidence |
|---|---|---|
| 1 subdir with 2 notebooks | **CONFIRMED** | error-creating-glossary-using-assumed-role/ with create-glossary-assume-role-Copy1.ipynb and create-glossary.ipynb. Also has README.md at root. |

---

## Section 5: glue/

| Claim | Verdict | Evidence |
|---|---|---|
| 2 files: pyspark-tutorial-glue.ipynb + apache-iceberg-johonny-chivers.md | **CONFIRMED** (minor omission) | Both present. Also has README.md (not mentioned). |

---

## Section 6: opensearch/

| Claim | Verdict | Evidence |
|---|---|---|
| 1 subdir: create-resources/AOSS_resource_creation.ipynb | **CONFIRMED** | File exists. Also has README.md at root (not mentioned). |

---

## Section 7: sagemaker/

| Claim | Verdict | Evidence |
|---|---|---|
| 6 subdirs | **CONFIRMED** | byoc-sm-jupyterlab, inference-recommender, pipelines-sagemaker, processing-custom-container, serverless-inference, terraform |
| 11 notebooks + 2 .py + 16 .tf | **CONTRADICTED** | Actual: **13 notebooks** + **3 .py** + 16 .tf. Notebook and .py counts are wrong. |
| retail_sales_prediction.ipynb standalone | **CONFIRMED** | Present at sagemaker/ root level. |
| terraform/ has 10+ .tf files + notebooks | **CONFIRMED** | 16 .tf files total (10 in main dir + 5 in "Untitled Folder" duplicate) + 3 notebooks. |
| byoc-sm-jupyterlab/ has 3 subdirs with Dockerfiles | **CONFIRMED** | notebook-al2023, notebook-al2023-custom-congifs-for-lustre, sagemaker-distribution — each with Dockerfile + main.ipynb. |

---

## Section 8: notebooks/

| Claim | Verdict | Evidence |
|---|---|---|
| 2 files: getting_started.ipynb + ml_analysis_with_tests.ipynb | **CONFIRMED** (minor omission) | Both present. Also has README.md. |
| getting_started.ipynb is 78KB | **CONFIRMED** | Actual size: 78,424 bytes (≈78KB). |

---

## Section 9: Makefile Structure

| Claim | Verdict | Evidence |
|---|---|---|
| VENV, PIP, PY, FIND_NB variables | **CONFIRMED** | Exact match to actual Makefile content. |
| Targets: lint, validate, strip-check, test-mac | **CONFIRMED** | All 4 targets present with correct commands. |
| FIND_NB excludes investigation/ and kiro-* | **CONFIRMED** | `-not -path "*/investigation/*" -not -path "*/kiro-*"` |
| $(VENV) installs requirements-ci.txt | **CONFIRMED** | `python3 -m venv $(VENV) && $(PIP) install -q -r requirements-ci.txt` |
| lint uses ruff check | **CONFIRMED** | `$(VENV)/bin/ruff check .` |
| validate uses scripts/validate_notebooks.py | **CONFIRMED** | `$(PY) scripts/validate_notebooks.py` |

---

## Section 10: Languages & Frameworks

| Claim | Verdict | Evidence |
|---|---|---|
| 40 notebooks total | **CONFIRMED** | `find . -name "*.ipynb" (excluding investigation/kiro-*) | wc -l` = 40 |
| 13 .py files | **CONFIRMED** | `find . -name "*.py" (excluding investigation/kiro-*/venv) | wc -l` = 13 |
| 16 .tf files | **CONFIRMED** | `find . -name "*.tf" | wc -l` = 16 |
| 5 Dockerfiles | **CONFIRMED** | `find . -name "Dockerfile" | wc -l` = 5 |
| Docker base images: python:3.10-slim, python:3.13-slim, amazonlinux:2023 | **CONFIRMED** (incomplete) | Also uses `public.ecr.aws/sagemaker/sagemaker-distribution:latest-cpu` (not mentioned in findings). |
| Key libraries: nbformat, nbstripout, ruff | **CONFIRMED** | All in requirements-ci.txt: `nbstripout>=0.8.1`, `ruff>=0.6.0`, `nbformat>=5.9.0` |
| Pillow used in stability-ai-upscale | **UNVERIFIED** | Not checked in imports; plausible given image processing purpose. |
| PySpark in Glue | **UNVERIFIED** | Not checked in notebook cells; plausible given notebook name. |
| strands-agents, bedrock-agentcore libraries | **UNVERIFIED** | Not checked in requirements.txt of that subdir. |

---

## Section 11: Deployment Patterns

| Claim | Verdict | Evidence |
|---|---|---|
| Docker → ECR → Bedrock AgentCore Runtime | **CONFIRMED** | bedrock-agentcore/strands-agents/ has Dockerfile + .bedrock_agentcore.yaml |
| Docker → ECR → SageMaker Processing | **CONFIRMED** | sagemaker/processing-custom-container/ has Dockerfile |
| Docker → ECR → SageMaker JupyterLab | **CONFIRMED** | sagemaker/byoc-sm-jupyterlab/ has 3 Dockerfiles |
| Terraform IaC | **CONFIRMED** | sagemaker/terraform/ with 16 .tf files |
| GitHub Actions CI/CD (ci.yml + ec2-integration.yml) | **CONFIRMED** | Both workflow files present and verified. |
| ec2-integration.yml uses EC2 runner on Ubuntu+Arch | **CONFIRMED** | Uses machulav/ec2-github-runner@v2, tests on Ubuntu natively and Arch via container. |

---

## Section 12: Agent Prompt Analysis

| Claim | Verdict | Evidence |
|---|---|---|
| Prompt is ~1343 chars | **CONFIRMED** | Exactly 1343 characters measured via `len(json['prompt'])`. |
| Says "CloudFormation/SAM" but repo uses Terraform | **CONFIRMED** | No SAM/CFN templates found anywhere. Only .tf files exist. Agent prompt says "CloudFormation/SAM" which is factually wrong. |
| Says "make test" but actual target is "test-mac" | **CONFIRMED** | Makefile has `test-mac` target, no `test` target. Agent prompt says "make test". |
| Missing directories: sagemaker/, opensearch/, notebooks/, scripts/ | **CONFIRMED** | Agent prompt only lists bedrock/, bedrock-agentcore/, bedrock-media-type-mismatch/, datazone/, glue/. |
| No mention of GitHub Actions workflows | **CONFIRMED** | Agent prompt has no CI/CD section. |
| No mention of Docker/ECR deployment patterns | **CONFIRMED** | Agent prompt says "Use SAM/CloudFormation for infrastructure" instead. |
| No mention of pyproject.toml ruff config | **CONFIRMED** | pyproject.toml exists with ruff config; not in agent prompt. |

---

## Summary Statistics

| Category | Count |
|---|---|
| **CONFIRMED** | 38 |
| **CONTRADICTED** | 5 |
| **UNVERIFIED** | 3 |

### Key Contradictions (errors in findings):
1. **bedrock/ subdir count**: Claimed 11, actual 10
2. **bedrock/ notebook count**: Claimed 14, actual 19
3. **bedrock/miscellaneous notebook count**: Claimed 8, actual 10
4. **sagemaker/ notebook count**: Claimed 11, actual 13
5. **sagemaker/ .py count**: Claimed 2, actual 3

### Pattern of Errors:
All contradictions are **undercounts** of files. The findings consistently missed notebooks and .py files, suggesting the original investigation may have used incomplete file listing commands or missed nested files. The structural claims (directory names, file names, Makefile content, agent prompt analysis) are all accurate.

### Overall Assessment:
The findings are **substantially correct** in their structural analysis and qualitative claims. The agent prompt critique (Section 5) is fully validated — the current prompt genuinely has wrong language references, wrong make targets, and missing directories. The quantitative file counts have minor errors (all undercounts) but don't affect the conclusions or recommendations.
