#!/usr/bin/env node

/**
 * Standalone MCP Server for Context Engineering
 * This version works without external API dependencies
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

class StandaloneMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'context-engineering-mcp',
        version: '2.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    // In-memory storage
    this.sessions = new Map();
    this.windows = new Map();
    this.templates = new Map();

    this.setupHandlers();
  }

  setupHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        // Simplified tools that work locally
        {
          name: 'create_context_session',
          description: 'Create a new context engineering session',
          inputSchema: {
            type: 'object',
            properties: {
              name: { type: 'string', description: 'Session name' },
              description: { type: 'string', description: 'Session description' },
            },
          },
        },
        {
          name: 'create_context_window',
          description: 'Create a new context window in a session',
          inputSchema: {
            type: 'object',
            properties: {
              session_id: { type: 'string', description: 'The session ID' },
              max_tokens: { type: 'integer', default: 8192 },
              reserved_tokens: { type: 'integer', default: 512 },
            },
            required: ['session_id'],
          },
        },
        {
          name: 'add_context_element',
          description: 'Add an element to a context window',
          inputSchema: {
            type: 'object',
            properties: {
              window_id: { type: 'string', description: 'The context window ID' },
              content: { type: 'string', description: 'The content to add' },
              type: {
                type: 'string',
                enum: ['system', 'user', 'assistant'],
                default: 'user',
              },
              priority: { type: 'integer', default: 5, minimum: 1, maximum: 10 },
            },
            required: ['window_id', 'content'],
          },
        },
        {
          name: 'get_context_stats',
          description: 'Get statistics about the context engineering system',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'create_prompt_template',
          description: 'Create a new prompt template',
          inputSchema: {
            type: 'object',
            properties: {
              name: { type: 'string', description: 'Template name' },
              description: { type: 'string', description: 'Template description' },
              template: { type: 'string', description: 'Template content with {variables}' },
              category: { type: 'string', default: 'general' },
            },
            required: ['name', 'description', 'template'],
          },
        },
        {
          name: 'list_prompt_templates',
          description: 'List available prompt templates',
          inputSchema: {
            type: 'object',
            properties: {
              category: { type: 'string', description: 'Filter by category' },
            },
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'create_context_session': {
            const sessionId = this.generateId();
            const session = {
              id: sessionId,
              name: args.name || 'New Session',
              description: args.description || '',
              created_at: new Date().toISOString(),
              windows: [],
            };
            this.sessions.set(sessionId, session);
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: true,
                    session_id: sessionId,
                    message: `Session created: ${session.name}`,
                  }, null, 2),
                },
              ],
            };
          }

          case 'create_context_window': {
            const windowId = this.generateId();
            const window = {
              id: windowId,
              session_id: args.session_id,
              max_tokens: args.max_tokens || 8192,
              reserved_tokens: args.reserved_tokens || 512,
              elements: [],
              created_at: new Date().toISOString(),
            };
            this.windows.set(windowId, window);

            const session = this.sessions.get(args.session_id);
            if (session) {
              session.windows.push(windowId);
            }

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: true,
                    window_id: windowId,
                    message: `Context window created with ${window.max_tokens} max tokens`,
                  }, null, 2),
                },
              ],
            };
          }

          case 'add_context_element': {
            const window = this.windows.get(args.window_id);
            if (!window) {
              throw new Error('Window not found');
            }

            const element = {
              content: args.content,
              type: args.type || 'user',
              priority: args.priority || 5,
              created_at: new Date().toISOString(),
            };

            window.elements.push(element);

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: true,
                    message: `Element added to context window`,
                    element_count: window.elements.length,
                  }, null, 2),
                },
              ],
            };
          }

          case 'get_context_stats': {
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    sessions: this.sessions.size,
                    windows: this.windows.size,
                    templates: this.templates.size,
                    status: 'operational',
                  }, null, 2),
                },
              ],
            };
          }

          case 'create_prompt_template': {
            const templateId = this.generateId();
            const template = {
              id: templateId,
              name: args.name,
              description: args.description,
              template: args.template,
              category: args.category || 'general',
              created_at: new Date().toISOString(),
            };
            this.templates.set(templateId, template);

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    success: true,
                    template_id: templateId,
                    message: `Template created: ${template.name}`,
                  }, null, 2),
                },
              ],
            };
          }

          case 'list_prompt_templates': {
            const templates = Array.from(this.templates.values());
            const filtered = args.category
              ? templates.filter(t => t.category === args.category)
              : templates;

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    templates: filtered,
                    total: filtered.length,
                  }, null, 2),
                },
              ],
            };
          }

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                error: error.message,
                tool: name,
              }, null, 2),
            },
          ],
          isError: true,
        };
      }
    });
  }

  generateId() {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Context Engineering MCP server running (standalone mode)');
  }
}

const server = new StandaloneMCPServer();
server.run().catch(console.error);