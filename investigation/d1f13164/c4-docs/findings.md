# Investigation Findings: AWS Documentation & Repository Analysis for CI/CD Setup

**Agent:** c4-docs (AWS Documentation)
**Date:** 2026-03-27
**Topic:** Repository structure analysis + AWS docs research for GitHub Actions CI/CD for Jupyter notebooks

---

## 1. Repository Structure Analysis

### 1.1 Top-Level Layout

```
aws-samples/
├── README.md                          # Repo overview
├── LICENSE                            # License file
├── .gitignore                         # Ignores config.py, env, .ipynb_checkpoints, .terraform
├── .libs.json                         # SageMaker Studio library config (S3 paths, conda)
├── TASK.md                            # CI/CD task description
├── SAGEMAKER_UNIFIED_STUDIO_README.md # SageMaker Unified Studio docs
├── bedrock/                           # Amazon Bedrock samples (11 subdirs)
├── bedrock-agentcore/                 # Bedrock AgentCore (strands-agents, gateway-cedar)
├── bedrock-media-type-mismatch/       # Bug reproduction scripts (.py files, no notebooks)
├── datazone/                          # Amazon DataZone samples
├── glue/                              # AWS Glue PySpark samples
├── notebooks/                         # General-purpose notebooks
├── opensearch/                        # Amazon OpenSearch samples
└── sagemaker/                         # SageMaker samples (8 subdirs)
```

### 1.2 Key Finding: NO Existing CI/CD or Configuration

- **No `.github/` directory** — no GitHub Actions workflows exist
- **No `Makefile`** — none at repo root or any subdirectory
- **No root `requirements.txt`** — only scattered per-project requirements
- **No `pyproject.toml`, `setup.py`, `setup.cfg`** — no Python project configuration
- **No pre-commit config** (`.pre-commit-config.yaml`)
- **No linting config** (`ruff.toml`, `.flake8`, etc.)

### 1.3 Existing `.gitignore`

```
config.py
env
.ipynb_checkpoints
*/.ipynb_checkpoints/*
sagemaker/how-to-use-inference-recommender/envi
sagemaker/how-to-use-inference-recommender/model/1
.terraform
*/.terraform/*
```

**Note:** Does NOT currently ignore notebook outputs, `.venv`, `__pycache__`, or CI artifacts.

### 1.4 Existing `requirements.txt` Files (Per-Project)

| Path | Contents |
|------|----------|
| `bedrock-agentcore/strands-agents/requirements.txt` | strands-agents-tools, uv, boto3, bedrock-agentcore, bedrock-agentcore-starter-toolkit |
| `bedrock/stability-ai-upscale/requirements.txt` | boto3, pillow |
| `sagemaker/processing-custom-container/requirements.txt` | pandas, joblib, numpy, rrcf, scipy, pyarrow, swifter |
| `sagemaker/inference-recommender/code/requirements.txt` | numpy==1.26.4, pillow==11.2.1 |

### 1.5 Jupyter Notebook Inventory

**Total: 40 notebooks** across the repository.

| Directory | Count | Notable Kernels |
|-----------|-------|-----------------|
| `bedrock/miscellaneous/` | 11 | Python 3 (ipykernel), conda_python3 |
| `sagemaker/` (all subdirs) | 13 | conda_pytorch_p310, conda_tensorflow2_p310, conda_python3 |
| `bedrock-agentcore/` | 2 | Python 3 (ipykernel) |
| `bedrock/` (other subdirs) | 8 | conda_python3, conda_tensorflow2_p310 |
| `notebooks/` | 2 | Python 3 (ipykernel), Python 3 |
| `glue/` | 1 | Glue PySpark |
| `opensearch/` | 1 | conda_tensorflow2_p310 |
| `datazone/` | 2 | conda_pytorch_p310 |

**Size range:** 0.1 KB (empty `Untitled.ipynb`) to 2006 KB (`retail_sales_prediction.ipynb`)
**Code cells range:** 0 to 108 cells per notebook
**Largest notebooks with outputs:** `retail_sales_prediction.ipynb` (2MB), `inference_recommender.ipynb` (734KB) — these contain embedded outputs that `nbstripout` would clean.

---

## 2. AWS Documentation Findings: CI/CD Best Practices

### 2.1 AWS Prescriptive Guidance — CI/CD Best Practices

**Source:** [Best practices for CI/CD pipelines](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-cicd-litmus/cicd-best-practices.html)

Key recommendations applicable to this project:
- **Review code in repositories** — require code reviews before merging; at least one senior reviewer
- **Make small and frequent merges** — push local changes continuously
- **Secure the production environment** — limit console/programmatic access
- **Separate accounts per environment** — isolate test from production

### 2.2 AWS Prescriptive Guidance — Tests for CI/CD Pipelines

**Source:** [Tests for CI/CD pipelines](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-cicd-litmus/tests-for-cicd-pipelines.html)

AWS defines these test types for pipelines:
- **Unit tests** — verify code performs as expected (pytest recommended)
- **Integration tests** — verify against provisioned test environment
- **SAST (Static Application Security Testing)** — analyze code for security violations
- **Acceptance tests** — verify user requirements

**Minimum recommended:** Unit tests + SAST on code, integration + acceptance tests on test environment.

**Relevance to this project:**
- `ruff` linting maps to SAST/static analysis
- Notebook JSON validation maps to unit testing
- EC2-based notebook loading maps to integration testing
- `nbstripout` is a pre-commit/CI hygiene tool (not a test per se)

### 2.3 AWS CI/CD Security Whitepaper

**Source:** [Security in every stage of CI/CD pipeline](https://docs.aws.amazon.com/whitepapers/latest/practicing-continuous-integration-continuous-delivery/security-in-every-stage-of-cicd-pipeline.html)

Relevant security stages for this project:
- **Pre-commit hooks** — `nbstripout` as a pre-commit hook to prevent accidental output commits
- **SAST** — `ruff` for Python linting/security checks
- **IDE tools and plugins** — local development validation via Makefile

---

## 3. AWS Documentation Findings: GitHub Actions Integration

### 3.1 GitHub Actions with AWS SAM (Reference Pattern)

**Source:** [Using GitHub Actions to deploy with AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/deploying-using-github.html)

Example workflow pattern from AWS docs:
```yaml
on:
  push:
    branches:
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
      - uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-2
```

**Key takeaway:** AWS officially recommends `ubuntu-latest` as the runner OS for GitHub Actions workflows. This aligns with the task requirement for `ubuntu-latest` CI.

### 3.2 CodeBuild-Hosted GitHub Actions Runners (Alternative for EC2)

**Source:** [Self-hosted GitHub Actions runners in AWS CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/action-runner-overview.html)

AWS CodeBuild can host self-hosted GitHub Actions runners, providing:
- Native IAM integration
- AWS Secrets Manager integration
- CloudTrail logging
- VPC access
- Latest instance types including ARM

**Workflow YAML syntax:**
```yaml
runs-on: codebuild-<project-name>-${{ github.run_id }}-${{ github.run_attempt }}
```

**Available compute images for CodeBuild runners:**

| Type | Image | Platform |
|------|-------|----------|
| `ubuntu` | `7.0` | Ubuntu 22.04 |
| `ubuntu` | `6.0` | Ubuntu 22.04 |
| `ubuntu` | `5.0` | Ubuntu 20.04 |
| `linux` | `5.0` | Amazon Linux 2023 |
| `arm` | `3.0` | Amazon Linux 2023 |

**Limitation for this project:** CodeBuild does NOT offer Arch Linux images. For Arch Linux integration tests, a self-hosted runner on a real EC2 instance with an Arch Linux AMI would be needed, or a Docker container approach.

### 3.3 AWS-SetupJupyter SSM Runbook

**Source:** [AWS-SetupJupyter](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/aws-setup-jupyter.html)

AWS provides an SSM Automation runbook `AWS-SetupJupyter` that:
- Sets up Jupyter Notebook on an EC2 instance
- Can launch a new instance or use existing
- Requires a SecureString parameter for Jupyter password
- Supports Linux platforms
- Uses CloudFormation for infrastructure

**Relevance:** This could be used for EC2-based integration tests, but for CI/CD purposes, installing Jupyter via pip in a GitHub Actions workflow is simpler and more maintainable.

---

## 4. Best Practices Research: Notebook CI/CD Tools

### 4.1 nbstripout — Stripping Notebook Outputs

**Purpose:** Remove cell outputs and execution counts from Jupyter notebooks before committing to version control.

**CI/CD usage pattern:**
```bash
pip install nbstripout
# Check mode (fails if outputs found — good for CI)
nbstripout --is-stripped *.ipynb
# Or strip in-place
find . -name '*.ipynb' -exec nbstripout {} +
```

**Best practice from AWS CI/CD guidance (SAST stage):**
- Run as a pre-commit hook locally
- Run as a CI check to enforce clean notebooks
- Prevents accidental commit of sensitive outputs (API keys, data samples)

**Known limitations:**
- Does not validate notebook structure
- Only checks/strips outputs, not metadata
- Some notebooks intentionally have outputs for documentation purposes

### 4.2 ruff — Python Linting for Notebook Cells

**Purpose:** Fast Python linter that can lint `.py` files extracted from notebook code cells.

**CI/CD usage pattern:**
```bash
pip install ruff nbconvert
# Extract .py from notebooks, then lint
jupyter nbconvert --to script *.ipynb
ruff check --select E,W,F *.py
```

**Alternative approach (ruff native notebook support):**
As of ruff 0.1.0+, ruff can lint `.ipynb` files directly:
```bash
ruff check --include "*.ipynb" .
```

**Best practice alignment:** Maps to SAST (Static Application Security Testing) in the AWS CI/CD pipeline reference architecture.

### 4.3 Notebook JSON Validation

**Purpose:** Verify that `.ipynb` files are valid JSON and conform to the nbformat schema.

**CI/CD usage pattern:**
```python
import json, sys, nbformat
for path in sys.argv[1:]:
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
    nbformat.validate(nb)
```

**Or simpler JSON-only validation:**
```bash
python -c "import json, sys; [json.load(open(f)) for f in sys.argv[1:]]" *.ipynb
```

**Best practice:** Validates notebook integrity after merges, prevents corrupted notebooks from entering the repo.

### 4.4 EC2-Based Integration Tests

**For Ubuntu:**
- GitHub Actions provides `ubuntu-latest` (Ubuntu 22.04) natively
- AWS CodeBuild provides Ubuntu 22.04 images
- Install Python, pip, jupyter, then validate notebooks load

**For Arch Linux:**
- No native GitHub Actions runner for Arch Linux
- No AWS CodeBuild image for Arch Linux
- **Options:**
  1. Self-hosted runner on EC2 with Arch Linux AMI
  2. Docker container with `archlinux:latest` image in GitHub Actions
  3. Use `runs-on: self-hosted` with a pre-configured Arch Linux EC2 instance

**Docker approach (recommended for CI):**
```yaml
jobs:
  test-arch:
    runs-on: ubuntu-latest
    container:
      image: archlinux:latest
    steps:
      - uses: actions/checkout@v4
      - run: pacman -Syu --noconfirm python python-pip jupyter-notebook
      - run: # validate notebooks
```

### 4.5 macOS Local-Only Testing via Makefile

**Purpose:** Allow developers on macOS to run the same validation locally without CI.

**Makefile pattern:**
```makefile
.PHONY: lint validate test-mac

lint:
	ruff check --include "*.ipynb" .

validate:
	python scripts/validate_notebooks.py

test-mac: lint validate
	@echo "All local tests passed"
```

**Best practice:** The Makefile should mirror CI steps so developers catch issues before pushing.

---

## 5. Known Limitations & Considerations

### 5.1 GitHub Actions Limitations
- **macOS runners** are available (`macos-latest`) but expensive (10x Linux cost) — hence the Makefile-only approach is cost-effective
- **Self-hosted runners** require maintenance and security hardening
- **Arch Linux** has no official GitHub Actions runner or CodeBuild image

### 5.2 Notebook-Specific Challenges
- **40 notebooks** with varying kernels (conda_python3, conda_pytorch_p310, etc.) — CI cannot replicate all SageMaker/Glue kernels
- **Large notebooks** (up to 2MB) with embedded outputs — `nbstripout` check will flag these
- **Glue PySpark notebook** uses `Glue PySpark` kernel — cannot be validated in standard Python environment
- **Some notebooks may have intentional outputs** for documentation

### 5.3 EC2 Integration Test Considerations
- Per AWS best practices, EC2 instances for testing should use IAM roles (not access keys)
- AWS recommends using SSM for managing EC2 instances
- For Arch Linux on EC2: community AMIs exist but are not officially supported by AWS
- Cost consideration: EC2 instances incur charges; use spot instances or terminate after tests

### 5.4 Security Considerations (from AWS CI/CD Whitepaper)
- Never embed credentials in workflow files — use GitHub Secrets
- Apply least-privilege IAM roles for any AWS integration
- Use pre-commit hooks (nbstripout) to prevent sensitive data leaks in notebook outputs
- Review all code changes before merging (AWS best practice)

---

## 6. Summary of Actionable Findings

| Item | Current State | Recommended Action |
|------|--------------|-------------------|
| `.github/workflows/` | Does not exist | Create CI workflow with lint, validate, strip-check jobs |
| `Makefile` | Does not exist | Create with `lint`, `validate`, `test-mac` targets |
| Root `requirements.txt` | Does not exist | Create CI-specific `requirements-ci.txt` (nbstripout, ruff, nbformat, jupyter) |
| `.gitignore` | Minimal | Add `__pycache__`, `.venv`, `*.py[cod]`, CI artifacts |
| Pre-commit config | Does not exist | Optional: add `.pre-commit-config.yaml` with nbstripout |
| Ruff config | Does not exist | Create `ruff.toml` or `pyproject.toml` with notebook-aware settings |
| Notebook outputs | Many notebooks have outputs | `nbstripout --is-stripped` check in CI (may need baseline exceptions) |
| EC2 integration tests | None | GitHub Actions workflow with Ubuntu + Arch Linux (Docker container) |
| macOS testing | None | Makefile `test-mac` target for local validation |

---

## 7. AWS Documentation Sources

1. [Best practices for CI/CD pipelines - AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-cicd-litmus/cicd-best-practices.html)
2. [Tests for CI/CD pipelines - AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-cicd-litmus/tests-for-cicd-pipelines.html)
3. [Security in every stage of CI/CD pipeline - AWS Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/practicing-continuous-integration-continuous-delivery/security-in-every-stage-of-cicd-pipeline.html)
4. [Using GitHub Actions to deploy with AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/deploying-using-github.html)
5. [Self-hosted GitHub Actions runners in AWS CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/action-runner-overview.html)
6. [Tutorial: Configure a CodeBuild-hosted GitHub Actions runner](https://docs.aws.amazon.com/codebuild/latest/userguide/action-runner.html)
7. [Compute images supported with CodeBuild-hosted GitHub Actions runner](https://docs.aws.amazon.com/codebuild/latest/userguide/sample-github-action-runners-update-yaml.images.html)
8. [AWS-SetupJupyter SSM Runbook](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/aws-setup-jupyter.html)
9. [SEC01-BP06 Automate testing and validation of security controls in pipelines - AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/2023-10-03/framework/sec_securely_operate_test_validate_pipeline.html)
