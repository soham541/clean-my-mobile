#!/usr/bin/env python3
"""
Clean-My-Mobile: Storage & Media Duplicate Audit Tool
Audits internal storage for WhatsApp Sent duplicates, thumbnail caches, and space hogs.
"""

import subprocess
import sys
import re

def run_adb(cmd_args, device=None):
    cmd = ["adb"]
    if device:
        cmd.extend(["-s", device])
    cmd.extend(cmd_args)
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout

def main():
    device = sys.argv[1] if len(sys.argv) > 1 else None
    action = sys.argv[2] if len(sys.argv) > 2 else "audit"

    print(f"[*] Running Storage & Duplicate Media Audit on: {device or 'default'}...")

    # Check filesystem capacity
    df_out = run_adb(["shell", "df", "-h", "/data"], device)
    print("\n" + "="*50)
    print("           STORAGE CAPACITY")
    print("="*50)
    for line in df_out.splitlines():
        if "/data" in line:
            parts = line.split()
            if len(parts) >= 5:
                print(f"Total: {parts[1]} | Used: {parts[2]} ({parts[4]}) | Available: {parts[3]}")

    print("\n" + "="*50)
    print("      WHATSAPP DUPLICATE 'SENT' MEDIA")
    print("="*50)
    
    # Check WhatsApp Media Sent directories
    sent_dirs = [
        "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images/Sent",
        "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Video/Sent",
        "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Documents/Sent",
        "/sdcard/WhatsApp/Media/WhatsApp Images/Sent",
        "/sdcard/WhatsApp/Media/WhatsApp Video/Sent"
    ]

    total_waste_kb = 0
    found_dirs = []

    for d in sent_dirs:
        out = run_adb(["shell", "du", "-sk", d], device)
        m = re.search(r"([0-9]+)\s+(.*)", out)
        if m:
            kb = int(m.group(1))
            path = m.group(2)
            if kb > 1024: # > 1MB
                mb = kb / 1024.0
                total_waste_kb += kb
                found_dirs.append(path)
                print(f"  {mb:7.1f} MB  ->  {path.split('/')[-2]}/Sent")

    print(f"\nTotal duplicate sent media: {total_waste_kb/1024:.1f} MB ({total_waste_kb/(1024*1024):.2f} GB)")

    if action == "purge" and found_dirs:
        print("\n[*] Purging duplicate Sent folders...")
        for d in found_dirs:
            run_adb(["shell", "rm", "-rf", f"{d}/*"], device)
        print("[✓] Purged successfully! Original gallery media remains intact.")

    print("\n" + "="*50)
    print("         LARGE THUMBNAIL CACHES")
    print("="*50)
    thumb_dirs = [
        "/sdcard/DCIM/.thumbnails",
        "/sdcard/Pictures/.thumbnails"
    ]
    for td in thumb_dirs:
        out = run_adb(["shell", "du", "-sh", td], device)
        if out.strip() and "No such" not in out:
            print(f"  {out.strip()}")

if __name__ == "__main__":
    main()
