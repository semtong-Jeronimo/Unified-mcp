import os
from mcp.server.fastmcp import FastMCP

# 각각의 독립 저장소에서 도구 등록 함수 임포트
from dart_tools import register_dart_tools
from ecos_tools import register_ecos_tools

# 통합 FastMCP 서버 인스턴스
mcp = FastMCP("Unified-Connector")

# 두 도구 마운트
register_dart_tools(mcp)
register_ecos_tools(mcp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", port=port, host="0.0.0.0")