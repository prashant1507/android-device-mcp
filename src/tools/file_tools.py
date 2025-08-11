from typing import Optional
from mcp.server.fastmcp import FastMCP

from src.file_system import list_files, pull_file, push_file


def register_file_tools(mcp: FastMCP):
    """Register file system tools with the MCP server"""
    
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
