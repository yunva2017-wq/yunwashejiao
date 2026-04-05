# Yunwa Chat - 项目索引

## 📱 Android APK 构建

### 快速构建

```bash
# 一键构建（推荐）
./build.sh

# 构建 Debug 版本
./build.sh debug

# 构建 Release 版本
./build.sh release
```

### APK 文件

| 文件 | 大小 | 状态 |
|------|------|------|
| `app-debug.apk` | 4.4 MB | ✅ 可直接安装 |
| `app-release-unsigned.apk` | 3.5 MB | ⚠️ 需签名 |

---

## 📚 文档索引

### 新手必读

1. [构建完成.md](构建完成.md) - 本次构建总结
2. [APK_README.md](APK_README.md) - APK 使用说明
3. [README.md](README.md) - 项目主文档

### 构建相关

4. [TOOLS.md](TOOLS.md) - 工具脚本使用指南
5. [APK_BUILD_GUIDE.md](APK_BUILD_GUIDE.md) - 详细构建指南
6. [APK_BUILD_REPORT.md](APK_BUILD_REPORT.md) - 构建报告
7. [frontend/android/KEYSTORE_SETUP.md](frontend/android/KEYSTORE_SETUP.md) - 签名配置

### 其他

8. [GITHUB_ACTIONS.md](GITHUB_ACTIONS.md) - GitHub Actions CI/CD
9. [README_本地构建.md](README_本地构建.md) - 本地构建说明（旧版）

---

## 🛠️ 工具脚本

| 脚本 | 用途 |
|------|------|
| `./build.sh` | 一键构建 APK（自动启动代理） |
| `./build-apk-local.sh` | 详细构建脚本 |
| `./clash-proxy.sh` | Clash 代理管理 |
| `./clean-build.sh` | 清理构建缓存 |
| `./start-frontend.sh` | 启动前端 |
| `./start-backend.sh` | 启动后端 |

---

## 🔧 常用命令

### 构建 APK

```bash
# 快速构建
./build.sh

# 查看代理状态
./clash-proxy.sh status

# 清理缓存
./clean-build.sh
```

### 运行应用

```bash
# 启动后端
./start-backend.sh

# 启动前端
./start-frontend.sh
```

### 安装 APK

```bash
# 通过 ADB 安装
adb install app-debug.apk

# 卸载
adb uninstall com.yunwa.chat
```

---

## 📁 目录结构

```
/usr/local/claude/
├── 📱 Android 构建
│   ├── app-debug.apk                  # Debug APK
│   ├── app-release-unsigned.apk       # Release APK（未签名）
│   ├── build.sh                       # 一键构建脚本
│   ├── build-apk-local.sh             # 详细构建脚本
│   ├── clean-build.sh                 # 清理脚本
│   └── clash-proxy.sh                 # Clash 代理脚本
│
├── 📚 文档
│   ├── 构建完成.md                    # 本次构建总结
│   ├── APK_README.md                  # APK 说明
│   ├── APK_BUILD_GUIDE.md             # 构建指南
│   ├── APK_BUILD_REPORT.md            # 构建报告
│   ├── TOOLS.md                       # 工具脚本指南
│   ├── KEYSTORE_SETUP.md              # 签名配置（frontend/android/）
│   ├── README.md                      # 项目主文档
│   ├── GITHUB_ACTIONS.md              # GitHub Actions
│   └── README_本地构建.md             # 本地构建说明
│
├── 🔧 启动脚本
│   ├── start-frontend.sh              # 启动前端
│   └── start-backend.sh               # 启动后端
│
└── 📂 项目目录
    ├── frontend/                      # 前端项目
    └── backend/                       # 后端项目
```

---

## ⚡ 快速参考

### 代理配置
- **HTTP 代理**: `http://127.0.0.1:7890`
- **SOCKS5**: `socks5://127.0.0.1:7890`

### Android SDK
- **路径**: `/opt/android-sdk`
- **版本**: 34, 35, 36
- **Build Tools**: 34.0.0, 35.0.0

### Java
- **版本**: OpenJDK 21
- **路径**: `/usr/lib/jvm/java-21-openjdk`

---

**最后更新**: 2026-04-03  
**项目**: Yunwa Chat
