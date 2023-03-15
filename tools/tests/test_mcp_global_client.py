import os
import sys
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_script = os.path.join(os.path.expanduser('~'), '.trae', 'mcp', 'langchain', 'server.py')
    python_cmd = sys.executable
    params = StdioServerParameters(command=python_cmd, args=[server_script])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            tool_list = getattr(tools_result, 'tools', tools_result)
            try:
                count = len(tool_list)
            except Exception:
                count = 0
            print('TOOLS COUNT:', count)

            result = await session.call_tool('ping', { 'message': 'global' })
            print('PING:', getattr(result, 'content', result))


if __name__ == '__main__':
    asyncio.run(main())