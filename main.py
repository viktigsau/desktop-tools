#!.venv/bin/python3

from config import Config
import subprocess
import os
import time


config = Config('config.json')

try:
    config.set("user", os.getlogin())
except OSError:
    if "user" not in config:
        raise UserWarning("user is not defined and cant be found please insert manuly by edeting the config.json and adding \"user\":\"your user\"")

def startTool(tool: dict):
    path = os.path.abspath(tool["path"])
    try:
        subprocess.run([path, config.get("user")])
    except FileNotFoundError:
        tools = config.get("tools")
    if not tools:
        print("No tools found in the configuration.")
        return

    for tool in tools:
        print("starting:", tool["name"])
        startTool(tool)

def main():
    for tool in config.get("tools"):
        print("starting:", tool["name"])
        startTool(tool)
    
    while True:
        time.sleep(1)

if __name__ == '__main__':
    print("starting...")
    main()