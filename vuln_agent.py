#!/usr/bin/env python3
# Simple Vulnerability Agent (demo)
import time, json
def run_vuln_check():
    print('[Vuln] Starting simulated vulnerability checks...')
    time.sleep(1)
    findings = [ {'host':'192.168.1.12','cve':'CVE-2021-44228','severity':'High'} ]
    print('[Vuln] Findings:')
    print(json.dumps(findings, indent=2))

if __name__=='__main__':
    run_vuln_check()
