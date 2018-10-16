cp __main__.py b9y-cli.py
rm -rf dist build
pyinstaller --onefile b9y-cli.py
