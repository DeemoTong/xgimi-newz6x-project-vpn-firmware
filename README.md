# XGIMI NEW Z6X VPN 固件（实验版）

这是面向 **XGIMI NEW Z6X / XH25L** 的社区实验固件项目，基于官方 **V12.15.180** 固件包。它将 Android 8.0/API 26 的 AOSP `VpnDialogs` 系统组件加入 `/system/priv-app`，为 Android VPN 应用提供系统 VPN 授权与管理对话框。项目所有者在一台 NEW Z6X/XH25L 上安装后，报告穿梭 VPN 已能连接。

本项目不是 XGIMI 官方固件，也没有加入 VPN 客户端、账号或线路。安装前请确认投影仪型号代码是 **XH25L**。其他 Z6X 变体、Z6、Z6X、Z6X Pro、其他 XGIMI 机型均未验证。

## 固件信息

- 固件包基础版本：XGIMI 官方 `V12.15.180`
- Android：8.0.0 / API 26
- 目标机型：NEW Z6X，设备代码 `XH25L` / `ironman`
- 文件名（合并后）：`XGIMI_IRONMAN_XH25L_V12.15.180_VPN-EXPERIMENTAL-CRC-FIXED.bin`
- SHA-256：`7da2d9d03eb0514b4385968b720aecd84351a27d0616504cd377aea13b388750`
- 测试范围：项目所有者报告一台 XH25L 实机的 VPN 连接成功；其他设备及 VPN 软件尚未验证

包内 Android build property 是 `v12.15.180`。测试过程中，设备界面曾显示 `V12.15.213`；若版本显示与文件名不一致，请不要据此推断所有分区都已更新，实际以 VPN 授权及连接测试为准。

## 解决的问题

部分 VPN 应用启动时会提示设备缺少 VPN 固件或系统不支持 VPN。此版本补入 Android 的 `VpnDialogs` 系统应用，处理 `VpnService` 的授权确认和连接管理界面。VPN 应用仍需由用户单独安装并配置。

## 下载与合并

前往 [Releases](https://github.com/DeemoTong/xgimi-newz6x-project-vpn-firmware/releases/latest)，下载两个固件分卷和 `SHA256SUMS.txt`。两个分卷都下载完成后，用 Python 3 合并并校验：

```powershell
python tools/join_release_parts.py `
  xgimi-newz6x-vpn-v12.15.180.part01.bin `
  xgimi-newz6x-vpn-v12.15.180.part02.bin `
  XGIMI_IRONMAN_XH25L_V12.15.180_VPN-EXPERIMENTAL-CRC-FIXED.bin
```

也可将脚本从仓库下载到分卷所在目录后运行。脚本会核对合并后文件大小和 SHA-256；校验失败时不要刷机。

## 安装

> **安装包会清除设备用户数据。** 请先备份应用、账号和个人文件。安装期间保持供电，不要拔掉 U 盘或断电。

1. 确认设备为 NEW Z6X / XH25L，并备份需要保留的数据。
2. 合并并校验两个 Release 分卷。
3. 将合并后的文件重命名为 **`XGIMI_IRONMAN_XH25L.bin`**。
4. 将文件放到 U 盘根目录。使用此前能让该设备识别官方 XH25L 固件的 USB 升级入口完成升级。
5. 等待设备自动重启后，重新安装 VPN 应用并配置线路，测试连接。

如果升级界面未识别安装包，先确认文件名完全一致、文件位于 U 盘根目录且合并校验通过。不要用其他型号固件试刷。

## 恢复官方固件

如需恢复，可从 [XGIMI NEW Z6X 官方固件页面](https://shop.xgimi.com/host_list/91?name=NEW%20Z6X)获取适用于 XH25L 的官方固件，再使用设备的 USB 升级入口刷回。升级可能再次清除用户数据。

## 源码与构建说明

`src/VpnDialogs` 是 AOSP `frameworks/base/packages/VpnDialogs`（Android 8.0.0_r1）的源码，保留了原始 Apache 2.0 版权说明。固件集成方式记录在 `patches/`；`tools/` 提供分卷合并、切分及 XGIMI CRC 校验工具。

仓库不包含 XGIMI 的完整系统源码、厂商二进制、签名私钥或官方基础固件。这个 Release 提供的是已构建固件；仅凭仓库源码不能从零重建 XGIMI 的全部固件镜像。

## 风险与免责声明

这是非官方实验固件，可能导致设备无法启动、升级失败或失去保修。请只在对应机型上使用，并保留官方固件以便恢复。使用者自行承担刷机风险。XGIMI 名称和固件中的第三方组件归各自权利人所有；本项目不代表 XGIMI。

