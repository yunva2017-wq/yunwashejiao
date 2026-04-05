#!/bin/bash
#
# Clash 代理启动脚本
# 自动启动 Clash Meta (Mihomo) 并加载订阅配置
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

# 配置
CLASH_HOME="/opt/clash"
CONFIG_DIR="/root/.config/clash"
CONFIG_FILE="${CONFIG_DIR}/config.yaml"
LOG_FILE="/var/log/clash.log"
PID_FILE="/var/run/clash.pid"
API_PORT="9091"
PROXY_PORT="7890"

# 订阅链接（您的 Clash 订阅）
SUB_URL="https://sublink.cute-cloud.de/link?token=feb4d233966f294af085db0d92809440"

# 检查是否已安装
check_installation() {
    if [ ! -f "${CLASH_HOME}/mihomo" ]; then
        log_error "Clash Meta 未安装，请先运行：$0 install"
        exit 1
    fi
}

# 创建配置文件
create_config() {
    log_info "创建配置文件..."
    mkdir -p "${CONFIG_DIR}"

    cat > "${CONFIG_FILE}" << 'EOF'
# Clash Meta 配置文件
mixed-port: 7890
allow-lan: false
mode: rule
log-level: info
ipv6: false

external-controller: 127.0.0.1:9091

# DNS 配置
dns:
  enable: true
  listen: 127.0.0.1:7874
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - 8.8.8.8
    - 1.1.1.1

# 订阅配置
proxy-providers:
  Subscribe:
    type: http
    url: "https://sublink.cute-cloud.de/link?token=feb4d233966f294af085db0d92809440"
    interval: 3600
    health-check:
      enable: true
      url: http://www.gstatic.com/generate_204
      interval: 300

# 代理组
proxy-groups:
  - name: Proxy
    type: select
    use:
      - Subscribe

# 规则
rules:
  - MATCH,Proxy
EOF

    log_info "配置文件已创建：${CONFIG_FILE}"
}

# 安装 Clash Meta
install() {
    log_info "正在安装 Clash Meta..."
    mkdir -p "${CLASH_HOME}"
    cd "${CLASH_HOME}"

    # 下载最新版本
    curl -sL "https://github.com/MetaCubeX/mihomo/releases/download/v1.19.0/mihomo-linux-amd64-compatible-v1.19.0.gz" -o mihomo.gz
    gunzip -f mihomo.gz
    chmod +x mihomo

    log_info "Clash Meta 已安装到 ${CLASH_HOME}"

    # 创建配置
    create_config
}

# 启动 Clash
start() {
    check_installation

    if [ -f "${PID_FILE}" ] && kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
        log_warn "Clash 已在运行中 (PID: $(cat "${PID_FILE}"))"
        return 0
    fi

    log_info "正在启动 Clash..."
    nohup "${CLASH_HOME}/mihomo" -d "${CONFIG_DIR}" > "${LOG_FILE}" 2>&1 &
    echo $! > "${PID_FILE}"

    # 等待启动
    sleep 5

    # 检查是否成功启动
    if kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
        log_info "Clash 已启动 (PID: $(cat "${PID_FILE}"))"
        log_info "代理端口：${PROXY_PORT}"
        log_info "API 端口：${API_PORT}"

        # 测试代理
        sleep 5
        if curl -s --connect-timeout 10 -x 127.0.0.1:${PROXY_PORT} https://www.google.com -o /dev/null; then
            log_info "代理测试成功！"
        else
            log_warn "代理测试失败，请检查日志：${LOG_FILE}"
        fi
    else
        log_error "Clash 启动失败，请检查日志：${LOG_FILE}"
        exit 1
    fi
}

# 停止 Clash
stop() {
    if [ -f "${PID_FILE}" ] && kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
        log_info "正在停止 Clash (PID: $(cat "${PID_FILE}"))..."
        kill "$(cat "${PID_FILE}")"
        rm -f "${PID_FILE}"
        log_info "Clash 已停止"
    else
        log_warn "Clash 未运行"
    fi

    # 清理可能的残留进程
    pkill -f "mihomo.*${CONFIG_DIR}" 2>/dev/null || true
}

# 重启 Clash
restart() {
    stop
    sleep 2
    start
}

# 查看状态
status() {
    if [ -f "${PID_FILE}" ] && kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
        log_info "Clash 正在运行 (PID: $(cat "${PID_FILE}"))"

        # 显示代理信息
        echo ""
        echo "代理信息:"
        curl -s http://127.0.0.1:${API_PORT}/proxies/Proxy 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print('  当前节点:', d.get('now', '未知'))
    print('  可用节点数:', len(d.get('all', [])))
except:
    print('  无法获取代理信息')
" 2>/dev/null || true

        echo ""
        echo "最近日志:"
        tail -5 "${LOG_FILE}"
    else
        log_warn "Clash 未运行"
    fi
}

# 显示使用方法
usage() {
    echo "使用方法:"
    echo "  $0 install   - 安装 Clash Meta"
    echo "  $0 start     - 启动 Clash"
    echo "  $0 stop      - 停止 Clash"
    echo "  $0 restart   - 重启 Clash"
    echo "  $0 status    - 查看状态"
    echo "  $0 config    - 创建配置文件"
    echo ""
    echo "代理设置:"
    echo "  HTTP 代理：http://127.0.0.1:${PROXY_PORT}"
    echo "  SOCKS5 代理：socks5://127.0.0.1:${PROXY_PORT}"
}

# 主程序
case "${1:-status}" in
    install)
        install
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    config)
        create_config
        ;;
    *)
        usage
        ;;
esac
