Option Explicit

Dim shell, command
Set shell = CreateObject("WScript.Shell")
shell.CurrentDirectory = "D:\Documents\Dev\projects\tg-analyst-userbot"
command = """D:\Documents\Dev\projects\tg-analyst-userbot\venv\Scripts\python.exe"" ""D:\Documents\Dev\projects\tg-analyst-userbot\main.py"""
shell.Run command, 0, False
Set shell = Nothing
