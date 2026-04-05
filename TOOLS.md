# 云娃聊天 - Android 构建工具集

## 📁 脚本列表

| 脚本 | 用途 | 用法 |
|------|------|------|
| `build.sh` | 一键构建 APK | `./build.sh [debug\|release]` |
| `build-apk-local.sh` | 详细构建脚本 | `./build-apk-local.sh --proxy` |
| `clean-build.sh` | 清理构建缓存 | `./clean-build.sh` |
| `clash-proxy.sh` | Clash 代理管理 | `./clash-proxy.sh [start\|stop\|status]` |

## 🚀 快速开始

### 首次使用

```bash
# 1. 安装并启动 Clash 代理
./clash-proxy.sh install
./clash-proxy.sh start

# 2. 构建 Debug APK
./build.sh
```

### 日常构建

```bash
# Debug 版本（已签名，可直接安装）
./build.sh debug

# Release 版本（需签名）
./build.sh release

# 查看代理状态
./clash-proxy.sh status
```

## 📋 详细说明

### build.sh - 一键构建

自动启动 Clash 代理并构建 APK。

```bash
# 构建 Debug 版本（默认）
./build.sh

# 构建 Release 版本
./build.sh release

# 显示帮助
./build.sh --help
```

### clash-proxy.sh - Clash 代理管理

管理 Clash Meta 代理服务。

```bash
# 安装 Clash（首次使用）
./clash-proxy.sh install

# 启动代理
./clash-proxy.sh start

# 停止代理
./clash-proxy.sh stop

# 重启代理
./clash-proxy.sh restart

# 查看状态
./clash-proxy.sh status

# 查看帮助
./clash-proxy.sh --help
```

**代理信息:**
- HTTP 代理：`http://127.0.0.1:7890`
- SOCKS5 代理：`socks5://127.0.0.1:7890`
- API 端口：`9091`

### build-apk-local.sh - 详细构建脚本

提供更多选项的构建脚本。

```bash
# 不使用代理
./build-apk-local.sh

# 使用默认代理 (127.0.0.1:7890)
./build-apk-local.sh --proxy

# 使用指定代理
./build-apk-local.sh --proxy 127.0.0.1:7890

# 显示帮助
./build-apk-local.sh --help
```

### clean-build.sh - 清理构建缓存

清理 Gradle 和 Android 构建缓存。

```bash
./clean-build.sh
```

## 📦 APK 输出位置

| 版本 | 路径 |
|------|------|
| Debug | `frontend/android/app/build/outputs/apk/debug/app-debug.apk` |
| Release | `frontend/android/app/build/outputs/apk/release/app-release.apk` |

## 🔧 环境要求

- **Java**: JDK 17 或更高（推荐 JDK 21）
- **Android SDK**: 34、35、36
- **内存**: 至少 4GB 可用内存
- **磁盘**: 至少 10GB 可用空间

## 🛠️ 故障排查

### Clash 无法启动

```bash
# 检查端口占用
netstat -tlnp | grep 7890
netstat -tlnp | grep 9091

# 查看日志
tail -50 /var/log/clash.log

# 重启 Clash
./clash-proxy.sh restart
```

### 构建失败

```bash
# 1. 检查代理状态
./clash-proxy.sh status

# 2. 测试代理
curl -x 127.0.0.1:7890 https://www.google.com

# 3. 清理缓存后重试
./clean-build.sh
./build.sh
```

### SDK 组件缺失

```bash
# 设置环境变量
export ANDROID_HOME=/opt/android-sdk
export ANDROID_SDK_ROOT=/opt/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# 安装缺失的组件
sdkmanager "platforms;android-36" "build-tools;35.0.0"
```

## 📚 相关文档

- [APK_README.md](APK_README.md) - APK 说明
- [APK_BUILD_GUIDE.md](APK_BUILD_GUIDE.md) - 构建指南
- [APK_BUILD_REPORT.md](APK_BUILD_REPORT.md) - 构建报告
- [构建完成.md](构建完成.md) - 本次构建总结
- [frontend/android/KEYSTORE_SETUP.md](frontend/android/KEYSTORE_SETUP.md) - 签名配置

## 🌐 代理订阅

当前使用的订阅链接已配置在 `clash-proxy.sh` 中。

如需更新订阅，编辑脚本中的 `SUB_URL` 变量：

```bash
SUB_URL="你的新订阅链接"
```

然后重启 Clash：

```bash
./clash-proxy.sh restart
```

---

**最后更新**: 2026-04-03  
**维护**: Yunwa 开发团队
