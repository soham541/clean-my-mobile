#!/usr/bin/env python3
"""
Clean-My-Mobile: Battery & Wakelock Audit Tool
Parses `adb shell dumpsys batterystats` to find power hogs and sleep-blocking wakelocks.
"""

import subprocess
import sys
import re

def run_adb(cmd_args, device=None):
    cmd = ["adb"]
    if device:
        cmd.extend(["-s", device])
    cmd.extend(cmd_args)
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return res.stdout

def get_package_map(device=None):
    # Map appIds to package names
    out = run_adb(["shell", "pm", "list", "packages", "-U"], device)
    pkg_map = {}
    for line in out.splitlines():
        # package:com.example uid:10123
        m = re.search(r"package:([^\s]+)\s+uid:([0-9]+)", line)
        if m:
            pkg = m.group(1)
            uid = int(m.group(2))
            pkg_map[uid] = pkg
    return pkg_map

def main():
    device = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"[*] Running Battery & Wakelock Audit on: {device or 'default'}...")
    
    # Check battery state
    batt_info = run_adb(["shell", "dumpsys", "battery"], device)
    level = re.search(r"level:\s+([0-9]+)", batt_info)
    temp = re.search(r"temperature:\s+([0-9]+)", batt_info)
    health = re.search(r"health:\s+([0-9]+)", batt_info)

    print("\n" + "="*50)
    print("           BATTERY HARDWARE STATUS")
    print("="*50)
    if level: print(f"Battery Level:  {level.group(1)}%")
    if temp:  print(f"Temperature:    {int(temp.group(1))/10.0:.1f} °C")
    if health:
        h_str = "Good" if health.group(1) == "2" else f"Code {health.group(1)}"
        print(f"Battery Health: {h_str}")

    # Parse batterystats
    pkg_map = get_package_map(device)
    stats = run_adb(["shell", "dumpsys", "batterystats"], device)

    print("\n" + "="*50)
    print("           TOP POWER CONSUMERS (mAh)")
    print("="*50)
    
    in_estimated = False
    drain_count = 0
    for line in stats.splitlines():
        if "Estimated power use (mAh):" in line:
            in_estimated = True
            continue
        if in_estimated:
            if not line.strip() or line.startswith("  All kernel") or line.startswith("  All partial"):
                break
            m = re.search(r"UID\s+(?:u0a([0-9]+)|([0-9]+)):\s+([0-9\.]+)\s+(.*)", line)
            if m:
                uid_num = int(m.group(1)) + 10000 if m.group(1) else int(m.group(2))
                mah = float(m.group(3))
                details = m.group(4)
                pkg_name = pkg_map.get(uid_num, f"UID {uid_num}")
                if mah >= 2.0 and drain_count < 15:
                    print(f"  {mah:6.1f} mAh : {pkg_name:32} {details[:40]}")
                    drain_count += 1

    print("\n" + "="*50)
    print("        TOP PARTIAL WAKELOCKS (Sleep Blockers)")
    print("="*50)
    in_wakelocks = False
    wl_count = 0
    for line in stats.splitlines():
        if "All partial wake locks:" in line:
            in_wakelocks = True
            continue
        if in_wakelocks:
            if not line.strip() or line.startswith("  All kernel") or line.startswith("  WiFi "):
                break
            m = re.search(r"Wake lock (?:u0a([0-9]+)|([0-9]+))\s+([^\s:]+):\s+([0-9a-z\s]+)", line)
            if m and wl_count < 10:
                uid_num = int(m.group(1)) + 10000 if m.group(1) else int(m.group(2))
                lock_name = m.group(3)
                duration = m.group(4)
                pkg_name = pkg_map.get(uid_num, f"UID {uid_num}")
                print(f"  [{duration:15}] {pkg_name:25} -> {lock_name}")
                wl_count += 1

if __name__ == "__main__":
    main()
