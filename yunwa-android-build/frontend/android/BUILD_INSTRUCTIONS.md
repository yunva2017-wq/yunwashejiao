# Android APK 构建说明

## GitHub Actions 自动构建

### 使用方法

1. **将代码推送到 GitHub**
   ```bash
   git init
   git remote add origin <你的 GitHub 仓库地址>
   git add .
   git commit -m "Initial commit - 云娃聊天应用"
   git push -u origin main
   ```

2. **等待构建完成**
   - 推送到 main/master 分支会自动触发构建
   - 在 GitHub 仓库的 **Actions** 标签页查看进度

3. **下载 APK**
   - 构建完成后，进入对应的 Workflow 运行
   - 在页面底部的 **Artifacts** 区域下载 `yunwa-chat-apk.zip`
   - 解压后得到 `app-debug.apk`

### 手动触发构建

1. 进入 GitHub 仓库的 **Actions** 标签页
2. 点击左侧的 **Build Android APK**
3. 点击 **Run workflow** 按钮
4. 选择分支后点击 **Run workflow**

---

## 本地构建（可选）

如果你想在本地电脑构建 APK：

### 环境要求
- Android Studio 或 Android SDK
- Node.js 18+
- Java JDK 17

### 构建步骤

```bash
# 1. 构建前端
cd frontend
npm install
npm run build

# 2. 同步到 Android
npx cap sync android

# 3. 构建 APK
cd android
./gradlew assembleDebug
```

APK 输出位置：`frontend/android/app/build/outputs/apk/debug/app-debug.apk`

---

## APK 安装

将生成的 `app-debug.apk` 文件传输到 Android 手机：

1. 在手机上允许"安装未知来源应用"
2. 点击 APK 文件进行安装
3. 打开应用，配置服务器地址即可使用

---

## 配置服务器地址

安装 APK 后，需要在应用中配置后端服务器地址：

1. 打开应用
2. 进入设置
3. 修改服务器地址为你的后端 IP 和端口

**开发环境**: `http://<你的电脑 IP>:8000`
**生产环境**: `https://<你的域名>`
