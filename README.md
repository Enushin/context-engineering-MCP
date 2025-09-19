# Context Engineering MCP

> 他のプロジェクトにインストール可能なMCPパッケージ - Claude Desktop/Code統合対応

日本語 | [English](README_EN.md)

## 概要

Context Engineering MCPは、AIコンテキスト管理を革新する包括的なMCPパッケージです。任意のプロジェクトにインストールして、高度なコンテキスト管理機能を追加できます。

### 主要機能

- **15のMCPツール**: AIガイド管理、コンテキスト最適化、テンプレート管理
- **Gemini 2.0 Flash統合**: セマンティック検索と分析
- **52%のトークン削減**: AI駆動の最適化
- **プロジェクト独立**: 任意のプロジェクトで利用可能

## インストール

### 🚀 ワンステップインストール（最も簡単）

プロジェクトディレクトリで実行:

#### 方法1: ローカルスクリプト
```bash
curl -sSL https://raw.githubusercontent.com/Enushin/context-engineering-MCP/main/install.sh | bash
```

#### 方法2: Pythonコマンド
```bash
uvx --from git+https://github.com/Enushin/context-engineering-MCP ce-quickstart
```

どちらも：
- GEMINI_API_KEYの入力を求められます
- 自動で.envファイル作成
- MCPツールをClaudeに登録

### 🛠 手動インストール（2ステップ）

#### ステップ1: API Key設定
```bash
echo "GEMINI_API_KEY=your-actual-key" > .env
```

#### ステップ2: MCPツール追加
```bash
claude mcp add context-eng -- uvx --from git+https://github.com/Enushin/context-engineering-MCP context-engineering-mcp start-mcp-server --project "$PWD"
```

### 💻 Claude Desktop設定（手動）

`~/Library/Application Support/Claude/claude_desktop_config.json`に追加:

```json
{
  "mcpServers": {
    "context-engineering": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Enushin/context-engineering-MCP",
        "context-engineering-mcp",
        "start-mcp-server",
        "--project",
        "${PROJECT_PATH}"
      ],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

## 使い方

### 基本的な使用

プロジェクトディレクトリで:

```bash
# MCP サーバー起動（Claude経由）
uvx --from git+https://github.com/Enushin/context-engineering-MCP \
  context-engineering-mcp start-mcp-server --project "$PWD"
```

### 環境変数設定（重要）

MCPツールはプロジェクトの`.env`ファイルからGEMINI_API_KEYを自動読み込み:

```bash
# プロジェクトルートに.envファイル作成
cat > .env << EOF
GEMINI_API_KEY=your-actual-api-key-here
EOF
```

または、グローバル環境変数として設定:

```bash
# ~/.zshrcまたは~/.bashrcに追加
export GEMINI_API_KEY="your-actual-api-key-here"
source ~/.zshrc  # 即座に反映
```

### 利用可能なコマンド

```bash
# MCPサーバー起動
context-engineering-mcp start-mcp-server --project /path/to/project

# セットアップ実行
context-engineering-mcp setup

# Claude Desktop設定生成
context-engineering-mcp config --output claude_config.json
```

## MCP ツール一覧

### AIガイド管理（4ツール）
- `list_ai_guides` - ガイド一覧取得
- `search_ai_guides` - キーワード検索
- `search_guides_with_gemini` - AI検索
- `analyze_guide` - ガイド分析

### コンテキスト管理（7ツール）
- `create_context_session` - セッション作成
- `create_context_window` - ウィンドウ作成
- `add_context_element` - 要素追加
- `analyze_context` - 品質分析
- `optimize_context` - 最適化
- `auto_optimize_context` - 自動最適化
- `get_context_stats` - 統計取得

### テンプレート管理（4ツール）
- `create_prompt_template` - テンプレート作成
- `generate_prompt_template` - AI生成
- `list_prompt_templates` - 一覧表示
- `render_template` - レンダリング

## 👨‍💻 プロジェクト統合例

### 1. 新規プロジェクトで使用

```bash
# プロジェクト作成
mkdir my-ai-project
cd my-ai-project

# ワンステップインストール
curl -sSL https://raw.githubusercontent.com/Enushin/context-engineering-MCP/main/install.sh | bash
# または: uvx --from git+https://github.com/Enushin/context-engineering-MCP ce-quickstart

# Claude Desktopで使用開始
```

### 2. 既存プロジェクトに統合

```bash
cd existing-project

# ワンステップインストール（API Keyを対話式で入力）
curl -sSL https://raw.githubusercontent.com/Enushin/context-engineering-MCP/main/install.sh | bash

# Claude Desktop/Codeで15のツールが利用可能に
```

## 開発者向け

### ローカル開発

```bash
# リポジトリクローン
git clone https://github.com/Enushin/context-engineering-MCP.git
cd context-engineering-MCP

# 開発環境セットアップ
pip install -e ".[dev]"
cd mcp-server && npm install

# テスト実行
pytest
npm test
```

### パッケージ構造

```
context-engineering-MCP/
├── context_engineering_mcp/   # Pythonパッケージ
│   ├── __init__.py
│   ├── cli.py                # CLIエントリーポイント
│   └── mcp_server.py         # MCPサーバーラッパー
├── mcp-server/               # Node.js MCPサーバー
│   └── context_mcp_server.js
├── pyproject.toml           # パッケージ設定
└── README.md
```

## トラブルシューティング

### GEMINI_API_KEY エラー
```bash
# 環境変数設定
export GEMINI_API_KEY="your-actual-key"

# または.envファイル
echo "GEMINI_API_KEY=your-actual-key" > .env
```

### Node.js エラー
```bash
# Node.js 18+が必要
node --version  # v18.0.0以上を確認
```

### ポート競合
```bash
# カスタムポート使用
context-engineering-mcp start-mcp-server --port 9002
```

## セキュリティ

脆弱性を発見した場合は、[Issues](https://github.com/Enushin/context-engineering-MCP/issues)に「SECURITY:」プレフィックスを付けて報告してください。

## ライセンス

MIT License

## 謝辞

このプロジェクトは [ShunsukeHayashi/context_engineering_MCP](https://github.com/ShunsukeHayashi/context_engineering_MCP) を参考に作成されました。
オリジナルプロジェクトの素晴らしいアーキテクチャとコンセプトに感謝いたします。

## コントリビューション

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容について議論してください。

## サポート

Issues: [GitHub Issues](https://github.com/Enushin/context-engineering-MCP/issues)

---

**Context Engineering MCP** - あらゆるプロジェクトに高度なコンテキスト管理を。