from mcp.server.fastmcp import FastMCP

from src.app_management import get_app_details, install_app, uninstall_app, launch_app
from src.device_management import list_installed_apps


def register_app_tools(mcp: FastMCP):
    """Register app management tools with the MCP server"""
    
    @mcp.tool(name="list_installed_apps", title="List Installed Applications",
              description="List all installed applications on a specific Android device")
    async def list_installed_apps_tool(serial: str):
        """List installed applications on a specific Android device"""
        return await list_installed_apps(serial)

    @mcp.tool(name="get_app_details", title="Get app details",
              description="Retrieve detailed information about an installed app using its name or package name.")
    async def get_app_details_tool(serial: str, app_package_name: str):
        """Fetch details of an installed application by specifying its name or package name."""
        return await get_app_details(serial, app_package_name)

    @mcp.tool(name="install_app", title="Install app",
              description="Install an APK file on an Android device.")
    async def install_app_tool(serial: str, apk_path: str):
        """Install an APK file on a connected Android device."""
        return await install_app(serial, apk_path)

    @mcp.tool(name="uninstall_app", title="Uninstall app",
              description="Uninstall an APP from an Android device.")
    async def uninstall_app_tool(serial: str, app_package_name: str):
        """Uninstall an APP from a connected Android device."""
        return await uninstall_app(serial, app_package_name)

    @mcp.tool(name="launch_app", title="Launch app",
              description="Launch an APP in an Android device.")
    async def launch_app_tool(serial: str, package_name: str):
        """Launch an APP in a connected Android device."""
        return await launch_app(serial, package_name)
