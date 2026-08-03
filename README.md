# MCP Server with PyTorch Tools

A simple implementation of a **Model Context Protocol (MCP)** server and client using Python. This repo demonstrates how an AI agent can communicate with multiple tools through an MCP server.

## Features

- MCP Server using FastMCP
- MCP Client using stdio transport
- AI Agent with multi-tool integration
- Safe Calculator Tool
- Live Weather Tool (Open-Meteo API)
- PyTorch Tensor Operations

## Tools

### Calculator Tool
Evaluates mathematical expressions safely.

Example:
```
25 * (10 + 2)
```

### Weather Tool
Fetches current weather using the Open-Meteo API.

Example:
```
Weather in Kolkata
```

### Tensor Tool
Performs PyTorch tensor operations.

Supported operations:
- mean
- norm
- eigen
## License

This project is licensed under the MIT License.
