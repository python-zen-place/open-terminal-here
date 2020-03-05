import ctypes
import getpass
import glob
import os
import sys
import time

def is_admin():
	return ctypes.windll.shell32.IsUserAnAdmin() != 0

def  get_icon_path():
	icon_path = glob.glob('C:/Program Files/WindowsApps/Microsoft.WindowsTerminal*/WindowsTerminal.exe')
	if len(icon_path) == 0:
		print('找不到图标')
		sys.exit()
	else:
		return icon_path[0].replace('\\', '/')

def get_terminal_path():
	user = getpass.getuser()
	terminal_path = glob.glob(f'C:\\Users\\{user}\\AppData\\Local\\Microsoft\\WindowsApps\\wt.exe')
	if len(terminal_path) == 0:
		print('找不到Windows Terminal.exe')
		sys.exit()
	else:
		return terminal_path[0].replace('\\', '\\\\')

def choose_function():
	menu_content = '''请选择功能：
	1.为空白区域添加右键菜单：在此打开Windows Terminal
	2.为目录添加右键菜单：在此目录打开Windows Terminal
	3.同时添加1和2中的右键菜单
	4.我不小心按到的，我要退出
	'''
	print(menu_content)
	while True:
		choice = input('请输入功能选项\n')
		if choice in ('1', '2', '3', '4'):
			return int(choice)
		else:
			print('输入有误')

def open_wt_for_empty_area():
	text = input('为右键菜单：在此打开Windows Terminal更改文字'
		'（默认为在此打开Windows Terminal）\n')
	if text == '':
		text = '在此打开Windows Terminal'
	reg = f'''Windows Registry Editor Version 5.00
	[HKEY_CLASSES_ROOT\Directory\Background\shell\wt]
	@="{text}"
	"Icon"="{icon_path},0"

	[HKEY_CLASSES_ROOT\Directory\Background\shell\wt\command]
	@="{terminal_path} -d ."
	'''
	with open('open_wt_for_empty_area.reg', 'w') as f:
		f.write(reg)
	os.system('regedit /s open_wt_for_empty_area.reg')
	os.system('del open_wt_for_empty_area.reg')

def open_wt_for_selected_dir():
	text = input('为右键菜单：在此目录打开Windows Terminal更改文字'
		'（默认为在此目录打开Windows Terminal）\n')
	if text == '':
		text = '在此目录打开Windows Terminal'
	reg = f'''Windows Registry Editor Version 5.00

	[HKEY_CLASSES_ROOT\Directory\shell\wt]
	@="{text}"
	"Icon"="{icon_path},0"

	[HKEY_CLASSES_ROOT\Directory\shell\wt\command]
	@="{terminal_path} -d %V"

	'''
	with open('open_wt_for_selected_dir.reg', 'w') as f:
		f.write(reg)
	os.system('regedit /s open_wt_for_selected_dir.reg')
	os.system('del open_wt_for_selected_dir.reg')

if __name__ == '__main__':
	if is_admin() == False:
		print('请以管理员身份运行脚本')
	else:
		icon_path = get_icon_path()
		terminal_path = get_terminal_path()
		choice = choose_function()
		if choice == 1:
			open_wt_for_empty_area()
		elif choice == 2:
			open_wt_for_selected_dir()
		elif choice == 3:
			open_wt_for_empty_area()
			open_wt_for_selected_dir()
		elif choice == 4:
			sys.exit()
		print('完成')
		os.system('pause')