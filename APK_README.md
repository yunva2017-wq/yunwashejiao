# Yunwa Chat - Android APK

## 下载

| 版本 | 文件 | 大小 | 说明 |
|------|------|------|------|
| **Debug** | `app-debug.apk` | 4.4 MB | 已签名，可直接安装 |
| **Release** | `app-release-unsigned.apk` | ~4 MB | 未签名，需要签名后安装 |

## 快速安装

### Debug 版本（推荐测试用）
```bash
adb install app-debug.apk
```

### Release 版本（需要签名）

Release APK 未签名，需要使用以下方法之一签名：

#### 方法 1: 使用 apksigner
```bash
# 生成签名密钥
keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-alias

# 签名 APK
apksigner sign --ks my-release-key.jks --ks-key-alias my-alias app-release-unsigned.apk

# 验证签名
apksigner verify app-release-unsigned.apk
```

#### 方法 2: 使用 jarsigner
```bash
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.jks app-release-unsigned.apk my-alias
```

## 系统要求

- **Android 版本**: Android 7.0 (API 24) 或更高版本
- **架构**: arm64-v8a, armeabi-v7a, x86, x86_64

## 功能

- 实时聊天
- 消息推送
- 文件上传
- 多语言支持

## 构建说明

### 本地构建

```bash
# 一键构建（自动启动代理）
./build.sh debug      # Debug 版本
./build.sh release    # Release 版本

# 或使用详细脚本
./build-apk-local.sh --proxy
```

### GitHub Actions

推送到 main 分支会自动触发构建，APK 会作为 Artifact 上传。

## 项目结构

```
/usr/local/claude/
├── app-debug.apk              # Debug APK（已签名）
├── app-release-unsigned.apk   # Release APK（未签名）
├── build.sh                   # 一键构建脚本
├── build-apk-local.sh         # 详细构建脚本
├── clash-proxy.sh             # Clash 代理管理
├── APK_BUILD_GUIDE.md         # 构建指南
├── APK_BUILD_REPORT.md        # 构建报告
└── frontend/android/          # Android 项目
```

## 常见问题

### Q: Debug APK 无法安装？
A: 确保允许安装未知来源应用。

### Q: Release APK 如何签名？
A: 使用 apksigner 或 jarsigner 签名后安装。

### Q: 构建失败？
A: 检查 Clash 代理是否运行：`./clash-proxy.sh status`

## 联系

如有问题，请提交 Issue 或联系开发团队。
