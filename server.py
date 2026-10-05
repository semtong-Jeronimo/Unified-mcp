import os
import sys

# 서브모듈 폴더 경로를 파이썬 탐색 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), "dart_module"))
sys.path.append(os.path.join(os.path.dirname(__file__), "ecos_module"))

from mcp.server.fastmcp import FastMCP
from dart_tools import register_dart_tools
from ecos_tools import register_ecos_tools

# 단일 MCP 인스턴스 생성
mcp = FastMCP("Unified-Connector")

# 두 도구 마운트
register_dart_tools(mcp)
register_ecos_tools(mcp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", port=port, host="0.0.0.0")