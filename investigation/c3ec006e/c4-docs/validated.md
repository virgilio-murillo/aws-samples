# Validated Findings: aws-samples-agent Enhancement (Documentation Claims)

**Validation Date:** 2026-05-24
**Method:** Cross-referenced claims against live AWS documentation pages and actual project filesystem.

---

## 1. Amazon Bedrock AgentCore — Core Services Count

**Claim:** AgentCore has 12 core services: Runtime, Harness, Memory, Gateway, Identity, Code Interpreter, Browser, Observability, Payments, Evaluations, Policy, Registry.

**Verdict: ✅ CONFIRMED**

Source: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html — The official docs list exactly these 12 services in the same order with matching descriptions.

---

## 2. AgentCore Framework Support

**Claim:** Framework-agnostic, supports CrewAI, LangGraph, LlamaIndex, Strands Agents, Google ADK, OpenAI Agents SDK. Supports MCP and A2A protocols.

**Verdict: ✅ CONFIRMED**

Source: Official docs explicitly state: "CrewAI, LangGraph, LlamaIndex, and Strands Agents" in the overview, and the Runtime row adds "Google ADK, OpenAI Agents SDK" and "popular protocols like MCP and A2A."

---

## 3. AgentCore Quotas

**Claim:** Active sessions 1,000 (us-east-1/us-west-2), 500 (other); Total agents 1,000; Endpoints/agent 10; Docker 2GB; Deploy pkg 250MB compressed/750MB uncompressed; Sync timeout 15min; Async 8hrs; Payload 100MB; Hardware 2vCPU/8GB.

**Verdict: ✅ CONFIRMED**

All values match exactly against https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html (verified 2026-05-24).

---

## 4. Bedrock Converse API ContentBlock Types

**Claim:** ContentBlock types are: `text`, `image` (ImageBlock), `document` (DocumentBlock), `video`, `toolUse`, `toolResult`, `guardContent`.

**Verdict: ⚠️ CONFIRMED (INCOMPLETE)**

The listed types are all valid. However, the official docs also document additional ContentBlock types not mentioned in the findings:
- `cachePoint` — for prompt caching
- `reasoningContent` — for reasoning/thinking blocks

These omissions don't invalidate the listed types but the list is not exhaustive.

---

## 5. DocumentBlock Requires Accompanying Text

**Claim:** DocumentBlock REQUIRES an accompanying `text` ContentBlock in the same message — omitting it causes errors.

**Verdict: ✅ CONFIRMED**

Source: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html explicitly states: "In the content field of the Message object, you must also include a text field with a prompt related to the document."

---

## 6. Document `name` Field Prompt Injection Vulnerability

**Claim:** Document `name` field is vulnerable to prompt injection; use neutral names.

**Verdict: ✅ CONFIRMED**

Source: Same docs page states: "The name field is vulnerable to prompt injections, because the model might inadvertently interpret it as instructions. Therefore, we recommend that you specify a neutral name."

---

## 7. S3 URI Alternative to Base64

**Claim:** S3 URI can be used as alternative to base64 bytes for images/documents.

**Verdict: ✅ CONFIRMED**

Source: Docs show explicit S3 URI examples with `s3Location` containing `uri` and `bucketOwner` fields for both ImageBlock and DocumentBlock.

---

## 8. Image Formats Supported

**Claim:** png, jpeg, gif, webp (varies by model).

**Verdict: ✅ CONFIRMED**

Source: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-multimodal-choose-approach.html confirms Nova Multimodal Embeddings supports: .png, .jpg, .jpeg, .gif, .webp. The "(varies by model)" qualifier is appropriate.

---

## 9. Multimodal Knowledge Bases — File Types

**Claim:** Nova Multimodal Embeddings supports images (.png, .jpg, .jpeg, .gif, .webp), audio (.mp3, .ogg, .wav), video (.mp4, .mov, .mkv, .webm, .flv, .mpeg, .mpg, .wmv, .3gp). BDA supports images (.png, .jpg, .jpeg), audio (.amr, .flac, .m4a, .mp3, .ogg, .wav), video (.mp4, .mov), documents (.pdf).

**Verdict: ✅ CONFIRMED**

Source: Exact match with the table at https://docs.aws.amazon.com/bedrock/latest/userguide/kb-multimodal-choose-approach.html

---

## 10. Multimodal Retrieval S3-Only Limitation

**Claim:** Multimodal retrieval only available for S3 data sources.

**Verdict: ✅ CONFIRMED**

Source: Docs state: "Multimodal retrieval is currently available only for Amazon S3 data sources. Other data sources (Confluence, SharePoint, Salesforce, Web Crawler) do not process multimodal files during ingestion."

---

## 11. AWS Glue Limitations

**Claim:** Max 10 partition columns; partition specs immutable after integration creation; cross-account console doesn't invoke CreateIntegrationTableProperty; multiple integrations of same source require separate Glue databases.

**Verdict: ✅ CONFIRMED**

Source: https://docs.aws.amazon.com/glue/latest/dg/limitations.html — All four limitations match exactly.

---

## 12. Amazon DataZone Quotas

**Claim:** Data assets 1M; Asset types 1,000; Environments 1,000; Glossaries 1,000; Terms 10,000; Domain units 500; Hierarchy levels 5; Data source runs/day 25; Data products 500,000.

**Verdict: ✅ CONFIRMED**

Source: https://docs.aws.amazon.com/datazone/latest/userguide/datazone-limits.html — All values match exactly.

---

## 13. DataZone API Rate Limits

**Claim:** Most APIs 20 TPS; subscription APIs 3-8 TPS; CreateGlossary 5 TPS.

**Verdict: ✅ CONFIRMED**

Source: Same quotas page confirms CreateGlossary at 5 TPS, most CRUD/list APIs at 20 TPS, subscription-related APIs at 3-8 TPS.

---

## 14. Project Subdirectories

**Claim:** Project has subdirs: `bedrock/`, `bedrock-media-type-mismatch/`, `bedrock-agentcore/`, `glue/`, `datazone/`.

**Verdict: ⚠️ CONFIRMED (INCOMPLETE)**

All claimed directories exist. However, the project also contains: `opensearch/`, `sagemaker/`, `notebooks/`, `scripts/`, `kiro-notes/`, `kiro-test/`. The findings omit these, which is a significant gap since `sagemaker/` and `opensearch/` are AWS service directories relevant to the agent prompt.

---

## 15. Project Uses CDK/SAM for Deployment

**Claim:** Project uses AWS CDK (TypeScript/Python) and AWS SAM for deployment. Table lists CDK, SAM, CloudFormation, Makefile as deployment patterns.

**Verdict: ❌ CONTRADICTED**

Filesystem check reveals: **No CDK files** (no `cdk.json`, no `.ts` files), **no SAM templates** (`template.yaml`/`template.yml` absent), **no CloudFormation templates**. The project uses only:
- A `Makefile` for linting/validation (ruff, nbstripout, notebook validation)
- GitHub Actions workflows (`.github/workflows/ci.yml`, `.github/workflows/ec2-integration.yml`)
- Python scripts and Jupyter notebooks

The findings explicitly noted this was "MEDIUM" confidence and "inferred from Makefile + service types (not verified against actual code)" — the self-assessment was correct that this was unverified.

---

## 16. Languages & Frameworks Used

**Claim:** Bedrock Agents use Python/Boto3; AgentCore uses Python/TypeScript with Strands Agents; Glue uses PySpark; DataZone uses Python/TypeScript with CDK; Infrastructure uses TypeScript/Python CDK v2 and SAM.

**Verdict: ⚠️ PARTIALLY CONTRADICTED**

- Python is the **only** language in this project. No TypeScript files exist.
- Boto3 usage: CONFIRMED (bedrock-media-type-mismatch scripts use boto3)
- Strands Agents: CONFIRMED (bedrock-agentcore/strands-agents/ exists with Python files)
- PySpark/Glue: CONFIRMED (glue/pyspark-tutorial-glue.ipynb exists)
- TypeScript/CDK claims: CONTRADICTED — no TypeScript or CDK in this repo
- SAM claims: CONTRADICTED — no SAM templates in this repo

---

## 17. CDK Best Practices & SAM Deployment Pattern

**Claim:** CDK best practices include organizing into logical constructs, one app per repo, CDK Pipelines. SAM pattern: `sam init` → `sam build` → `sam deploy --guided`.

**Verdict: ⚠️ UNVERIFIED (IRRELEVANT)**

These are general AWS documentation facts that are likely accurate (sourced from official docs URLs), but they are **not applicable** to this project since it uses neither CDK nor SAM. The documentation URLs cited are valid pages, but the relevance to this specific project is nil.

---

## Summary Table

| # | Finding | Verdict |
|---|---------|---------|
| 1 | AgentCore 12 services | ✅ CONFIRMED |
| 2 | AgentCore framework support | ✅ CONFIRMED |
| 3 | AgentCore quotas | ✅ CONFIRMED |
| 4 | Converse API ContentBlock types | ✅ CONFIRMED (incomplete — missing cachePoint, reasoningContent) |
| 5 | DocumentBlock requires text | ✅ CONFIRMED |
| 6 | Document name prompt injection | ✅ CONFIRMED |
| 7 | S3 URI alternative | ✅ CONFIRMED |
| 8 | Image formats | ✅ CONFIRMED |
| 9 | Multimodal KB file types | ✅ CONFIRMED |
| 10 | Multimodal S3-only limitation | ✅ CONFIRMED |
| 11 | Glue limitations | ✅ CONFIRMED |
| 12 | DataZone quotas | ✅ CONFIRMED |
| 13 | DataZone API rate limits | ✅ CONFIRMED |
| 14 | Project subdirectories | ✅ CONFIRMED (incomplete — misses opensearch/, sagemaker/) |
| 15 | Project uses CDK/SAM | ❌ CONTRADICTED |
| 16 | Languages & frameworks | ⚠️ PARTIALLY CONTRADICTED (Python-only, no TypeScript/CDK/SAM) |
| 17 | CDK/SAM best practices | ⚠️ UNVERIFIED (accurate docs but irrelevant to project) |

---

## Key Corrections for Downstream Use

1. **This project is Python-only** — no TypeScript, no CDK, no SAM, no CloudFormation. Deployment tooling is Makefile + GitHub Actions.
2. **Missing service directories**: `opensearch/` and `sagemaker/` are significant project subdirectories not covered in the findings.
3. **ContentBlock types list is incomplete** — add `cachePoint` and `reasoningContent` to the known types.
4. All AWS documentation-sourced facts (quotas, limitations, API details) were accurate and well-cited.
