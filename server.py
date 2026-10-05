import os
import sys

# 1. 서브모듈(dart_module, ecos_module) 경로 등록
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "dart_module"))
sys.path.append(os.path.join(current_dir, "ecos_module"))

from mcp.server.fastmcp import FastMCP

# 2. FastMCP 인스턴스 생성
mcp = FastMCP("Unified-Connector")

# 3. 도구 등록
try:
    from dart_tools import register_dart_tools
    register_dart_tools(mcp)
    print("DART 도구 등록 성공")
except Exception as e:
    print(f"DART 도구 로드 중 경고: {e}")

try:
    from ecos_tools import register_ecos_tools
    register_ecos_tools(mcp)
    print("ECOS 도구 등록 성공")
except Exception as e:
    print(f"ECOS 도구 로드 중 경고: {e}")

# 4. SSE 표준 구동
if __name__ == "__main__":
    mcp.run(transport="sse")