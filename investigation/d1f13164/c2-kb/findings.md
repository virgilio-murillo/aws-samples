# Knowledge Base Investigation: aws-samples CI/CD

**Agent**: c2-kb (Knowledge Base & Lessons Learned search)
**Date**: 2026-03-27T20:28 CDT
**Sources**: Local filesystem inspection, `search_lessons` (14 queries), `knowledge search` (8 queries)

---

## 1. Repository Structure (CONFIRMED — filesystem inspection)

### Git Remote
- **Origin**: `https://github.com/virgilio-murillo/aws-samples.git`
- **Branch**: `main` (single branch, no feature branches)

### Top-Level Files
| File | Purpose |
|------|---------|
| `README.md` | Repo overview with service directory links |
| `LICENSE` | License file |
| `.gitignore` | Ignores `config.py`, `env`, `.ipynb_checkpoints`, `.terraform` |
| `.libs.json` | SageMaker Studio library config (S3 paths, conda/pip) |
| `TASK.md` | CI/CD task description (the current task) |
| `SAGEMAKER_UNIFIED_STUDIO_README.md` | SageMaker Unified Studio docs |

### NO existing CI/CD infrastructure
- **No `.github/` directory** — no workflows, no Actions, no dependabot
- **No `Makefile`** — none at any level
- **No root `requirements.txt`** — only subdirectory-level ones
- **No `.pre-commit-config.yaml`**
- **No `pyproject.toml` or `setup.py`**
- **No `ruff.toml` or `.ruff.toml`**

### Service Directories (7 top-level)
1. `bedrock/` — 11 subdirs, 11 notebooks
2. `bedrock-agentcore/` — 2 subdirs, 2 notebooks
3. `bedrock-media-type-mismatch/` — Python scripts only (no notebooks)
4. `sagemaker/` — 7 subdirs, 10 notebooks
5. `glue/` — 1 notebook
6. `opensearch/` — 1 notebook
7. `datazone/` — 2 notebooks
8. `notebooks/` — 2 general notebooks

---

## 2. Notebook Inventory (CONFIRMED — 40 total)

All `.ipynb` files found (excluding `.ipynb_checkpoints`):

| Directory | Count | Notable |
|-----------|-------|---------|
| `bedrock/miscellaneous/` | 8 | Largest group; includes 199KB huggingface test |
| `sagemaker/` (all subdirs) | 10 | Includes 2MB `retail_sales_prediction.ipynb` |
| `bedrock/agent-runtime/` | 2 | |
| `bedrock/batch-inference/` | 1 | |
| `bedrock/testing/` | 2 | |
| `bedrock/prompt-caching/` | 1 | |
| `bedrock/model-import/` | 1 | |
| `bedrock/common-errors/` | 1 | |
| `bedrock/bedrock-marketplace/` | 1 | |
| `bedrock-agentcore/` | 2 | |
| `opensearch/` | 1 | |
| `datazone/` | 2 | |
| `glue/` | 1 | |
| `notebooks/` | 2 | `getting_started.ipynb` (78KB), `ml_analysis_with_tests.ipynb` (6KB) |

### Python Files (12 total)
Located in: `bedrock-media-type-mismatch/`, `bedrock/stability-ai-upscale/`, `bedrock/miscellaneous/`, `sagemaker/inference-recommender/`, `sagemaker/processing-custom-container/`, `bedrock-agentcore/strands-agents/`

### Existing requirements.txt (4 subdirectory-level)
1. `bedrock-agentcore/strands-agents/requirements.txt` — strands-agents-tools, uv, boto3, bedrock-agentcore
2. `bedrock/stability-ai-upscale/requirements.txt` — boto3, pillow
3. `sagemaker/processing-custom-container/requirements.txt` — pandas, joblib, numpy, rrcf, scipy, pyarrow, swifter
4. `sagemaker/inference-recommender/code/requirements.txt` — numpy, pillow

### Dockerfiles (5)
In `bedrock-agentcore/strands-agents/`, `sagemaker/byoc-sm-jupyterlab/` (3 variants), `sagemaker/processing-custom-container/`

### YAML Files (1)
Only `bedrock-agentcore/strands-agents/.bedrock_agentcore.yaml`

---

## 3. Knowledge Base & Lessons Learned Search Results

### Queries Executed (22 total)

**search_lessons queries** (14):
1. "GitHub Actions CI/CD Jupyter notebooks" → 4 results (low confidence) — repo inventory lessons
2. "EC2 integration tests Ubuntu Arch Linux Makefile" → 2 results (low) — CodeBuild ECR auth
3. "nbstripout ruff linting notebook validation" → 0 results
4. "GitHub Actions workflow YAML CI CD pipeline configuration" → 2 results (low)
5. "aws-samples repository structure notebooks bedrock sagemaker" → 6 results (high/medium) — **BEST MATCH**: confirmed repo structure
6. "Makefile Python linting testing automation" → 4 results (low) — Python snippets
7. "notebook JSON validation ipynb format structure" → 0 results
8. "ruff Python linter formatter code quality" → 0 results
9. "nbstripout strip notebook output git pre-commit" → 2 results (low)
10. "macOS local testing development workflow" → 4 results (medium/low)
11. "EC2 self-hosted runner GitHub Actions" → 2 results (low)
12. "GitHub Actions matrix strategy multiple OS runners" → 0 results
13. "Arch Linux pacman package manager setup" → 0 results
14. "pre-commit hooks code quality automation" → 4 results (low)

**knowledge search queries** (8):
1. "GitHub Actions CI/CD notebooks" → no results
2. "nbstripout ruff linting Makefile" → no results
3. "Makefile targets lint validate test" → no results
4. "EC2 integration tests self-hosted runner" → no results
5. "GitHub Actions best practices workflow" → no results
6. "pre-commit hooks Python code quality" → no results
7. "notebook ipynb JSON schema validation" → no results
8. "EC2 Ubuntu Arch Linux testing" → no results

### Key Findings from Knowledge Sources

**No indexed knowledge bases exist** — the `knowledge show` command returned empty. All knowledge search queries returned no results.

**Lessons learned had relevant repo structure data** (high confidence):
- Confirmed Bedrock samples at `github.com/virgilio-murillo/aws-samples/bedrock/` covering agent-runtime, batch inference, fine-tuning, model import, prompt caching, Stability AI upscaling
- Confirmed SageMaker samples at `github.com/virgilio-murillo/aws-samples/sagemaker/` covering processing-custom-container, serverless-inference, pipelines, inference-recommender, terraform
- Confirmed AgentCore samples covering gateway Cedar policies, Strands agent hosting, MCP server deployment

**No lessons found for CI/CD tooling specifics**:
- No lessons on nbstripout, ruff, notebook JSON validation
- No lessons on GitHub Actions workflow configuration
- No lessons on EC2 self-hosted runners or Arch Linux testing
- No lessons on Makefile patterns for Python/notebook projects

---

## 4. Best Practices Research (from general knowledge — no KB hits)

Since no knowledge bases or lessons covered the specific CI/CD tools, here is what is known from general domain knowledge:

### nbstripout
- Tool to strip output cells from Jupyter notebooks
- Install: `pip install nbstripout`
- Usage: `nbstripout notebook.ipynb` (in-place) or `nbstripout --verify notebook.ipynb` (check-only, exit 1 if outputs present)
- CI use: `find . -name '*.ipynb' -exec nbstripout --verify {} +` — fails if any notebook has outputs
- **Important for this repo**: The 2MB `retail_sales_prediction.ipynb` likely has large outputs

### ruff (linting .py cells from notebooks)
- Fast Python linter/formatter
- Can lint notebooks directly: `ruff check --include "*.ipynb"` (since ruff 0.1.0+)
- Alternatively, extract cells with `jupyter nbconvert --to script` then lint the `.py` files
- Config via `ruff.toml` or `[tool.ruff]` in `pyproject.toml`
- Recommended rules for notebooks: `E`, `F`, `W` (pyflakes + pycodestyle basics)

### Notebook JSON Validation
- `.ipynb` files are JSON with a specific schema (nbformat)
- Validate with: `python -c "import json; json.load(open('notebook.ipynb'))"` (basic JSON)
- Better: `jupyter nbconvert --validate notebook.ipynb` or `python -m nbformat.validator notebook.ipynb`
- Or use `nbformat` Python API: `nbformat.read(f, as_version=4)` with `nbformat.validate(nb)`

### EC2-Based Integration Tests
- **Ubuntu runner**: `apt-get install python3-pip jupyter-notebook` then validate notebooks load
- **Arch Linux runner**: `pacman -S python python-pip jupyter-notebook` then validate
- GitHub Actions can use self-hosted runners on EC2 instances
- Alternative: use `runs-on: ubuntu-latest` for Ubuntu, and a custom Docker container or self-hosted runner for Arch
- Notebook load test: `python -c "import nbformat; nbformat.read('notebook.ipynb', as_version=4)"`

### macOS Local-Only Testing via Makefile
- Makefile target `test-mac` that runs the same lint/validate steps locally
- Use `$(shell uname -s)` to gate macOS-only behavior
- Targets: `lint` (ruff), `validate` (nbformat), `test-mac` (all local checks)

---

## 5. Recommended CI/CD File Structure

Based on the investigation, these files need to be CREATED (none exist):

```
.github/
  workflows/
    ci.yml              # Main CI: nbstripout verify, ruff lint, JSON validate
    ec2-integration.yml # EC2 tests on Ubuntu + Arch Linux
Makefile                # lint, validate, test-mac targets
requirements-ci.txt     # CI-only deps: nbstripout, ruff, nbformat, jupyter
pyproject.toml          # or ruff.toml for ruff configuration
```

### Key Constraints (from TASK.md)
- **DO NOT modify existing notebooks**
- Focus on ADDING CI/CD and validation only
- GitHub Actions on `ubuntu-latest` for: nbstripout, ruff, notebook JSON validation
- EC2 integration tests on Ubuntu + Arch Linux
- macOS local-only via `make test-mac`
- Makefile targets: `lint`, `validate`, `test-mac`

---

## 6. Summary of Gaps

| Topic | KB/Lessons Found? | Notes |
|-------|-------------------|-------|
| Repo structure | ✅ Yes (high confidence) | Lessons confirmed directory layout |
| Existing CI/CD | ✅ Confirmed absent | No .github/, Makefile, or CI config |
| nbstripout best practices | ❌ No | General knowledge only |
| ruff notebook linting | ❌ No | General knowledge only |
| Notebook JSON validation | ❌ No | General knowledge only |
| EC2 integration tests | ❌ No | General knowledge only |
| Arch Linux setup | ❌ No | General knowledge only |
| macOS Makefile patterns | ❌ No | General knowledge only |
| GitHub Actions workflows | ❌ No | General knowledge only |
| Self-hosted runners | ❌ No | General knowledge only |
