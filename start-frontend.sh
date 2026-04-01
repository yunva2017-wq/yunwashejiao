#!/bin/bash

# 云娃聊天应用 - 前端启动脚本

echo "🚀 启动前端开发服务器..."

# 进入前端目录
cd "$(dirname "$0")/frontend"

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

# 启动开发服务器
echo "🚀 启动前端服务..."
npm run dev
