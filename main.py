# -*- coding : utf-8 -*-
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

def render_reg_for_empty_area(text):
	reg = f'''
	[HKEY_CLASSES_ROOT\Directory\Background\shell\wt]
	@="{text}"
	"Icon"="{icon_path},0"

	[HKEY_CLASSES_ROOT\Directory\Background\shell\wt\command]
	@="{terminal_path} -d ."
	'''
	return reg

def render_reg_for_selected_dir(text):
	reg = f'''
	[HKEY_CLASSES_ROOT\Directory\shell\wt]
	@="{text}"
	"Icon"="{icon_path},0"

	[HKEY_CLASSES_ROOT\Directory\shell\wt\command]
	@="{terminal_path} -d %V"

	'''
	return reg

def creat_right_click_menu():
	text  = input('请输入右键菜单文字（默认为：在此打开Windows Terminal）\n')
	if text == '':
		text = '在此打开Windows Terminal'
	with open('wt.reg', 'w') as f:
		f.writelines('Windows Registry Editor Version 5.00')
		f.write(render_reg_for_empty_area(text))
		f.write(render_reg_for_selected_dir(text))
	os.system('regedit /s wt.reg')
	os.system('del wt.reg')

def del_right_click_menu():
	with open('del-wt.reg', 'w') as f:
		f.write('Windows Registry Editor Version 5.00\n')
		f.write('[-HKEY_CLASSES_ROOT\Directory\Background\shell\wt]\n')
		f.write('[-HKEY_CLASSES_ROOT\Directory\shell\wt]\n')
	os.system('regedit /s del-wt.reg')
	os.system('del del-wt.reg')

def choose_function():
	menu_content = '''Windows Terminal 右键菜单添加脚本
	请选择功能：
	1.添加菜单
	2.删除菜单
	3.退出
	'''
	print(menu_content)
	while True:
		choice = input('请输入功能选项\n')
		if choice in ('1', '2', '3'):
			return int(choice)
		else:
			print('输入有误')


if __name__ == '__main__':
	if is_admin():
		icon_path = get_icon_path()
		terminal_path = get_terminal_path()
		choice = choose_function()
		if choice == 1:
			creat_right_click_menu()
		elif choice == 2:
			del_right_click_menu()
		elif choice == 3:
			sys.exit()
		print('完成')
		os.system('pause')
	else:
		print('请以管理员身份运行脚本')
		