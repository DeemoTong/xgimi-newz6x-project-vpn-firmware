**English** | [简体中文](README.zh-CN.md)

# XGIMI NEW Z6X VPN Firmware (Experimental)

A community experiment for **XGIMI NEW Z6X / XH25L**, based on the official **V12.15.180** firmware package. It adds Android 8.0/API 26 AOSP `VpnDialogs` to `/system/priv-app`, providing the system VPN authorization and management dialogs expected by Android VPN apps. The project owner reported that a VPN connection succeeded on one NEW Z6X/XH25L after installation.

This is not an official XGIMI firmware and does not include a VPN client, account, or service. Confirm the device code is **XH25L**. Other Z6X variants and XGIMI models have not been tested.

## Firmware details

- Base package: official XGIMI `V12.15.180`
- Android: 8.0.0 / API 26
- Target: NEW Z6X, device code `XH25L` / `ironman`
- Reassembled filename: `XGIMI_IRONMAN_XH25L_V12.15.180_VPN-EXPERIMENTAL-CRC-FIXED.bin`
- SHA-256: `7da2d9d03eb0514b4385968b720aecd84351a27d0616504cd377aea13b388750`
- Test report: one owner-tested XH25L connected using a VPN app; other devices and VPN apps are unverified

The package build property is `v12.15.180`. During testing, the projector UI was also observed to display `V12.15.213`; do not infer that every partition updated from the displayed version alone. Verify the VPN authorization flow and connection.

## What it changes

Some VPN apps report that the device lacks VPN firmware or system VPN support. This build adds Android's `VpnDialogs` system app, which handles `VpnService` authorization and connection-management dialogs. Users must install and configure a VPN app separately.

## Download and join

Open [Releases](https://github.com/DeemoTong/xgimi-newz6x-project-vpn-firmware/releases/latest) and download both firmware parts and `SHA256SUMS.txt`. After both parts finish downloading, join and verify them with Python 3:

```powershell
python tools/join_release_parts.py `
  xgimi-newz6x-vpn-v12.15.180.part01.bin `
  xgimi-newz6x-vpn-v12.15.180.part02.bin `
  XGIMI_IRONMAN_XH25L_V12.15.180_VPN-EXPERIMENTAL-CRC-FIXED.bin
```

Download the script from this repository into the same folder if needed. Do not flash the result unless the script confirms the expected size and SHA-256.

## Installation

> **Installing this package wipes user data.** Back up apps, accounts, and personal files first. Keep the projector powered throughout the update; do not remove the USB drive or interrupt power.

1. Confirm the model is NEW Z6X / XH25L and back up anything you need.
2. Join and verify the two release parts.
3. Rename the joined file to exactly **`XGIMI_IRONMAN_XH25L.bin`**.
4. Put it in the USB drive's root directory. Use the same USB update entry that recognized the official XH25L firmware on this device.
5. Wait for the projector to reboot. Reinstall and configure your VPN app, then test the connection.

If the update screen does not detect the package, check the exact filename, USB root location, and join verification. Do not try firmware for another model.

## Restore stock firmware

Download the XH25L-compatible official firmware from [XGIMI's NEW Z6X page](https://shop.xgimi.com/host_list/91?name=NEW%20Z6X), then use the projector's USB update entry to restore it. Restoring firmware may also wipe user data.

## Source and build notes

`src/VpnDialogs` contains AOSP `frameworks/base/packages/VpnDialogs` source from Android `android-8.0.0_r1`, retaining its Apache 2.0 notices. Integration notes are in `patches/`; `tools/` contains release part joining/splitting and XGIMI CRC verification utilities.

This repository does not contain the complete XGIMI system source, proprietary vendor binaries, signing private keys, or the official base firmware. The release is a built firmware image; the repository source alone cannot rebuild all XGIMI firmware partitions from scratch.

## Risks and disclaimer

This is unofficial experimental firmware. It may fail to install, prevent boot, or affect warranty coverage. Use only with the specified model and keep the official package for recovery. Flash at your own risk. XGIMI marks and third-party components remain the property of their respective owners. This project is not affiliated with XGIMI.

