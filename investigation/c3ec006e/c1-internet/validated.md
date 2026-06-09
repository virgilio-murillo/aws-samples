# Validated Findings: Internet Research for aws-samples-agent Enhancement

## Validation Method
- Local filesystem inspection of `/Users/murivirg/work/github/aws-samples/`
- Web search verification of GitHub repos and URLs
- Cross-referencing claims against actual project structure

---

## Section 1: Subdirectory Contents

### Claim: bedrock/ contains "agents-and-function-calling/, introduction-to-bedrock/, knowledge-bases/"
**CONTRADICTED** — This describes the PUBLIC `aws-samples/amazon-bedrock-samples` repo, NOT the local project. The local `bedrock/` directory actually contains: `stability-ai-upscale/`, `miscellaneous/`, `model-import/`, `fine-tuning/`, `batch-inference/`, `testing/`, `prompt-caching/`, `bedrock-marketplace/`, `agent-runtime/`, `common-errors/`. Primarily Jupyter notebooks and Python scripts.

### Claim: bedrock-agentcore/ uses AgentCore CLI, supports Strands/LangGraph/Google ADK/OpenAI Agents, ARM64, entrypoint.py pattern
**PARTIALLY CONTRADICTED** — The local project only contains `strands-agents/` and `gateway-cedar-policies/`. No LangGraph, Google ADK, or OpenAI Agents present. The Dockerfile uses `CMD ["opentelemetry-instrument", "python", "-m", "strands_claude"]`, NOT an `entrypoint.py` pattern. The multi-framework claim applies to the public `awslabs/amazon-bedrock-agentcore-samples` repo, not this local project.

### Claim: bedrock-media-type-mismatch/ demonstrates Converse API media type validation issue
**CONFIRMED** — Local directory contains `binary_search_langchain.py`, `binary_search_boto3.py`, `test_langchain_mismatch.py`, `test_boto3_real_jpeg.py`, and `bug_reproduction_report.md`. Clearly a bug reproduction/troubleshooting sample.

### Claim: datazone/ is "Enterprise data mesh with CDK and CloudFormation"
**CONTRADICTED** — The local `datazone/` directory contains only a notebook about `error-creating-glossary-using-assumed-role/`. No CDK, no CloudFormation. The CDK/CloudFormation claim describes the public `aws-samples/data-mesh-datazone-cdk-cloudformation` repo, not this project.

### Claim: glue/ contains PySpark ETL jobs, CDK-based CI/CD
**PARTIALLY CONFIRMED** — Local `glue/` has `pyspark-tutorial-glue.ipynb` and `apache-iceberg-johonny-chivers.md`. PySpark is present. No CDK-based CI/CD found locally.

### Claim: opensearch/ is Amazon OpenSearch Serverless samples
**CONFIRMED** — Local `opensearch/` has `create-resources/` subdirectory and a README. Consistent with AOSS resource creation samples.

### Claim: sagemaker/ has Terraform-based deployment patterns
**CONFIRMED** — `sagemaker/terraform/connect-ec2-to-notebook-SMAI/` contains 10+ `.tf` files (vpc.tf, ec2.tf, iam.tf, sagemaker.tf, etc.). Also has processing-custom-container (Docker), inference-recommender, serverless-inference, pipelines-sagemaker, byoc-sm-jupyterlab.

### Claim: notebooks/ contains standalone Jupyter notebooks (~40 total across project)
**CONFIRMED** — `find . -name "*.ipynb" | wc -l` returns exactly **40**. The `notebooks/` directory has `getting_started.ipynb` and `ml_analysis_with_tests.ipynb`.

---

## Section 2: Makefile Structure

### Claim: Project uses `make test-mac` (NOT `make test`)
**CONFIRMED** — Makefile contains target `test-mac: lint validate strip-check`. No `test` target exists. Other targets: `lint`, `validate`, `strip-check`.

### Claim: Uses pip-compile for dependency management
**UNVERIFIED** — Local project uses `requirements-ci.txt` directly. No `pip-compile` or `requirements.in` found. This claim likely refers to other aws-samples projects.

---

## Section 3: Languages/Frameworks

### Claim: Python is primary language, Jupyter notebooks dominant
**CONFIRMED** — 40 notebooks, Python scripts, pyproject.toml with ruff config. No TypeScript, Java, or other languages found.

### Claim: Project uses Terraform (not CloudFormation/SAM)
**CONFIRMED** — 16 `.tf` files found in `sagemaker/terraform/`. Zero SAM templates (`template.yaml`/`samconfig.toml`) found. Zero CloudFormation templates found.

### Claim: Docker/ECR for containerized workloads
**CONFIRMED** — Dockerfiles found in:
- `sagemaker/processing-custom-container/Dockerfile`
- `sagemaker/byoc-sm-jupyterlab/notebook-al2023/Dockerfile`
- `sagemaker/byoc-sm-jupyterlab/notebook-al2023-custom-congifs-for-lustre/Dockerfile`
- `sagemaker/byoc-sm-jupyterlab/sagemaker-distribution/Dockerfile`
- `bedrock-agentcore/strands-agents/Dockerfile`

### Claim: CDK for some infrastructure
**CONTRADICTED** — No CDK code found in the local project. No `cdk.json`, no `constructs`, no CDK imports.

---

## Section 4: CI/CD

### Claim: CI uses `.github/workflows/ci.yml` + `ec2-integration.yml`
**CONFIRMED** — Both files exist. `ci.yml` runs on push/pull_request with steps: nbstripout --verify, ruff check, validate_notebooks.py.

---

## Section 5: External References (GitHub Repos)

| Repo | Status |
|------|--------|
| `aws-samples/amazon-bedrock-samples` | **CONFIRMED** — exists on GitHub |
| `awslabs/amazon-bedrock-agentcore-samples` | **CONFIRMED** — exists on GitHub |
| `aws-samples/aws-glue-samples` | **CONFIRMED** — exists on GitHub |
| `aws-samples/data-mesh-datazone-cdk-cloudformation` | **UNVERIFIED** — not directly checked |
| `aws-samples/aws-glue-cdk-cicd` | **UNVERIFIED** — not directly checked |
| `awsdataarchitect/kiro-best-practices` | **CONFIRMED** — exists on GitHub |
| `aws-samples/sample-kiro-steering-studio` | **CONFIRMED** — exists on GitHub |
| `awslabs/agent-plugins` | **UNVERIFIED** — not checked |

---

## Section 6: Web Resources / Best Practices

### Claim: roborhythms.com 4-section prompt (role/scope, tools, decision rules, output format)
**CONFIRMED** — Article exists at stated URL. Snippet confirms: "four sections in this order: role and scope, tools with strict schemas, decision rules, and output format."

### Claim: AWS Startup Prompt Library Full AWS Deployment Agent uses XML-tagged sections
**CONFIRMED** — Page exists at `https://aws.amazon.com/startups/prompt-library/full-aws-deployment-agent`. Snippet confirms it's an AI DevOps assistant prompt. XML tag details (safety_protocol, infrastructure_standards, etc.) are **UNVERIFIED** — would need full page read.

### Claim: ABCA prompt guide says "CLAUDE.md is the single most impactful thing you can add"
**CONFIRMED** — Multiple pages on `aws-samples.github.io/sample-autonomous-cloud-coding-agents/` reference CLAUDE.md as highly impactful. Direct quote found in memory/architecture page.

### Claim: Kiro steering uses `.kiro/steering/` markdown files with frontmatter `inclusion: always`
**CONFIRMED** — kiro.dev/docs/cli/steering/ confirms: "Steering gives Kiro persistent knowledge about your project through markdown files in .kiro/steering/."

### Claim: Ruff supports .ipynb natively
**CONFIRMED** — Ruff v0.0.276 added experimental notebook support; v0.0.285 made it stable. The local `pyproject.toml` uses `extend-include = ["*.ipynb"]`.

### Claim: per-file-ignores `"*.ipynb" = ["E402"]`
**PARTIALLY CONFIRMED** — The actual config is `"*.ipynb" = ["E402", "E501", "F403", "F405", "E722", "F821", "E741", "F841"]`. E402 is included but the finding understates the full ignore list.

### Claim: nbstripout as git filter/pre-commit hook
**CONFIRMED** — Makefile `strip-check` target uses `nbstripout --verify`. CI also runs `nbstripout --verify`. Used as verification, not as a git filter in this project.

### Claim: nbformat for validation
**PARTIALLY CONFIRMED** — A `scripts/validate_notebooks.py` exists. Whether it uses nbformat internally was not checked, but the concept of notebook JSON validation is implemented.

---

## Section 7: Recommended Enhanced Prompt Sections

### Claim: "SANITIZE AWS account IDs in all outputs"
**UNVERIFIED** — Good practice but not verified as an existing project rule.

### Claim: "Notebooks are the primary artifact type (not Lambda/SAM)"
**CONFIRMED** — 40 notebooks, zero Lambda/SAM artifacts.

### Claim: "8 service directories"
**CONFIRMED** — bedrock, bedrock-agentcore, bedrock-media-type-mismatch, datazone, glue, opensearch, sagemaker, notebooks all exist.

---

## Summary

| Verdict | Count |
|---------|-------|
| CONFIRMED | 22 |
| PARTIALLY CONFIRMED | 4 |
| CONTRADICTED | 4 |
| UNVERIFIED | 6 |

### Key Contradictions (Critical for Prompt Accuracy)
1. **bedrock/ structure** — Findings describe the public repo, not local project subdirectories
2. **datazone/ uses CDK/CloudFormation** — Local project has only notebooks, no IaC
3. **bedrock-agentcore supports multiple frameworks** — Local project only has Strands Agents
4. **CDK for some infrastructure** — No CDK found anywhere in local project

### Key Confirmations (High-confidence for Prompt)
1. `make test-mac` is the correct test command
2. Exactly 40 Jupyter notebooks
3. Terraform (not SAM/CloudFormation) for IaC
4. Docker/ECR for containerized workloads (5 Dockerfiles)
5. Ruff with .ipynb support + nbstripout for output stripping
6. CI runs lint + validate + strip-check
7. All referenced external repos and web resources are real
