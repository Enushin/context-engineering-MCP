#!/bin/bash

# Context Engineering MCP - ワンステップインストーラー
# 使い方: curl -sSL https://raw.githubusercontent.com/Enushin/context-engineering-MCP/main/install.sh | bash

set -e

# カラー設定
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}     Context Engineering MCP - ワンステップセットアップ     ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# 1. GEMINI_API_KEYのチェックと設定
if [ -f .env ] && grep -q "GEMINI_API_KEY=" .env; then
    echo -e "${GREEN}✓ GEMINI_API_KEYが既に設定されています${NC}"
else
    # 環境変数をチェック
    if [ ! -z "$GEMINI_API_KEY" ]; then
        echo -e "${GREEN}✓ 環境変数からGEMINI_API_KEYを検出${NC}"
        echo "GEMINI_API_KEY=$GEMINI_API_KEY" >> .env
    else
        # インタラクティブに入力を求める
        echo -e "${YELLOW}GEMINI_API_KEYが見つかりません${NC}"
        echo -e "${BLUE}Google AI Studioから取得: https://makersuite.google.com/app/apikey${NC}"
        echo -n "GEMINI_API_KEY を入力してください: "
        read -s API_KEY
        echo

        if [ -z "$API_KEY" ]; then
            echo -e "${YELLOW}⚠ API Keyがスキップされました。後で.envファイルに設定してください${NC}"
            echo "GEMINI_API_KEY=your-api-key-here" >> .env
        else
            echo "GEMINI_API_KEY=$API_KEY" >> .env
            echo -e "${GREEN}✓ API Keyを.envファイルに保存しました${NC}"
        fi
    fi
fi

# 2. Claude MCP追加コマンドの実行
echo -e "\n${BLUE}MCPツールをインストール中...${NC}"

# claude mcp add コマンドを実行
claude mcp add context-eng -- uvx --from git+https://github.com/Enushin/context-engineering-MCP context-engineering-mcp start-mcp-server --project "$PWD"

echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}              インストール完了！              ${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${BLUE}利用可能なツール:${NC}"
echo -e "  • AIガイド管理 (4ツール)"
echo -e "  • コンテキスト管理 (7ツール)"
echo -e "  • テンプレート管理 (4ツール)"

echo -e "\n${BLUE}次のステップ:${NC}"
echo -e "  1. Claude Desktop/Codeを再起動"
echo -e "  2. MCPツールが自動的に利用可能になります"

if [ -f .env ]; then
    if grep -q "your-api-key-here" .env; then
        echo -e "\n${YELLOW}⚠ 注意: .envファイルのGEMINI_API_KEYを実際の値に更新してください${NC}"
    fi
fi