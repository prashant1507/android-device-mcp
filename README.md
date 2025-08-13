<img src="https://github.com/prashant1507/android-device-mcp/blob/main/resources/mcp.png" alt="Android MCP" width="200">


# Android Device MCP

A Model Context Protocol (MCP) server that provides comprehensive Android device management capabilities through ADB (Android Debug Bridge). This tool allows you to interact with Android devices programmatically for device management, app management, file operations, and system monitoring.

---

## Features

### Device Management

- **List Devices**: Get detailed information about all connected Android devices, including OS version, hardware specs,
  battery status, and network details
- **Device Control**: Reboot and shut down devices with optional boot modes
- **Screenshots**: Capture device screenshots and save them locally
- **Screen Recording**: Record device screen activity for specified durations
- **Screen Dump**: Export current screen layout as XML for UI automation
- **Network Information**: Retrieve Wi-Fi details, IP addresses, and connection status

### App Management

- **List Installed Apps**: Get a complete list of installed applications with package names
- **App Details**: Retrieve detailed information about specific apps (version, SDK, install dates)
- **Install Apps**: Install APK files on connected devices
- **Uninstall Apps**: Remove applications from devices
- **Launch Apps**: Start applications on devices

### File System Operations

- **List Files**: Browse directories on Android devices
- **Pull Files**: Copy files from devices to the local system
- **Push Files**: Copy files from the local system to the devices
- **Remove Files**: Delete files from devices

### System Monitoring

- **Log Management**: Clear and capture device logs (logcat)
- **Shell Commands**: Execute arbitrary shell commands on devices
- **Real-time Logging**: Collect logs for specified durations

## Prerequisites

- Python 3.13 or higher
- ADB (Android Debug Bridge) installed and accessible in PATH
- Android device(s) connected via USB with USB debugging enabled
- Device(s) authorized for ADB access
- UV is installed

## Installation

1. Clone the repository:

```bash
git clone https://github.com/prashant1507/android-device-mcp.git
cd android-device-mcp
```

2. Install dependencies using uv (recommended) or pip:

```bash
# Using uv
uv sync
```

3. Configure your MCP client (LM Studio, CursorAI, Claude, etc.) to use the Android Device MCP server:

```json
{
  "mcpServers": {
    "android-device-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "./android-device-mcp-server.py"
      ],
      "cwd": "/path/to/android-device-mcp"
    }
  }
}
```

**Note**: Replace `/path/to/android-device-mcp` with the actual path to your project directory.

---

## Error Handling

All functions include comprehensive error handling and will return descriptive error messages if operations fail. Common
error scenarios include:

- Device not connected or unauthorized
- ADB server not running
- Invalid file paths
- Insufficient permissions
- Timeout errors for long-running operations

---

## Troubleshooting

### Device Not Detected

1. Ensure USB debugging is enabled on the device
2. Check that the device is authorized for ADB access
3. Verify ADB is properly installed and in PATH
4. Try restarting the ADB server: `adb kill-server && adb start-server`

### Permission Errors

- Ensure the device is unlocked and authorized
- Check that the app has the necessary permissions
- For file operations, verify the target directories are writable

### Timeout Issues

- Increase timeout values for slow devices or large file transfers
- Check device performance and available storage
- Ensure a stable USB connection

---

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

## Acknowledgments

This project leverages the Android Debug Bridge (ADB) for device communication and the Model Context Protocol (MCP) for
tool integration.
