# Investigation Findings: Enhance aws-samples-agent

## Sources
- Knowledge Base: `search_lessons` (12+ relevant lessons)
- Direct file inspection of project structure, Makefile, CI workflows, configs

---

## 1. Samples in Each Subdirectory

### bedrock/ (11 subdirs)
| Subdirectory | Content | Language |
|---|---|---|
| agent-runtime/ | invoke_agent.ipynb, invoke_agent_stream.ipynb | Python/Jupyter |
| batch-inference/ | batch-inference-35-haiku-cache.ipynb, batch-101-records.jsonl | Python/Jupyter + JSONL data |
| fine-tuning/ | finetunning-nova-micro.jsonl | JSONL training data |
| model-import/ | import_IBM_granite.ipynb | Python/Jupyter |
| prompt-caching/ | prompt-caching-sonnet-3.7.ipynb | Python/Jupyter |
| stability-ai-upscale/ | complete_demo.py, stability_upscale.py, create_test_image.py | Python scripts |
| bedrock-marketplace/ | autogluon-forecasting-chronos-bolt-base/ | (subdir) |
| miscellaneous/ | 8 notebooks (quickstart, conversation, RAG, cross-region, multimodal, etc.) | Python/Jupyter |
| testing/ | cross-region-inference.ipynb, invoke_agent_stream_scape_new_lines.ipynb | Python/Jupyter |
| common-errors/ | RAG_with_query_decomposition.ipynb | Python/Jupyter |

### bedrock-agentcore/ (2 subdirs)
| Subdirectory | Content | Language |
|---|---|---|
| gateway-cedar-policies/ | gateway_cedar_policies_setup.ipynb (46KB) | Python/Jupyter |
| strands-agents/ | strands_claude.py, runtime_with_strands_and_bedrock_models.sync.ipynb, Dockerfile, .bedrock_agentcore.yaml, requirements.txt | Python + Docker + YAML config |

### bedrock-media-type-mismatch/ (standalone)
- binary_search_langchain.py, binary_search_boto3.py, test_langchain_mismatch.py, test_boto3_real_jpeg.py
- bug_reproduction_report.md
- **Purpose**: Reproduce & diagnose LangChain Bedrock 400 media type mismatch errors

### datazone/ (1 subdir)
- error-creating-glossary-using-assumed-role/: 2 notebooks (create-glossary.ipynb, create-glossary-assume-role-Copy1.ipynb)

### glue/ (flat)
- pyspark-tutorial-glue.ipynb, apache-iceberg-johonny-chivers.md, README.md

### opensearch/ (1 subdir)
- create-resources/AOSS_resource_creation.ipynb

### sagemaker/ (6 subdirs)
| Subdirectory | Content |
|---|---|
| processing-custom-container/ | Dockerfile, requirements.txt, anomaly-detection-processing.ipynb, standalone_region_training_test.py |
| inference-recommender/ | inference_recommender.ipynb, BYOC_serverless_inference.ipynb, inference_script.py |
| terraform/connect-ec2-to-notebook-SMAI/ | Terraform configs (17 files) |
| serverless-inference/ | SI_walkthrough subdir |
| pipelines-sagemaker/ | sagemaker-pipelines-preprocess-train-evaluate-batch-transform/ |
| byoc-sm-jupyterlab/ | 3 subdirs (notebook-al2023, custom-configs-for-lustre, sagemaker-distribution) |

### notebooks/ (flat)
- getting_started.ipynb (78KB), ml_analysis_with_tests.ipynb

### kiro-test/ (empty except .venv)
- Contains a Python virtual environment only

### kiro-notes/ (flat)
- INDEX.md, 001_notes_repo_baseline.md, 002_cmd_nbstripout_verify.txt, 003_cmd_ruff_check.txt

---

## 2. Makefile Structure

```makefile
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
FIND_NB := find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -not -path "*/investigation/*" -not -path "*/kiro-*"

Targets:
- lint        → ruff check .
- validate    → python scripts/validate_notebooks.py
- strip-check → nbstripout --verify on all notebooks
- test-mac    → lint + validate + strip-check (local macOS target)
```

**Key design**: Uses local .venv, auto-creates if missing. Excludes investigation/ and kiro-* from notebook scanning.

---

## 3. Languages/Frameworks Used

| Language/Tool | Usage |
|---|---|
| **Python** | Primary language (100% of code) |
| **Jupyter Notebooks** | Primary format for samples (~25+ notebooks) |
| **boto3** | AWS SDK calls (Bedrock, SageMaker, DataZone, OpenSearch) |
| **LangChain** | Bedrock integration (media-type-mismatch samples) |
| **Strands Agents SDK** | AgentCore runtime agent hosting |
| **PySpark** | Glue ETL jobs |
| **Docker** | Container builds (SageMaker processing, AgentCore) |
| **Terraform** | SageMaker EC2-to-notebook infrastructure |
| **CloudFormation/SAM** | Referenced in AgentCore gateway setup |
| **Cedar** | Authorization policies for AgentCore Gateway |
| **ruff** | Python linter (pyproject.toml config) |
| **nbstripout** | Notebook output stripping |
| **GitHub Actions** | CI/CD (ci.yml + ec2-integration.yml) |

---

## 4. Deployment Patterns

| Sample Area | Deployment Pattern |
|---|---|
| **bedrock/** | No deployment — interactive notebooks run in SageMaker/local Jupyter |
| **bedrock-agentcore/** | Docker → ECR → CodeBuild → AgentCore Runtime (`.bedrock_agentcore.yaml` config). Uses `bedrock-agentcore` CLI SDK. |
| **bedrock-media-type-mismatch/** | Local Python scripts — no deployment |
| **sagemaker/processing-custom-container/** | Docker → ECR → SageMaker Processing Job |
| **sagemaker/terraform/** | Terraform apply → EC2 + SageMaker notebook instance |
| **sagemaker/byoc-sm-jupyterlab/** | Docker → ECR → SageMaker JupyterLab custom image |
| **datazone/, glue/, opensearch/** | Interactive notebooks — no deployment infra |
| **CI/CD** | GitHub Actions: (1) ci.yml on push/PR → lint+validate+strip-check, (2) ec2-integration.yml → self-hosted EC2 runner with Ubuntu + Arch Linux containers |

---

## 5. What the Enhanced Prompt Should Contain

Based on KB lessons (especially "kiro agent scoping" and "Critical Rules section has highest ROI"):

### Recommended Prompt Structure

1. **Identity & Purpose** (~2 sentences)
   - "You are the aws-samples agent. You help maintain and extend a collection of AWS service samples..."

2. **Critical Rules** (HIGHEST ROI — put first after identity)
   - NEVER modify existing notebook content (only add new files or CI/CD)
   - ALWAYS sanitize AWS account IDs before committing (replace with 123456789012)
   - ALWAYS run `make test-mac` before presenting changes as complete
   - NEVER commit notebook outputs (nbstripout enforced)
   - Verify factual claims against actual source code before stating them

3. **Repository Map** (concise reference)
   - Service directories: bedrock/, bedrock-agentcore/, bedrock-media-type-mismatch/, datazone/, glue/, opensearch/, sagemaker/, notebooks/
   - Infra: .github/workflows/ (ci.yml, ec2-integration.yml), Makefile, pyproject.toml
   - Meta: kiro-notes/, kiro-test/, investigation/

4. **Scope Boundaries** (what to do vs refuse)
   - IN SCOPE: Add new samples, fix CI/CD, add tests, update READMEs, lint fixes
   - OUT OF SCOPE: Modifying existing notebook logic, deploying to production, managing AWS resources

5. **Deployment Patterns** (so agent knows how each area works)
   - Notebooks: no deployment, just validate JSON + strip outputs
   - AgentCore: Docker → ECR → CodeBuild → AgentCore Runtime
   - SageMaker containers: Docker → ECR → Processing/Training jobs
   - Terraform: terraform init/plan/apply

6. **Code Standards**
   - Python: ruff (E, F, W rules), line-length 120
   - Notebooks: nbstripout required, E402/E501/F403/F405/E722/F821/E741/F841 ignored
   - All code: Python 3.11+, boto3 for AWS SDK

7. **CI/CD Awareness**
   - ci.yml: runs on every push/PR (lint, validate, strip-check)
   - ec2-integration.yml: runs on push to main + manual dispatch (Ubuntu + Arch)
   - Makefile: local macOS equivalent via `make test-mac`

8. **Your Available Tools** (if applicable)
   - List the specific tools the agent has access to

---

## Key Insights from KB

1. **"Critical Rules section has highest ROI" [seen: 7]** — The most impactful section of any agent prompt is the Critical Rules. Put non-negotiable constraints here.

2. **"Verify factual claims against actual source" [seen: 6]** — Agent must read files before making claims about them.

3. **"SANITIZE AWS account IDs" [seen: 2]** — The .bedrock_agentcore.yaml contains real account ID (794038231401). Agent must know to sanitize these.

4. **Agent scoping lesson** — Add "Scope Boundaries" and "Your Available Tools" sections. Agents with explicit scope are 52% faster and 59-71% cheaper.

5. **Multi-stack CloudFormation lesson** — AgentCore uses ordered stack deployment (SAM → Cognito → Gateway → Targets). Agent should understand this pattern.

6. **Media type mismatch lesson** — The bedrock-media-type-mismatch/ dir exists specifically to reproduce a LangChain bug where declared content type doesn't match actual image format.
