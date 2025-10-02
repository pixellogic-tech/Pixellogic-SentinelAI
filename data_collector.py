#!/usr/bin/env python3
# Data Collector Agent - gathers metadata and basic artifacts for authorized targets
import os, json, platform, socket, time

def collect_local_metadata(outpath='reports/collector_local.json'):
    meta = {
        'hostname': socket.gethostname(),
        'platform': platform.platform(),
        'time': int(time.time())
    }
    with open(outpath,'w') as f:
        json.dump(meta, f, indent=2)
    print('[Collector] Local metadata saved to', outpath)
    return outpath

if __name__=='__main__':
    collect_local_metadata()
