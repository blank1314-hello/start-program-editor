#start program
import os
import winreg as reg
import time
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def run_as_admin():
    if not is_admin():
        print("관리자 권한이 아닙니다. 관리자 권한으로 재실행합니다.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def wrong():
    print("it was wrong command.")
    time.sleep(1)

def open_registry_key():
    """레지스트리 키를 열어 반환합니다."""
    return reg.OpenKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, reg.KEY_SET_VALUE)

def add_to_startup(exe_path):
    """주어진 exe 파일 경로를 시작 프로그램에 추가합니다."""
    try:
        with open_registry_key() as key:
            reg.SetValueEx(key, os.path.basename(exe_path), 0, reg.REG_SZ, os.path.abspath(exe_path))
        print(f"{exe_path}was added on start menu.")
    except Exception as e:
        print(f"오류 발생: {e}")

def remove_from_startup(app_name):
    """주어진 프로그램 이름을 시작 프로그램에서 제거합니다."""
    try:
        with open_registry_key() as key:
            reg.DeleteValue(key, app_name)
        print(f"{app_name} was deleted on start menu.")
    except FileNotFoundError:
        print(f"{app_name} is not in start menu.")
    except Exception as e:
        print(f"wrong: {e}")

def main():
    run_as_admin()
    action = input("what do you want?: ").strip().lower()

    if action == 'add':
        exe_file = input("type path about the program to add:").strip().strip('"')
        if os.path.isfile(exe_file):
            add_to_startup(exe_file)
            main()
        else:
            wrong()

    elif action == 'delete':
        app_name = input("type program's name to delete:").strip()
        remove_from_startup(app_name)
        main()

    else:
        wrong()

if __name__ == "__main__":
    main()
    h = input("type 'q':")
    if h == 'q':
        print("bye~")
        time.sleep(0.5)
