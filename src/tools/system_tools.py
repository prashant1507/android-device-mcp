from typing import Optional
from mcp.server.fastmcp import FastMCP

from src.device_management import clear_logs, get_logs, execute_shell


def register_system_tools(mcp: FastMCP):
    """Register system monitoring and shell command tools with the MCP server"""
    
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

    @mcp.tool(name="execute_shell_command", title="Execute shell command",
              description="Execute shell command in an Android device.")
    async def execute_shell_command_tool(serial: str, command: str):
        """
        Execute shell command in a connected Android device.
        E.g., If you want to execute `adb shell ls /sdcard/` then just provide `ls /sdcard`
        """
        return await execute_shell(serial, command)
