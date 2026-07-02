"""Run airline evaluation with thinking mode enabled."""
import sys
sys.argv = [
    "tau2", "run",
    "--domain", "airline",
    "--agent-llm", "openai/qwen3.5-397b-a17b",
    "--agent-llm-args", '{"temperature": 1.0, "top_p": 0.95, "extra_body": {"enable_thinking": true}}',
    "--user-llm", "openai/qwen3.7-max-2026-06-08",
    "--user-llm-args", '{"temperature": 0.0}',
    "--num-trials", "1",
]

from tau2.cli import main
main()
