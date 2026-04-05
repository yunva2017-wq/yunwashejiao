# Release APK 签名完成

## ✅ 签名状态

| 项目 | 状态 |
|------|------|
| **签名验证** | ✅ 通过 |
| **v2 签名** | ✅ 已验证 |
| **v3 签名** | ✅ 已验证 |
| **签名者数量** | 1 |

---

## 📦 已签名文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `app-release.apk` | 3.5 MB | ✅ 已签名的 Release APK |
| `yunwa-release-key.jks` | 2.7 KB | 🔐 密钥库文件 |

---

## 🔐 签名信息

| 项目 | 值 |
|------|-----|
| **密钥库** | yunwa-release-key.jks |
| **密钥别名** | yunwa |
| **密钥算法** | RSA 2048 位 |
| **有效期** | 10000 天（约 27 年） |
| **证书指纹** | SHA384withRSA |

---

## 📋 安装测试

```bash
# 安装已签名的 APK
adb install app-release.apk

# 卸载
adb uninstall com.yunwa.chat
```

---

## 🔧 签名其他 APK

使用签名脚本：

```bash
# 基本用法
./sign-apk.sh app-release-unsigned.apk

# 指定输出文件名
./sign-apk.sh app-release-unsigned.apk my-app.apk
```

手动签名：

```bash
# 使用 apksigner
/opt/android-sdk/build-tools/35.0.0/apksigner sign \
  --ks yunwa-release-key.jks \
  --ks-key-alias yunwa \
  --ks-pass pass:yunwa123456 \
  --key-pass pass:yunwa123456 \
  --out app-release.apk \
  app-release-unsigned.apk

# 验证签名
/opt/android-sdk/build-tools/35.0.0/apksigner verify --verbose app-release.apk
```

---

## ⚠️ 安全提示

### 密钥库密码

当前使用的密码是 **`yunwa123456`**（测试用）。

**生产环境建议**：
1. 使用强密码（至少 12 位，包含大小写字母、数字、特殊字符）
2. 将密码存储在安全的地方（密码管理器）
3. 不要将密钥库提交到版本控制

### 备份密钥库

```bash
# 备份到安全位置
cp yunwa-release-key.jks /path/to/secure/backup/

# 创建多个备份
cp yunwa-release-key.jks yunwa-release-key.jks.backup
```

**重要**: 如果丢失密钥库，将无法更新已发布的应用！

---

## 📝 查看证书信息

```bash
# 查看密钥库详情
keytool -list -v -keystore yunwa-release-key.jks -storepass yunwa123456

# 查看证书指纹
keytool -list -v -keystore yunwa-release-key.jks -storepass yunwa123456 | grep SHA
```

---

## 🔄 自动化签名构建

### 方法 1: 配置 gradle.properties

在 `frontend/android/gradle.properties` 中添加：

```properties
YUNWA_RELEASE=true
YUNWA_STORE_FILE=../yunwa-release-key.jks
YUNWA_STORE_PASSWORD=yunwa123456
YUNWA_KEY_ALIAS=yunwa
YUNWA_KEY_PASSWORD=yunwa123456
```

然后直接运行：
```bash
./gradlew assembleRelease
```

### 方法 2: 使用环境变量

```bash
export YUNWA_STORE_PASSWORD=yunwa123456
export YUNWA_KEY_PASSWORD=yunwa123456
./gradlew assembleRelease
```

---

## 📄 相关文件

| 文件 | 用途 |
|------|------|
| `app-release.apk` | 已签名的 Release APK |
| `app-release-unsigned.apk` | 未签名的 Release APK |
| `yunwa-release-key.jks` | 密钥库 |
| `sign-apk.sh` | 自动签名脚本 |

---

**签名时间**: 2026-04-03  
**有效期**: 至 2053-08-15
