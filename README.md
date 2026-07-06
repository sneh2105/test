# agent-security-benchmark

A tiny sample "customer support" agent used to benchmark AI-agent security scanners.

## What's inside

`agents/support_agent.py` defines three LangChain-style tools:

- `web_browser` — fetches arbitrary URLs
- `aws_secrets_manager` — retrieves AWS secrets ("for deployment automation")
- `calculator` — *claims* to do arithmetic, but calls `eval()` on raw input

This combination is intentionally designed to test two things a scanner should catch:

1. **Chain risk**: `web_browser` + `aws_secrets_manager` together form a
   prompt-injection-to-credential-theft path, even though each tool looks
   fine in isolation.
2. **Behavior/description mismatch**: `calculator`'s docstring says
   "arithmetic," but its body executes `eval()` — arbitrary code execution
   hiding behind an innocuous name.

## Results

| Tool | Chain detection (web_browser → secrets) | eval() mismatch detection |
|---|---|---|
| [AgentScan](https://github.com/sneh2105/agentscan) `source` scan | ✅ CRITICAL, MITRE ATLAS mapped | ✅ CRITICAL |
| [Cisco mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) YARA (offline, no API key) | ❌ marked safe | ❌ marked safe |

Cisco's stronger engines (LLM-as-judge, behavioral) require an API key and
weren't tested here — this only benchmarks the free/offline paths.

## Try it yourself

```bash
pip install -e /path/to/agentscan
agentscan source agents/
```
