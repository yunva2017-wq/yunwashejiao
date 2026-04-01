# 云娃聊天应用 - Android APK 本地构建指南

## 快速开始

### 方法 A: 使用 Android Studio（最简单）

1. **安装 Android Studio**
   - 下载地址：https://developer.android.com/studio
   - 按照默认选项安装

2. **打开项目**
   - 启动 Android Studio
   - File → Open → 选择 `frontend/android` 目录
   - 点击 "OK"

3. **构建 APK**
   - 等待 Gradle 同步完成
   - Build → Build Bundle(s)/APK(s) → Build APK(s)
   - 等待构建完成

4. **获取 APK**
   - 构建完成后点击 "locate"
   - 或在 `app/build/outputs/apk/debug/` 目录找到 `app-debug.apk`

---

### 方法 B: 使用命令行

**环境要求：**
- Java JDK 17
- Android SDK (含 platform-tools, build-tools)
- Gradle 8.x

**构建步骤：**

```bash
# 1. 进入 Android 项目目录
cd frontend/android

# 2. 首次构建需要设置 SDK 路径
# 编辑 local.properties 文件，添加：
# sdk.dir=/path/to/your/android/sdk

# Windows 示例:
# sdk.dir=C:\\Users\\YourName\\AppData\\Local\\Android\\Sdk

# macOS 示例:
# sdk.dir=/Users/YourName/Library/Android/sdk

# Linux 示例:
# sdk.dir=/home/YourName/Android/Sdk

# 3. 构建 APK
./gradlew assembleDebug

# 4. APK 输出位置
# app/build/outputs/apk/debug/app-debug.apk
```

---

## 安装到手机

1. **启用未知来源**
   - 设置 → 安全 → 未知来源（允许）

2. **传输 APK**
   - 通过 USB、微信、QQ 等方式传输 `app-debug.apk` 到手机

3. **安装**
   - 点击 APK 文件安装

4. **配置服务器**
   - 打开应用
   - 配置后端服务器地址（如：http://你的电脑IP:8000）

---

## 常见问题

### Q: Gradle 同步失败
A: 检查网络连接，或尝试使用国内镜像。

### Q: 构建时提示 SDK 未找到
A: 在 Android Studio 中：Tools → SDK Manager → 安装 Android SDK Platform 34 和 Build-Tools 34.0.0

### Q: 应用无法连接服务器
A:
- 确保手机和电脑在同一局域网
- 使用电脑 IP 地址而非 localhost
- 确保后端服务正在运行

---

## 文件结构

```
yunwa-chat-android.zip
├── frontend/android/          # Android 项目（用 Android Studio 打开此目录）
├── frontend/dist/             # 已构建的前端静态文件
├── frontend/package.json      # 前端依赖配置
└── README_本地构建.md         # 本文件
```

---

## 技术支持

如遇到问题，请检查：
1. Android Studio 版本（建议最新）
2. Java 版本（JDK 17）
3. 网络连接状态
