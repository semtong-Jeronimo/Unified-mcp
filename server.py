import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "dart_module"))
sys.path.append(os.path.join(current_dir, "ecos_module"))

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Unified-Connector")

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

if __name__ == "__main__":
    # Render 환경변수 PORT를 바인딩하고 host를 0.0.0.0으로 명시
    import uvicorn
    # fastmcp의 내장 sse / mcp 앱 인스턴스 실행
    port = int(os.environ.get("PORT", 10000))
    # mcp의 sse app을 uvicorn으로 직접 구동
    uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=port)