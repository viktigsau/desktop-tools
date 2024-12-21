#!.venv/bin/python3

import config
import subprocess
import os


def startTool(tool: dict):
    path = os.path.abspath(tool["path"])
    subprocess.run([path])

def main():
    for tool in config.get("tools"):
        startTool(tool)

if __name__ == '__main__':
    main()