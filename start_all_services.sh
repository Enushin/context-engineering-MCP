#!/bin/bash

# Context Engineering MCP Platform 起動スクリプト

echo "🚀 Context Engineering MCP Platform を起動しています..."

# 環境変数の設定
export GEMINI_API_KEY="AIzaSyC5y-XqtgM73xr761nVAfR2vnmvi0dFIzI"

# AI Guides APIサーバーの起動
echo "📚 AI Guides API サーバーを起動中..."
cd /Users/Work/MCP/context_engineering_MCP
python -m uvicorn main:app --host 0.0.0.0 --port 8888 --reload > /tmp/ai_guides_api.log 2>&1 &
AI_GUIDES_PID=$!
echo "   PID: $AI_GUIDES_PID"

# 少し待つ
sleep 3

# Context Engineering APIサーバーの起動
echo "🔧 Context Engineering API サーバーを起動中..."
cd /Users/Work/MCP/context_engineering_MCP/context_engineering
python context_api.py > /tmp/context_engineering_api.log 2>&1 &
CONTEXT_PID=$!
echo "   PID: $CONTEXT_PID"

# サービスの起動を待つ
echo "⏳ サービスの起動を待っています..."
sleep 5

# 起動確認
echo ""
echo "📊 サービスステータス:"
echo "------------------------"

# AI Guides APIの確認
if curl -s http://localhost:8888/health > /dev/null 2>&1; then
    echo "✅ AI Guides API: 正常起動 (http://localhost:8888)"
else
    echo "❌ AI Guides API: 起動失敗"
    echo "   ログ: /tmp/ai_guides_api.log"
fi

# Context Engineering APIの確認
if curl -s http://localhost:9001/api/stats > /dev/null 2>&1; then
    echo "✅ Context Engineering API: 正常起動 (http://localhost:9001)"
else
    echo "❌ Context Engineering API: 起動失敗"
    echo "   ログ: /tmp/context_engineering_api.log"
fi

echo ""
echo "🎯 MCPサーバーを起動するには:"
echo "   cd /Users/Work/MCP/context_engineering_MCP/mcp-server"
echo "   node context_mcp_server.js"
echo ""
echo "💡 サービスを停止するには:"
echo "   kill $AI_GUIDES_PID $CONTEXT_PID"
echo ""
echo "📝 プロセスIDを保存しています..."
echo "$AI_GUIDES_PID" > /tmp/ai_guides_api.pid
echo "$CONTEXT_PID" > /tmp/context_engineering_api.pid

echo ""
echo "✨ 起動完了！Claude Desktop を再起動してください。"