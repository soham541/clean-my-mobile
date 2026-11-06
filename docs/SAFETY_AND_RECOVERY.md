# 🛡️ Safety & Recovery Protocol

How Clean-My-Mobile guarantees 100% device safety with zero brick risk.

---

## 1. Why Clean-My-Mobile Cannot Brick Your Device

1. **User-Space Isolation (`pm disable-user --user 0`):**
   * Traditional "root debloating" removes APK files from `/system` or `/vendor`. If a required dependency is removed, the phone goes into a bootloop.
   * Clean-My-Mobile strictly disables packages in **user space (`--user 0`)**. The original factory APKs remain completely untouched in the read-only system partitions.
   * If any package ever causes an unexpected behavior, it can be re-enabled instantly with a single ADB command.

2. **Automated Revert Script Generation:**
   * Every time `clean.sh` or an automated debloat action runs, it writes an exact restoration command for every single modified package into `restore.sh`.
   * Reverting all changes is as simple as running:
     ```bash
     ./restore.sh <device_ip_or_serial>
     ```

3. **Critical Protected Packages (Whitelisted):**
   * Clean-My-Mobile strictly blacklists critical system services from ever being disabled:
     * Telephony & SMS (`com.android.phone`, `telephony-common`)
     * Display Compositor (`surfaceflinger`, `bootanimation`)
     * System UI (`com.android.systemui`)
     * Core Input / Keyboard (`com.google.android.inputmethod.latin`)
     * Emergency Services (`com.android.emergency`, `com.oplus.sos`)
     * Android Auto (`com.google.android.projection.gearhead`)

---

## 2. Emergency Recovery Instructions

If you ever experience an issue or want to return to complete factory default:

### Method A: Run the Restore Script
Connect your phone via ADB and run:
```bash
./restore.sh
```

### Method B: Manual ADB Restore
To restore any individual package:
```bash
# If disabled via pm disable-user:
adb shell pm enable <package.name>

# If uninstalled for user 0:
adb shell cmd package install-existing <package.name>
```

### Method C: Factory Reset (Fail-Safe)
Because all system APKs remain completely untouched in Android's system image, a standard factory reset via your phone's Settings menu will restore 100% of the original factory state with zero trace of modifications.
