import json

from src.adb_manager import run_adb


async def get_app_details(serial: str, app_package_name: str):
    """Get details of an installed application by app name or package name"""
    try:
        code, app_details_out, err = await run_adb("-s", serial, "shell", "dumpsys", "package", app_package_name)
        if code != 0:
            raise RuntimeError(f"adb failed to get package details: {err.strip()}")
        else:
            info = {}
            lines = app_details_out.split('\n')
            for line in lines:
                line = line.strip()
                if 'versionName=' in line:
                    info['versionName'] = line.split('versionName=')[1].split()[0]
                elif 'targetSdk=' in line:
                    info['targetSdk'] = line.split('targetSdk=')[1].split()[0]
                elif 'firstInstallTime=' in line:
                    info['firstInstallTime'] = line.split('firstInstallTime=')[1].split()[0]
                elif 'lastUpdateTime=' in line:
                    info['lastUpdateTime'] = line.split('lastUpdateTime=')[1].split()[0]

            return json.dumps(info, indent=4)
    except Exception as e:
        return f"Failed to get package/app details for device '{serial}': {str(e)}"


async def install_app(serial: str, apk_path: str):
    """Install an app in an Android device using apk."""
    try:
        code, app_details_out, err = await run_adb("-s", serial, "install", apk_path)
        if code != 0:
            raise RuntimeError(f"adb failed to install app using apk: {err.strip()}")
        else:
            return f"App installed successfully in device '{serial}'"
    except Exception as e:
        return f"Failed to install app using apk: {serial}: {str(e)}"


async def uninstall_app(serial: str, app_package_name: str):
    """Uninstall an app from an Android device using app or package name"""
    try:
        code, app_details_out, err = await run_adb("-s", serial, "uninstall", app_package_name)
        if code != 0:
            raise RuntimeError(f"adb failed to uninstall app: {err.strip()}")
        else:
            return f"App uninstalled successfully from device '{serial}'"
    except Exception as e:
        return f"Failed to uninstall app: {serial}: {str(e)}"


async def launch_app(serial: str, package_name: str):
    """Launch an app in an Android device using app or package name"""
    try:
        code, app_details_out, err = await run_adb("-s", serial, "shell",  "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1")
        if code != 0:
            raise RuntimeError(f"adb failed to launch an app: {err.strip()}")
        else:
            return f"App launched successfully in device '{serial}'"
    except Exception as e:
        return f"Failed to uninstall app: {serial}: {str(e)}"