#!/bin/bash
#
# 清理构建缓存脚本
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 进入项目目录
cd "$(dirname "$0")/frontend/android"

log_info "=== 清理 Android 构建缓存 ==="

# 清理 Gradle 构建
log_info "清理 Gradle 构建..."
./gradlew clean --no-daemon

# 清理 build 目录
log_info "清理 build 目录..."
rm -rf app/build
rm -rf build

# 清理 .gradle 缓存（可选）
if [ -d ".gradle" ]; then
    log_warn "发现 .gradle 缓存目录"
    log_info "如需清理 Gradle 缓存，请手动删除 .gradle 目录"
fi

log_info "=== 清理完成 ==="
echo ""
echo "提示："
echo "  - APK 文件已从输出目录清除"
echo "  - 下次构建将重新编译所有资源"
echo "  - Gradle 依赖缓存位于 ~/.gradle/caches"
