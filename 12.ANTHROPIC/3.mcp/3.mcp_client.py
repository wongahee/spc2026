import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(command="python", args=["2.mcp_server.py"])

    # 입출력 비동기 실행
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
        # server-client간에 handshake가 이루어짐 (json 형태 정보 공유)
            await session.initialize()  # 초기화

            # 서버에 호출하고 싶은 내용
            result = await session.call_tool("hello", {"name": "John"})

            print(result.content[0].text)   # hello, John!

if __name__ == "__main__":
    asyncio.run(main())