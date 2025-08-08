from mcp.server.fastmcp import FastMCP

from src.device import list_devices

mcp = FastMCP("android-device-mcp")

@mcp.tool(name="list_devices", description="List connected android devices via ADB with detailed information")
async def list_devices_tool():
    """List connected Android devices with detailed information"""
    return await list_devices()