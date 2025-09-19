# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please:

1. **DO NOT** open a public issue
2. Email the maintainers directly at [create an issue with "SECURITY:" prefix]
3. Include detailed information about the vulnerability
4. Allow reasonable time for us to address the issue before public disclosure

## Security Best Practices

When using Context Engineering MCP:

1. **API Keys**: Never commit API keys to the repository
   - Use `.env` files (excluded from git)
   - Use environment variables
   - Store keys securely in your CI/CD system

2. **Dependencies**: Keep all dependencies up to date
   - Regularly run `pip install --upgrade`
   - Monitor security advisories

3. **Data Privacy**: Be careful with context data
   - Do not store sensitive information in templates
   - Review context elements before sharing

## Known Security Considerations

- **Gemini API**: All AI operations require a valid GEMINI_API_KEY
- **MCP Communication**: Uses stdio mode for secure inter-process communication
- **Template Storage**: Templates may contain user data - handle with care

## Updates and Patches

Security updates are released as soon as possible after discovery. Check the [releases page](https://github.com/Enushin/context-engineering-MCP/releases) for updates.