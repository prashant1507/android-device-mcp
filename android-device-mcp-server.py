from typing import Optional

from mcp.server.fastmcp import FastMCP

from src.device_management import reboot_device, shutdown_device, take_screenshot, list_devices, screen_recording, \
    list_installed_apps, clear_logs, get_logs
from src.file_system import list_files, pull_file, push_file

mcp = FastMCP("android-device-mcp")


@mcp.tool(name="list_devices", title="List Devices",
          description="List all connected Android devices with their serial numbers and detailed info.")
async def list_devices_tool():
    """Returns a list of connected Android devices with serial numbers and detailed information."""
    return await list_devices()


@mcp.tool(name="reboot_device", title="Reboot Device",
          description="Reboot a specific Android device using its serial number.")
async def reboot_device_tool(serial: str):
    """Reboots the Android device identified by the given serial number."""
    return await reboot_device(serial)


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


@mcp.tool(name="list_files", title="List Files",
          description="List all files in a given directory on an Android device using its serial number.")
async def list_files_tool(serial: str, file_path_in_device: str):
    """Lists all files in the specified directory on the Android device identified by the serial number."""
    return await list_files(serial, file_path_in_device)


@mcp.tool(name="pull_file", title="Copy Files from Device",
          description="Pull or copy files from a given directory on an Android device using its serial number.")
async def pull_file_tool(serial: str, file_path_in_device: str, local_folder: Optional[str] = None):
    """Pull or copy a file from the specified directory on the Android device identified by the serial number."""
    return await pull_file(serial, file_path_in_device, local_folder)


@mcp.tool(name="push_file", title="Copy File to Device",
          description="Push or copy files from a given directory on local machine to an Android device using its serial number.")
async def push_file_tool(serial: str, local_file: str, folder_path_in_device: str):
    """Push or copy a file from the specified local directory to the Android device identified by the serial number."""
    return await push_file(serial, local_file, folder_path_in_device)


@mcp.tool(name="list_installed_apps", title="List Installed Applications",
          description="List all installed applications on a specific Android device")
async def list_installed_apps_tool(serial: str):
    """List installed applications on a specific Android device"""
    return await list_installed_apps(serial)


@mcp.tool(name="clear_device_logs", title="Clears Logs",
          description="Clear logs from logcat on a specific Android device")
async def clear_device_logs_tool(serial: str):
    """Clear logs from logcat on a specific Android device"""
    return await clear_logs(serial)


@mcp.tool(name="get_device_logs", title="Get and Save Logs",
          description="Get and save logs from logcat on a specific Android device")
async def get_device_logs_tool(serial: str, time_out: float = 10.0, local_log_file_path: Optional[str] = None):
    """Get and save logs from logcat on a specific Android device"""
    return await get_logs(serial, time_out, local_log_file_path)
