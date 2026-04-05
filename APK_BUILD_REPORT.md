# Yunwa Chat - Android APK 构建报告

## 构建信息

| 项目 | 详情 |
|------|------|
| **应用名称** | Yunwa Chat |
| **包名** | com.yunwa.chat |
| **构建类型** | Debug |
| **Android 版本** | SDK 36 |
| **最小 SDK** | 24 (Android 7.0) |
| **构建时间** | 2026-04-03 |
| **APK 大小** | 4.4 MB |

## 构建配置

### 代理设置
- **HTTP/HTTPS 代理**: `http://127.0.0.1:7890`
- **Clash 状态**: 运行中

### SDK 环境
- **Java**: OpenJDK 21
- **Android SDK**: /opt/android-sdk
- **已安装组件**:
  - Android SDK Platform 36
  - Android SDK Platform 34
  - Android SDK Build-Tools 35.0.0
  - Android SDK Build-Tools 34.0.0

## 构建输出

```
APK 文件：/usr/local/claude/app-debug.apk
完整路径：/usr/local/claude/frontend/android/app/build/outputs/apk/debug/app-debug.apk
```

## 构建说明

### 使用代理构建（推荐）
```bash
./build-apk-local.sh --proxy
```

### 手动构建
```bash
cd frontend/android
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
./gradlew assembleDebug
```

## 依赖版本

| 库 | 版本 |
|----|------|
| androidx.activity:activity | 1.11.0 |
| androidx.appcompat:appcompat | 1.7.1 |
| androidx.core:core-ktx | 1.17.0 |
| androidx.core:core-splashscreen | 1.2.0 |
| androidx.coordinatorlayout:coordinatorlayout | 1.3.0 |

## 注意事项

1. Debug APK 仅用于测试，不包含签名
2. 生产环境请使用 `assembleRelease` 构建
3. 需要至少 Android 7.0 (API 24) 或更高版本

## 构建日志

```
BUILD SUCCESSFUL in 2m 43s
97 actionable tasks: 97 executed
```
