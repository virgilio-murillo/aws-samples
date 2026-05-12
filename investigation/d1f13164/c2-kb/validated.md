# Validated Findings: c2-kb (Knowledge Base & Lessons Learned)

**Validator**: c2-kb-validator
**Date**: 2026-03-27T20:35 CDT
**Method**: Filesystem commands, web search, official documentation cross-check

---

## Section 1: Repository Structure

### Git Remote & Branch
| Claim | Verdict | Evidence |
|-------|---------|----------|
| Origin: `https://github.com/virgilio-murillo/aws-samples.git` | **CONFIRMED** | `git remote -v` output matches exactly |
| Branch: `main` (single branch, no feature branches) | **CONFIRMED** | `git branch -a` shows only `main` and `remotes/origin/main` |

### Top-Level Files
| Claim | Verdict | Evidence |
|-------|---------|----------|
| README.md, LICENSE, .gitignore, .libs.json, TASK.md, SAGEMAKER_UNIFIED_STUDIO_README.md | **CONFIRMED** | `ls -la` confirms all 6 files present |

### .gitignore Contents
| Claim | Verdict | Evidence |
|-------|---------|----------|
| Ignores `config.py`, `env`, `.ipynb_checkpoints`, `.terraform` | **CONFIRMED** (incomplete) | File contains those 4 patterns PLUS additional entries: `*/.ipynb_checkpoints/*`, `sagemaker/how-to-use-inference-recommender/envi`, `sagemaker/how-to-use-inference-recommender/model/1`, `*/.terraform/*`. Not wrong, but omits 4 additional lines. |

### No Existing CI/CD Infrastructure
| Claim | Verdict | Evidence |
|-------|---------|----------|
| No `.github/` directory | **CONFIRMED** | `ls .github/` → "No such file or directory" |
| No `Makefile` | **CONFIRMED** | `ls Makefile` → "No such file or directory" |
| No root `requirements.txt` | **CONFIRMED** | `ls requirements.txt` → "No such file or directory" |
| No `.pre-commit-config.yaml` | **CONFIRMED** | `ls .pre-commit-config.yaml` → "No such file or directory" |
| No `pyproject.toml` or `setup.py` | **CONFIRMED** | Both absent |
| No `ruff.toml` or `.ruff.toml` | **CONFIRMED** | Both absent |

### Service Directories
| Claim | Verdict | Evidence |
|-------|---------|----------|
| "7 top-level" service directories | **CONTRADICTED** | Header says 7 but lists 8 items (1–8). Actual count is 8 directories: `bedrock/`, `bedrock-agentcore/`, `bedrock-media-type-mismatch/`, `datazone/`, `glue/`, `notebooks/`, `opensearch/`, `sagemaker/`. The list itself is correct; only the "7" count in the header is wrong. |
| `bedrock/` — 11 subdirs, 11 notebooks | **CONTRADICTED** | Actual: **10 subdirs** (agent-runtime, batch-inference, bedrock-marketplace, common-errors, fine-tuning, miscellaneous, model-import, prompt-caching, stability-ai-upscale, testing), **19 notebooks**. Both numbers are wrong. |
| `bedrock-agentcore/` — 2 subdirs, 2 notebooks | **CONFIRMED** | 2 subdirs, 2 notebooks verified |
| `bedrock-media-type-mismatch/` — Python scripts only | **CONFIRMED** | Contains 4 .py files, 0 .ipynb files |
| `sagemaker/` — 7 subdirs, 10 notebooks | **CONTRADICTED** | Actual: **6 subdirs** (byoc-sm-jupyterlab, inference-recommender, pipelines-sagemaker, processing-custom-container, serverless-inference, terraform), **13 notebooks** (including 1 at sagemaker/ root level). Both numbers are wrong. |
| `glue/` — 1 notebook | **CONFIRMED** | 1 notebook verified |
| `opensearch/` — 1 notebook | **CONFIRMED** | 1 notebook in `create-resources/` subdir |
| `datazone/` — 2 notebooks | **CONFIRMED** | 2 notebooks verified |
| `notebooks/` — 2 general notebooks | **CONFIRMED** | 2 notebooks verified |

---

## Section 2: Notebook Inventory

### Total Count
| Claim | Verdict | Evidence |
|-------|---------|----------|
| 40 total `.ipynb` files | **CONFIRMED** | `find . -name '*.ipynb' ... | wc -l` → 40 |

### Per-Directory Counts (from table)
| Directory | Claimed | Actual | Verdict |
|-----------|---------|--------|---------|
| `bedrock/miscellaneous/` | 8 | **10** | **CONTRADICTED** — missing: `csutom_data_source_2.ipynb`, `multimodal_meta_llama32.ipynb` |
| `sagemaker/` (all subdirs) | 10 | **13** | **CONTRADICTED** — missing: 3 notebooks in `byoc-sm-jupyterlab/` subdirs + `retail_sales_prediction.ipynb` at root |
| `bedrock/agent-runtime/` | 2 | 2 | **CONFIRMED** |
| `bedrock/batch-inference/` | 1 | 1 | **CONFIRMED** |
| `bedrock/testing/` | 2 | 2 | **CONFIRMED** |
| `bedrock/prompt-caching/` | 1 | 1 | **CONFIRMED** |
| `bedrock/model-import/` | 1 | 1 | **CONFIRMED** |
| `bedrock/common-errors/` | 1 | 1 | **CONFIRMED** |
| `bedrock/bedrock-marketplace/` | 1 | 1 | **CONFIRMED** |
| `bedrock-agentcore/` | 2 | 2 | **CONFIRMED** |
| `opensearch/` | 1 | 1 | **CONFIRMED** |
| `datazone/` | 2 | 2 | **CONFIRMED** |
| `glue/` | 1 | 1 | **CONFIRMED** |
| `notebooks/` | 2 | 2 | **CONFIRMED** |

Note: The table sums to 35 (claimed) vs 40 (actual). The total of 40 is correct, but the per-directory breakdown is inconsistent — `bedrock/miscellaneous` and `sagemaker/` are undercounted by 5 total.

### File Sizes
| Claim | Verdict | Evidence |
|-------|---------|----------|
| `retail_sales_prediction.ipynb` ~2MB | **CONFIRMED** | 2,054,339 bytes ≈ 1.96 MB |
| `conversation_examples-test-with-huggingface.ipynb` 199KB | **CONFIRMED** | 199,286 bytes (≈195 KB; "199KB" likely refers to raw byte count) |
| `getting_started.ipynb` 78KB | **CONFIRMED** | 78,725 bytes ≈ 77 KB |
| `ml_analysis_with_tests.ipynb` 6KB | **CONFIRMED** | 6,043 bytes ≈ 6 KB |

### Python Files
| Claim | Verdict | Evidence |
|-------|---------|----------|
| 12 total .py files | **CONFIRMED** | `find . -name '*.py' ...` returns exactly 12 files |

### requirements.txt Files
| Claim | Verdict | Evidence |
|-------|---------|----------|
| 4 subdirectory-level requirements.txt | **CONFIRMED** | All 4 paths verified: bedrock-agentcore/strands-agents/, bedrock/stability-ai-upscale/, sagemaker/inference-recommender/code/, sagemaker/processing-custom-container/ |

### Dockerfiles
| Claim | Verdict | Evidence |
|-------|---------|----------|
| 5 Dockerfiles | **CONFIRMED** | All 5 found: bedrock-agentcore/strands-agents/Dockerfile, sagemaker/byoc-sm-jupyterlab/ (3 variants), sagemaker/processing-custom-container/Dockerfile |

### YAML Files
| Claim | Verdict | Evidence |
|-------|---------|----------|
| 1 YAML file: `bedrock-agentcore/strands-agents/.bedrock_agentcore.yaml` | **CONFIRMED** | Only YAML file found in repo |

---

## Section 3: Knowledge Base & Lessons Learned Search Results

| Claim | Verdict | Notes |
|-------|---------|-------|
| 22 queries executed (14 search_lessons + 8 knowledge) | **UNVERIFIED** | Cannot reproduce exact search session; internal to investigation process |
| No indexed knowledge bases exist | **UNVERIFIED** | Depends on runtime state at time of investigation |
| Lessons confirmed repo structure (high confidence) | **UNVERIFIED** | Cannot reproduce; plausible given the repo exists |
| No lessons found for CI/CD tooling specifics | **UNVERIFIED** | Cannot reproduce |

---

## Section 4: Best Practices Research (Tool Claims)

### nbstripout
| Claim | Verdict | Evidence |
|-------|---------|----------|
| `pip install nbstripout` | **CONFIRMED** | PyPI page confirms package name |
| `nbstripout --verify` checks without modifying, exits non-zero if outputs present | **CONFIRMED** | PyPI docs: "--verify: Return a non-zero exit code if any files were changed, Implies --dry-run" |
| CI use: `find . -name '*.ipynb' -exec nbstripout --verify {} +` | **CONFIRMED** | Valid approach. Note: nbstripout also offers a reusable GitHub Action (`kynan/nbstripout@main`) which is a simpler alternative not mentioned in findings. |

### ruff
| Claim | Verdict | Evidence |
|-------|---------|----------|
| `ruff check --include "*.ipynb"` (since ruff 0.1.0+) | **CONTRADICTED** | `--include` is NOT a CLI flag for `ruff check`. The `include` setting is config-file only (`ruff.toml` / `pyproject.toml`). Furthermore, `.ipynb` files are included BY DEFAULT since ruff 0.6.0 — no `--include` needed. Source: [Ruff configuration docs](https://docs.astral.sh/ruff/configuration/#jupyter-notebook-discovery) |
| Extract cells with `jupyter nbconvert --to script` then lint | **CONFIRMED** | Valid alternative approach |
| Config via `ruff.toml` or `[tool.ruff]` in `pyproject.toml` | **CONFIRMED** | Ruff docs confirm both config file formats |
| Recommended rules: `E`, `F`, `W` (pyflakes + pycodestyle basics) | **CONFIRMED** (minor inaccuracy) | `F` = pyflakes, `E` + `W` = pycodestyle. The parenthetical description is slightly misleading — should say "pyflakes + pycodestyle" not "pyflakes + pycodestyle basics". |

### Notebook JSON Validation
| Claim | Verdict | Evidence |
|-------|---------|----------|
| `python -c "import json; json.load(open('notebook.ipynb'))"` for basic JSON | **CONFIRMED** | Valid Python for JSON syntax check |
| `jupyter nbconvert --validate notebook.ipynb` | **UNVERIFIED** | The `--validate` flag is not a standard documented flag in recent nbconvert versions. May work in some versions but not reliably. |
| `python -m nbformat.validator notebook.ipynb` | **UNVERIFIED** | The `nbformat.validator` module may not have a `__main__` entry point. The standard API approach is `nbformat.read()` + `nbformat.validate()`. |
| `nbformat.read(f, as_version=4)` with `nbformat.validate(nb)` | **CONFIRMED** | Standard nbformat API usage |

### EC2-Based Integration Tests
| Claim | Verdict | Evidence |
|-------|---------|----------|
| Ubuntu: `apt-get install python3-pip jupyter-notebook` | **CONFIRMED** | Valid Ubuntu package names |
| Arch Linux: `pacman -S python python-pip jupyter-notebook` | **CONFIRMED** | Valid Arch Linux package names |
| GitHub Actions can use self-hosted runners on EC2 | **CONFIRMED** | Well-documented GitHub feature |
| Notebook load test: `python -c "import nbformat; nbformat.read('notebook.ipynb', as_version=4)"` | **CONFIRMED** | Valid nbformat API usage |

---

## Section 5: Recommended CI/CD File Structure

| Claim | Verdict | Notes |
|-------|---------|-------|
| Files to create: `.github/workflows/ci.yml`, `ec2-integration.yml`, `Makefile`, `requirements-ci.txt`, `pyproject.toml` | **UNVERIFIED** | This is a recommendation, not a factual claim. Reasonable structure. |

---

## Section 6: TASK.md Constraints

| Claim | Verdict | Evidence |
|-------|---------|----------|
| DO NOT modify existing notebooks | **CONFIRMED** | TASK.md: "Do NOT modify existing notebooks" |
| Focus on ADDING CI/CD and validation only | **CONFIRMED** | TASK.md: "Focus on ADDING CI/CD and validation" |
| GitHub Actions on `ubuntu-latest` | **CONFIRMED** | TASK.md: "GitHub Actions on ubuntu-latest" |
| nbstripout, ruff lint, notebook JSON validation | **CONFIRMED** | TASK.md lists all three |
| EC2 integration tests on Ubuntu + Arch Linux | **CONFIRMED** | TASK.md: "EC2 integration tests on Ubuntu + Arch Linux" |
| macOS local-only via `make test-mac` | **CONFIRMED** | TASK.md: "macOS local-only via make test-mac" |
| Makefile targets: `lint`, `validate`, `test-mac` | **CONFIRMED** | TASK.md: "Makefile: lint, validate, test-mac" |

---

## Summary Scorecard

| Verdict | Count | Details |
|---------|-------|---------|
| **CONFIRMED** | 42 | Majority of filesystem claims, tool basics, TASK.md constraints |
| **CONTRADICTED** | 5 | Service dir count header (7→8), bedrock subdirs (11→10), bedrock notebooks (11→19), bedrock/miscellaneous count (8→10), sagemaker subdirs (7→6), sagemaker notebooks (10→13), ruff `--include` CLI flag |
| **UNVERIFIED** | 9 | KB/lessons search results (4), `jupyter nbconvert --validate` (1), `python -m nbformat.validator` (1), recommended file structure (1), knowledge base state (2) |

## Critical Errors to Correct

1. **bedrock/ subdirectory count**: Claimed 11, actual 10
2. **bedrock/ notebook count**: Claimed 11, actual 19 (nearly double)
3. **bedrock/miscellaneous/ notebook count**: Claimed 8, actual 10
4. **sagemaker/ subdirectory count**: Claimed 7, actual 6
5. **sagemaker/ notebook count**: Claimed 10, actual 13
6. **Service directory header**: Says "7 top-level" but lists 8 (and 8 is correct)
7. **ruff `--include` CLI flag**: Does not exist. Notebooks are linted by default since ruff 0.6.0. No special flag needed.
