# 기존 코드:
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8000))
#     mcp.run(transport="sse", port=port, host="0.0.0.0")

# 수정 후:
if __name__ == "__main__":
    mcp.run(transport="sse")