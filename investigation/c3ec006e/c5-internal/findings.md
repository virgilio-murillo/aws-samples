# Internal Sources Investigation: Enhance aws-samples-agent

**Date:** 2026-05-24  
**Source:** Local project analysis (Midway auth expired — Atlas/InternalSearch/SearchSoftwareRecommendations unavailable)  
**Confidence:** HIGH for project structure (direct filesystem), MEDIUM for best practices (derived from shared bus findings + prior investigation d1f13164)

---

## 1. Samples in Each Subdirectory

### bedrock/ (19 notebooks, 4 .py files)
| Subdirectory | Content | Purpose |
|---|---|---|
| agent-runtime/ | invoke_agent.ipynb, invoke_agent_stream.ipynb | Bedrock Agent invocation patterns |
| batch-inference/ | batch-inference-35-haiku-cache.ipynb + batch-101-records.jsonl | Batch inference with caching |
| bedrock-marketplace/ | autogluon-forecasting-chronos-bolt-base/main.ipynb | Marketplace model deployment |
| common-errors/ | RAG_with_query_decomposition.ipynb | RAG troubleshooting patterns |
| fine-tuning/ | finetunning-nova-micro.jsonl (data only) | Fine-tuning data prep |
| miscellaneous/ | 10 notebooks: quickstart, cross-region-inference, conversation examples, custom datasource, knowledge bases, multimodal, 100_limit, 6g_upload_test.py | General Bedrock exploration |
| model-import/ | import_IBM_granite.ipynb | Custom model import |
| prompt-caching/ | prompt-caching-sonnet-3.7.ipynb | Prompt caching with Claude |
| stability-ai-upscale/ | 3 .py files + README + images | Image upscaling with Stability AI |
| testing/ | cross-region-inference.ipynb, invoke_agent_stream_scape_new_lines.ipynb | Testing/debugging |

### bedrock-agentcore/ (2 notebooks, 1 .py file)
| Subdirectory | Content | Purpose |
|---|---|---|
| gateway-cedar-policies/ | gateway_cedar_policies_setup.ipynb | Gateway + Cedar policy setup with Cognito OAuth |
| strands-agents/ | strands_claude.py, runtime_with_strands_and_bedrock_models.sync.ipynb, Dockerfile, .bedrock_agentcore.yaml, requirements.txt | Strands SDK agent deployed to AgentCore runtime |

### bedrock-media-type-mismatch/ (4 .py files)
- binary_search_boto3.py, binary_search_langchain.py — Bug reproduction scripts
- test_boto3_real_jpeg.py, test_langchain_mismatch.py — Test files
- bug_reproduction_report.md — Documentation of media type mismatch issue

### datazone/ (2 notebooks)
- error-creating-glossary-using-assumed-role/ — Reproduces glossary creation bug with assumed roles

### glue/ (1 notebook + 1 markdown)
- pyspark-tutorial-glue.ipynb — PySpark ETL tutorial
- apache-iceberg-johonny-chivers.md — Apache Iceberg on AWS tutorial (Athena + S3 + CloudFormation)

### opensearch/ (1 notebook)
- create-resources/AOSS_resource_creation.ipynb — Amazon OpenSearch Serverless resource creation

### sagemaker/ (13 notebooks, 2 .py files, 16 .tf files)
| Subdirectory | Content | Purpose |
|---|---|---|
| byoc-sm-jupyterlab/ | 3 notebooks (al2023, lustre, sagemaker-distribution) | BYOC JupyterLab images |
| inference-recommender/ | 2 notebooks + inference scripts + payload | SageMaker Inference Recommender |
| pipelines-sagemaker/ | 1 notebook | SageMaker Pipelines end-to-end |
| processing-custom-container/ | 1 notebook + Dockerfile + standalone_region_training_test.py | Custom container for anomaly detection |
| serverless-inference/ | 2 notebooks | Serverless inference walkthrough |
| terraform/ | 2 notebooks + 10 .tf files | Terraform IaC for EC2-to-notebook connectivity |
| (root) | retail_sales_prediction.ipynb | Retail ML prediction |

### notebooks/ (2 notebooks)
- getting_started.ipynb — SageMaker Unified Studio intro
- ml_analysis_with_tests.ipynb — ML analysis patterns

---

## 2. Makefile Structure

```makefile
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
FIND_NB := find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -not -path "*/investigation/*" -not -path "*/kiro-*"

.PHONY: lint validate strip-check test-mac

$(VENV):                    # Auto-creates venv + installs requirements-ci.txt
lint: $(VENV)               # ruff check .
validate: $(VENV)           # python scripts/validate_notebooks.py
strip-check: $(VENV)        # nbstripout --verify on all notebooks
test-mac: lint validate strip-check  # Runs all checks locally
```

**Key design decisions:**
- Venv-based isolation (not system Python)
- Excludes investigation/ and kiro-* from notebook discovery
- `strip-check` uses `--verify` flag (non-zero exit if outputs present)
- `test-mac` is the local developer entrypoint

---

## 3. Languages & Frameworks

| Language/Framework | Usage | Files |
|---|---|---|
| **Python (boto3)** | Primary — all notebooks + scripts | 40 .ipynb, 13 .py |
| **Strands Agents SDK** | Bedrock AgentCore agent framework | strands_claude.py |
| **LangChain** | Media type mismatch testing | binary_search_langchain.py |
| **Terraform (HCL)** | SageMaker infrastructure | 16 .tf files |
| **PySpark** | Glue ETL | 1 notebook |
| **Docker** | Container builds for ECR | 2 Dockerfiles (agentcore, sagemaker) |
| **YAML** | AgentCore config, GitHub Actions | .bedrock_agentcore.yaml, ci.yml, ec2-integration.yml |
| **JSONL** | Batch inference data, fine-tuning data | 2 files |

**Python dependencies (from various requirements.txt):**
- Core: boto3, requests
- AgentCore: strands-agents-tools, uv, bedrock-agentcore, bedrock-agentcore-starter-toolkit
- SageMaker: pandas, joblib, numpy, rrcf, scipy, pyarrow, swifter
- CI: nbstripout>=0.8.1, ruff>=0.6.0, nbformat>=5.9.0
- Image: pillow (stability-ai-upscale)

---

## 4. Deployment Patterns

| Pattern | Used By | Mechanism |
|---|---|---|
| **Bedrock AgentCore Runtime** | bedrock-agentcore/strands-agents | Docker → ECR → CodeBuild → AgentCore Runtime (ARM64, HTTP, OTel) |
| **SageMaker Processing Jobs** | sagemaker/processing-custom-container | Docker → ECR → SageMaker Processing API |
| **Terraform IaC** | sagemaker/terraform | terraform init/plan/apply for VPC, EC2, SageMaker Domain |
| **Direct API calls** | Most bedrock/ notebooks | boto3 client calls (no deployment) |
| **GitHub Actions CI/CD** | .github/workflows/ | ubuntu-latest + EC2 self-hosted runners (Ubuntu + Arch) |
| **SageMaker Notebook execution** | sagemaker/byoc-sm-jupyterlab | BYOC images for JupyterLab spaces |
| **CloudFormation** | glue/ (referenced) | Stack for S3 + Glue DB + Athena workgroup |

**AgentCore deployment flow (most complex):**
1. `bedrock-agentcore` CLI creates IAM roles, ECR repo, CodeBuild project
2. Docker build (ARM64) with opentelemetry-instrument entrypoint
3. Push to ECR
4. CodeBuild triggers deployment to AgentCore Runtime
5. Agent accessible via HTTP with OAuth (Cognito) + Cedar policies

---

## 5. Enhanced Prompt Recommendations

Based on shared bus findings (c1-internet found AWS Startup Prompt Library structure, c2-kb found agent scoping best practices), the enhanced prompt should contain:

### Recommended Structure (4 sections, per best practices):

#### Section 1: Role & Scope
- Identity: "You are an AWS samples development assistant for this repository"
- Scope boundaries: Only operates within ~/work/github/aws-samples/
- Services covered: Bedrock, Bedrock AgentCore, SageMaker, Glue, OpenSearch, DataZone
- Languages: Python (primary), Terraform (IaC), PySpark (Glue)

#### Section 2: Tools & Available Resources
- Makefile targets: lint, validate, strip-check, test-mac
- CI pipeline: GitHub Actions (ci.yml, ec2-integration.yml)
- Linting: ruff (pyproject.toml config, E/F/W rules, notebook-specific ignores)
- Notebook hygiene: nbstripout --verify
- Validation: scripts/validate_notebooks.py (nbformat schema check)
- Docker: Dockerfiles in bedrock-agentcore/ and sagemaker/processing-custom-container/
- AgentCore CLI: .bedrock_agentcore.yaml for deployment config

#### Section 3: Critical Rules (Highest ROI per shared learnings)
1. **NEVER modify existing notebooks** — add new files only
2. **SANITIZE AWS account IDs** before committing (seen: 2 in shared learnings)
3. **Verify factual claims** against actual source code (seen: 6 in shared learnings)
4. **Run `make test-mac`** before suggesting commits
5. **Exclude investigation/ and kiro-* dirs** from notebook operations
6. **Use inference profiles** for Bedrock models (not direct model IDs)
7. **ARM64 architecture** for AgentCore containers
8. **nbstripout --verify** (not --dry-run) for CI enforcement
9. **ruff extend-include = ["*.ipynb"]** already configured in pyproject.toml
10. **Per-file-ignores for notebooks**: E402, E501, F403, F405, E722, F821, E741, F841

#### Section 4: Output Format & Conventions
- Notebooks: nbformat v4.5, python3 kernel preferred
- Python: 120 char line length, ruff E/F/W rules
- READMEs: Each service dir has one
- File organization: service-name/feature-name/files
- Docker: python:3.13-slim base, non-root user, EXPOSE 8080/8000
- Terraform: provider.tf, variables.tf, outputs.tf, resource-specific .tf files

---

## Limitations

- **Midway auth expired**: Could not access Atlas, InternalSearch (wikis/Sage/broadcasts), SearchSoftwareRecommendations, or TicketingReadActions
- **No internal best practices retrieved**: Recommendations derived from local project analysis + shared bus findings from other agents
- **Account ID exposure**: .bedrock_agentcore.yaml contains account 794038231401 — this should be parameterized in the enhanced prompt's Critical Rules

---

## Summary

The aws-samples repo is a **personal learning/experimentation repository** with 40 notebooks and 13 Python scripts spanning 8 AWS services. It uses a **Python-first approach** with boto3 as the primary SDK. The most sophisticated deployment pattern is **Bedrock AgentCore** (Docker → ECR → CodeBuild → Runtime). The CI/CD is already implemented via GitHub Actions + Makefile. The enhanced prompt should emphasize the Critical Rules section (highest ROI per shared learnings) and provide explicit tool/target references to avoid hallucination.
