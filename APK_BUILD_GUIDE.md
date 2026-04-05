# Android APK 构建指南

本项目支持使用 Clash 代理加速下载 Android SDK 组件，然后构建 APK 文件。

## 目录

1. [快速开始](#快速开始)
2. [安装 Clash 代理](#安装-clash-代理)
3. [安装 Android SDK 组件](#安装-android-sdk-组件)
4. [构建 APK](#构建-apk)

---

## 快速开始

```bash
# 1. 安装并启动 Clash 代理
./clash-proxy.sh install
./clash-proxy.sh start

# 2. 设置环境变量
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
export ANDROID_HOME=/opt/android-sdk
export ANDROID_SDK_ROOT=/opt/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 3. 安装 SDK 组件
sdkmanager "platforms;android-34" "build-tools;34.0.0"

# 4. 构建 APK
./build-apk-local.sh
```

---

## 安装 Clash 代理

### 自动安装（推荐）

```bash
# 安装 Clash Meta
./clash-proxy.sh install

# 启动代理服务
./clash-proxy.sh start

# 查看状态
./clash-proxy.sh status
```

### 手动安装

```bash
# 1. 下载 Clash Meta
mkdir -p /opt/clash
cd /opt/clash
curl -sL "https://github.com/MetaCubeX/mihomo/releases/download/v1.19.0/mihomo-linux-amd64-compatible-v1.19.0.gz" -o mihomo.gz
gunzip mihomo.gz
chmod +x mihomo

# 2. 创建配置文件
mkdir -p /root/.config/clash
# 将配置文件写入 /root/.config/clash/config.yaml

# 3. 启动
nohup /opt/clash/mihomo -d /root/.config/clash > /var/log/clash.log 2>&1 &
```

### 代理配置

- **HTTP 代理**: `http://127.0.0.1:7890`
- **HTTPS 代理**: `http://127.0.0.1:7890`
- **SOCKS5 代理**: `socks5://127.0.0.1:7890`

### 常用命令

```bash
./clash-proxy.sh start    # 启动
./clash-proxy.sh stop     # 停止
./clash-proxy.sh restart  # 重启
./clash-proxy.sh status   # 状态
```

---

## 安装 Android SDK 组件

### 设置环境

```bash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
export ANDROID_HOME=/opt/android-sdk
export ANDROID_SDK_ROOT=/opt/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
```

### 安装 SDK 组件

```bash
# 安装 Android 34 平台和构建工具
sdkmanager "platforms;android-34" "build-tools;34.0.0"

# 安装 cmdline-tools（如果未安装）
sdkmanager "cmdline-tools;latest"

# 查看已安装的组件
sdkmanager --list_installed

# 查看可用组件
sdkmanager --list
```

---

## 构建 APK

### 使用构建脚本（推荐）

```bash
# 使用代理构建
./build-apk-local.sh --proxy

# 不使用代理构建
./build-apk-local.sh

# 使用指定代理
./build-apk-local.sh --proxy 127.0.0.1:7890
```

### 手动构建

```bash
cd frontend/android

# 设置环境变量
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
export GRADLE_OPTS="-Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=7890 -Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=7890"

# 构建 Debug APK
./gradlew assembleDebug

# 构建 Release APK
./gradlew assembleRelease

# 清理构建
./gradlew clean
```

### APK 输出位置

- **Debug**: `frontend/android/app/build/outputs/apk/debug/app-debug.apk`
- **Release**: `frontend/android/app/build/outputs/apk/release/app-release.apk`

---

## 故障排查

### Clash 无法启动

```bash
# 检查日志
tail -50 /var/log/clash.log

# 检查端口占用
netstat -tlnp | grep 7890
netstat -tlnp | grep 9091
```

### 代理不可用

```bash
# 测试代理
curl -x 127.0.0.1:7890 https://www.google.com

# 查看可用节点
curl -s http://127.0.0.1:9091/proxies/Proxy | python3 -m json.tool
```

### SDK 下载失败

```bash
# 确认代理正常工作
curl -x 127.0.0.1:7890 https://dl.google.com/android/repository/repository2-1.xml -o /dev/null

# 检查 Android SDK 路径
echo $ANDROID_HOME
echo $ANDROID_SDK_ROOT
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `clash-proxy.sh` | Clash 代理管理脚本 |
| `build-apk-local.sh` | APK 本地构建脚本 |
| `/root/.config/clash/config.yaml` | Clash 配置文件 |
| `/opt/clash/mihomo` | Clash Meta 核心 |
| `/opt/android-sdk` | Android SDK 安装目录 |

---

## 注意事项

1. Clash 订阅链接已配置在 `clash-proxy.sh` 中，如有需要可以修改
2. 首次启动 Clash 时需要下载订阅节点，可能需要等待几分钟
3. 构建 APK 需要至少 4GB 内存和 10GB 磁盘空间
4. 建议使用 Java 17 或更高版本
