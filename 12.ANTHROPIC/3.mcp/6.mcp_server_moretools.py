from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-more-tool-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """ 두 정수 a와 b를 더한다 """
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """ 두 정수 a와 b를 곱한다 """
    return a * b

@mcp.tool()
def word_count(text: str) -> int:
    """ 주어진 문장에서 단어 갯수를 센다 """
    return len(text.split())    # ['hello', 'world']

if __name__ == "__main__":
    mcp.run()