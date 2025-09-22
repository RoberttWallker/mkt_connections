from pathlib import Path

#---------------------------------------------------------------------------------------
# Pastas principais
ROOT_PATH = Path(__file__).resolve().parent.parent
schedule_path = ROOT_PATH / "app_schedule"
bat_vbs_files_path = "bat_vbs_files"

#---------------------------------------------------------------------------------------
# Pastas secundárias
graph_api_path = ROOT_PATH / "graph_api"
google_ads_api_path = ROOT_PATH / "google_ads_api"

#---------------------------------------------------------------------------------------
# Arquivos principais
# Facebook
facebook_download_all_data_path = schedule_path / "facebook_download_all_data.py"
facebook_check_token_validity_path = schedule_path / "facebook_check_token_validity.py"
gui_update_token_path = graph_api_path / "gui_tkinter.pyw"

# Google
google_download_all_data_path = schedule_path / "google_download_all_data.py"

#---------------------------------------------------------------------------------------
# FUNÇÕES DE AGENDAMENTO FACEBOOK
def facebook_automation():
    bat_file = schedule_path / bat_vbs_files_path / "facebook_schedule.bat"
    vbs_file = schedule_path / bat_vbs_files_path / "facebook_ghost_schedule.vbs"

    for file in (bat_file, vbs_file):
        file.parent.mkdir(parents=True, exist_ok=True)

    bat_content = f"""
        @echo off
        pushd "{str(ROOT_PATH)}"
        call venv\\Scripts\\activate
        python "{str(facebook_download_all_data_path)}"
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

def facebook_check_validity():
    bat_file = schedule_path / bat_vbs_files_path / "facebook_check_token_validity.bat"
    vbs_file = schedule_path / bat_vbs_files_path / "facebook_ghost_token_validity.vbs"

    for file in (bat_file, vbs_file):
        file.parent.mkdir(parents=True, exist_ok=True)

    bat_content = f"""
        @echo off
        pushd "{str(ROOT_PATH)}"
        call venv\\Scripts\\activate
        python "{str(facebook_check_token_validity_path)}"
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

def facebook_gui_update_token():
    bat_file = schedule_path / bat_vbs_files_path / "facebook_gui_update_token.bat"
    vbs_file = schedule_path / bat_vbs_files_path / "facebook_gui_update_token.vbs"

    for file in (bat_file, vbs_file):
        file.parent.mkdir(parents=True, exist_ok=True)

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

# FUNÇÕES DE AGENDAMENTO GOOGLE
def google_automation():
    bat_file = schedule_path / bat_vbs_files_path / "google_schedule.bat"
    vbs_file = schedule_path / bat_vbs_files_path / "google_ghost_schedule.vbs"

    for file in (bat_file, vbs_file):
        file.parent.mkdir(parents=True, exist_ok=True)

    bat_content = f"""
        @echo off
        pushd "{str(ROOT_PATH)}"
        call venv\\Scripts\\activate
        python "{str(google_download_all_data_path)}"
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
    facebook_check_validity()
    facebook_automation()
    facebook_gui_update_token()
    google_automation()

if __name__ == "__main__":
    print("Iniciando o aplicativo.")
    main()
