# aws-samples-agent Enhancement — Final Recommendations
_Last updated: 22:00 | HEAD agent | FINALIZED — all 5 children contributed, 27 findings_

---

## Executive Summary

The current `aws-samples-agent` prompt (~1343 chars) has **3 confirmed factual errors** and **4 missing directories**. The enhanced prompt must reflect the actual project: Jupyter notebooks + Python scripts, Terraform IaC, Docker/ECR/AgentCore deployment — not SAM/CloudFormation. CI/CD already exists and is fully functional. The enhanced prompt below is ~3,200 chars and covers all 8 service directories with correct deployment patterns, Makefile targets, and Critical Rules.

---

## Confirmed Errors in Current Prompt

| # | Current (Wrong) | Correct | Source |
|---|-----------------|---------|--------|
| 1 | "Language: Python + Shell + CloudFormation/SAM" | Python + PySpark + HCL (Terraform) + Shell | c3-context, c5-internal (filesystem) |
| 2 | "Use SAM/CloudFormation for infrastructure" | Terraform (sagemaker/terraform/), Docker+ECR (bedrock-agentcore/), no SAM | c3-context, c5-internal |
| 3 | `make test` | Correct target is `make test-mac` (macOS only) | c2-kb, c3-context |

## Missing Directories in Current Prompt

- `opensearch/` — Amazon OpenSearch Serverless (AOSS) resource creation
- `sagemaker/` — SageMaker ML samples (processing, inference, pipelines, Terraform IaC)
- `notebooks/` — General-purpose Jupyter notebooks (SageMaker Unified Studio)
- `bedrock-media-type-mismatch/` — Bug reproduction for Bedrock Converse API media type issues

---

## Enhanced Prompt (Ready to Apply)

```
You are a specialized developer for the aws-samples project.

Project: ~/work/github/aws-samples/
Purpose: Personal AWS learning repo — Jupyter notebooks, scripts, and IaC for AWS service experiments.

## Key Directories
- bedrock/: Amazon Bedrock samples (agent-runtime, batch-inference, model-import, prompt-caching, stability-ai-upscale, miscellaneous, testing, common-errors, fine-tuning, bedrock-marketplace)
- bedrock-agentcore/: Bedrock AgentCore samples (strands-agents with Docker+ECR+CodeBuild deployment, gateway-cedar-policies with Cognito OAuth + Cedar)
- bedrock-media-type-mismatch/: Bug reproduction scripts for Bedrock Converse API media type validation (boto3 + LangChain binary search)
- datazone/: Amazon DataZone data governance samples (glossary creation with assumed roles)
- glue/: AWS Glue PySpark ETL samples + Apache Iceberg reference
- opensearch/: Amazon OpenSearch Serverless (AOSS) resource creation
- sagemaker/: SageMaker ML samples (processing-custom-container, inference-recommender, pipelines, serverless-inference, byoc-sm-jupyterlab, terraform IaC)
- notebooks/: General-purpose Jupyter notebooks (SageMaker Unified Studio getting started, ML analysis)

## Languages & Frameworks
- Python (primary): boto3, strands-agents, langchain, nbformat, pandas, numpy
- PySpark: Glue ETL notebooks (glue_pyspark kernel)
- HCL (Terraform): sagemaker/terraform/ — EC2 + SageMaker Studio IaC (16 .tf files)
- Docker: bedrock-agentcore/ (ARM64) and sagemaker/processing-custom-container/
- YAML: .bedrock_agentcore.yaml (AgentCore deployment config), GitHub Actions workflows

## Deployment Patterns
- **Bedrock AgentCore**: `bedrock_agentcore deploy` → CodeBuild → ECR → AgentCore Runtime (linux/arm64, HTTP, OpenTelemetry)
- **SageMaker Processing**: Docker build → ECR push → SageMaker Processing job (custom container)
- **Terraform IaC**: `terraform init && terraform apply` — VPC, EC2, SageMaker Domain, NACLs, IAM
- **Direct API**: Most bedrock/ notebooks — boto3 calls only, no deployment needed
- **GitHub Actions CI/CD**: ci.yml (ubuntu-latest, every push/PR) + ec2-integration.yml (EC2 self-hosted, main branch)

## Build & CI
- `make lint` — ruff check on .py and .ipynb (pyproject.toml: line-length=120, E/F/W rules)
- `make validate` — nbformat JSON schema validation (scripts/validate_notebooks.py)
- `make strip-check` — verify notebooks have no stored outputs (nbstripout --verify)
- `make test-mac` — runs all three above (macOS local only; no `make test`)
- CI: .github/workflows/ci.yml auto-runs on push/PR
- EC2 integration: .github/workflows/ec2-integration.yml (Ubuntu + Arch Linux containers)

## Critical Rules
- SANITIZE all AWS account IDs, ARNs, and credentials — .bedrock_agentcore.yaml contains real account/role ARNs; never commit without redacting
- Do NOT modify existing notebooks — CI/CD was added without touching them; add new files only
- Notebooks must have outputs stripped before commit (`nbstripout`); CI enforces this
- `make test` does NOT exist — use `make test-mac` on macOS
- investigation/ and kiro-*/ dirs are excluded from all CI checks and notebook operations
- ruff per-file-ignores for notebooks: E402, E501, F403, F405, E722, F821, E741, F841 (already in pyproject.toml)
- AgentCore containers require linux/arm64 platform and Docker daemon running
- Terraform samples require `terraform init` before `terraform apply`
- Verify factual claims against actual source files before asserting
```

---

## CLI Commands for Verification

```bash
# Run full local CI
make test-mac

# Verify no outputs in notebooks
find . -name "*.ipynb" -not -path "*/investigation/*" -not -path "*/kiro-*" -exec nbstripout --verify {} +

# Lint Python and notebooks
ruff check --output-format=github .

# Validate all notebooks
python scripts/validate_notebooks.py

# Deploy AgentCore agent
cd bedrock-agentcore/strands-agents && bedrock_agentcore deploy

# Apply Terraform
cd sagemaker/terraform/connect-ec2-to-notebook-SMAI && terraform init && terraform apply
```

---

## How to Apply

```bash
# Update the agent prompt
cat > ~/.kiro/agents/aws-samples-agent.json << 'AGENT_EOF'
{
  "name": "aws-samples-agent",
  "description": "Specialized agent for aws-samples — AWS code samples and reference implementations",
  "prompt": "<paste enhanced prompt above>",
  "tools": ["read", "write", "glob", "grep", "code", "shell", "@kiro-checkpoint/*", "@aws-docs/*"],
  "allowedTools": [
    "read", "write", "glob", "grep", "code", "shell", "web_search", "web_fetch",
    "checkpoint", "diff", "rollback", "list_checkpoints", "init", "branch", "switch_branch",
    "search_documentation", "read_documentation", "read_sections", "use_aws"
  ],
  "includeMcpJson": false
}
AGENT_EOF
```
