# Validated Findings: c4-docs (AWS Documentation & Repository Analysis)

**Validator run:** 2026-03-27
**Source:** `findings.md` from c4-docs agent

---

## Section 1: Repository Structure Analysis

### 1.1 Top-Level Layout

| Claim | Verdict | Evidence |
|-------|---------|----------|
| Directories: bedrock, bedrock-agentcore, bedrock-media-type-mismatch, datazone, glue, notebooks, opensearch, sagemaker | **CONFIRMED** | `ls` output matches all listed directories |
| Files: README.md, LICENSE, .gitignore, .libs.json, TASK.md, SAGEMAKER_UNIFIED_STUDIO_README.md | **CONFIRMED** | All files present in directory listing |

### 1.2 No Existing CI/CD or Configuration

| Claim | Verdict | Evidence |
|-------|---------|----------|
| No `.github/` directory | **CONFIRMED** | `ls .github` → "No such file or directory" |
| No `Makefile` | **CONFIRMED** | `find . -name "Makefile"` → empty |
| No root `requirements.txt` | **CONFIRMED** | `ls requirements.txt` → "No such file or directory" |
| No `pyproject.toml`, `setup.py`, `setup.cfg` | **CONFIRMED** | All three missing |
| No `.pre-commit-config.yaml` | **CONFIRMED** | File not found |
| No `ruff.toml`, `.flake8` | **CONFIRMED** | Neither file found |

### 1.3 .gitignore Contents

| Claim | Verdict | Evidence |
|-------|---------|----------|
| .gitignore contents match exactly | **CONFIRMED** | `cat .gitignore` output is byte-for-byte identical to what findings report |
| Does NOT ignore notebook outputs, `.venv`, `__pycache__`, CI artifacts | **CONFIRMED** | None of these patterns appear in .gitignore |

### 1.4 Requirements.txt Files

| Claim | Verdict | Evidence |
|-------|---------|----------|
| 4 requirements.txt files exist at stated paths | **CONFIRMED** | `find . -name "requirements.txt"` returns exactly these 4 |
| Contents of each file match | **CONFIRMED** | `cat` output matches findings exactly |

### 1.5 Jupyter Notebook Inventory

| Claim | Verdict | Evidence |
|-------|---------|----------|
| Total: 40 notebooks | **CONFIRMED** | `find . -name "*.ipynb" | wc -l` → 40 |
| bedrock/miscellaneous: 11 notebooks | **CONTRADICTED** | Actual count: **10**. The notebook list shows 10 files in bedrock/miscellaneous/ |
| sagemaker (all subdirs): 13 | **CONFIRMED** | `find ./sagemaker -name "*.ipynb" | wc -l` → 13 |
| bedrock-agentcore: 2 | **CONFIRMED** | Count verified: 2 |
| bedrock (other subdirs): 8 | **CONTRADICTED** | Actual count: **9**. (10 misc + 9 other = 19 total bedrock, which is correct, but the split is wrong) |
| notebooks: 2 | **CONFIRMED** | Count verified: 2 |
| glue: 1 | **CONFIRMED** | Count verified: 1 |
| opensearch: 1 | **CONFIRMED** | Count verified: 1 |
| datazone: 2 | **CONFIRMED** | Count verified: 2 |
| bedrock has "11 subdirs" | **CONTRADICTED** | Actual: **10 subdirectories** (agent-runtime, batch-inference, bedrock-marketplace, common-errors, fine-tuning, miscellaneous, model-import, prompt-caching, stability-ai-upscale, testing) |
| retail_sales_prediction.ipynb ~2006 KB (2MB) | **CONFIRMED** | Actual: 2,054,339 bytes = 2006 KB |
| inference_recommender.ipynb ~734KB | **CONFIRMED** | Actual: 752,035 bytes ≈ 734 KB |
| Smallest notebook 0.1 KB | **CONFIRMED** (approx) | Smallest is Untitled.ipynb at 72 bytes (0.07 KB). Close enough to "0.1 KB" |
| sagemaker has "8 subdirs" | **UNVERIFIED** | Not explicitly counted, but directory listing shows: terraform, processing-custom-container, inference-recommender, retail_sales_prediction.ipynb (file), serverless-inference, pipelines-sagemaker, byoc-sm-jupyterlab = 7 subdirs (not 8). Likely **CONTRADICTED** if the file is excluded. |

---

## Section 2: AWS Documentation Findings — CI/CD Best Practices

| Claim | Verdict | Evidence |
|-------|---------|----------|
| URL: `docs.aws.amazon.com/prescriptive-guidance/latest/strategy-cicd-litmus/cicd-best-practices.html` exists | **UNVERIFIED** | Not fetched directly, but this is a well-known AWS Prescriptive Guidance page |
| Recommendations: code reviews, small merges, secure prod, separate accounts | **UNVERIFIED** | Standard AWS CI/CD guidance; plausible but not cross-checked |
| URL: `docs.aws.amazon.com/prescriptive-guidance/latest/strategy-cicd-litmus/tests-for-cicd-pipelines.html` | **UNVERIFIED** | Not fetched |
| Test types: unit, integration, SAST, acceptance | **UNVERIFIED** | Standard CI/CD taxonomy; plausible |
| URL: `docs.aws.amazon.com/whitepapers/latest/practicing-continuous-integration-continuous-delivery/security-in-every-stage-of-cicd-pipeline.html` | **UNVERIFIED** | Not fetched |

---

## Section 3: AWS Documentation — GitHub Actions Integration

### 3.1 SAM GitHub Actions Example

| Claim | Verdict | Evidence |
|-------|---------|----------|
| AWS SAM docs show GitHub Actions example with `ubuntu-latest` | **CONFIRMED** | Fetched actual page; example uses `runs-on: ubuntu-latest` |
| Example uses `actions/checkout@v3`, `actions/setup-python@v3`, `aws-actions/configure-aws-credentials@v1` | **CONFIRMED** | All present in the actual AWS docs example |
| Findings omit `aws-actions/setup-sam@v2` step from the example | **CONFIRMED** (minor omission) | The actual AWS docs example includes this step; findings presented it as a "pattern" which is acceptable but incomplete |

### 3.2 CodeBuild-Hosted GitHub Actions Runners

| Claim | Verdict | Evidence |
|-------|---------|----------|
| `runs-on: codebuild-<project-name>-${{ github.run_id }}-${{ github.run_attempt }}` syntax | **CONFIRMED** | Exact match with AWS CodeBuild docs |
| ubuntu 7.0 = Ubuntu 22.04 | **CONFIRMED** | AWS docs confirm |
| ubuntu 6.0 = Ubuntu 22.04 | **CONFIRMED** | AWS docs confirm |
| ubuntu 5.0 = Ubuntu 20.04 | **CONFIRMED** | AWS docs confirm |
| linux 5.0 = Amazon Linux 2023 | **CONFIRMED** | AWS docs confirm |
| arm 3.0 = Amazon Linux 2023 | **CONFIRMED** | AWS docs confirm |
| CodeBuild does NOT offer Arch Linux images | **CONFIRMED** | Full image table reviewed; no Arch Linux entries |
| CodeBuild provides native IAM, Secrets Manager, CloudTrail, VPC integration | **UNVERIFIED** | Not explicitly checked in the fetched page, but consistent with CodeBuild's known capabilities |

### 3.3 AWS-SetupJupyter SSM Runbook

| Claim | Verdict | Evidence |
|-------|---------|----------|
| Sets up Jupyter Notebook on EC2 | **CONFIRMED** | AWS docs: "helps you set up Jupyter Notebook on an Amazon EC2 instance" |
| Can launch new instance or use existing | **CONFIRMED** | AmiId (optional) + InstanceId parameters confirmed |
| Requires SecureString parameter for Jupyter password | **CONFIRMED** | JupyterPasswordSSMKey parameter documented as required |
| Supports Linux platforms | **CONFIRMED** | Platforms: "Linux" |
| Uses CloudFormation for infrastructure | **CONFIRMED** | StackName parameter + cloudformation:* IAM permissions confirmed |

---

## Section 4: Tool Claims

### 4.1 nbstripout

| Claim | Verdict | Evidence |
|-------|---------|----------|
| `nbstripout --is-stripped *.ipynb` is the check mode for CI | **CONTRADICTED** | The correct flag is `--verify`, not `--is-stripped`. From the official README: "`nbstripout --verify FILE.ipynb` — Do a verification run, which works like dry run but will fail if any files would have been stripped." The `--is-installed` flag checks installation status, not file state. |
| Can strip in-place with `find . -name '*.ipynb' -exec nbstripout {} +` | **CONFIRMED** | Documented in official README |
| Prevents accidental commit of sensitive outputs | **CONFIRMED** | Core purpose of the tool |
| Does not validate notebook structure | **CONFIRMED** | nbstripout only strips outputs/metadata |
| Only checks/strips outputs, not metadata | **CONTRADICTED** | nbstripout DOES strip certain metadata by default (signature, widgets, ExecuteTime, collapsed, execution, heading_collapsed, hidden, scrolled) |
| nbstripout has a reusable GitHub Action | **NOT MENTIONED** (gap) | The findings don't mention `kynan/nbstripout@main` GitHub Action, which provides a ready-made CI check. This is a significant omission for a CI/CD-focused investigation. |

### 4.2 ruff — Python Linting

| Claim | Verdict | Evidence |
|-------|---------|----------|
| ruff can lint `.ipynb` files directly | **CONFIRMED** | Documented in ruff docs and multiple sources |
| "As of ruff 0.1.0+" for native notebook support | **CONTRADICTED** (minor) | Notebook support was stabilized in **v0.1.5** (per astral.sh blog), not v0.1.0. Preview support existed earlier. |
| `ruff check --include "*.ipynb" .` syntax | **CONFIRMED** | Valid CLI syntax; alternatively `extend-include = ["*.ipynb"]` in config |
| Alternative: `jupyter nbconvert --to script` then lint | **CONFIRMED** | Standard approach, though less preferred now that ruff has native support |

### 4.3 Notebook JSON Validation

| Claim | Verdict | Evidence |
|-------|---------|----------|
| nbformat can validate notebook schema | **UNVERIFIED** | Standard nbformat capability; not tested but well-documented |
| Code snippets are syntactically correct | **UNVERIFIED** | Not executed |

### 4.4 EC2-Based Integration Tests / Arch Linux

| Claim | Verdict | Evidence |
|-------|---------|----------|
| No native GitHub Actions runner for Arch Linux | **CONFIRMED** | GitHub only provides ubuntu, windows, macos runners |
| No AWS CodeBuild image for Arch Linux | **CONFIRMED** | Verified against full CodeBuild image table |
| Docker container approach with `archlinux:latest` is viable | **UNVERIFIED** | Plausible approach but not tested |
| `pacman -Syu --noconfirm python python-pip jupyter-notebook` for Arch setup | **UNVERIFIED** | Standard pacman syntax; package names not verified |

---

## Section 5: Limitations & Considerations

| Claim | Verdict | Evidence |
|-------|---------|----------|
| macOS runners are 10x Linux cost | **CONFIRMED** | GitHub docs: "macOS runners consume minutes at 10 times the rate that jobs on Linux runners consume" ($0.08/min vs $0.008/min) |
| Self-hosted runners require maintenance and security hardening | **CONFIRMED** | Standard operational truth |
| 40 notebooks with varying kernels | **CONFIRMED** (count); kernels **UNVERIFIED** |
| Glue PySpark notebook cannot be validated in standard Python | **CONFIRMED** | Glue PySpark kernel requires AWS Glue environment |
| Arch Linux community AMIs exist but not officially supported by AWS | **UNVERIFIED** | Plausible but not verified |

---

## Summary

| Category | CONFIRMED | CONTRADICTED | UNVERIFIED |
|----------|-----------|--------------|------------|
| Repo structure (Section 1) | 22 | 4 | 1 |
| AWS CI/CD docs (Section 2) | 0 | 0 | 5 |
| GitHub Actions/CodeBuild (Section 3) | 14 | 0 | 1 |
| Tool claims (Section 4) | 5 | 3 | 4 |
| Limitations (Section 5) | 4 | 0 | 2 |
| **TOTAL** | **45** | **7** | **13** |

### Key Contradictions

1. **bedrock/miscellaneous notebook count**: Claimed 11, actual 10
2. **bedrock other subdirs notebook count**: Claimed 8, actual 9
3. **bedrock subdirectory count**: Claimed 11, actual 10
4. **sagemaker subdirectory count**: Likely 7, not 8 (one entry is a file, not a subdir)
5. **`nbstripout --is-stripped`**: Flag does not exist. Correct flag is `--verify`
6. **nbstripout "only checks outputs, not metadata"**: It also strips metadata by default
7. **ruff notebook support "0.1.0+"**: Stabilized in v0.1.5, not v0.1.0

### Key Gaps (Not Contradictions)

1. nbstripout has a reusable GitHub Action (`kynan/nbstripout@main`) not mentioned in findings — significant for CI/CD setup
2. SAM example omits `aws-actions/setup-sam@v2` step (minor, findings framed it as a pattern)
3. CodeBuild image table in findings is a subset (acceptable, not claimed as exhaustive)
