import os
import sys
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_script = os.path.join(os.path.expanduser('~'), '.trae', 'mcp', 'langchain', 'server.py')
    python_cmd = sys.executable
    params = StdioServerParameters(command=python_cmd, args=[server_script])

    # workspace CSV path
    workspace = os.path.abspath(os.path.join(os.getcwd()))
    csv_path = os.path.join(workspace, 'dados', 'criando_uma_apresentacao_executiva.csv')

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            tool_list = getattr(tools_result, 'tools', [])
            print('TOOLS:', [getattr(t, 'name', str(t)) for t in tool_list])

            # Summarize CSV
            if os.path.exists(csv_path):
                res = await session.call_tool('summarize_csv', {
                    'path': csv_path,
                    'delimiter': ',',
                    'encoding': 'utf-8',
                    'max_rows': 50000,
                })
                print('CSV SUMMARY:', getattr(res, 'content', res))
            else:
                print('CSV not found at:', csv_path)


if __name__ == '__main__':
    asyncio.run(main())