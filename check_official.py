"""Check official leaderboard config vs our run."""
import json

# Load official result
with open(r'd:\qoderws\tau2-bench\data\tau2\results\final\gpt-4.1-2025-04-14_retail_default_gpt-4.1-2025-04-14_4trials.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

info = d['info']
print("=== Official Retail Config (gpt-4.1) ===")
print(f"Agent: {info['agent_info']['implementation']} -> {info['agent_info']['llm']}")
print(f"Agent args: {info['agent_info'].get('llm_args')}")
print(f"User:  {info['user_info']['implementation']} -> {info['user_info']['llm']}")
print(f"User args: {info['user_info'].get('llm_args')}")
print(f"Trials: {info['num_trials']}")
print(f"Max Steps: {info['max_steps']}")
print(f"Seed: {info['seed']}")
print(f"Environment: {info['environment_info']['domain_name']}")

# Compute pass rate
sims = d['simulations']
rewards = [s['reward_info']['reward'] for s in sims if s.get('reward_info')]
print(f"\nTotal sims: {len(sims)}")
print(f"Avg Reward: {sum(rewards)/len(rewards):.4f}")
passes = sum(1 for r in rewards if r >= 1.0)
print(f"Pass^1 (all trials): {passes}/{len(rewards)} = {passes/len(rewards):.3f}")

# Per-task pass (at least 1 trial passes)
from collections import defaultdict
task_results = defaultdict(list)
for s in sims:
    if s.get('reward_info'):
        task_results[s['task_id']].append(s['reward_info']['reward'])

task_pass = sum(1 for rewards_list in task_results.values() if any(r >= 1.0 for r in rewards_list))
print(f"Tasks with at least 1 pass: {task_pass}/{len(task_results)}")
