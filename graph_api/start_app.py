from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent
schedule_path = ROOT_PATH / "app_schedule"

download_all_data = schedule_path / "download_all_data.py"
check_token_validity = schedule_path / "check_token_validity.py"

def automation():
    bat_file = schedule_path / "schedule.bat"
    vbs_file = schedule_path / "ghost_schedule.vbs"

    bat_content = f"""
        @echo off
        pushd "{str(ROOT_PATH)}"
        call venv\\Scripts\\activate
        python "{str(download_all_data)}"
        pause
    """

    vbs_content = f"""
        Set WshShell = CreateObject("WScript.Shell")
        WshShell.Run chr(34) & "{str(bat_file)}" & chr(34), 0
        Set WshShell = Nothing
    """

    with open(bat_file, "w") as bat:
        bat.write(bat_content)

    with open(vbs_file, "w") as vbs:
        vbs.write(vbs_content)

def check_validity():
    bat_file = schedule_path / "check_token_validity.bat"
    vbs_file = schedule_path / "ghost_token_validity.vbs"

    bat_content = f"""
        @echo off
        pushd "{str(ROOT_PATH)}"
        call venv\\Scripts\\activate
        python "{str(check_token_validity)}"
        pause
    """

    vbs_content = f"""
        Set WshShell = CreateObject("WScript.Shell")
        WshShell.Run chr(34) & "{str(bat_file)}" & chr(34), 0
        Set WshShell = Nothing
    """

    with open(bat_file, "w") as bat:
        bat.write(bat_content)

    with open(vbs_file, "w") as vbs:
        vbs.write(vbs_content)

def main():
    check_validity()
    automation()

if __name__ == "__main__":
    print("Iniciando o aplicativo.")
    main()
