#!.venv/bin/python3

import os
import sys
import config
import subprocess
import stat


try:
    user = sys.argv[1]
except IndexError:
    print("please give a user")
    exit()

def install():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    destination = os.path.join(f'/home/{user}', "snap", os.path.basename(script_dir))

    if not os.path.exists(f'/home/{user}'):
        print("the user given is invalid")
        exit()

    if os.path.exists(destination):
        os.system(f'rm -rf {destination}')

    os.system(f'cp -r {script_dir} {destination}')

    try:
        subprocess.run(['chown', '-R', user, destination], check=True)
        print(f"Ownership of '{destination}' changed to {user}.")
    except Exception as e:
        print(f"Failed to change ownership: {e}")
        return

    # Set permissions to read, write, and execute for the user
    try:
        os.chmod(destination, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        print(f"Permissions for '{destination}' have been set.")
    except Exception as e:
        print(f"Failed to set permissions: {e}")

    service = config.get('service')
    os.system(f'touch /etc/systemd/system/{service}')

    with open(f'/etc/systemd/system/{service}', 'w') as f:
        with open(f'{service}') as service_file:
            f.write(service_file.read().replace('__dir__', destination))

    os.system(f'systemctl daemon-reload')
    os.system(f'systemctl enable {service}')
    os.system(f'systemctl restart {service}')

if __name__ == '__main__':
    install()