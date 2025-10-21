## Excel MCP Server Minio

原作者开发的Excel MCP Server，只能在本地使用（因为文件只能保存在本地文件系统），不支持在线平台的远程访问功能（上传和下载）

本项目在Excel MCP Server的基础上，添加了minio远程上传下载文件的功能：

- 每次操作excel文件用户需传入文件名，大模型会自动访问远程存在的excel文件。
- 然后可以读取数据、插入数据、生成图表、数据计算等等...
- 最后将生成后的excel文件下载链接返回给用户。

注：远程文件访问平台使用的是minio



### 如何部署

下载打包好的docker镜像，[excel-mcp-server-minio-image.tar](https://github.com/Hualiuliu6767/excel-mcp-server-minio/releases/download/excel-mcp-server-minio-v1.0/excel-mcp-server-minio-image.tar)

```shell
# 加载镜像
docker load -i excel-mcp-server-minio-image.tar

# 配置物理机的excel_files路径
# 配置物理机的config.ini路径
# 启动
docker run -d \
--name excel-mcp-server-minio \
-p 8000:8017 \
-v ./excel_files:/app/excel_files \
-v ./config.ini:/app/conf/config.ini \
-e EXCEL_FILES_PATH="/app/excel_files" \
excel-mcp-server-minio:1.0

# 如何导入大模型平台使用，参考下面Usage部分

# 导入成功后，可以使用下面提示词来测试
1、conversation_id的值为{#每个会话的id#}。
2、有关excel的一切操作都需要调用excel_mcp_server工具
3、每次调用excel_mcp_server都要返回下载链接。
4、用户每次有操作excel的需求时，先查看一下是否有这个文件，如果有则在该文件的基础上修改、计算等。
```



config.ini示例：

```
[minio]
endpoint = ip:port
access_key = xxx
secret_key = xxx
bucket = xxx
secure = false
```





## Features

<p align="center">
  <img src="https://raw.githubusercontent.com/haris-musa/excel-mcp-server/main/assets/logo.png" alt="Excel MCP Server Logo" width="300"/>
</p>

[![PyPI version](https://img.shields.io/pypi/v/excel-mcp-server.svg)](https://pypi.org/project/excel-mcp-server/)
[![Total Downloads](https://static.pepy.tech/badge/excel-mcp-server)](https://pepy.tech/project/excel-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![smithery badge](https://smithery.ai/badge/@haris-musa/excel-mcp-server)](https://smithery.ai/server/@haris-musa/excel-mcp-server)
[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=excel-mcp-server&config=eyJjb21tYW5kIjoidXZ4IGV4Y2VsLW1jcC1zZXJ2ZXIgc3RkaW8ifQ%3D%3D)

A Model Context Protocol (MCP) server that lets you manipulate Excel files without needing Microsoft Excel installed. Create, read, and modify Excel workbooks with your AI agent.



- 📊 **Excel Operations**: Create, read, update workbooks and worksheets
- 📈 **Data Manipulation**: Formulas, formatting, charts, pivot tables, and Excel tables
- 🔍 **Data Validation**: Built-in validation for ranges, formulas, and data integrity
- 🎨 **Formatting**: Font styling, colors, borders, alignment, and conditional formatting
- 📋 **Table Operations**: Create and manage Excel tables with custom styling
- 📊 **Chart Creation**: Generate various chart types (line, bar, pie, scatter, etc.)
- 🔄 **Pivot Tables**: Create dynamic pivot tables for data analysis
- 🔧 **Sheet Management**: Copy, rename, delete worksheets with ease
- 🔌 **Triple transport support**: stdio, SSE (deprecated), and streamable HTTP
- 🌐 **Remote & Local**: Works both locally and as a remote service

## Usage

The server supports three transport methods:

### 1. Stdio Transport (for local use)

```bash
uvx excel-mcp-server stdio
```

```json
{
   "mcpServers": {
      "excel": {
         "command": "uvx",
         "args": ["excel-mcp-server", "stdio"]
      }
   }
}
```

### 2. SSE Transport (Server-Sent Events - Deprecated)

```bash
uvx excel-mcp-server sse
```

**SSE transport connection**:
```json
{
   "mcpServers": {
      "excel": {
         "url": "http://localhost:8000/sse",
      }
   }
}
```

### 3. Streamable HTTP Transport (Recommended for remote connections)

```bash
uvx excel-mcp-server streamable-http
```

**Streamable HTTP transport connection**:
```json
{
   "mcpServers": {
      "excel": {
         "url": "http://localhost:8000/mcp",
      }
   }
}
```

## Environment Variables & File Path Handling

### SSE and Streamable HTTP Transports

When running the server with the **SSE or Streamable HTTP protocols**, you **must set the `EXCEL_FILES_PATH` environment variable on the server side**. This variable tells the server where to read and write Excel files.
- If not set, it defaults to `./excel_files`.

You can also set the `FASTMCP_PORT` environment variable to control the port the server listens on (default is `8017` if not set).
- Example (Windows PowerShell):
  ```powershell
  $env:EXCEL_FILES_PATH="E:\MyExcelFiles"
  $env:FASTMCP_PORT="8007"
  uvx excel-mcp-server streamable-http
  ```
- Example (Linux/macOS):
  ```bash
  EXCEL_FILES_PATH=/path/to/excel_files FASTMCP_PORT=8007 uvx excel-mcp-server streamable-http
  ```

### Stdio Transport

When using the **stdio protocol**, the file path is provided with each tool call, so you do **not** need to set `EXCEL_FILES_PATH` on the server. The server will use the path sent by the client for each operation.

## Available Tools

The server provides a comprehensive set of Excel manipulation tools. See [TOOLS.md](TOOLS.md) for complete documentation of all available tools.

## License

MIT License - see [LICENSE](LICENSE) for details.
