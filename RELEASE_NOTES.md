# XGIMI NEW Z6X / XH25L VPN firmware — V12.15.180-vpn.1

Unofficial experimental firmware based on the official XGIMI V12.15.180 package. It adds Android 8.0/API 26 AOSP `VpnDialogs` to the XH25L system image so compatible VPN apps can request and manage Android VPN access. The project owner reported a successful connection with 穿梭 on one NEW Z6X / XH25L. Other units and VPN apps are unverified.

## Download

Download both `.bin` parts and `SHA256SUMS.txt`, then run the Python 3 join script from the source repository:

```powershell
python tools/join_release_parts.py `
  xgimi-newz6x-vpn-v12.15.180.part01.bin `
  xgimi-newz6x-vpn-v12.15.180.part02.bin `
  XGIMI_IRONMAN_XH25L_V12.15.180_VPN-EXPERIMENTAL-CRC-FIXED.bin
```

The merged firmware is 2,672,910,368 bytes. Its SHA-256 is:

```text
7da2d9d03eb0514b4385968b720aecd84351a27d0616504cd377aea13b388750
```

The join script checks the exact size and full-file SHA-256. Do not install if it reports an error.

## Installation warning

**Installing this firmware wipes user data.** Use only on XGIMI NEW Z6X with device code XH25L / `ironman`. Rename the verified merged file to exactly `XGIMI_IRONMAN_XH25L.bin`, place it in the USB drive root, then use the USB update procedure that recognizes official XH25L packages. Keep the projector powered during installation. Other Z6X variants are not verified. See `README.md` for recovery and details.

This is not an official XGIMI release, includes no VPN client or service, and may fail to install or boot. The package's build property is V12.15.180; during the test the projector UI also displayed V12.15.213, so verify the VPN authorization and connection after installation.
