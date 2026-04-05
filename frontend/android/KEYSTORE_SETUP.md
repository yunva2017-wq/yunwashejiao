# 签名配置示例

## 生成 Release 签名密钥

```bash
# 进入 Android 项目目录
cd frontend/android

# 生成密钥库
keytool -genkey -v \
  -keystore yunwa-release-key.jks \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias yunwa-chat \
  -dname "CN=Yunwa Chat, OU=Development, O=Yunwa, L=Beijing, S=Beijing, C=CN"
```

## 配置 keystore.properties

创建 `keystore.properties` 文件：

```properties
storePassword=你的密钥库密码
keyPassword=你的密钥密码
keyAlias=yunwa-chat
storeFile=../yunwa-release-key.jks
```

**注意**: 请将 `keystore.properties` 添加到 `.gitignore`，不要提交到版本控制！

## 配置 build.gradle

在 `app/build.gradle` 的 `android` 块中添加：

```gradle
signingConfigs {
    release {
        if (project.hasProperty('YUNWA_RELEASE')) {
            storeFile file(YUNWA_STORE_FILE)
            storePassword YUNWA_STORE_PASSWORD
            keyAlias YUNWA_KEY_ALIAS
            keyPassword YUNWA_KEY_PASSWORD
        }
    }
}

buildTypes {
    release {
        signingConfig signingConfigs.release
        minifyEnabled true
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
}
```

## 自动化签名构建

在 `gradle.properties` 中添加：

```properties
YUNWA_RELEASE=true
YUNWA_STORE_FILE=../yunwa-release-key.jks
YUNWA_STORE_PASSWORD=你的密钥库密码
YUNWA_KEY_ALIAS=yunwa-chat
YUNWA_KEY_PASSWORD=你的密钥密码
```

## 使用命令行签名

```bash
# 方法 1: 使用 gradle.properties 配置
./gradlew assembleRelease

# 方法 2: 命令行参数
./gradlew assembleRelease \
  -PYUNWA_RELEASE=true \
  -PYUNWA_STORE_FILE=../yunwa-release-key.jks \
  -PYUNWA_STORE_PASSWORD=密码 \
  -PYUNWA_KEY_ALIAS=yunwa-chat \
  -PYUNWA_KEY_PASSWORD=密码
```

## 验证签名

```bash
# 使用 apksigner 验证
apksigner verify --verbose app/build/outputs/apk/release/app-release.apk

# 使用 jarsigner 验证
jarsigner -verify -verbose -certs app/build/outputs/apk/release/app-release.apk
```

## 安全提示

1. **备份密钥库**: 将 `yunwa-release-key.jks` 备份到安全位置
2. **不要提交密码**: 使用环境变量或本地配置文件
3. **使用环境变量**（推荐）:
   ```bash
   export YUNWA_STORE_PASSWORD=$(pass mobile/yunwa-keystore)
   export YUNWA_KEY_PASSWORD=$(pass mobile/yunwa-keystore)
   ```
