#!/bin/bash
#
# 一键构建 APK 脚本 - 自动启动代理并构建
#

set -e

# 颜色输出
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

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Clash 是否运行
check_clash() {
    if pgrep -f "mihomo.*clash" > /dev/null 2>&1; then
        log_info "Clash 代理正在运行"
        return 0
    else
        log_warn "Clash 代理未运行，正在启动..."
        $(dirname "$0")/clash-proxy.sh start
        sleep 3
    fi
}

# 构建 APK
build_apk() {
    local build_type="${1:-debug}"

    export HTTP_PROXY="http://127.0.0.1:7890"
    export HTTPS_PROXY="http://127.0.0.1:7890"
    export GRADLE_OPTS="-Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=7890 -Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=7890"
    export JAVA_HOME=/usr/lib/jvm/java-21-openjdk

    cd "$(dirname "$0")/frontend/android"

    log_info "开始构建 ${build_type^} APK..."

    if [ "$build_type" == "release" ]; then
        ./gradlew assembleRelease --no-daemon
    else
        ./gradlew assembleDebug --no-daemon
    fi

    if [ $? -eq 0 ]; then
        log_info "构建成功!"
        if [ "$build_type" == "release" ]; then
            log_info "APK 路径：$(pwd)/app/build/outputs/apk/release/app-release.apk"
        else
            log_info "APK 路径：$(pwd)/app/build/outputs/apk/debug/app-debug.apk"
        fi
    else
        log_error "构建失败"
        exit 1
    fi
}

# 主程序
main() {
    log_info "=== Yunwa Chat APK 构建工具 ==="
    echo ""

    # 检查 Clash
    check_clash

    # 构建类型
    local build_type="${1:-debug}"

    # 构建
    build_apk "$build_type"

    echo ""
    log_info "=== 构建完成 ==="
}

# 显示使用方法
usage() {
    echo "使用方法:"
    echo "  $0 [debug|release]"
    echo ""
    echo "示例:"
    echo "  $0          # 构建 Debug 版本"
    echo "  $0 debug    # 构建 Debug 版本"
    echo "  $0 release  # 构建 Release 版本"
}

case "${1:-}" in
    -h|--help)
        usage
        ;;
    *)
        main "$1"
        ;;
esac
