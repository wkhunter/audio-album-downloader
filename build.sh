#!/usr/bin/env bash
# windows 可执行文件需要在 windows 环境下打包，可使用 wine 或者虚拟机
rm -r build
rm -r dist
pyinstaller main.py --onefile
# windows
# pyinstaller main.py --onefile --noupx --icon=icon.ico
