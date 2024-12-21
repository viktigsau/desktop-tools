#!.venv/bin/python3
import keyboard
import pymsgbox
import pyperclip
import time
import sys
import os
sys.path.append(f'/home/{os.getlogin()}/Desktop/Private/desktop-tools')
import config

def main():
    def to_hex(hex: bytes | None=None, text: str | None=None, split: int=1, encoding: str |None=None):
        if hex:
            length = len(hex)
            out = []
            for i in range(0, length, split):
                out.append(hex[i:][:split].hex())
            return "0x"+" 0x".join(out)
        byte = text.encode(encoding)
        length = len(text)
        out = []
        for i in range(0, length, split):
            out.append(byte[i:][:split].hex())
        return "0x"+" 0x".join(out)

    encodings = {
        "ascii":{"bytes":2, "bits":7},
        "utf-8":{"bytes":2, "bits":8},
        "utf-16":{"bytes":4, "bits":16},
        "utf-32":{"bytes":8, "bits":32},
    }

    def write_hex():
        char = pymsgbox.prompt(title="Hex Value")
        encoding = config.enshure("HexTools.Encoding", "utf-8")

        chars = bytes.fromhex(char.removeprefix("0x")).decode(encoding)

        pyperclip.copy(chars)
        pymsgbox.alert(text=f"Copied to clipboard: {chars}", title="Hex to Text")

    def inspect_str():
        clipboard = pyperclip.paste()
        try:
            text = [
                f"Value: {clipboard}",
                *(f"Encoding: {i}\nHex Value: {to_hex(text=clipboard, split=encodings[i]['bytes'], encoding=i)}" for i in encodings.keys())
            ]
        except TypeError:
            pymsgbox.alert(text="an error ocured, are you shure you have something in your clipboard?", title="Error")
            return
        pymsgbox.alert(text="\n".join(text), title="Inspect Clipboard")

    write_path = "HexTools.keyBinds.write"
    inspect_path = "HexTools.keyBinds.inspect"

    keyboard.add_hotkey(config.enshure(write_path, "ctrl+f8"), write_hex)

    keyboard.add_hotkey(config.enshure(inspect_path, "ctrl+f9"), inspect_str)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()