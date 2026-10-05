import os
import sys

# 서브모듈(dart_module, ecos_module) 경로를 시스템 경로에 등록
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "dart_module"))
sys.path.append(os.path.join(current_dir, "ecos_module"))

from mcp.server.fastmcp import FastMCP

# 1. FastMCP 인스턴스 정의 (NameError 방지)
mcp = FastMCP("Unified-Connector")

# 2. 독립 모듈 등록 시도 (에러 발생 시에도 서버 다운 방지 예외처리)
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

# 3. 서버 실행
if __name__ == "__main__":
    mcp.run(transport="sse")