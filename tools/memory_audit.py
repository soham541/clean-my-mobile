#!/usr/bin/env python3
"""
Clean-My-Mobile: Memory Audit Tool
Parses `adb shell dumpsys meminfo` and ranks actual physical RAM consumers (PSS).
"""

import subprocess
import sys
import re

def get_meminfo(device=None):
    cmd = ["adb"]
    if device:
        cmd.extend(["-s", device])
    cmd.extend(["shell", "dumpsys", "meminfo"])
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout
    except Exception as e:
        print(f"Error running adb: {e}", file=sys.stderr)
        sys.exit(1)

def parse_meminfo(output):
    procs = {}
    in_pss = False
    total_ram = 0
    free_ram = 0
    used_ram = 0
    zram = (0, 0)

    for line in output.splitlines():
        if "Total RAM:" in line:
            m = re.search(r"Total RAM:\s+([0-9,]+)K", line)
            if m: total_ram = int(m.group(1).replace(",", "")) / 1024
        if "Free RAM:" in line:
            m = re.search(r"Free RAM:\s+([0-9,]+)K", line)
            if m: free_ram = int(m.group(1).replace(",", "")) / 1024
        if "Used RAM:" in line:
            m = re.search(r"Used RAM:\s+([0-9,]+)K", line)
            if m: used_ram = int(m.group(1).replace(",", "")) / 1024
        if "ZRAM:" in line:
            m = re.search(r"ZRAM:\s+([0-9,]+)K physical used for ([0-9,]+)K in swap", line)
            if m:
                zram = (int(m.group(1).replace(",", "")) / 1024, int(m.group(2).replace(",", "")) / 1024)

        if "Total PSS by process:" in line:
            in_pss = True
            continue
        if in_pss:
            if "Total PSS by category:" in line or "Total RSS by process:" in line:
                in_pss = False
                continue
            m = re.search(r"([0-9,]+)K:\s+([a-zA-Z0-9_\.:]+)\s+\(pid\s+[0-9]+", line)
            if m:
                kb = int(m.group(1).replace(",", ""))
                proc = m.group(2)
                pkg = proc.split(":")[0]
                procs[pkg] = procs.get(pkg, 0) + kb

    return {
        "total_ram": total_ram,
        "free_ram": free_ram,
        "used_ram": used_ram,
        "zram": zram,
        "procs": sorted(procs.items(), key=lambda x: x[1], reverse=True)
    }

def main():
    device = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"[*] Auditing RAM on device: {device or 'default'}...")
    raw = get_meminfo(device)
    data = parse_meminfo(raw)

    print("\n" + "="*50)
    print("           MEMORY AUDIT SUMMARY")
    print("="*50)
    print(f"Total Physical RAM: {data['total_ram']:.1f} MB")
    print(f"Used RAM:           {data['used_ram']:.1f} MB ({(data['used_ram']/data['total_ram'])*100:.1f}%)")
    print(f"Available/Free RAM: {data['free_ram']:.1f} MB")
    if data['zram'][0] > 0:
        print(f"ZRAM Swap:          {data['zram'][0]:.1f} MB used ({data['zram'][1]:.1f} MB compressed)")
    print("-" * 50)
    print("TOP MEMORY CONSUMERS (PSS > 20 MB):")
    print("-" * 50)
    for pkg, kb in data["procs"]:
        mb = kb / 1024
        if mb >= 20.0:
            print(f"  {mb:7.1f} MB  ->  {pkg}")

if __name__ == "__main__":
    main()
