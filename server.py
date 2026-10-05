import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "dart_module"))
sys.path.append(os.path.join(current_dir, "ecos_module"))
sys.path.append(os.path.join(current_dir, "onbid_module"))  
sys.path.append(os.path.join(current_dir, "auction_module"))

from fastmcp import FastMCP

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

 
try:
    from onbid_tools import register_onbid_tools
    register_onbid_tools(mcp)
    print("ONBID 도구 등록 성공")
except Exception as e:
    print(f"ONBID 도구 로드 중 경고: {e}")

try:
    from auction_tools import register_auction_tools
    register_auction_tools(mcp)
    print("AUCTION 도구 등록 성공")
except Exception as e:
    print(f"AUCTION 도구 로드 중 경고: {e}")
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    mcp.run(transport="http", host="0.0.0.0", port=port)