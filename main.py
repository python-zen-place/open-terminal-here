import ctypes
import getpass
import glob
import os
import sys
import time

# 检查管理员权限
is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
if not is_admin:
	print('请以管理员身份运行脚本')
	sys.exit()

# 查找图标
icon_path = glob.glob('C:/Program Files/WindowsApps/Microsoft.WindowsTerminal*/WindowsTerminal.exe')
if len(icon_path) == 0:
	print('找不到图标')
else:
	icon_path = icon_path[0]

# 查找wt.exe
user = getpass.getuser()
terminal_path = f'C:\\Users\\{user}\\AppData\\Local\\Microsoft\\WindowsApps\\wt.exe'
if len(terminal_path) == 0:
	print('找不到Windows Terminal.exe')

text = input('自定义右键菜单文字（默认为： Open Windows Terminal here）\n')
print(text)
if text == '':
	text = 'Open Windows Terminal here'

reg = f'''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\Background\shell\wt]
@="{text}"
"Icon"="{icon_path},0"

[HKEY_CLASSES_ROOT\Directory\Background\shell\wt\command]
@="{terminal_path} -d ."
'''
with open('00101000.reg', 'w') as f:
	print('正在生成注册表文件')
	f.write(reg)
	print('成功生成')

print('正在导入到你的注册表')
time.sleep(3)
os.system('regedit /s 00101000.reg')
print('导入成功')
os.system('pause')