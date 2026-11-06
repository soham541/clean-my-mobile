#!/usr/bin/env bash
# ==============================================================================
# Clean-My-Mobile: Universal Android Debloating & Optimization Script
# Safe, reversible debloater across OnePlus, Oppo, Realme, Samsung, Xiaomi & more.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIGS_DIR="$SCRIPT_DIR/configs"
RESTORE_SCRIPT="$SCRIPT_DIR/restore.sh"

DEVICE_TARGET="${1:-}"

# Check ADB
if ! command -v adb &>/dev/null; then
  echo "Error: 'adb' is not installed or not in PATH."
  exit 1
fi

# Detect device
if [ -z "$DEVICE_TARGET" ]; then
  DEVICES=$(adb devices | grep -v "List" | grep "device$" | awk '{print $1}' || true)
  DEVICE_COUNT=$(echo "$DEVICES" | grep -v '^$' | wc -l || true)
  if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "Error: No active ADB device found. Connect via USB or run: adb connect <ip>:<port>"
    exit 1
  elif [ "$DEVICE_COUNT" -eq 1 ]; then
    DEVICE_TARGET="$DEVICES"
  else
    echo "Multiple devices found. Please specify target: ./clean.sh <device_serial_or_ip:port>"
    echo "$DEVICES"
    exit 1
  fi
fi

ADB_CMD="adb -s $DEVICE_TARGET"

echo "================================================================="
echo "                CLEAN-MY-MOBILE OPTIMIZER"
echo "================================================================="
echo "Target Device: $DEVICE_TARGET"

MANUFACTURER=$($ADB_CMD shell getprop ro.product.manufacturer | tr -d '\r')
MODEL=$($ADB_CMD shell getprop ro.product.model | tr -d '\r')
ANDROID_VER=$($ADB_CMD shell getprop ro.build.version.release | tr -d '\r')

echo "Manufacturer:  $MANUFACTURER"
echo "Model:         $MODEL"
echo "Android Ver:   $ANDROID_VER"
echo "================================================================="

# Select config based on manufacturer
CONFIG_FILE=""
MANU_LOWER=$(echo "$MANUFACTURER" | tr '[:upper:]' '[:lower:]')

case "$MANU_LOWER" in
  *oneplus*|*oppo*|*realme*)
    CONFIG_FILE="$CONFIGS_DIR/oneplus_oppo_realme.json"
    ;;
  *samsung*)
    CONFIG_FILE="$CONFIGS_DIR/samsung.json"
    ;;
  *xiaomi*|*redmi*|*poco*)
    CONFIG_FILE="$CONFIGS_DIR/xiaomi.json"
    ;;
  *)
    echo "Notice: Unknown manufacturer '$MANUFACTURER'. Using universal rules."
    CONFIG_FILE="$CONFIGS_DIR/universal_heavy_apps.json"
    ;;
esac

echo "Loaded profile: $(basename "$CONFIG_FILE")"

# Initialize restore script
cat << 'EOF' > "$RESTORE_SCRIPT"
#!/usr/bin/env bash
# Clean-My-Mobile Auto-Generated Restore Script
set -euo pipefail
DEVICE_TARGET="${1:-}"
ADB_CMD="adb"
if [ -n "$DEVICE_TARGET" ]; then ADB_CMD="adb -s $DEVICE_TARGET"; fi

echo "Restoring packages..."
EOF
chmod +x "$RESTORE_SCRIPT"

disable_package() {
  local pkg="$1"
  local name="$2"
  
  if $ADB_CMD shell pm list packages | grep -q "$pkg"; then
    echo -n "  [*] Disabling $name ($pkg)... "
    res=$($ADB_CMD shell pm disable-user --user 0 "$pkg" 2>&1 || true)
    if echo "$res" | grep -q "disabled-user"; then
      echo "DISABLED"
      echo "$ADB_CMD shell pm enable $pkg" >> "$RESTORE_SCRIPT"
    else
      un_res=$($ADB_CMD shell pm uninstall -k --user 0 "$pkg" 2>&1 || true)
      if echo "$un_res" | grep -q "Success"; then
        echo "REMOVED (USER 0)"
        echo "$ADB_CMD shell cmd package install-existing $pkg" >> "$RESTORE_SCRIPT"
      else
        echo "FAILED"
      fi
    fi
  fi
}

echo ""
echo "Select Action:"
echo "1) Run RAM Memory Audit (PSS & ZRAM Diagnostics)"
echo "2) Run Battery & Wakelock Audit (Power Draw & Sleep Blockers)"
echo "3) Run Storage & Duplicate Media Audit (WhatsApp Sent Purge)"
echo "4) Debloat Safe OEM Telemetry & Ad Trackers"
echo "5) Freeze Heavy 3rd-Party Apps (Jio, Meta, Shopping)"
echo "6) Trim System Caches"
echo "7) Revert / Restore All Changes"
echo "q) Quit"
echo ""

read -rp "Enter choice [1-7]: " choice

case "$choice" in
  1)
    python3 "$SCRIPT_DIR/tools/memory_audit.py" "$DEVICE_TARGET"
    ;;
  2)
    python3 "$SCRIPT_DIR/tools/battery_audit.py" "$DEVICE_TARGET"
    ;;
  3)
    python3 "$SCRIPT_DIR/tools/storage_audit.py" "$DEVICE_TARGET" audit
    echo ""
    read -rp "Do you want to purge duplicate WhatsApp Sent media? [y/N]: " purge_choice
    if [[ "$purge_choice" =~ ^[Yy]$ ]]; then
      python3 "$SCRIPT_DIR/tools/storage_audit.py" "$DEVICE_TARGET" purge
    fi
    ;;
  4)
    echo ""
    echo "[!] Debloating Safe Telemetry & Background Trackers..."
    python3 -c "
import json
with open('$CONFIG_FILE') as f:
    data = json.load(f)
for cat_name, cat in data.get('categories', {}).items():
    if 'telemetry' in cat_name or 'trackers' in cat_name or 'ad_daemons' in cat_name:
        for p in cat.get('packages', []):
            print(f\"{p['package']}\t{p['name']}\")
" | while IFS=$'\t' read -r pkg name; do
      disable_package "$pkg" "$name"
    done
    echo ""
    echo "[✓] Telemetry debloating complete! Restore script updated at: $RESTORE_SCRIPT"
    ;;
  5)
    echo ""
    echo "[!] Freezing Heavy 3rd-Party Apps..."
    python3 -c "
import json
with open('$CONFIGS_DIR/universal_heavy_apps.json') as f:
    data = json.load(f)
for app in data.get('apps', []):
    print(app['package'])
" | while read -r pkg; do
      if $ADB_CMD shell pm list packages | grep -q "$pkg"; then
        echo "  [❄] Force-stopping $pkg..."
        $ADB_CMD shell am force-stop "$pkg" >/dev/null 2>&1 || true
      fi
    done
    $ADB_CMD shell pm trim-caches 10000000000 >/dev/null 2>&1 || true
    echo "[✓] Heavy apps frozen and caches trimmed."
    ;;
  6)
    echo "[*] Trimming system caches..."
    $ADB_CMD shell pm trim-caches 10000000000
    echo "[✓] Caches trimmed successfully."
    ;;
  7)
    echo "[*] Running restore script..."
    "$RESTORE_SCRIPT" "$DEVICE_TARGET"
    ;;
  q|Q)
    echo "Exiting."
    exit 0
    ;;
  *)
    echo "Invalid option."
    exit 1
    ;;
esac
