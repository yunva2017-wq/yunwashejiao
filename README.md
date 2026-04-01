# 云娃聊天应用 (Yunwa Chat)

类似云娃 APP 的实时社交聊天应用，支持文字聊天和语音通话功能。

## ✨ 功能特性

- 📝 **用户注册/登录** - 简单的用户名密码注册登录
- 💬 **实时文字聊天** - 基于 WebSocket 的实时消息
- 🎤 **语音消息** - 录制并发送语音消息
- 📞 **语音通话** - 基于 WebRTC 的实时语音通话
- 👥 **聊天室** - 支持多个聊天室
- 🟢 **在线状态** - 显示在线用户列表

## 🛠️ 技术栈

### 后端
- Python 3.9+
- FastAPI
- Socket.IO (WebSocket)
- SQLAlchemy (PostgreSQL)
- WebRTC

### 前端
- Vue 3
- Element Plus
- Socket.IO Client
- Pinia (状态管理)

## 📦 快速开始

### 1. 环境要求
- Python 3.9+
- Node.js 16+
- PostgreSQL

### 2. 数据库配置

```bash
# 创建数据库
createdb glimmer_chat
```

### 3. 后端启动

```bash
# 方式一：使用启动脚本
chmod +x start-backend.sh
./start-backend.sh

# 方式二：手动启动
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:socket_app --host 0.0.0.0 --port 8000 --reload
```

### 4. 前端启动

```bash
# 方式一：使用启动脚本
chmod +x start-frontend.sh
./start-frontend.sh

# 方式二：手动启动
cd frontend
npm install
npm run dev
```

### 5. 访问应用

打开浏览器访问：http://localhost:3000

## 📁 项目结构

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── models/       # 数据库模型
│   │   ├── schemas/      # Pydantic Schema
│   │   ├── services/     # 业务逻辑
│   │   ├── utils/        # 工具函数
│   │   └── main.py       # 应用入口
│   ├── static/uploads/   # 上传文件
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/          # API 请求
│   │   ├── assets/       # 静态资源
│   │   ├── components/   # 组件
│   │   ├── views/        # 页面
│   │   └── router/       # 路由配置
│   └── package.json
└── start-*.sh           # 启动脚本
```

## 🔧 配置

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp backend/.env.example backend/.env
```

## 📝 API 接口

### 用户接口
- `POST /api/register` - 用户注册
- `POST /api/login` - 用户登录
- `GET /api/users/{id}` - 获取用户信息

### 消息接口
- `GET /api/messages/{room_id}` - 获取聊天记录
- `POST /api/upload-voice` - 上传语音

### WebSocket 事件
- `join` - 加入聊天室
- `chat_message` - 发送消息
- `voice_call` - 发起语音通话
- `call_accept` - 接听通话
- `call_reject` - 拒绝通话
- `call_end` - 结束通话
- `webrtc_offer` - WebRTC Offer
- `webrtc_answer` - WebRTC Answer
- `ice_candidate` - ICE Candidate

## ⚠️ 注意事项

1. 生产环境请修改 `SECRET_KEY`
2. 建议配置 TURN 服务器以支持更多 WebRTC 场景
3. PostgreSQL 数据库需要提前创建
4. 确保麦克风权限已授权

## 📄 License

MIT
