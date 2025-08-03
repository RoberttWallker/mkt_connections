from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent
schedule_path = ROOT_PATH / "app_schedule"
graph_api_path = ROOT_PATH / "graph_api"

download_all_data_path = schedule_path / "download_all_data.py"
check_token_validity_path = schedule_path / "check_token_validity.py"
gui_update_token_path = graph_api_path / "gui_tkinter.pyw"

def automation():
    bat_file = schedule_path / "schedule.bat"
    vbs_file = schedule_path / "ghost_schedule.vbs"

    bat_content = f"""
        @echo off
        pushd "{str(ROOT_PATH)}"
        call venv\\Scripts\\activate
        python "{str(download_all_data_path)}"
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
        python "{str(check_token_validity_path)}"
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

def gui_update_token():
    bat_file = schedule_path / "gui_update_token.bat"
    vbs_file = schedule_path / "gui_update_token.vbs"

    bat_content = f"""
        @echo off
        pushd "{str(ROOT_PATH)}"
        call venv\\Scripts\\activate
        python "{str(gui_update_token_path)}"
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
    gui_update_token()

if __name__ == "__main__":
    print("Iniciando o aplicativo.")
    main()
