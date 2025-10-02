#!/usr/bin/env python3
# Recon Agent - light-weight TCP connect scanner for authorized testing
import socket, ipaddress, json, time, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_host_port(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def scan_host(host, ports, timeout):
    open_ports = []
    for p in ports:
        if scan_host_port(host, p, timeout):
            open_ports.append(p)
    return open_ports

def run_scan(network, ports=[22,80,443], timeout=1.0, concurrency=50):
    net = ipaddress.ip_network(network, strict=False)
    results = []
    hosts = [str(ip) for ip in net.hosts()]
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        future_to_host = {ex.submit(scan_host, h, ports, timeout): h for h in hosts}
        for fut in as_completed(future_to_host):
            h = future_to_host[fut]
            try:
                open_ports = fut.result()
                if open_ports:
                    results.append({'host': h, 'open_ports': open_ports})
            except Exception as e:
                pass
    ts = int(time.time())
    out = {'scan_time': ts, 'network': network, 'results': results}
    with open(f'reports/recon_{ts}.json','w') as f:
        json.dump(out, f, indent=2)
    print(f'[Recon] Scan complete. {len(results)} hosts with open ports. Report saved to reports/recon_{ts}.json')
    return out

if __name__=='__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--network', default='192.168.1.0/24')
    p.add_argument('--ports', nargs='*', type=int, default=[22,80,443,3389,445])
    p.add_argument('--timeout', type=float, default=1.0)
    p.add_argument('--concurrency', type=int, default=50)
    args = p.parse_args()
    run_scan(args.network, args.ports, args.timeout, args.concurrency)
