# Final Investigation Report: aws-samples CI/CD for Jupyter Notebooks

**Date:** 2026-03-27  
**Repo:** https://github.com/virgilio-murillo/aws-samples  
**Investigation ID:** d1f13164  
**Streams completed:** c1-internet ✅, c2-kb ✅, c3-context ❌ (rate-limited), c4-docs ✅, c5-internal ❌ (rate-limited)

---

## Executive Summary

The `virgilio-murillo/aws-samples` repository contains **40 Jupyter notebooks** across 8 service directories (bedrock, bedrock-agentcore, bedrock-media-type-mismatch, datazone, glue, notebooks, opensearch, sagemaker). It has **zero existing CI/CD infrastructure** — no `.github/`, no `Makefile`, no `pyproject.toml`, no `requirements.txt` at root.

**34 of 40 notebooks (85%) contain stored outputs** that need stripping before CI can enforce clean commits. All 40 notebooks are valid JSON. Kernels span `python3`, `conda_python3`, `conda_pytorch_p310`, `conda_tensorflow2_p310`, and `glue_pyspark` — the Glue notebook requires special handling.

The investigation resolved **3 critical contradictions** across streams (all related to `nbstripout` flag naming and notebook counts) and confirmed the full CI/CD architecture needed per `TASK.md`.

---

## Confirmed Findings

### Repository Structure (Confidence: HIGH — verified by all 3 streams + direct filesystem)

| Item | Value |
|------|-------|
| Git remote | `https://github.com/virgilio-murillo/aws-samples.git` |
| Branch | `main` (only branch) |
| Top-level files | README.md, LICENSE, .gitignore, .libs.json, TASK.md, SAGEMAKER_UNIFIED_STUDIO_README.md |
| Service directories | 8: bedrock, bedrock-agentcore, bedrock-media-type-mismatch, datazone, glue, notebooks, opensearch, sagemaker |
| Total notebooks | **40** |
| Notebooks with outputs | **34/40 (85%)** — confirmed by direct inspection |
| Invalid JSON notebooks | **0** — all 40 are valid JSON |
| nbformat versions | 4.4 (3 notebooks), 4.5 (37 notebooks) |
| Python files (.py) | 12 |
| requirements.txt files | 4 (subdirectory-level only) |
| Dockerfiles | 5 |

### Notebook Distribution (Confidence: HIGH — verified by orchestrator directly)

| Directory | Notebooks |
|-----------|-----------|
| bedrock/miscellaneous/ | 10 |
| bedrock/agent-runtime/ | 2 |
| bedrock/batch-inference/ | 1 |
| bedrock/testing/ | 2 |
| bedrock/prompt-caching/ | 1 |
| bedrock/model-import/ | 1 |
| bedrock/common-errors/ | 1 |
| bedrock/bedrock-marketplace/ | 1 |
| **bedrock/ total** | **19** |
| bedrock-agentcore/ | 2 |
| sagemaker/ (all subdirs + root) | 13 |
| glue/ | 1 |
| opensearch/ | 1 |
| datazone/ | 2 |
| notebooks/ | 2 |
| **TOTAL** | **40** |

### Kernelspec Distribution (Confidence: HIGH — verified by orchestrator)

| Kernel | Count | Notes |
|--------|-------|-------|
| python3 | 17 | Standard — fully testable |
| conda_python3 | 10 | SageMaker-specific conda env |
| conda_tensorflow2_p310 | 7 | SageMaker TF env |
| conda_pytorch_p310 | 4 | SageMaker PyTorch env |
| glue_pyspark | 1 | Requires AWS Glue — cannot validate locally |
| none | 1 | No kernelspec metadata |

### No Existing CI/CD (Confidence: HIGH — confirmed by all 3 streams)

No `.github/`, `Makefile`, `pyproject.toml`, `setup.py`, `ruff.toml`, `.pre-commit-config.yaml`, or root `requirements.txt` exist.

### TASK.md Constraints (Confidence: HIGH — confirmed by c2-kb + direct read)

- Do NOT modify existing notebooks
- GitHub Actions on `ubuntu-latest`
- nbstripout to strip outputs
- ruff lint on .py cells
- Validate notebook JSON
- EC2 integration tests on Ubuntu + Arch Linux
- macOS local-only via `make test-mac`
- Makefile targets: `lint`, `validate`, `test-mac`

### Tool Capabilities (Confidence: HIGH — confirmed by c1-internet + c2-kb + c4-docs)

**nbstripout:**
- PyPI: `nbstripout`, latest stable: 0.8.1 (PyPI), 0.9.1 (GitHub)
- `--verify`: returns non-zero exit code if any files would be changed (implies `--dry-run`) — **correct CI flag**
- `--dry-run`: only prints what would change, always exits 0 — **wrong for CI enforcement**
- Also strips metadata by default (signature, widgets, ExecuteTime, etc.) — not just outputs
- GitHub Action available: `kynan/nbstripout@main`

**ruff:**
- Native `.ipynb` support stabilized in v0.1.5; notebooks included by default since v0.6.0
- No `--include` CLI flag — notebook inclusion is config-file only (`extend-include = ["*.ipynb"]` in `ruff.toml`) or automatic since 0.6.0
- `ruff-action@v3` (latest: v3.6.1) supports `args` parameter and `--output-format=github`
- Recommended rules for notebooks: `E`, `F`, `W`; add `per-file-ignores = {"*.ipynb" = ["E402"]}` for import order

**nbformat:**
- Standard validation: `nbformat.read(f, as_version=4)` + `nbformat.validate(nb)`
- `python -m nbformat.validator` is NOT a reliable CLI entry point — use a script
- `jupyter nbconvert --validate` flag is not reliably documented in recent versions

**EC2 integration tests:**
- `machulav/ec2-github-runner@v2` is the standard action for EC2 self-hosted runners
- Requires: AWS credentials, GitHub PAT (repo scope), VPC/subnet/security group
- Ubuntu: `apt-get install python3-pip jupyter-notebook`
- Arch Linux: no native GitHub Actions runner, no AWS CodeBuild image — must use self-hosted EC2 with Arch AMI (community) or Docker container (`archlinux:latest`)
- GitHub self-hosted runners work on any Linux distribution

**macOS cost:** GitHub macOS runners consume minutes at 10x the rate of Linux ($0.08/min vs $0.008/min) — justifies Makefile-only local approach.

---

## Contradictions Found

### Contradiction 1: `nbstripout` CI flag — `--dry-run` vs `--verify`
**Claimed (original findings):** Use `nbstripout --dry-run` for CI enforcement  
**Resolution:** **`--verify` is correct.** `--dry-run` always exits 0 regardless of notebook state. `--verify` implies `--dry-run` AND returns non-zero exit code when files would be changed. All three completed streams (c1, c2, c4) independently confirmed this. The Debian manpage is unambiguous.  
**Impact:** Any CI workflow using `--dry-run` would silently pass even when notebooks contain outputs.

### Contradiction 2: bedrock/miscellaneous notebook count
**Claimed:** 8 or 11 (varied by stream)  
**Resolution:** **10 notebooks.** Verified directly: 100_limit, bedrock_agent, bedrock-quickstart, conversation_examples-test-with-huggingface, conversation_examples, cross-region-inference, csutom_data_source_2, custom_datasource, Knowledgebases_and_rag, multimodal_meta_llama32.

### Contradiction 3: ruff `--include` CLI flag
**Claimed (c2-kb):** `ruff check --include "*.ipynb"` is not a valid CLI flag  
**Claimed (c4-docs):** `ruff check --include "*.ipynb" .` is valid CLI syntax  
**Resolution:** c2-kb is correct. `--include` is a config-file-only setting. Since ruff 0.6.0, `.ipynb` files are discovered automatically. For explicit control, use `extend-include = ["*.ipynb"]` in `ruff.toml`. The `ruff check .` command alone covers notebooks in modern ruff.

---

## Gaps Identified

### Gap 1: c3-context and c5-internal streams failed (rate-limited)
**Finding:** Both streams hit API rate limits and produced no `validated.md`. The three completed streams (c1, c2, c4) provided sufficient coverage — all critical facts were confirmed by at least two independent streams.

### Gap 2: Arch Linux AMI availability
**Claimed:** Community Arch Linux AMIs exist in AWS Marketplace  
**Investigation:** Not independently verified. However, the Docker container approach (`archlinux:latest` on a standard Ubuntu EC2) is a more reliable and reproducible alternative that avoids AMI availability concerns. This is the recommended approach.

### Gap 3: Glue notebook testability
**Finding (orchestrator-verified):** `glue/pyspark-tutorial-glue.ipynb` uses `glue_pyspark` kernel. This notebook cannot be validated with standard Python tooling. It should be excluded from integration tests via path filter (`--ignore glue/`).

### Gap 4: 34/40 notebooks have stored outputs
**Finding (orchestrator-verified):** This was not quantified in any stream. 85% of notebooks need output stripping. The `nbstripout` pre-commit hook or CI check is critical — not optional.

### Gap 5: nbformat version compatibility
**Finding (orchestrator-verified):** 3 notebooks use nbformat 4.4, 37 use 4.5. The validation script should use `as_version=nbformat.NO_CONVERT` or `as_version=4` with appropriate minor version handling to avoid false failures.

---

## Recommended Actions

### Files to Create

```
.github/
  workflows/
    ci.yml              # Tier 1: lint + strip check + JSON validation
    ec2-integration.yml # Tier 2: EC2 Ubuntu + Arch Linux tests
Makefile                # Tier 3: local macOS targets
pyproject.toml          # ruff config
requirements-ci.txt     # CI tool dependencies
scripts/
  validate_notebooks.py # nbformat validation script
```

### 1. `requirements-ci.txt`
```
nbstripout>=0.8.1
ruff>=0.6.0
nbformat>=5.9.0
nbmake>=1.5.0
```

### 2. `pyproject.toml`
```toml
[tool.ruff]
extend-include = ["*.ipynb"]
select = ["E", "F", "W"]

[tool.ruff.per-file-ignores]
"*.ipynb" = ["E402"]
```

### 3. `.github/workflows/ci.yml` (Tier 1 — ubuntu-latest)
```yaml
name: CI
on: [push, pull_request]
jobs:
  lint-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements-ci.txt
      - name: Check notebook outputs stripped
        run: find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -not -path "*/investigation/*" -exec nbstripout --verify {} +
      - name: Lint notebooks with ruff
        uses: astral-sh/ruff-action@v3
        with:
          args: "check --output-format=github ."
      - name: Validate notebook JSON/schema
        run: python scripts/validate_notebooks.py
```

### 4. `scripts/validate_notebooks.py`
```python
import sys, glob, nbformat

notebooks = glob.glob("**/*.ipynb", recursive=True)
notebooks = [n for n in notebooks if ".ipynb_checkpoints" not in n and "investigation" not in n]

errors = []
for path in notebooks:
    try:
        with open(path) as f:
            nb = nbformat.read(f, as_version=4)
        nbformat.validate(nb)
    except Exception as e:
        errors.append(f"{path}: {e}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"All {len(notebooks)} notebooks valid.")
```

### 5. `Makefile`
```makefile
.PHONY: lint validate strip-check test-mac

lint:
	ruff check .

validate:
	python scripts/validate_notebooks.py

strip-check:
	find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -not -path "*/investigation/*" -exec nbstripout --verify {} +

test-mac: lint validate strip-check
	pytest --nbmake notebooks/ bedrock/testing/ --ignore=glue/
```

### 6. EC2 Integration Test Strategy
- Use `machulav/ec2-github-runner@v2` for self-hosted EC2 runners
- Ubuntu: standard `ubuntu-latest` AMI, install deps via `apt-get`
- Arch Linux: use Docker container `archlinux:latest` on Ubuntu EC2 (more reliable than community AMIs)
- Exclude `glue/` from all integration tests (requires AWS Glue environment)
- Test scope: validate notebooks load (`nbformat.read`), not full execution (avoids AWS API calls)

### 7. Pre-commit (optional but recommended)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/kynan/nbstripout
    rev: 0.9.1
    hooks:
      - id: nbstripout
```

---

## References

| # | Source | Used For |
|---|--------|----------|
| 1 | https://github.com/kynan/nbstripout | nbstripout `--verify` flag, pre-commit hook |
| 2 | https://manpages.debian.org/testing/nbstripout/nbstripout.1 | Definitive `--verify` vs `--dry-run` distinction |
| 3 | https://docs.astral.sh/ruff/configuration/#jupyter-notebook-discovery | ruff notebook auto-discovery since 0.6.0 |
| 4 | https://astral.sh/blog/ruff-v0.1.5 | ruff notebook support stabilized in v0.1.5 |
| 5 | https://github.com/astral-sh/ruff-action | ruff-action@v3 |
| 6 | https://github.com/jupyter/nbformat | nbformat validation API |
| 7 | https://github.com/machulav/ec2-github-runner | EC2 self-hosted runner action |
| 8 | https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners/about-github-hosted-runners#standard-github-hosted-runners-for-public-repositories | macOS 10x minute cost |
| 9 | https://github.com/treebeardtech/nbmake | pytest notebook execution |
| 10 | Direct filesystem inspection | All notebook counts, output presence, kernelspecs |
