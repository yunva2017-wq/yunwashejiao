# 云娃聊天应用 - GitHub Actions 部署指南

## 自动构建 APK

本项目已配置 GitHub Actions 自动构建 Android APK。

### 工作流程文件

位置：`.github/workflows/`

| 文件 | 说明 | 触发条件 |
|------|------|----------|
| `build-apk.yml` | 构建调试版 APK | 推送到 main/master 分支 / 手动触发 |
| `build-release-apk.yml` | 构建签名发布版 APK | 仅手动触发 |

---

## 使用步骤

### 1. 初始化 Git 仓库（如果没有）

```bash
cd /usr/local/claude
git init
git add .
git commit -m "Initial commit - 云娃聊天应用"
```

### 2. 创建 GitHub 仓库并推送

```bash
# 在 GitHub.com 创建新仓库，然后：
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

### 3. 查看构建状态

1. 进入你的 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 选择 **Build Android APK** 工作流
4. 查看构建进度和结果

### 4. 下载 APK

构建完成后：
1. 点击最近的一次运行记录
2. 滚动到页面底部
3. 点击 **yunwa-chat-apk** 下载
4. 解压得到 `app-debug.apk`

---

## 手动触发构建

1. 进入 **Actions** 标签页
2. 点击左侧的 **Build Android APK**
3. 点击 **Run workflow** 按钮
4. 选择分支（通常是 main）
5. 点击 **Run workflow**

---

## 构建签名发布版 APK

### 第一步：生成密钥库

```bash
keytool -genkey -v -keystore release-key.keystore \
  -alias yunwa-chat \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

### 第二步：上传密钥库到 GitHub Secrets

1. 将密钥库文件转换为 base64：
   ```bash
   base64 release-key.keystore > keystore.txt
   ```

2. 复制 `keystore.txt` 的内容

3. 在 GitHub 仓库中：
   - Settings → Secrets and variables → Actions
   - New repository secret
   - Name: `RELEASE_KEYSTORE_B64`
   - Value: 粘贴 keystore.txt 的内容

4. 添加其他 secrets：
   - `RELEASE_KEYSTORE_PASSWORD`: 密钥库密码
   - `RELEASE_KEY_ALIAS`: 密钥别名
   - `RELEASE_KEY_PASSWORD`: 密钥密码

### 第三步：运行发布构建

1. Actions → Build Android Release APK
2. Run workflow
3. 输入版本号和版本代码
4. 下载签名后的 APK

---

## 自动构建触发条件

以下情况会自动触发构建：

- 推送代码到 `main` 或 `master` 分支
- 创建拉取请求到 `main` 或 `master` 分支
- 修改了 `frontend/` 目录下的文件

---

## 注意事项

1. **密钥库安全**：不要将 `release-key.keystore` 提交到 Git
2. **构建时长**：首次构建约 10-15 分钟（下载依赖）
3. **存储空间**：GitHub 提供 500MB Actions 存储空间
4. **运行时长限制**：每个 job 最长运行 6 小时

---

## 常见问题

**Q: 构建失败怎么办？**
A: 查看 Actions 日志，常见原因：
- 依赖下载超时（重试即可）
- 内存不足（减少并发）
- 配置错误（检查 workflow 文件）

**Q: 如何下载历史版本的 APK？**
A: Artifacts 保留 30 天，过期后无法下载。建议将重要版本上传到 Releases。

**Q: 可以自定义 APK 名称吗？**
A: 可以，修改 `android/app/build.gradle` 中的 `applicationId` 和 `archivesBaseName`。
