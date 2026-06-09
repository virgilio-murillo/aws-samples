# AWS Documentation Findings: aws-samples-agent Enhancement

## Investigation Summary

Investigated official AWS documentation for all services represented in the aws-samples project subdirectories: Bedrock, Bedrock AgentCore, Glue, and DataZone. Focused on deployment patterns, API references, known limitations, and best practices relevant to building an enhanced agent prompt.

---

## 1. Service-by-Service Documentation Findings

### Amazon Bedrock (subdirs: `bedrock/`, `bedrock-media-type-mismatch/`)

**What it is:** Managed service for building generative AI applications with foundation models. Agents orchestrate FM interactions, data sources, and APIs.

**Key APIs & Patterns:**
- **Converse API** (`bedrock-runtime` endpoint): Unified multi-turn chat API supporting all Bedrock models
  - ContentBlock types: `text`, `image` (ImageBlock), `document` (DocumentBlock), `video`, `toolUse`, `toolResult`, `guardContent`
  - Source: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html
- **Agent Action Groups**: Defined via OpenAPI schemas or function schemas; backed by Lambda functions
  - Source: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html
- **Agent Deployment**: Create → Configure (model + action groups + knowledge bases) → Test (TSTALIASID) → Create alias → Deploy
  - Source: https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html

**Known Limitations (media type mismatch context):**
- DocumentBlock **REQUIRES** an accompanying `text` ContentBlock in the same message — omitting it causes errors
- Image formats supported: png, jpeg, gif, webp (varies by model)
- Document `name` field vulnerable to prompt injection; use neutral names
- S3 URI alternative to base64 bytes for images/documents
- Source: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html

**Multimodal Knowledge Bases:**
- Nova Multimodal Embeddings: images (.png, .jpg, .jpeg, .gif, .webp), audio (.mp3, .ogg, .wav), video (.mp4, .mov, .mkv, .webm, .flv, .mpeg, .mpg, .wmv, .3gp)
- BDA approach: images (.png, .jpg, .jpeg), audio (.amr, .flac, .m4a, .mp3, .ogg, .wav), video (.mp4, .mov), documents (.pdf)
- Limitation: Multimodal retrieval only available for S3 data sources
- Source: https://docs.aws.amazon.com/bedrock/latest/userguide/kb-multimodal-choose-approach.html

**Quotas:**
- Token-based quotas per model per region (varies by model)
- Provisioned Throughput available for higher capacity
- Source: https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html

---

### Amazon Bedrock AgentCore (subdir: `bedrock-agentcore/`)

**What it is:** Modular agentic platform for building, deploying, and operating AI agents at scale. Framework-agnostic (CrewAI, LangGraph, LlamaIndex, Strands Agents, Google ADK, OpenAI Agents SDK). Supports MCP and A2A protocols.

**Core Services (12 total):**
1. **Runtime** — Serverless agent hosting with microVM isolation, fast cold starts
2. **Harness** — Managed agent loop (single API call: model + prompt + tools)
3. **Memory** — Short-term (multi-turn) and long-term (cross-session) memory
4. **Gateway** — Convert APIs/Lambda to MCP-compatible tools
5. **Identity** — OAuth 2.0, workload identities, JWT authorizers
6. **Code Interpreter** — Sandboxed code execution (Python, JS, TS)
7. **Browser** — Cloud-based browser for web interaction (Playwright, BrowserUse)
8. **Observability** — OpenTelemetry-compatible tracing and debugging
9. **Payments** — Microtransactions via x402 protocol
10. **Evaluations** — Automated agent quality assessment
11. **Policy** — Cedar-based deterministic control boundaries
12. **Registry** — Centralized catalog for agents, MCP servers, tools

Source: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html

**Deployment Pattern:**
- Direct code deployment (ZIP ≤250MB compressed, ≤750MB uncompressed) OR Docker container (≤2GB)
- CLI setup, TypeScript, containerized agents, WebSocket streaming tutorials available
- Source: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-getting-started.html

**Key Quotas:**
| Limit | Value | Adjustable |
|-------|-------|-----------|
| Active sessions/account (us-east-1, us-west-2) | 1,000 | Yes |
| Active sessions/account (other regions) | 500 | Yes |
| Total agents/account | 1,000 | Yes |
| Endpoints per agent | 10 | Yes |
| Max Docker image | 2 GB | No |
| Max deploy package (compressed) | 250 MB | No |
| Sync request timeout | 15 min | No |
| Async job max duration | 8 hours | No |
| Max payload size | 100 MB | No |
| Max hardware per session | 2vCPU/8GB | No |

Source: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html

---

### AWS Glue (subdir: `glue/`)

**What it is:** Serverless ETL service with Data Catalog, crawlers, PySpark/Python Shell jobs, visual ETL canvas.

**Key Patterns:**
- **PySpark ETL Jobs**: DynamicFrame classes, transforms, GlueContext
  - CDK: `@aws-cdk/aws-glue-alpha.PySparkEtlJob` construct
  - Source: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python.html
- **Data Catalog**: Centralized metadata repository with schema versioning, lineage tracking
  - Crawlers infer schemas via classifiers, create partitions
  - ETL jobs can update catalog directly via `enableUpdateCatalog`
  - Source: https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html
- **Python Libraries**: pip3 install, wheel files, zip artifacts supported in Glue 2.0+
  - Source: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html

**Known Limitations:**
- Max 10 partition columns per integration
- Partition specs immutable after integration creation
- Cross-account: Console doesn't invoke CreateIntegrationTableProperty for target tables in other accounts (workaround: manual API call)
- Multiple integrations of same source require separate Glue databases
- Source: https://docs.aws.amazon.com/glue/latest/dg/limitations.html

**Deployment via CDK:**
- `PySparkEtlJob`, `PySparkFlexEtlJob` constructs (alpha module)
- Source: https://docs.aws.amazon.com/cdk/api/v2/docs/@aws-cdk_aws-glue-alpha.PySparkEtlJob.html

---

### Amazon DataZone (subdir: `datazone/`)

**What it is:** Data management service for cataloging, discovering, governing, sharing, and analyzing data across accounts and regions. Integrates with Redshift, Athena, Glue, Lake Formation.

**Key Concepts:**
- Domains → Projects → Environments → Data Sources
- Business glossaries for metadata governance
- Subscription-based data sharing model
- Source: https://docs.aws.amazon.com/datazone/latest/userguide/what-is-datazone.html

**Deployment Pattern:**
- Domain creation via console or API (IAM roles, KMS, SSO)
- Environment profiles and blueprints
- Source: https://docs.aws.amazon.com/datazone/latest/userguide/create-domain.html

**Key Quotas:**
| Resource | Limit |
|----------|-------|
| Data assets per domain | 1,000,000 |
| Data asset types | 1,000 |
| Environments per domain | 1,000 |
| Glossaries per domain | 1,000 |
| Glossary terms per domain | 10,000 |
| Domain units | 500 |
| Hierarchy levels | 5 |
| Data source runs/source/day | 25 |
| Data products | 500,000 |

**API Rate Limits:** Most APIs 20 TPS; subscription APIs 3-8 TPS; CreateGlossary 5 TPS.
Source: https://docs.aws.amazon.com/datazone/latest/userguide/datazone-limits.html

---

## 2. Deployment Patterns (from AWS Docs)

### Common Patterns Across Samples:

| Pattern | Tool | Use Case |
|---------|------|----------|
| **AWS CDK** | TypeScript/Python | Complex infrastructure (Bedrock agents, Glue jobs, DataZone domains) |
| **AWS SAM** | YAML templates | Serverless Lambda-based samples |
| **CloudFormation** | YAML/JSON | Direct infrastructure templates |
| **Makefile** | GNU Make | Build orchestration, multi-target deployment |

### CDK Best Practices (from official docs):
- Organize apps into logical constructs (API, database, monitoring)
- One app per repository for CI/CD isolation
- Start simple, add complexity only when needed
- Align with Well-Architected Framework
- Use CDK Pipelines for automated deployment
- Source: https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html

### SAM Deployment Pattern:
- `sam init` → `sam build` → `sam deploy --guided`
- Transform: AWS::Serverless-2016-10-31
- Source: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html

---

## 3. Languages & Frameworks (from AWS Docs)

Based on the services in the project, expected languages/frameworks:

| Service | Primary Language | Framework/SDK |
|---------|-----------------|---------------|
| Bedrock Agents | Python | Boto3, Powertools for Lambda |
| Bedrock AgentCore | Python/TypeScript | Strands Agents, LangGraph, CrewAI |
| Glue ETL | Python (PySpark) | GlueContext, DynamicFrame |
| DataZone | Python/TypeScript | Boto3, CDK |
| Infrastructure | TypeScript/Python | AWS CDK v2, SAM |

---

## 4. What the Enhanced Prompt Should Contain

Based on documentation analysis, the agent prompt should include knowledge of:

### Critical Rules (highest ROI per shared learnings):
1. **SANITIZE AWS account IDs** — never expose real account IDs in outputs
2. **Verify factual claims** — cross-reference against actual source code, not assumptions
3. **Service-specific constraints** — e.g., DocumentBlock requires text, Glue partition limits

### Service Knowledge:
- Bedrock Converse API ContentBlock types and their constraints
- AgentCore's 12 modular services and when to use each
- Glue ETL patterns (PySpark DynamicFrame vs Spark DataFrame)
- DataZone domain/project/environment hierarchy

### Deployment Awareness:
- CDK constructs available for each service (including alpha modules for Glue)
- SAM for serverless Lambda patterns
- Makefile as build orchestrator

### Known Pitfalls:
- Bedrock media type mismatches (DocumentBlock without text, wrong image format)
- Glue partition immutability post-creation
- DataZone 25 data source runs/day limit
- AgentCore 2GB Docker image limit, 15min sync timeout

---

## 5. Key Documentation References

| Topic | URL |
|-------|-----|
| Bedrock Agents Overview | https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html |
| Bedrock Converse API | https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html |
| Bedrock Action Groups | https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html |
| Bedrock Lambda Integration | https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html |
| AgentCore Overview | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html |
| AgentCore Runtime | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html |
| AgentCore Quotas | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html |
| AgentCore Gateway (OpenAPI) | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-schema-openapi.html |
| Glue PySpark Programming | https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python.html |
| Glue Crawlers | https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html |
| Glue Limitations | https://docs.aws.amazon.com/glue/latest/dg/limitations.html |
| DataZone Overview | https://docs.aws.amazon.com/datazone/latest/userguide/what-is-datazone.html |
| DataZone Quotas | https://docs.aws.amazon.com/datazone/latest/userguide/datazone-limits.html |
| CDK Best Practices | https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html |
| SAM Overview | https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html |
| Multimodal KB | https://docs.aws.amazon.com/bedrock/latest/userguide/kb-multimodal-choose-approach.html |

---

## 6. Confidence Assessment

| Finding | Confidence | Basis |
|---------|-----------|-------|
| AgentCore 12 services | HIGH | Official docs read directly |
| Converse API ContentBlock types | HIGH | Official docs read directly |
| DocumentBlock requires text | HIGH | Official docs explicit statement |
| Glue partition limitations | HIGH | Official docs read directly |
| DataZone quotas | HIGH | Official docs read directly |
| AgentCore quotas | HIGH | Official docs read directly |
| Project uses CDK/SAM | MEDIUM | Inferred from Makefile + service types (not verified against actual code) |
| Languages used | MEDIUM | Inferred from service documentation patterns (not verified against actual code) |

---

*Investigation completed: 2026-05-24. All findings sourced exclusively from docs.aws.amazon.com.*
