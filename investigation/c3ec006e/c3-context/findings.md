# Investigation Findings: aws-samples Repository Context Analysis

## 1. Samples in Each Subdirectory

### bedrock/ (11 subdirs, 14 notebooks + 4 .py files)
| Subdirectory | Content | Purpose |
|---|---|---|
| `agent-runtime/` | invoke_agent.ipynb, invoke_agent_stream.ipynb | Bedrock Agent invocation (sync + streaming) |
| `batch-inference/` | batch-inference-35-haiku-cache.ipynb + .jsonl data | Batch inference with Claude 3.5 Haiku + caching |
| `bedrock-marketplace/autogluon-forecasting-chronos-bolt-base/` | main.ipynb | AutoGluon forecasting from Bedrock Marketplace |
| `common-errors/` | RAG_with_query_decomposition.ipynb | RAG patterns + common error handling |
| `fine-tuning/` | finetunning-nova-micro.jsonl | Fine-tuning data for Nova Micro |
| `miscellaneous/` | 8 notebooks + 1 .py | Cross-region inference, conversations, KB/RAG, custom datasources, multimodal Llama, quickstart, 100-limit testing, 6G upload test |
| `model-import/` | import_IBM_granite.ipynb | Importing external models (IBM Granite) |
| `prompt-caching/` | prompt-caching-sonnet-3.7.ipynb | Prompt caching with Claude Sonnet 3.7 |
| `stability-ai-upscale/` | 3 .py files + README + images | Stability AI Conservative Upscale via inference profiles |
| `testing/` | 2 notebooks | Cross-region inference testing, agent stream newline escaping |

### bedrock-agentcore/ (2 subdirs)
| Subdirectory | Content | Purpose |
|---|---|---|
| `strands-agents/` | strands_claude.py, Dockerfile, .bedrock_agentcore.yaml, requirements.txt, notebook | Strands SDK agent deployed to Bedrock AgentCore Runtime via Docker/ECR/CodeBuild |
| `gateway-cedar-policies/` | gateway_cedar_policies_setup.ipynb | Gateway setup with Cedar policy-based authorization, Cognito OAuth, MCP protocol |

### bedrock-media-type-mismatch/ (5 files)
- Bug reproduction scripts for Bedrock Converse API media type validation change
- `binary_search_langchain.py` / `binary_search_boto3.py` — version bisection scripts
- `bug_reproduction_report.md` — detailed root cause analysis
- Test scripts proving server-side validation change

### datazone/ (1 subdir)
| Subdirectory | Content | Purpose |
|---|---|---|
| `error-creating-glossary-using-assumed-role/` | 2 notebooks | Reproducing/fixing DataZone glossary creation with assumed IAM roles |

### glue/ (2 files)
- `pyspark-tutorial-glue.ipynb` — AWS Glue Studio PySpark interactive session tutorial
- `apache-iceberg-johonny-chivers.md` — Apache Iceberg reference notes

### opensearch/ (1 subdir)
| Subdirectory | Content | Purpose |
|---|---|---|
| `create-resources/` | AOSS_resource_creation.ipynb | Amazon OpenSearch Serverless (AOSS) resource creation |

### sagemaker/ (6 subdirs, 11 notebooks + 2 .py + 16 .tf)
| Subdirectory | Content | Purpose |
|---|---|---|
| `processing-custom-container/` | notebook + Dockerfile + .py + README | Custom Docker container for SageMaker Processing (RRCF anomaly detection) |
| `inference-recommender/` | 2 notebooks + inference scripts + payload | SageMaker Inference Recommender + BYOC serverless inference |
| `terraform/connect-ec2-to-notebook-SMAI/` | 10+ .tf files + notebooks | Terraform IaC for EC2↔SageMaker Unified Studio connectivity |
| `byoc-sm-jupyterlab/` | 3 subdirs with Dockerfiles + notebooks | BYOC JupyterLab images (AL2023, Lustre configs, SM Distribution) |
| `serverless-inference/` | notebook + walkthrough | Serverless inference setup |
| `pipelines-sagemaker/` | 1 notebook | SageMaker Pipelines: preprocess→train→evaluate→batch-transform |
| `retail_sales_prediction.ipynb` | standalone notebook | Retail sales ML prediction |

### notebooks/ (2 files)
- `getting_started.ipynb` — SageMaker Unified Studio getting started (78KB, comprehensive)
- `ml_analysis_with_tests.ipynb` — ML analysis with testing patterns

---

## 2. Makefile Structure

```makefile
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
FIND_NB := find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -not -path "*/investigation/*" -not -path "*/kiro-*"

Targets:
- $(VENV)       → Creates virtualenv, installs requirements-ci.txt
- lint          → ruff check .
- validate      → python scripts/validate_notebooks.py (JSON + nbformat schema)
- strip-check   → nbstripout --verify on all notebooks
- test-mac      → lint + validate + strip-check (local macOS target)
```

**Key design**: Excludes `investigation/` and `kiro-*` dirs from all checks. Uses venv isolation.

---

## 3. Languages & Frameworks

| Language/Tool | Usage | Files |
|---|---|---|
| **Python** | Primary language | 13 .py files + 40 notebooks |
| **Jupyter Notebooks** | Main content format | 40 notebooks (kernels: python3, conda_python3, conda_tensorflow2_p310, conda_pytorch_p310, glue_pyspark) |
| **Terraform (HCL)** | Infrastructure | 16 .tf files (VPC, EC2, SageMaker, IAM, NACLs) |
| **Docker** | Container builds | 5 Dockerfiles (python:3.10-slim, python:3.13-slim, amazonlinux:2023) |
| **Shell/Makefile** | Build automation | Makefile + CI scripts |

### Key Python Libraries Used
- **boto3** — AWS SDK (all samples)
- **strands-agents** + **bedrock-agentcore** — Agent framework (bedrock-agentcore/)
- **sagemaker** SDK — ML workflows
- **langchain-aws** — LangChain integration (media-type-mismatch)
- **rrcf** — Robust Random Cut Forest (anomaly detection)
- **nbformat**, **nbstripout**, **ruff** — CI tooling
- **Pillow** — Image processing (stability-ai-upscale)
- **PySpark** — Glue data processing

---

## 4. Deployment Patterns

| Pattern | Used In | Details |
|---|---|---|
| **Docker → ECR → Bedrock AgentCore Runtime** | bedrock-agentcore/strands-agents | Dockerfile + .bedrock_agentcore.yaml + CodeBuild. Deploys via `bedrock-agentcore` CLI toolkit |
| **Docker → ECR → SageMaker Processing** | sagemaker/processing-custom-container | Custom container pushed to ECR, invoked as SageMaker Processing Job |
| **Docker → ECR → SageMaker JupyterLab** | sagemaker/byoc-sm-jupyterlab | BYOC images for SageMaker Spaces |
| **Terraform** | sagemaker/terraform | Full IaC: VPC, subnets, NACLs, SGs, EC2, SageMaker Domain/Spaces |
| **Direct API calls (boto3)** | bedrock/, opensearch/, datazone/ | Notebook-driven, no deployment infra needed |
| **SageMaker Pipelines** | sagemaker/pipelines-sagemaker | Orchestrated ML workflow |
| **GitHub Actions CI/CD** | .github/workflows/ | ci.yml (lint/validate/strip-check) + ec2-integration.yml (EC2 runner on Ubuntu+Arch) |

---

## 5. Current Agent Prompt Analysis

**Location**: `~/.kiro/agents/aws-samples-agent.json`  
**Current size**: ~1343 chars in the `prompt` field

### What's CORRECT in current prompt:
- Project path: ~/work/github/aws-samples/
- Lists bedrock/, bedrock-agentcore/, bedrock-media-type-mismatch/, datazone/, glue/
- Mentions Makefile
- Critical Rules: sanitize AWS account IDs, READMEs, error handling

### What's WRONG or MISSING:
1. **Missing directories**: `sagemaker/`, `opensearch/`, `notebooks/`, `scripts/`
2. **Wrong language claim**: Says "CloudFormation/SAM" but repo uses **Terraform** (no SAM/CFN exists)
3. **Wrong Makefile targets**: Says `make test` but actual targets are `lint`, `validate`, `strip-check`, `test-mac`
4. **Missing CI/CD awareness**: No mention of GitHub Actions workflows (ci.yml, ec2-integration.yml)
5. **Missing deployment patterns**: Docker/ECR, Bedrock AgentCore, SageMaker Processing
6. **Missing tooling**: ruff, nbstripout, nbformat validation, pyproject.toml config
7. **Missing file counts**: 40 notebooks, 13 .py, 16 .tf, 5 Dockerfiles
8. **No mention of .bedrock_agentcore.yaml** config pattern
9. **No mention of SAGEMAKER_UNIFIED_STUDIO_README.md** (reference doc)

---

## 6. Recommended Enhanced Prompt Content

Based on analysis, the enhanced prompt should include:

### Must-Have Sections:
1. **Project Overview** — Path, purpose, GitHub remote
2. **Complete Directory Map** — All 8 service dirs + scripts/ + notebooks/ with brief descriptions
3. **Languages & Frameworks** — Python (primary), Terraform, Docker, Jupyter
4. **Build & CI/CD** — Correct Makefile targets + GitHub Actions workflows
5. **Deployment Patterns** — The 4-5 distinct patterns used
6. **Critical Rules** (highest ROI per shared learnings):
   - SANITIZE AWS account IDs, ARNs, credentials in all outputs
   - Never modify existing notebooks (CI validates them)
   - Each sample self-contained with README
   - Use inference profiles for Bedrock models (not direct model IDs)
   - Exclude `investigation/` and `kiro-*` from all operations
7. **Key Config Files** — pyproject.toml (ruff config), requirements-ci.txt, .bedrock_agentcore.yaml pattern
8. **Common Tasks** — Adding samples, running CI locally, deploying agents

### Should Remove:
- "CloudFormation/SAM" references (doesn't exist in repo)
- `make test` (wrong target name)
- Incomplete directory listing

---

## Sources
- Direct file inspection of ~/work/github/aws-samples/ (all findings verified against actual files)
- ~/.kiro/agents/aws-samples-agent.json (current prompt)
- ~/.kiro/projects/projects.tsv (project registration)
- ~/.kiro/steering/tools/aws-samples-repo.md (steering file)
