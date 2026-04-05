#!/bin/bash
#
# APK 签名脚本
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

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 配置
APKSIGNER="/opt/android-sdk/build-tools/35.0.0/apksigner"
KEYSTORE="yunwa-release-key.jks"
KEYSTORE_PASS="yunwa123456"
KEY_ALIAS="yunwa"
KEY_PASS="yunwa123456"

# 使用方法
usage() {
    echo "使用方法:"
    echo "  $0 <unsigned-apk> [output-apk]"
    echo ""
    echo "示例:"
    echo "  $0 app-release-unsigned.apk"
    echo "  $0 app-release-unsigned.apk my-app.apk"
    echo ""
    echo "当前密钥库：$KEYSTORE"
    echo "密钥别名：$KEY_ALIAS"
}

# 检查参数
if [ $# -lt 1 ]; then
    usage
    exit 1
fi

INPUT_APK="$1"
OUTPUT_APK="${2:-${INPUT_APK%.apk}-signed.apk}"

# 检查输入文件
if [ ! -f "$INPUT_APK" ]; then
    log_error "找不到 APK 文件：$INPUT_APK"
    exit 1
fi

# 检查密钥库
if [ ! -f "$KEYSTORE" ]; then
    log_error "找不到密钥库：$KEYSTORE"
    log_info "请先运行以下命令生成密钥库:"
    echo ""
    echo "keytool -genkey -v \\"
    echo "  -keystore $KEYSTORE \\"
    echo "  -keyalg RSA \\"
    echo "  -keysize 2048 \\"
    echo "  -validity 10000 \\"
    echo "  -alias $KEY_ALIAS"
    exit 1
fi

log_info "开始签名 APK..."
echo "  输入：$INPUT_APK"
echo "  输出：$OUTPUT_APK"
echo "  密钥库：$KEYSTORE"
echo ""

# 签名
"$APKSIGNER" sign \
  --ks "$KEYSTORE" \
  --ks-key-alias "$KEY_ALIAS" \
  --ks-pass "pass:$KEYSTORE_PASS" \
  --key-pass "pass:$KEY_PASS" \
  --out "$OUTPUT_APK" \
  "$INPUT_APK"

# 验证
echo ""
log_info "验证签名..."
if "$APKSIGNER" verify --verbose "$OUTPUT_APK" 2>&1 | grep -q "Verifies"; then
    log_info "签名验证成功！"
    echo ""
    echo "已签名的 APK: $OUTPUT_APK"
    ls -lh "$OUTPUT_APK"
else
    log_error "签名验证失败！"
    exit 1
fi
