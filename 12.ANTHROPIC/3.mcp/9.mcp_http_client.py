import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "http://localhost:8000/mcp"

async def main():
    async with streamable_http_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = (await session.list_tools()).tools
            print("도구: ", [t.name for t in tools])

if __name__ == "__main__":
    asyncio.run(main())