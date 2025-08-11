from mcp.server.fastmcp import FastMCP

from src.tools.device_tools import register_device_tools
from src.tools.app_tools import register_app_tools
from src.tools.file_tools import register_file_tools
from src.tools.system_tools import register_system_tools

# Create the MCP server instance
mcp = FastMCP("android-device-mcp")

# Register all tool categories
register_device_tools(mcp)
register_app_tools(mcp)
register_file_tools(mcp)
register_system_tools(mcp)

if __name__ == "__main__":
    pass