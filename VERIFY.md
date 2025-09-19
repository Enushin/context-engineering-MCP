# Context Engineering MCP - 動作確認手順

## 他のプロジェクトでのインストール確認

### 1. テストプロジェクトの準備
```bash
mkdir test-mcp
cd test-mcp
```

### 2. インストール方法A: ワンステップインストール
```bash
curl -sSL https://raw.githubusercontent.com/Enushin/context-engineering-MCP/main/install.sh | bash
```

### 3. インストール方法B: 手動インストール
```bash
# API Key設定（オプション）
echo "GEMINI_API_KEY=your-key-here" > .env.local

# MCPツール追加
claude mcp add context-eng -- uvx --from git+https://github.com/Enushin/context-engineering-MCP context-engineering-mcp start-mcp-server --project "$PWD"
```

### 4. Claude Desktop/Codeで確認
```bash
claude --dangerously-skip-permissions
```

コマンド内で `/mcp` を実行して、以下を確認：
- Context-eng MCP Server が表示される
- Status: ✓ running になる

### 5. ツールの動作確認

Claudeで以下のコマンドを試す：

```
「create_context_sessionツールを使って新しいセッションを作成して」
```

期待される結果：
```json
{
  "success": true,
  "session_id": "xxxxx",
  "message": "Session created: New Session"
}
```

## トラブルシューティング

### "MCP server file not found" エラー
最新版を強制再インストール：
```bash
uvx --reinstall --from git+https://github.com/Enushin/context-engineering-MCP context-engineering-mcp start-mcp-server --project "$PWD"
```

### Status: ✘ failed の場合
1. Pythonバージョン確認: `python --version` (3.8+必要)
2. uvxインストール確認: `which uvx`
3. 手動で実行テスト:
```bash
uvx --from git+https://github.com/Enushin/context-engineering-MCP context-engineering-mcp start-mcp-server --project "$PWD"
```

## 確認項目チェックリスト

- [ ] インストールスクリプトが正常終了
- [ ] Claude Desktopで `/mcp` 実行時にサーバーが表示
- [ ] Status: ✓ running になる
- [ ] create_context_session ツールが動作
- [ ] Node.js/npmが不要で動作する
- [ ] エラーメッセージが出ない