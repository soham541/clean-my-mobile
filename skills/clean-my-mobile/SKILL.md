---
name: clean-my-mobile
description: Complete diagnostic, debloat, RAM optimization, battery audit, and rootless modernization framework for Android smartphones via wireless or USB ADB. Safely categorizes bloatware into verified groups (OEM telemetry, optional features, heavy 3rd-party apps) with 100% reversible backups and zero brick risk.
---

# Clean-My-Mobile: Autonomous Android Optimizer Skill

Use this skill whenever a user wants to clean, debloat, speed up, save battery, or reclaim RAM on their Android smartphone via ADB (wireless debugging or USB).

---

## 🛡️ Core Rules & Safety Protocol (MANDATORY)

1. **Verify Before Action:** NEVER disable, freeze, or remove any app without showing the user the exact package list and asking for explicit confirmation.
2. **100% Reversible Guarantee:**
   - Always use `pm disable-user --user 0 <package>` or `pm uninstall -k --user 0 <package>`.
   - Never wipe system partitions or permanently delete APKs.
   - Automatically record every modified package in a local `restore.sh` script before making changes.
3. **Preserve Mission-Critical Functions:**
   - Sparing Android Auto (`com.google.android.projection.gearhead`) unless the user explicitly requests its removal.
   - NEVER touch telephony (`com.android.phone`), display rendering (`surfaceflinger`), emergency SOS, or base keyboard/input methods.
4. **Zero-Fluff Transparency:**
   - Do not overwhelm the user with raw terminal log dumps.
   - Synthesize actions into clear, readable tables.
   - State the current phase, progress, and immediate next step clearly.

---

## 🚀 Execution Workflow

### Phase 1: Device Connection & Fingerprinting

1. Check connection:
   ```bash
   adb devices
   adb shell getprop ro.product.manufacturer
   adb shell getprop ro.product.model
   adb shell getprop ro.build.version.release
   ```
2. If wireless debugging failed:
   - Check if port changed (Android 11+ assigns random ephemeral ports 30000-50000).
   - If unpaired, instruct the user to open "Pair device with pairing code" and execute `adb pair <ip>:<port> <code>`.
3. Load the matching OEM config file from `configs/`:
   - `oneplus_oppo_realme.json` (ColorOS / OxygenOS / RealmeUI)
   - `samsung.json` (One UI)
   - `xiaomi.json` (MIUI / HyperOS)
   - `universal_heavy_apps.json` (Third-party apps)

---

### Phase 2: Comprehensive Diagnostics

Before changing anything, run three diagnostics:

#### 1. RAM Audit (Physical PSS Consumption)
Run `tools/memory_audit.py` or:
```bash
adb shell dumpsys meminfo
```
Extract:
- Total Physical RAM vs Used RAM vs Available RAM (`MemAvailable` in `/proc/meminfo`).
- ZRAM swap consumption.
- Top memory consumers ranked by PSS (> 20 MB).

#### 2. Battery & Wakelock Audit
Run `tools/battery_audit.py` or:
```bash
adb shell dumpsys batterystats
adb shell dumpsys battery
```
Identify:
- Top mAh power consumers.
- Top partial wakelocks (e.g., continuous background WorkManager loops, media indexers).
- Proximity/gyro sensor wakes from Always-On Display.

#### 3. Radio & Network Audit
Check background scanning:
```bash
adb shell settings get global wifi_scan_always_enabled
adb shell settings get global ble_scan_always_enabled
```
Check for redundant modem services (e.g. 5G polling daemons on 4G LTE devices).

---

### Phase 3: Category-Wise Verification Menu

Present the findings in three clear categories for the user to approve:

#### Group 1: OEM Telemetry & Push Ad Trackers (Highly Recommended)
*Completely safe with zero functional loss.*
- ColorOS/OxygenOS: `com.heytap.mcs` (saves ~250MB RAM), `deepthinker`, `statistics.rom`, `crashbox`, `sau`, `romupdate`, `logkit`.
- One UI: `com.sec.android.diagmonagent`, `com.samsung.android.rubin.app`, `com.facebook.services`.
- HyperOS/MIUI: `com.miui.msa.global`, `com.miui.analytics`, `joyose`, `daemon`.

#### Group 2: OEM Optional Features (Caveats Explained)
*Disable only if user doesn't use the feature.*
- OnePlus Shelf (`com.oneplus.opshelf`), Work-Life Balance (`com.oneplus.opwlb`), Theme Store, Games hub.
- Samsung Bixby suite, Samsung Kids, Galaxy Store.
- Universal: Print Spooler (`com.android.printspooler`), Google Lens, Weather background sync.

#### Group 3: Third-Party Heavy Background Apps
- Target apps: `MyJio`, `JioCloud`, `Instagram`, `Threads`, `Basel`, `Reddit`, `Meesho`, `Amazon`, `Flipkart`, `Zomato`, `Swiggy`, `Truecaller`.
- Offer **1-Tap Freezing** via Shizuku + Hail instead of permanent uninstallation so user accounts, logins, and carts remain intact.

---

### Phase 4: Rootless 1-Tap Control (Shizuku + Hail)

To allow the user to freeze heavy apps right from their phone without a PC:
1. Check if Shizuku is installed: `adb shell pm list packages | grep shizuku`.
2. Start Shizuku server via ADB:
   ```bash
   adb shell /data/app/*moe.shizuku.privileged.api*/lib/arm64/libshizuku.so
   ```
3. Install **Hail** APK (fetch from official GitHub releases: `aistra0528/Hail`).
4. Guide user:
   - Working Mode: **Shizuku**.
   - Check the heavy apps to freeze.
   - Add the **Hail Quick Settings Tile** to the Control Center or place the **1-Tap Freeze Widget** on the home screen.

---

### Phase 5: Zero-RAM Modernization Suite

Offer lightweight upgrades that consume **0 MB background RAM**:

1. **System-Wide Ad-Blocking (0 MB RAM):**
   - Guide user to: **Settings > Connection & sharing > Private DNS > `dns.adguard-dns.com`**.
   - Blocks in-app ads and telemetry without running a VPN or app.
2. **Material You Themed Icons (0 MB RAM):**
   - Install **Lawnicons** APK directly via ADB.
   - Apply via native launcher settings: **Settings > Personalizations > Icons > Lawnicons**.
3. **Live Alerts / Dynamic Island (~40 MB RAM):**
   - Direct user to **dynamicSpot** on Google Play Store via intent:
     `adb shell am start -a android.intent.action.VIEW -d "market://details?id=com.jamworks.dynamicspot"`
4. **Camera Tuning (GCam):**
   - Configure Snapdragon profile (Interface: Pixel 4/5, Model: Pixel 4 XL / IMX586, Motion: OFF, Aux: OFF) to eliminate crashes.

---

### Phase 6: Memory Reality Check & Wrap-Up

When users ask *"Why does my phone still show ~4 GB used?"*:
- Explain the Linux philosophy: *"Unused RAM is Wasted RAM"*.
- Detail the non-negotiable core OS foundation: GPU VRAM (~350MB), Kernel drivers (~650MB), `system_server` + `SurfaceFlinger` + `SystemUI` (~1.2GB), GMS & Phone (~450MB).
- Highlight `MemAvailable` (the real free memory headroom).
- **RAM Expansion Warning:** Strongly advise keeping RAM Expansion / Virtual RAM **OFF** (prevents flash storage thrashing, micro-stutters, and heat).
- Instruct user to turn **OFF Wireless Debugging** once finished for security.
