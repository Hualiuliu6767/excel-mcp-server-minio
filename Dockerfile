FROM astral/uv:python3.10-bookworm-slim

WORKDIR /app

COPY . /app/excel-mcp-server

WORKDIR /app/excel-mcp-server
RUN uv sync --default-index https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["uv", "run", "excel-mcp-server"]
CMD ["sse"]