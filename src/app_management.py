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
