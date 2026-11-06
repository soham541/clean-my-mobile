# ⚡ Zero-RAM Modernization Guide

How to modernize and enhance your Android experience without running heavy background services or sacrificing your hard-earned RAM gains.

---

## 1. System-Wide Ad-Blocking (0 MB RAM, 0% Extra Battery)

Instead of running heavy VPN-based adblockers (like AdGuard app, Blokada) that keep a persistent 80–120 MB process in RAM:

### How to Enable:
1. Open **Settings > Connection & sharing > Private DNS** (or *Network & Internet > Private DNS*).
2. Select **Designated private DNS** (or *Private DNS provider hostname*).
3. Enter:
   ```
   dns.adguard-dns.com
   ```
4. Tap **Save**.

### Why It Uses 0 MB RAM:
Private DNS is processed natively at Android's Linux kernel network socket layer (DNS over TLS / DoT). It uses **zero additional RAM and zero extra CPU cycles**, while blocking mobile ads and tracking SDKs system-wide.

---

## 2. Material You Themed Icons via Native Launcher (0 MB RAM)

Third-party launchers (like Nova, Smart Launcher) take 100–180 MB of persistent RAM. Your phone's stock launcher (OnePlus Launcher, Samsung One UI Home, Pixel Launcher) already supports dynamic icons with zero overhead.

### How to Enable:
1. Install an open-source static icon pack like **[Lawnicons](https://github.com/LawnchairLauncher/lawnicons)**.
2. Go to: **Settings > Personalizations > Icons** (or long-press your home screen > **Icons**).
3. Select **Lawnicons** and apply.

### Why It Uses 0 MB RAM:
The stock launcher loads the static SVG vector icons directly from storage into its existing cache. The icon pack app never runs in the background.

---

## 3. AMOLED True-Black Wallpapers (0 MB RAM + Major Battery Savings)

On AMOLED displays, true-black pixels (`#000000`) physically turn off completely (0 mA current draw).

* **Avoid:** Live wallpapers, 3D parallax wallpapers, video backgrounds (run continuous OpenGL threads, 60–100 MB RAM).
* **Use:** Static AMOLED wallpapers from curated sources like [r/Amoledbackgrounds](https://www.reddit.com/r/Amoledbackgrounds/) or **Wallman** (F-Droid).
* **Result:** 0 MB background CPU/RAM overhead, and saves ~15–25% display battery.

---

## 4. Hardware Dolby Atmos Audio Tuning (0 MB RAM)

Most smartphones with dual stereo speakers have hardware Dolby Atmos audio profiles set to a flat default profile:

* Open: **Settings > Sound & vibration > Dolby Atmos**.
* Switch from *Smart/Auto* to:
  * **Movie:** Maximizes the stereo soundstage and gives punchier bass.
  * **Music:** Enhances vocal clarity and detailed instrument separation.
* Processed directly by the Qualcomm/MediaTek DSP audio hardware chip—**zero CPU/RAM cost**.

---

## 5. Turn Off Redundant 24/7 Radio Scanning

Android by default keeps Wi-Fi and Bluetooth beacon scanners active 24/7 for Google Location accuracy, even when your Wi-Fi and Bluetooth toggles are off:

* Go to: **Settings > Location > Wi-Fi and Bluetooth scanning**.
* Turn **OFF** both *Wi-Fi scanning* and *Bluetooth scanning*.
* GPS navigation and normal Wi-Fi/Bluetooth connections remain 100% functional, saving ~8–12% battery per day.
