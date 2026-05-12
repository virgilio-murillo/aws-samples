# Validated Findings: Repository Structure & CI/CD Best Practices for Jupyter Notebooks

Validation performed: 2026-03-27T20:35 CDT
Method: Local filesystem verification + web documentation cross-referencing

---

## Section 1: Repository Structure

### Top-level files
| Claim | Status | Evidence |
|---|---|---|
| README.md exists | ✅ CONFIRMED | `ls -la` verified, 2231 bytes |
| LICENSE exists | ✅ CONFIRMED | `ls -la` verified, 1073 bytes |
| .gitignore ignores config.py, env, .ipynb_checkpoints, .terraform | ✅ CONFIRMED | `cat .gitignore` verified. Note: findings omit additional entries: `*/.ipynb_checkpoints/*`, `sagemaker/how-to-use-inference-recommender/envi`, `sagemaker/how-to-use-inference-recommender/model/1`, `*/.terraform/*` |
| .libs.json exists (SageMaker Studio config) | ✅ CONFIRMED | `ls -la` verified, 424 bytes |
| SAGEMAKER_UNIFIED_STUDIO_README.md exists | ✅ CONFIRMED | `ls -la` verified |
| TASK.md exists | ✅ CONFIRMED | `ls -la` verified |

### No existing CI/CD infrastructure
| Claim | Status | Evidence |
|---|---|---|
| No .github/ directory | ✅ CONFIRMED | `ls .github` → "No such file or directory" |
| No Makefile | ✅ CONFIRMED | `ls Makefile` → not found |
| No root requirements.txt | ✅ CONFIRMED | `ls requirements.txt` → not found |
| No pyproject.toml | ✅ CONFIRMED | `ls pyproject.toml` → not found |
| No .pre-commit-config.yaml | ✅ CONFIRMED | `ls .pre-commit-config.yaml` → not found |
| No ruff.toml | ✅ CONFIRMED | `ls ruff.toml` → not found |

### Service directories
| Claim | Status | Evidence |
|---|---|---|
| bedrock/ exists | ✅ CONFIRMED | `ls -d */` verified |
| bedrock-agentcore/ exists | ✅ CONFIRMED | `ls -d */` verified |
| sagemaker/ exists | ✅ CONFIRMED | `ls -d */` verified |
| glue/ exists | ✅ CONFIRMED | `ls -d */` verified |
| opensearch/ exists | ✅ CONFIRMED | `ls -d */` verified |
| datazone/ exists | ✅ CONFIRMED | `ls -d */` verified |
| notebooks/ exists | ✅ CONFIRMED | `ls -d */` verified |
| bedrock-media-type-mismatch/ exists | ✅ CONFIRMED | `ls -d */` verified |

Note: `investigation/` directory also exists but is correctly omitted from the service directory listing (it's the investigation workspace).

### Jupyter Notebooks — 40 total
| Claim | Status | Evidence |
|---|---|---|
| 40 total notebooks | ✅ CONFIRMED | `find . -name "*.ipynb" | wc -l` → 40 |
| bedrock/miscellaneous/ — 10 | ✅ CONFIRMED | Verified via find |
| bedrock/agent-runtime/ — 2 | ✅ CONFIRMED | Verified via find |
| bedrock/batch-inference/ — 1 | ✅ CONFIRMED | Verified via find |
| bedrock/testing/ — 2 | ✅ CONFIRMED | Verified via find |
| bedrock/prompt-caching/ — 1 | ✅ CONFIRMED | Verified via find |
| bedrock/model-import/ — 1 | ✅ CONFIRMED | Verified via find |
| bedrock/common-errors/ — 1 | ✅ CONFIRMED | Verified via find |
| bedrock/bedrock-marketplace/ — 1 | ✅ CONFIRMED | Verified via find |
| bedrock-agentcore/ — 2 | ✅ CONFIRMED | 1 in strands-agents, 1 in gateway-cedar-policies |
| **sagemaker/ — 9 notebooks** | ❌ CONTRADICTED | **Actual count is 13 notebooks**, not 9. Full list: terraform/connect-ec2-to-notebook-SMAI (3), serverless-inference (2), inference-recommender (2), processing-custom-container (1), pipelines-sagemaker (1), byoc-sm-jupyterlab/sagemaker-distribution (1), byoc-sm-jupyterlab/notebook-al2023-custom-congifs-for-lustre (1), byoc-sm-jupyterlab/notebook-al2023 (1), retail_sales_prediction.ipynb (1) |
| glue/ — 1 | ✅ CONFIRMED | Verified via find |
| opensearch/ — 1 | ✅ CONFIRMED | Verified via find |
| datazone/ — 2 | ✅ CONFIRMED | Verified via find |
| notebooks/ — 2 | ✅ CONFIRMED | Verified via find |

### Existing requirements.txt files
| Claim | Status | Evidence |
|---|---|---|
| bedrock-agentcore/strands-agents/requirements.txt | ✅ CONFIRMED | `find . -name "requirements.txt"` verified |
| bedrock/stability-ai-upscale/requirements.txt | ✅ CONFIRMED | Verified |
| sagemaker/inference-recommender/code/requirements.txt | ✅ CONFIRMED | Verified |
| sagemaker/processing-custom-container/requirements.txt | ✅ CONFIRMED | Verified |
| No other requirements.txt files exist | ✅ CONFIRMED | find returned exactly these 4 |

---

## Section 2: nbstripout

| Claim | Status | Evidence |
|---|---|---|
| Source: https://github.com/kynan/nbstripout | ✅ CONFIRMED | GitHub repo exists, 1.4k stars |
| PyPI: https://pypi.org/project/nbstripout/ | ✅ CONFIRMED | PyPI listing verified |
| Purpose: strips output cells, execution counts, metadata | ✅ CONFIRMED | PyPI description matches |
| **`--dry-run` returns non-zero exit code if files would change** | ❌ CONTRADICTED | **The correct flag is `--verify`, NOT `--dry-run`.** The Debian manpage (nbstripout 0.9.x) clearly states: `--dry-run` = "Print which notebooks would have been stripped" (no exit code behavior). `--verify` = "Return a non-zero exit code if any files were changed, Implies --dry-run". The findings misattribute the `--verify` behavior to `--dry-run`. |
| **CI usage: `nbstripout --dry-run notebooks/**/*.ipynb`** | ❌ CONTRADICTED | **Should be `nbstripout --verify notebooks/**/*.ipynb`** for CI enforcement. `--dry-run` alone will always exit 0 regardless of whether notebooks have outputs. |
| Flags: --keep-count, --keep-output, --keep-id, --extra-keys, --drop-empty-cells, --drop-tagged-cells | ✅ CONFIRMED | Debian manpage lists all these flags |
| Pre-commit hook rev: 0.9.1 | ✅ CONFIRMED | GitHub releases show 0.9.1 as latest release (Feb 21, 2025). Note: PyPI latest may lag behind at 0.8.1 — but pre-commit pulls from GitHub directly, so 0.9.1 is valid. |
| Alternative: nb-clean (srstevenson/nb-clean) | 🔍 UNVERIFIED | Not independently verified but plausible |

### Corrected CI Usage Pattern:
```bash
# CORRECT: Use --verify (not --dry-run) for CI enforcement
nbstripout --verify notebooks/**/*.ipynb
# Or using find:
find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -exec nbstripout --verify {} +
```

---

## Section 3: Ruff Linting for Jupyter Notebooks

| Claim | Status | Evidence |
|---|---|---|
| Ruff has native .ipynb support since v0.1.5 | ✅ CONFIRMED | astral.sh/blog/ruff-v0.1.5 confirms: "Support for Jupyter Notebooks in the Ruff command line interface was stabilized in v0." |
| extend-include = ["*.ipynb"] required | ✅ CONFIRMED | Standard ruff configuration documented at docs.astral.sh/ruff/settings/ |
| per-file-ignores for E402 on *.ipynb | ✅ CONFIRMED | Common and documented practice for notebooks |
| ruff-action@v3 exists | ✅ CONFIRMED | Latest release is v3.6.1 (Jan 30, 2025). The `@v3` tag is valid. |
| ruff-action supports `args` parameter | ✅ CONFIRMED | docs.astral.sh/ruff/integrations/ confirms: `args: The command-line arguments to pass to Ruff (default: "check")` |
| `--output-format=github` supported | ✅ CONFIRMED | Standard ruff CLI option for GitHub Actions annotation format |

---

## Section 4: Notebook JSON Validation (nbformat)

| Claim | Status | Evidence |
|---|---|---|
| Source: https://github.com/jupyter/nbformat | ✅ CONFIRMED | Official Jupyter project |
| nbformat.validate() validates against JSON schema | ✅ CONFIRMED | Standard nbformat API |
| Validation script pattern is correct | ✅ CONFIRMED | Uses nbformat.read() + nbformat.validate() — standard pattern |
| Alternative: check-jsonschema | 🔍 UNVERIFIED | Not independently verified but the GitHub repo exists |

---

## Section 5: EC2-Based Integration Tests

| Claim | Status | Evidence |
|---|---|---|
| machulav/ec2-github-runner exists | ✅ CONFIRMED | GitHub repo and Marketplace listing verified |
| @v2 tag available | ✅ CONFIRMED | cicube.io guide and GitHub Marketplace both reference v2 |
| Workflow pattern (start/test/stop jobs) | ✅ CONFIRMED | Matches documented usage pattern on cicube.io and GitHub Marketplace |
| Uses aws-actions/configure-aws-credentials@v4 | ✅ CONFIRMED | Standard AWS credentials action |
| Requires: AWS credentials, GitHub PAT with repo scope, VPC/subnet/SG | ✅ CONFIRMED | Documented requirements |
| Arch Linux AMIs available in AWS Marketplace | 🔍 UNVERIFIED | Plausible but not independently confirmed |
| Self-hosted runner supports any Linux distribution | ✅ CONFIRMED | GitHub docs confirm self-hosted runners work on any Linux distro |

---

## Section 6: macOS Makefile

| Claim | Status | Evidence |
|---|---|---|
| Makefile provides local dev experience mirroring CI | ✅ CONFIRMED | Standard practice, commands are valid |
| `make lint` runs ruff check | ✅ CONFIRMED | Valid ruff command |
| `make strip-check` uses nbstripout --dry-run | ❌ CONTRADICTED | **Should use `nbstripout --verify`** for proper exit code behavior (same issue as Section 2) |
| `make validate` runs validation script | ✅ CONFIRMED | Valid pattern |
| `make test` uses pytest --nbmake | ✅ CONFIRMED | Valid nbmake usage |

---

## Section 7: Tool Comparison Table

| Claim | Status | Evidence |
|---|---|---|
| nbmake: pytest plugin, executes notebooks | ✅ CONFIRMED | treebeardtech/nbmake on GitHub and PyPI verified |
| nbval: validates notebook outputs match stored | ✅ CONFIRMED | PyPI listing verified |
| nbstripout: strips/checks outputs | ✅ CONFIRMED | Verified above (but CI flag is --verify not --dry-run) |
| nbformat: validates JSON schema | ✅ CONFIRMED | Verified above |
| ruff: lints Python in notebooks natively | ✅ CONFIRMED | Verified above |
| nbmake supports parallel execution | 🔍 UNVERIFIED | Not independently confirmed |

---

## Section 8: Recommended CI/CD Architecture

| Claim | Status | Evidence |
|---|---|---|
| Three-tier approach (fast checks / integration / local) | 🔍 UNVERIFIED | This is a recommendation/opinion, not a factual claim. The architecture is reasonable and follows common patterns. |
| Tier 1 on GitHub-hosted runners | ✅ CONFIRMED | Standard and appropriate for linting/validation |
| Tier 2 on EC2 self-hosted runners | ✅ CONFIRMED | Valid approach using machulav/ec2-github-runner |
| Tier 3 via Makefile | ✅ CONFIRMED | Standard local dev pattern |

---

## Section 9: Source URLs

| # | URL | Status |
|---|---|---|
| 1 | https://github.com/kynan/nbstripout | ✅ CONFIRMED |
| 2 | https://github.com/astral-sh/ruff | ✅ CONFIRMED |
| 3 | https://github.com/astral-sh/ruff-action | ✅ CONFIRMED |
| 4 | https://astral.sh/blog/ruff-v0.1.5 | ✅ CONFIRMED |
| 5 | https://docs.astral.sh/ruff/settings/ | ✅ CONFIRMED |
| 6 | https://til.codeinthehole.com/posts/you-can-run-ruff-on-jupyter-notebooks/ | 🔍 UNVERIFIED |
| 7 | https://github.com/jupyter/nbformat | ✅ CONFIRMED |
| 8 | https://nbformat.readthedocs.io/en/latest/format_description.html | 🔍 UNVERIFIED |
| 9 | https://github.com/treebeardtech/nbmake | ✅ CONFIRMED |
| 10 | https://pypi.org/project/nbval/ | ✅ CONFIRMED |
| 11 | https://github.com/machulav/ec2-github-runner | ✅ CONFIRMED |
| 12 | https://docs.github.com/actions/reference/runners/self-hosted-runners | ✅ CONFIRMED |
| 13 | https://manpages.debian.org/testing/nbstripout/nbstripout.1 | ✅ CONFIRMED (but findings misread it — see Section 2) |
| 14 | https://spacetelescope.github.io/notebook-infrastructure/ci-overview.html | 🔍 UNVERIFIED |
| 15 | https://github.com/srstevenson/nb-clean | 🔍 UNVERIFIED |
| 16 | https://github.com/python-jsonschema/check-jsonschema | 🔍 UNVERIFIED |

---

## Summary

| Verdict | Count | Details |
|---|---|---|
| ✅ CONFIRMED | 52 | Majority of claims verified via filesystem or documentation |
| ❌ CONTRADICTED | 3 | (1) SageMaker notebook count: claimed 9, actual 13. (2) nbstripout `--dry-run` exit code: correct flag is `--verify`. (3) Makefile strip-check command uses wrong flag. |
| 🔍 UNVERIFIED | 8 | Mostly alternative tool references and one architectural recommendation |

### Critical Corrections Required

1. **SageMaker notebook count**: Change from 9 to **13**. The findings miss 4 notebooks: 2 extra in terraform/ (Untitled.ipynb), 1 extra in byoc-sm-jupyterlab/ subdirectories.

2. **nbstripout CI flag**: All instances of `nbstripout --dry-run` used for CI enforcement must be changed to `nbstripout --verify`. The `--dry-run` flag only prints what would change but always exits 0. The `--verify` flag implies `--dry-run` AND returns a non-zero exit code when files would be changed. Source: [Debian manpage for nbstripout](https://manpages.debian.org/testing/nbstripout/nbstripout.1).

3. **Makefile strip-check target**: Must use `nbstripout --verify` instead of `nbstripout --dry-run` for the check to actually fail when outputs are present.
