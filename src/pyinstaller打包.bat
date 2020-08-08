pyinstaller --hidden-import pkg_resources.py2_warn --noconfirm -w  -i icon.ico QuickHand.py

echo d | xcopy /y /s .\dist\rely .\dist\QuickHand

del /F /Q QuickHand_Win64_pyinstaller.7z

7z a -t7z QuickHand_Win64_pyinstaller.7z .\dist\QuickHand -mx=9 -ms=200m -mf -mhc -mhcf  -mmt -r

pause