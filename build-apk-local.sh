#!/bin/bash
#
# 本地构建 APK 脚本 - 支持通过代理加速下载
#
# 使用方法:
#   ./build-apk-local.sh                    # 不使用代理
#   ./build-apk-local.sh --proxy            # 使用默认代理 (127.0.0.1:7890)
#   ./build-apk-local.sh --proxy 127.0.0.1:7891  # 使用指定代理
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 默认配置
PROXY_ENABLED=false
PROXY_HOST="127.0.0.1"
PROXY_PORT="7890"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --proxy)
            PROXY_ENABLED=true
            if [[ -n "$2" && ! "$2" =~ ^-- ]]; then
                if [[ "$2" == *:* ]]; then
                    PROXY_HOST="${2%%:*}"
                    PROXY_PORT="${2##*:}"
                else
                    PROXY_PORT="$2"
                fi
                shift
            fi
            shift
            ;;
        --help)
            echo "使用方法:"
            echo "  $0                    # 不使用代理"
            echo "  $0 --proxy            # 使用默认代理 (127.0.0.1:7890)"
            echo "  $0 --proxy HOST:PORT  # 使用指定代理"
            echo "  $0 --help             # 显示帮助"
            exit 0
            ;;
        *)
            log_error "未知参数：$1"
            exit 1
            ;;
    esac
done

# 设置代理环境变量
setup_proxy() {
    if [ "$PROXY_ENABLED" = true ]; then
        log_info "启用代理：${PROXY_HOST}:${PROXY_PORT}"
        export HTTP_PROXY="http://${PROXY_HOST}:${PROXY_PORT}"
        export HTTPS_PROXY="http://${PROXY_HOST}:${PROXY_PORT}"
        export http_proxy="http://${PROXY_HOST}:${PROXY_PORT}"
        export https_proxy="http://${PROXY_HOST}:${PROXY_PORT}"

        # Gradle 代理配置
        export GRADLE_OPTS="${GRADLE_OPTS} -Dhttp.proxyHost=${PROXY_HOST} -Dhttp.proxyPort=${PROXY_PORT} -Dhttps.proxyHost=${PROXY_HOST} -Dhttps.proxyPort=${PROXY_PORT}"
    else
        log_info "未使用代理"
    fi
}

# 配置 Android SDK 镜像（可选，如果代理失效可使用国内镜像）
setup_android_mirror() {
    # 这里可以配置使用国内镜像，如果需要通过代理则跳过
    # export REPO_URL="https://maven.aliyun.com/repository/google"
    log_info "使用官方源（通过代理下载）"
}

# 主构建流程
main() {
    log_info "=== 开始构建 APK ==="

    # 设置代理
    setup_proxy

    # 设置 Android SDK 镜像
    setup_android_mirror

    # 检查 Java 环境
    if ! command -v java &> /dev/null; then
        log_error "未找到 Java 环境，请先安装 Java 17+"
        exit 1
    fi
    log_info "Java 版本：$(java -version 2>&1 | head -n 1)"

    # 检查 Android SDK
    if [ -z "$ANDROID_HOME" ] && [ -z "$ANDROID_SDK_ROOT" ]; then
        log_warn "未设置 ANDROID_HOME 或 ANDROID_SDK_ROOT 环境变量"
        log_warn "请确保已安装 Android SDK 并设置相应环境变量"
    fi

    # 进入前端目录
    cd "$(dirname "$0")/frontend/android"

    # 清理之前的构建（可选）
    # ./gradlew clean

    # 构建 APK
    log_info "开始构建 Debug APK..."
    ./gradlew assembleDebug --no-daemon --stacktrace

    # 输出结果
    APK_PATH="app/build/outputs/apk/debug/app-debug.apk"
    if [ -f "$APK_PATH" ]; then
        log_info "=== 构建成功 ==="
        log_info "APK 路径：$(pwd)/$APK_PATH"
    else
        log_error "构建失败，未找到 APK 文件"
        exit 1
    fi
}

# 运行主流程
main
