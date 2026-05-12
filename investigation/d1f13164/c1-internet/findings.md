# Investigation Findings: Repository Structure & CI/CD Best Practices for Jupyter Notebooks

## 1. Repository Structure (virgilio-murillo/aws-samples)

### Confirmed Facts (from local filesystem inspection)

**Top-level files:**
- `README.md` — Overview of the repo as an AWS samples collection
- `LICENSE` — License file
- `.gitignore` — Ignores `config.py`, `env`, `.ipynb_checkpoints`, `.terraform`
- `.libs.json` — SageMaker Studio library config (S3 paths, conda/pip packages)
- `SAGEMAKER_UNIFIED_STUDIO_README.md` — SageMaker Unified Studio docs
- `TASK.md` — Task description file

**No existing CI/CD or tooling infrastructure:**
- ❌ No `.github/` directory (no GitHub Actions workflows)
- ❌ No `Makefile`
- ❌ No root-level `requirements.txt`
- ❌ No `pyproject.toml`
- ❌ No `.pre-commit-config.yaml`
- ❌ No `ruff.toml` or linting configuration

**Service directories:**
| Directory | Description |
|---|---|
| `bedrock/` | Amazon Bedrock samples (agents, batch inference, marketplace, prompt caching, etc.) |
| `bedrock-agentcore/` | Strands agents, gateway Cedar policies |
| `sagemaker/` | SageMaker ML samples (inference recommender, processing, pipelines, BYOC, terraform) |
| `glue/` | AWS Glue PySpark examples |
| `opensearch/` | Amazon OpenSearch Service samples |
| `datazone/` | Amazon DataZone data governance |
| `notebooks/` | General-purpose notebooks (getting_started, ml_analysis_with_tests) |
| `bedrock-media-type-mismatch/` | Bug reproduction for Bedrock media type issue |

### Jupyter Notebooks (40 total)

Found across the repo:
- `bedrock/miscellaneous/` — 10 notebooks (quickstart, agents, RAG, cross-region, etc.)
- `bedrock/agent-runtime/` — 2 notebooks
- `bedrock/batch-inference/` — 1 notebook
- `bedrock/testing/` — 2 notebooks
- `bedrock/prompt-caching/` — 1 notebook
- `bedrock/model-import/` — 1 notebook
- `bedrock/common-errors/` — 1 notebook
- `bedrock/bedrock-marketplace/` — 1 notebook
- `bedrock-agentcore/` — 2 notebooks
- `sagemaker/` — 9 notebooks (retail_sales_prediction, inference recommender, BYOC, pipelines, terraform, serverless)
- `glue/` — 1 notebook
- `opensearch/` — 1 notebook
- `datazone/` — 2 notebooks
- `notebooks/` — 2 notebooks

### Existing requirements.txt files (per-project, not root):
- `bedrock-agentcore/strands-agents/requirements.txt`
- `bedrock/stability-ai-upscale/requirements.txt`
- `sagemaker/inference-recommender/code/requirements.txt`
- `sagemaker/processing-custom-container/requirements.txt`

---

## 2. nbstripout — Stripping Notebook Outputs

### Tool: `kynan/nbstripout`
- **Source:** https://github.com/kynan/nbstripout
- **PyPI:** https://pypi.org/project/nbstripout/
- **Purpose:** Strips output cells, execution counts, and metadata from Jupyter notebooks before they enter version control.

### Key Features for CI:
- **`--dry-run` flag:** Prints what would change without modifying files.
- **`--check` flag (via `--dry-run`):** Returns non-zero exit code if any files would be changed — perfect for CI enforcement.
  - Source: [Debian manpage for nbstripout](https://manpages.debian.org/testing/nbstripout/nbstripout.1) confirms: `--dry-run` "Return a non-zero exit code if any files were changed"
- **Additional flags:** `--keep-count`, `--keep-output`, `--keep-id`, `--extra-keys`, `--drop-empty-cells`, `--drop-tagged-cells`

### CI Usage Pattern:
```bash
# Check that all notebooks have outputs stripped (fails if any have outputs)
nbstripout --dry-run notebooks/**/*.ipynb
# Or using find:
find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -exec nbstripout --dry-run {} +
```

### Pre-commit hook config (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/kynan/nbstripout
    rev: 0.9.1
    hooks:
      - id: nbstripout
```

### Alternative: `nb-clean`
- **Source:** https://github.com/srstevenson/nb-clean
- Also removes metadata, outputs, and execution counts with pre-commit support.

---

## 3. Ruff Linting for Jupyter Notebooks

### Native .ipynb Support
Ruff has **native Jupyter notebook support** since v0.1.5. It can lint and format `.ipynb` files directly without extracting `.py` cells first.

- **Source:** https://astral.sh/blog/ruff-v0.1.5
- **Source:** https://til.codeinthehole.com/posts/you-can-run-ruff-on-jupyter-notebooks/

### Configuration (`pyproject.toml`):
```toml
[tool.ruff]
extend-include = ["*.ipynb"]

[tool.ruff.lint.per-file-ignores]
# Notebooks commonly have imports not at top of file
"*.ipynb" = ["E402"]
```

### GitHub Actions Integration:
```yaml
- name: Lint with Ruff
  uses: astral-sh/ruff-action@v3
  with:
    args: "check --output-format=github"
```

- **Source:** https://github.com/astral-sh/ruff-action
- The `ruff-action` GitHub Action installs and runs ruff automatically.
- Supports `args` parameter for passing `check`, `format --check`, etc.

### Key Ruff Settings for Notebooks:
- `extend-include = ["*.ipynb"]` — Required to include notebooks in linting scope
- `per-file-ignores` for `*.ipynb` — Common to ignore `E402` (module-level imports) since notebook cells are independent
- Source: https://docs.astral.sh/ruff/settings/

---

## 4. Notebook JSON Validation

### Tool: `nbformat`
- **Source:** https://github.com/jupyter/nbformat
- **Docs:** https://nbformat.readthedocs.io/en/latest/format_description.html
- The official Jupyter Notebook format is defined with a JSON schema. `nbformat.validate()` validates notebooks against this schema.

### CI Validation Script Pattern:
```python
import nbformat
import sys
import glob

errors = []
for nb_path in glob.glob("**/*.ipynb", recursive=True):
    try:
        nb = nbformat.read(nb_path, as_version=4)
        nbformat.validate(nb)
    except Exception as e:
        errors.append(f"{nb_path}: {e}")

if errors:
    for e in errors:
        print(e, file=sys.stderr)
    sys.exit(1)
```

### Alternative: Simple JSON validation
```bash
# Verify all .ipynb files are valid JSON
find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -exec python -m json.tool {} > /dev/null \;
```

### Alternative: `check-jsonschema`
- **Source:** https://github.com/python-jsonschema/check-jsonschema
- CLI tool with pre-commit hooks for JSON schema validation.

---

## 5. EC2-Based Integration Tests (Ubuntu & Arch Linux)

### Approach: On-Demand Self-Hosted Runners via `machulav/ec2-github-runner`

- **Source:** https://github.com/machulav/ec2-github-runner
- **Usage guide:** https://cicube.io/workflow-hub/machulav-ec2-github-runner

### Workflow Pattern:
```yaml
name: Integration Tests
on:
  push:
    branches: [main]
  pull_request:

jobs:
  start-ubuntu-runner:
    name: Start Ubuntu EC2 Runner
    runs-on: ubuntu-latest
    outputs:
      label: ${{ steps.start-ec2-runner.outputs.label }}
      ec2-instance-id: ${{ steps.start-ec2-runner.outputs.ec2-instance-id }}
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}
      - name: Start EC2 runner
        id: start-ec2-runner
        uses: machulav/ec2-github-runner@v2
        with:
          mode: start
          github-token: ${{ secrets.GH_PERSONAL_ACCESS_TOKEN }}
          ec2-image-id: ami-UBUNTU_AMI_ID
          ec2-instance-type: t3.medium
          subnet-id: ${{ secrets.SUBNET_ID }}
          security-group-id: ${{ secrets.SG_ID }}

  test-ubuntu:
    name: Run tests on Ubuntu
    needs: start-ubuntu-runner
    runs-on: ${{ needs.start-ubuntu-runner.outputs.label }}
    steps:
      - uses: actions/checkout@v4
      - name: Run integration tests
        run: |
          pip install -r requirements-test.txt
          pytest --nbmake **/*.ipynb

  stop-ubuntu-runner:
    name: Stop Ubuntu EC2 Runner
    needs: [start-ubuntu-runner, test-ubuntu]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}
      - name: Stop EC2 runner
        uses: machulav/ec2-github-runner@v2
        with:
          mode: stop
          github-token: ${{ secrets.GH_PERSONAL_ACCESS_TOKEN }}
          label: ${{ needs.start-ubuntu-runner.outputs.label }}
          ec2-instance-id: ${{ needs.start-ubuntu-runner.outputs.ec2-instance-id }}
```

### Arch Linux Runner:
- Same pattern as Ubuntu but with a custom Arch Linux AMI (`ec2-image-id: ami-ARCH_AMI_ID`)
- Arch Linux AMIs are available in AWS Marketplace or can be built with Packer
- The self-hosted runner application supports any Linux distribution
- Source: https://docs.github.com/actions/reference/runners/self-hosted-runners

### Requirements for EC2 Runners:
- AWS credentials (access key + secret) stored as GitHub secrets
- A GitHub Personal Access Token with `repo` scope
- Pre-configured VPC with subnet and security group
- AMIs with Python, pip, and Jupyter pre-installed (or install in workflow)

---

## 6. macOS Local-Only Testing via Makefile

### Design Pattern:
The Makefile provides local developer experience that mirrors CI checks but runs on macOS. It is NOT used in GitHub Actions — CI uses its own workflow steps.

### Recommended Makefile Structure:
```makefile
.PHONY: lint test validate strip-check clean install

install:
	pip install nbstripout ruff nbformat nbmake pytest

lint:
	ruff check --extend-include "*.ipynb" .

format-check:
	ruff format --check --extend-include "*.ipynb" .

strip-check:
	find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" \
		-exec nbstripout --dry-run {} +

validate:
	python scripts/validate_notebooks.py

test:
	pytest --nbmake notebooks/**/*.ipynb

all: lint format-check strip-check validate

clean:
	find . -name ".ipynb_checkpoints" -type d -exec rm -rf {} +
	find . -name "__pycache__" -type d -exec rm -rf {} +
```

### Key Points:
- `make lint` — Runs ruff on all Python and notebook files
- `make strip-check` — Verifies no notebook outputs are committed
- `make validate` — Validates notebook JSON schema
- `make test` — Executes notebooks via nbmake (for notebooks that can run locally)
- Source: https://stackoverflow.com/questions/66918575/how-to-use-your-own-makefile-in-github-actions

---

## 7. Notebook Testing Tools Comparison

| Tool | Purpose | CI Usage |
|---|---|---|
| **nbmake** | Pytest plugin — executes notebooks, checks for errors | `pytest --nbmake **/*.ipynb` |
| **nbval** | Pytest plugin — validates notebook outputs match stored outputs | `pytest --nbval **/*.ipynb` |
| **nbstripout** | Strips/checks outputs are stripped | `nbstripout --dry-run *.ipynb` |
| **nbformat** | Validates notebook JSON against schema | `python -c "import nbformat; ..."` |
| **ruff** | Lints Python code in notebooks natively | `ruff check --extend-include "*.ipynb"` |

- **nbmake** (https://github.com/treebeardtech/nbmake) — Best for CI execution testing. Runs notebooks top-to-bottom and fails if any cell errors. Supports parallel execution.
- **nbval** (https://pypi.org/project/nbval/) — Best for output regression testing. Compares execution outputs against stored outputs.

---

## 8. Recommended CI/CD Architecture

### Three-Tier Approach:

**Tier 1: Fast Checks (GitHub-hosted runner, every PR)**
- Notebook JSON validation (nbformat)
- Output stripping check (nbstripout --dry-run)
- Ruff linting (ruff check)
- Ruff format check (ruff format --check)

**Tier 2: Integration Tests (EC2 self-hosted runners, on merge to main)**
- Ubuntu EC2 runner: Execute notebooks with nbmake
- Arch Linux EC2 runner: Execute notebooks with nbmake
- Uses `machulav/ec2-github-runner` for on-demand provisioning

**Tier 3: Local Development (macOS Makefile)**
- `make all` runs lint + strip-check + validate
- `make test` runs notebook execution locally
- Mirrors Tier 1 checks for fast local feedback

### GitHub Actions Workflow File Structure:
```
.github/
  workflows/
    ci.yml          # Tier 1: Fast checks on every PR
    integration.yml # Tier 2: EC2-based integration tests
```

---

## 9. Key Sources

1. kynan/nbstripout — https://github.com/kynan/nbstripout
2. astral-sh/ruff — https://github.com/astral-sh/ruff
3. astral-sh/ruff-action — https://github.com/astral-sh/ruff-action
4. Ruff Jupyter support blog — https://astral.sh/blog/ruff-v0.1.5
5. Ruff settings docs — https://docs.astral.sh/ruff/settings/
6. Ruff extend-include for notebooks — https://til.codeinthehole.com/posts/you-can-run-ruff-on-jupyter-notebooks/
7. jupyter/nbformat — https://github.com/jupyter/nbformat
8. nbformat docs — https://nbformat.readthedocs.io/en/latest/format_description.html
9. treebeardtech/nbmake — https://github.com/treebeardtech/nbmake
10. nbval — https://pypi.org/project/nbval/
11. machulav/ec2-github-runner — https://github.com/machulav/ec2-github-runner
12. GitHub self-hosted runners docs — https://docs.github.com/actions/reference/runners/self-hosted-runners
13. nbstripout manpage (--dry-run flag) — https://manpages.debian.org/testing/nbstripout/nbstripout.1
14. Space Telescope notebook CI overview — https://spacetelescope.github.io/notebook-infrastructure/ci-overview.html
15. nb-clean alternative — https://github.com/srstevenson/nb-clean
16. check-jsonschema — https://github.com/python-jsonschema/check-jsonschema
