#!/usr/bin/env python3
# Task Scheduler - simple orchestrator that runs agents sequentially
import subprocess, time, json, os
cfg = 'config/agent_config.json'
if os.path.exists(cfg):
    with open(cfg) as f:
        conf = json.load(f)
else:
    conf = {}
agents = conf.get('agents', {})
# run recon -> vuln -> collector if enabled
if agents.get('recon', {}).get('enabled', True):
    print('[Scheduler] Running recon_agent')
    subprocess.call(['python', 'agents/recon_agent.py'])
time.sleep(0.5)
if agents.get('vuln', {}).get('enabled', True):
    print('[Scheduler] Running vuln_agent')
    # locate latest recon report if exists
    reports = sorted([p for p in os.listdir('reports') if p.startswith('recon_')])
    input_file = None
    if reports:
        input_file = os.path.join('reports', reports[-1])
    cmd = ['python', 'agents/vuln_agent.py']
    if input_file:
        cmd += ['--input', input_file]
    subprocess.call(cmd)
time.sleep(0.5)
if agents.get('collector', {}).get('enabled', True):
    print('[Scheduler] Running data_collector')
    subprocess.call(['python', 'agents/data_collector.py'])
print('[Scheduler] Finished scheduled run.')
