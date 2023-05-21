#██████╗  ██████╗ ██╗   ██╗██╗   ██╗ █████╗     ███████╗██╗  ██╗ █████╗ ██╗  ██╗██████╗ ██████╗  █████╗ ███╗   ███╗██╗
#██╔══██╗██╔═══██╗██║   ██║╚██╗ ██╔╝██╔══██╗    ██╔════╝██║  ██║██╔══██╗██║  ██║██╔══██╗██╔══██╗██╔══██╗████╗ ████║██║
#██████╔╝██║   ██║██║   ██║ ╚████╔╝ ███████║    ███████╗███████║███████║███████║██████╔╝██║  ██║███████║██╔████╔██║██║
#██╔═══╝ ██║   ██║██║   ██║  ╚██╔╝  ██╔══██║    ╚════██║██╔══██║██╔══██║██╔══██║██╔══██╗██║  ██║██╔══██║██║╚██╔╝██║██║
#██║     ╚██████╔╝╚██████╔╝   ██║   ██║  ██║    ███████║██║  ██║██║  ██║██║  ██║██║  ██║██████╔╝██║  ██║██║ ╚═╝ ██║██║
#╚═╝      ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝
                                                                                                                     
import subprocess
import os
import sqlite3
import shutil
import os

def retrieve_wifi_passwords():
    os_type = os.name

    if os_type == 'nt': 
        retrieve_wifi_passwords_windows()
    elif os_type == 'posix': 
        retrieve_wifi_passwords_macos()
    else:
        return

def retrieve_wifi_passwords_windows():
    command_output = subprocess.run('netsh wlan show profiles', capture_output=True, text=True)
    profiles = [line.split(':')[1].strip() for line in command_output.stdout.split('\n') if 'All User Profile' in line]

    with open(os.path.expanduser('~/Desktop/wifi_passwords.txt'), 'w') as file:
        for profile in profiles:
            password_output = subprocess.run(f'netsh wlan show profile name="{profile}" key=clear', capture_output=True, text=True)
            password_lines = password_output.stdout.split('\n')
            password = [line.split(':')[1].strip() for line in password_lines if 'Key Content' in line]
            if password:
                file.write(f"Profile: {profile}\nPassword: {password[0]}\n\n")


def retrieve_wifi_passwords_macos():
    command_output = subprocess.run('security find-generic-password -wa "Wi-Fi"', capture_output=True, text=True)
    password = command_output.stdout.strip()

    with open(os.path.expanduser('~/Desktop/keysaved.txt'), 'w') as file:
        file.write(f"Wi-Fi Password: {password}")


retrieve_wifi_passwords()


