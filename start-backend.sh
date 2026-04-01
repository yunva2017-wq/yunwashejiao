#!/bin/bash

# 云娃聊天应用 - 启动脚本

echo "🚀 启动云娃聊天应用..."

# 进入后端目录
cd "$(dirname "$0")/backend"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install -r requirements.txt

# 创建上传目录
mkdir -p static/uploads/{voice,avatar}

# 启动后端服务
echo "🚀 启动后端服务..."
python -m uvicorn app.main:socket_app --host 0.0.0.0 --port 8000 --reload
