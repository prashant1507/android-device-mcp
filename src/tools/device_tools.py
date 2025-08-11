from typing import Optional

from mcp.server.fastmcp import FastMCP

from src.device_management import reboot_device, shutdown_device, take_screenshot, list_devices, screen_recording, \
    get_network_details, dump_screen


def register_device_tools(mcp: FastMCP):
    """Register device management tools with the MCP server"""

    @mcp.tool(name="list_devices", title="List Devices",
              description="List all connected Android devices with their serial numbers and detailed info.")
    async def list_devices_tool():
        """Returns a list of connected Android devices with serial numbers and detailed information."""
        return await list_devices()

    @mcp.tool(name="reboot_device", title="Reboot Device",
              description="Reboot a specific Android device using its serial number.")
    async def reboot_device_tool(serial: str, mode: Optional[str] = None):
        """
            Reboots the Android device identified by the given serial number.
            Device can be rebooted in any desired mode
        """
        return await reboot_device(serial, mode)

    @mcp.tool(name="shutdown_device", title="Shutdown Device",
              description="Shut down a specific Android device using its serial number.")
    async def shutdown_device_tool(serial: str):
        """Shuts down the Android device identified by the given serial number."""
        return await shutdown_device(serial)

    @mcp.tool(name="take_screenshot", title="Take Screenshot",
              description="Capture a screenshot from an Android device using its serial number.")
    async def take_screenshot_tool(serial: str, local_file_path: Optional[str] = None):
        """Captures a screenshot from the Android device identified by the given serial number."""
        return await take_screenshot(serial, local_file_path)

    @mcp.tool(name="screen_recording", title="Screen Recording",
              description="Record the screen of an Android device using its serial number.")
    async def screen_recording_tool(serial: str, time_limit: str = "5", local_file_path: Optional[str] = None):
        """Records the screen of the Android device identified by the given serial number."""
        return await screen_recording(serial, time_limit, local_file_path)

    @mcp.tool(name="dump_screen", title="Dump screen",
              description="Dump current screen of Android device.")
    async def dump_screen_tool(serial: str, local_file_path: Optional[str] = None):
        """Dump current screen of an Android screen in .xml file"""
        return await dump_screen(serial, local_file_path)

    @mcp.tool(name="get_network_details", title="Get network details",
              description="Retrieve network, Wi-Fi information for an Android device by serial number.")
    async def network_details_tool(serial: str):
        """Retrieve network, Wi-Fi information for a connected Android device."""
        return await get_network_details(serial)
