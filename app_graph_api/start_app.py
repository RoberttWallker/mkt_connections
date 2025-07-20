from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent
schedule_path = ROOT_PATH / "schedule_graph_api"

py_file = schedule_path / "download_all_data.py"

def main():
    bat_file = schedule_path / "schedule.bat"
    vbs_file = schedule_path / "ghost_schedule.vbs"

    bat_content = f"""
        @echo off
        cd "{str(ROOT_PATH)}"
        call venv\\Scripts\\activate
        python "{str(py_file)}"
        pause
    """

    vbs_content = f"""
        Set WshShell = CreateObject("WScript.Shell")
        WshShell.Run chr(34) & "{str(bat_file)}" & chr(34), 0
        Set WshShell = Nothing
    """

    with open(bat_file, "w") as bat:
        bat.write(bat_content)

    with open(vbs_file, "w") as bat:
        bat.write(vbs_content)

if __name__ == "__main__":
    print("Iniciando o aplicativo.")
    main()
