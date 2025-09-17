# Context Engineering MCP セットアップガイド

## 📋 前提条件

- Node.js 18+ がインストール済み
- Python 3.8+ がインストール済み
- Gemini API キーを取得済み
- Claude Desktop がインストール済み

## 🚀 クイックセットアップ

### 1. 依存関係のインストール

```bash
# Pythonパッケージのインストール
pip install -r requirements.txt

# Context Engineering用パッケージ
cd context_engineering
pip install -r requirements.txt
cd ..

# MCPサーバー用パッケージ
cd mcp-server
npm install
cd ..
```

### 2. 環境変数の設定

`.env` ファイルを作成：

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. サービスの起動

すべてのサービスを一括起動：

```bash
./start_all_services.sh
```

または個別に起動：

```bash
# AI Guides API (ポート8888)
python -m uvicorn main:app --host 0.0.0.0 --port 8888 --reload

# Context Engineering API (ポート9001)
cd context_engineering
python context_api.py
```

### 4. Claude Desktop の設定

Claude Desktop の設定ファイルは自動的に以下の場所に保存されています：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

以下の設定が既に追加されているか確認してください：

```json
{
  "mcpServers": {
    "context-engineering": {
      "command": "node",
      "args": [
        "/Users/Work/MCP/context_engineering_MCP/mcp-server/context_mcp_server.js"
      ],
      "env": {
        "GEMINI_API_KEY": "your_api_key",
        "CONTEXT_API_URL": "http://localhost:9001",
        "AI_GUIDES_API_URL": "http://localhost:8888"
      }
    }
  }
}
```

### 5. Claude Desktop を再起動

設定を反映するため、Claude Desktop を完全に再起動してください：

1. Claude Desktop を終了
2. Activity Monitor (macOS) でプロセスが残っていないか確認
3. Claude Desktop を再起動

## ✅ 動作確認

### APIサービスの確認

```bash
# AI Guides API
curl http://localhost:8888/health

# Context Engineering API
curl http://localhost:9001/api/stats
```

### MCPサーバーのテスト

```bash
cd mcp-server
node context_mcp_server.js
# "Context Engineering MCP Server running on stdio" が表示されれば正常
```

### Claude Desktop での確認

Claude Desktop で以下のコマンドを入力：
- `/mcp list` - 利用可能なMCPツールの一覧表示
- 「context-engineering」が表示されれば成功

## 🔧 トラブルシューティング

### エラー: MCPサーバーが認識されない

1. **Claude Desktop を完全に再起動**
   ```bash
   # macOSの場合
   killall Claude
   ```

2. **設定ファイルのパスを確認**
   - パスは絶対パスで指定する必要があります
   - `~` は使用できません（完全なパスを使用）

3. **Node.js のバージョン確認**
   ```bash
   node --version  # v18.0.0 以上が必要
   ```

### エラー: APIサービスが起動しない

1. **ポートの競合確認**
   ```bash
   lsof -i :8888  # AI Guides API
   lsof -i :9001  # Context Engineering API
   ```

2. **ログファイルの確認**
   ```bash
   cat /tmp/ai_guides_api.log
   cat /tmp/context_engineering_api.log
   ```

### エラー: Gemini API エラー

1. **API キーの確認**
   - `.env` ファイルに正しいキーが設定されているか確認
   - Claude Desktop 設定の `GEMINI_API_KEY` も確認

2. **APIクォータの確認**
   - [Google AI Studio](https://makersuite.google.com/) でクォータを確認

## 📊 利用可能なMCPツール（15個）

### AI Guides ツール（4個）
- `list_guides` - ガイド一覧の取得
- `search_guides` - キーワード検索
- `search_guides_semantic` - セマンティック検索
- `analyze_guide` - ガイドの分析

### Context ツール（7個）
- `create_session` - セッション作成
- `create_context_window` - コンテキストウィンドウ作成
- `add_context_element` - 要素追加
- `analyze_context` - コンテキスト分析
- `optimize_context` - コンテキスト最適化
- `auto_optimize_context` - 自動最適化
- `get_optimization_status` - 最適化ステータス

### Template ツール（4個）
- `create_template` - テンプレート作成
- `generate_template` - AI生成テンプレート
- `list_templates` - テンプレート一覧
- `render_template` - テンプレートレンダリング

## 🛑 サービスの停止

```bash
# プロセスIDファイルから停止
kill $(cat /tmp/ai_guides_api.pid)
kill $(cat /tmp/context_engineering_api.pid)

# または全プロセスを検索して停止
pkill -f "uvicorn main:app"
pkill -f "context_api.py"
```

## 📚 詳細ドキュメント

- [API Documentation](./README.md)
- [MCP Tools Reference](./mcp-server/README.md)
- [Context Engineering Guide](./context_engineering/README.md)

## 💡 ヒント

- サービス起動時は必ず API サービスを先に起動してください
- Claude Desktop の設定変更後は必ず再起動が必要です
- ログファイルは `/tmp/` に保存されます
- 開発時は `--reload` オプションを使用すると便利です