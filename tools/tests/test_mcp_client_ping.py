import os
import sys
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Aponta para o servidor local em tools/dev
    server_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dev', 'mcp_langchain_server.py')
    python_cmd = sys.executable
    params = StdioServerParameters(command=python_cmd, args=[server_script])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # List available tools to confirm handshake
            tools = await session.list_tools()
            try:
                names = [getattr(t, 'name', None) or (t['name'] if isinstance(t, dict) else str(t)) for t in tools]
            except Exception:
                names = [str(t) for t in tools]
            print('TOOLS:', names)

            # Call the ping tool
            result = await session.call_tool('ping', { 'message': 'hello' })
            print('PING RESULT:', getattr(result, 'content', result))


if __name__ == '__main__':
    asyncio.run(main())