# fastapi <-- flask 떠올리면 됨
# 실행 시 표준 입출력을 기다리는 상태가 됨

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("HelloWorld")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()