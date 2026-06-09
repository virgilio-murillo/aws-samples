# Internet Research Findings: Enhance aws-samples-agent

## 1. What Samples Exist in Each Subdirectory (from public repos)

Based on web research of the aws-samples ecosystem:

### bedrock/
- **Source**: [aws-samples/amazon-bedrock-samples](https://github.com/aws-samples/amazon-bedrock-samples)
- Contains examples for all foundational models on Amazon Bedrock
- Typical structure: Jupyter notebooks organized by use case (agents, knowledge-bases, RAG, multimodal)
- Categories: `agents-and-function-calling/`, `introduction-to-bedrock/`, `knowledge-bases/`

### bedrock-agentcore/
- **Source**: [awslabs/amazon-bedrock-agentcore-samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples)
- Python-based agent deployment to AgentCore Runtime
- Uses AgentCore CLI or SDK for deployment
- Supports frameworks: Strands Agents, LangGraph, Google ADK, OpenAI Agents
- **Architecture**: ARM64 required, serverless environments, entrypoint.py pattern

### bedrock-media-type-mismatch/
- Likely demonstrates/troubleshoots the Bedrock Converse API media type validation issue
- Common error: "The provided image does not match the specified image format"
- Related to multimodal content handling where type must be explicitly specified (defaults to text)
- Source: [AWS docs on multimodal KB troubleshooting](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-multimodal-troubleshooting.html)

### datazone/
- **Source**: [aws-samples/data-mesh-datazone-cdk-cloudformation](https://github.com/aws-samples/data-mesh-datazone-cdk-cloudformation)
- Enterprise data mesh with Amazon DataZone
- Uses CDK and CloudFormation infrastructure

### glue/
- **Source**: [aws-samples/aws-glue-samples](https://github.com/aws-samples/aws-glue-samples)
- PySpark ETL jobs, Python Shell jobs
- Patterns: CDK-based CI/CD for Glue ([aws-glue-cdk-cicd](https://github.com/aws-samples/aws-glue-cdk-cicd))

### opensearch/ (confirmed by head agent)
- Likely Amazon OpenSearch Serverless (AOSS) samples
- Common pattern: vector database for RAG, knowledge base backing store

### sagemaker/ (confirmed by head agent)
- Terraform-based deployment patterns (per head agent directive)
- Training, inference, model deployment

### notebooks/ (confirmed by head agent)
- Standalone Jupyter notebooks (~40 total across project)

---

## 2. Makefile Structure (from web patterns)

Common aws-samples Makefile patterns found:

**CDK Python projects** (aws-samples/aws-cdk-project-structure-python):
- `scripts/install-deps.sh` + `scripts/run-tests.sh`
- `npx cdk deploy <StackName>`
- `pip-compile` for dependency management

**Head agent confirmed**: The actual project uses `make test-mac` (NOT `make test`).

---

## 3. Languages/Frameworks Used

| Service | Primary Language | Framework/Tools |
|---------|-----------------|-----------------|
| Bedrock | Python | Jupyter notebooks, boto3, Bedrock SDK |
| Bedrock AgentCore | Python | AgentCore CLI/SDK, Strands, LangGraph |
| DataZone | Python/TypeScript | CDK, CloudFormation |
| Glue | Python | PySpark, Glue ETL libraries |
| OpenSearch | Python | OpenSearch client, AOSS |
| SageMaker | Python | Terraform, SageMaker SDK |

**Key correction from head agent**: Project uses Jupyter + Terraform + Docker/ECR, NOT SAM/CloudFormation as the current prompt claims.

---

## 4. Deployment Patterns

| Sample | Deployment Method |
|--------|------------------|
| Bedrock notebooks | Manual execution (Jupyter) |
| Bedrock AgentCore | `agentcore deploy` CLI, direct code deployment (.zip), Docker containers |
| DataZone | CDK/CloudFormation stacks |
| Glue | CDK-based CI/CD pipelines |
| SageMaker | Terraform |
| General | Docker/ECR for containerized workloads |

---

## 5. What the Enhanced Prompt Should Contain

### Best Practices from Research

**A. Optimal Agent Prompt Structure** (from [roborhythms.com](https://www.roborhythms.com/fix-agent-tool-hallucinations-4-section-prompt/)):
Four sections in order:
1. Role and scope
2. Tools with strict schemas
3. Decision rules
4. Output format

**B. AWS Startup Prompt Library Reference** ([Full AWS Deployment Agent](https://aws.amazon.com/startups/prompt-library/full-aws-deployment-agent)):
Uses XML-tagged sections:
- `<safety_protocol>` - pause on risky actions
- `<infrastructure_standards>` - MUST-follow constraints
- `<service_recommendations>` - decision tables
- `<decision_criteria>` - when to choose what

**C. ABCA (Autonomous Background Coding Agents) Prompt Guide** ([aws-samples](https://aws-samples.github.io/sample-autonomous-cloud-coding-agents/customizing/prompt-engineering/)):
- "CLAUDE.md is the single most impactful thing you can add"
- Should include: Build commands, Conventions, Architecture sections
- Describe end state, not steps
- State constraints and define success
- Point to the right area (file paths)

**D. Kiro Steering Best Practices** ([kiro.dev](https://kiro.dev/docs/cli/steering/)):
- `.kiro/steering/` markdown files for persistent project context
- Frontmatter with `inclusion: always` for critical rules
- Reference: [awsdataarchitect/kiro-best-practices](https://github.com/awsdataarchitect/kiro-best-practices)
- Reference: [aws-samples/sample-kiro-steering-studio](https://github.com/aws-samples/sample-kiro-steering-studio)

**E. Jupyter Notebook Agent Conventions** (from Microsoft SKILL.md + community):
- Keep each code cell focused on one step
- Add markdown cells explaining purpose and expected result
- Validate notebooks top-to-bottom
- Use `ruff check` natively on `.ipynb` files
- Configure per-file-ignores: `"*.ipynb" = ["E402"]` in pyproject.toml
- Use `nbstripout` as git filter/pre-commit hook to strip outputs
- `nbformat` for validation

### Recommended Enhanced Prompt Sections

Based on all research, the enhanced prompt should contain:

1. **Critical Rules** (highest ROI per shared learnings):
   - SANITIZE AWS account IDs in all outputs
   - Verify factual claims against actual source code
   - Use `make test-mac` not `make test`
   - Notebooks are the primary artifact type (not Lambda/SAM)

2. **Project Architecture**:
   - 8 service directories: bedrock, bedrock-agentcore, bedrock-media-type-mismatch, datazone, glue, opensearch, sagemaker, notebooks
   - ~40 Jupyter notebooks total
   - CI: `.github/workflows/ci.yml` + `ec2-integration.yml`

3. **Technology Stack**:
   - Python (primary), Jupyter notebooks
   - Terraform (not CloudFormation/SAM)
   - Docker/ECR for containerized workloads
   - AgentCore CLI for Bedrock agent deployment
   - CDK for some infrastructure

4. **Deployment Patterns per Service** (decision table)

5. **Notebook Conventions**:
   - Cell structure rules
   - Linting with ruff
   - Output stripping for git
   - Validation requirements

6. **Build/Test Commands**:
   - Actual Makefile targets (make test-mac, etc.)
   - How to validate notebooks

---

## Sources

1. https://github.com/aws-samples/amazon-bedrock-samples
2. https://github.com/awslabs/amazon-bedrock-agentcore-samples
3. https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-code-deploy-python.html
4. https://github.com/aws-samples/aws-glue-samples
5. https://github.com/aws-samples/data-mesh-datazone-cdk-cloudformation
6. https://aws.amazon.com/startups/prompt-library/full-aws-deployment-agent
7. https://aws-samples.github.io/sample-autonomous-cloud-coding-agents/customizing/prompt-engineering/
8. https://kiro.dev/docs/cli/steering/
9. https://github.com/awsdataarchitect/kiro-best-practices
10. https://www.roborhythms.com/fix-agent-tool-hallucinations-4-section-prompt/
11. https://github.com/aws-samples/aws-cdk-project-structure-python
12. https://docs.aws.amazon.com/bedrock/latest/userguide/kb-multimodal-troubleshooting.html
13. https://github.com/awslabs/agent-plugins
14. https://github.com/microsoft/ai-agents-for-beginners (Jupyter Notebook SKILL.md)
15. https://docs.astral.sh/ruff/linter/ (ruff .ipynb support)
