# ❄️ Rootless 1-Tap App Freezing Guide (Shizuku + Hail)

How to freeze heavy apps (MyJio, JioCloud, Instagram, Threads, Shopping apps) with 1 tap right from your phone's notification shade or home screen without needing a PC or Root.

---

## The Problem
Many essential daily apps (telecom apps, social networks, shopping apps) run aggressive background notification pollers, analytics SDKs, and location listeners that drain **1.5 GB+ of RAM** and waste battery even when closed.

Standard uninstallation is inconvenient because you lose your login sessions and cart data.

---

## The Solution
Android's built-in `pm disable` or `am force-stop` instantly halts an app's processes and background services while keeping all accounts, logins, and data 100% intact. 

By pairing **Shizuku** (which grants ADB privilege on-device) with **Hail** (an open-source app freezer), you can trigger this in 1 tap.

---

## Step 1: Install & Start Shizuku

1. Install **[Shizuku](https://play.google.com/store/apps/details?id=moe.shizuku.privileged.api)** from Google Play Store.
2. Ensure **Wireless Debugging** is turned ON in *Developer Options*.
3. Open Shizuku:
   * **If connected to PC via ADB:** Run the starter command:
     ```bash
     adb shell /data/app/*moe.shizuku.privileged.api*/lib/arm64/libshizuku.so
     ```
   * **If without PC:** Tap **"Pairing"** in Shizuku > enter the 6-digit Wi-Fi pairing code > tap **"Start"**.

---

## Step 2: Install & Configure Hail

1. Download and install **[Hail](https://github.com/aistra0528/Hail/releases)** (Free & Open Source).
2. Open Hail and tap **Allow all the time** when prompted for Shizuku access.
3. Tap **Settings (Gear icon)** > **Working Mode** > Select **Shizuku (Disable)** or **Shizuku (Hide)**.
4. On the main screen, tap the **"+"** button and select the heavy apps you want to control:
   * **Telecom:** `MyJio`, `JioCloud`
   * **Social:** `Instagram`, `Threads`, `Basel`, `Reddit`, `Facebook Lite`
   * **Shopping / Food:** `Meesho`, `Amazon`, `Flipkart`, `Zomato`, `Swiggy`, `Blinkit`
   * **Utilities:** `Truecaller`

---

## Step 3: Add the 1-Tap Control Center Tile

1. Pull down your phone's notification shade twice.
2. Tap the **Pencil (Edit)** icon.
3. Scroll down through available quick settings tiles until you see **Hail**.
4. Drag the **Hail** tile into your active Control Center tiles.

*(Optional: Long-press your home screen > Widgets > Drag Hail's "Freeze all" widget to your desktop).*

---

## How to Use It Daily:
* When you need to use an app, tap its icon to open it normally.
* When you are finished, pull down your Control Center and tap the **Hail** tile.
* **Result:** All dormant apps are instantly frozen, clearing **over 1.2 GB of RAM** and halting battery drain until your next intentional use.
