import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(command="python", args=["debug_proxy.py", "2.mcp_server.py"])

    # 입출력 비동기 실행
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
        # server-client간에 handshake가 이루어짐 (json 형태 정보 공유)
            print(f"[CLIENT] 서버와 HS 전", file=sys.stderr)
            await session.initialize()
            print(f"[CLIENT] 서버와 HS 후", file=sys.stderr)

        # 도구
            tools = (await session.list_tools()).tools
            print(f"[CLIENT] 서버가 쓸 수 있는 도구 받아옴. 도구: ", [t.name for t in tools])

            # 서버에 호출하고 싶은 내용
            result = await session.call_tool("hello", {"name": "John"})

            print(result.content[0].text)   # hello, John!

if __name__ == "__main__":
    print(f"[CLIENT] 클라이언트가 시작됨", file=sys.stderr)
    asyncio.run(main())