#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import sys

def check_dependencies():
    """檢查依賴"""
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def clean_build_dirs():
    """清理之前的建置目錄"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def create_spec_file():
    """創建 spec"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('default', 'default'),
        ('resources.py', '.'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'keyboard',
        'tkinter',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KeyBoard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('KeyBoard.spec', 'w', encoding='utf-8') as f: # 改name
        f.write(spec_content)
    print("已新增spec")

def build_exe():

    result = subprocess.run([
        'pyinstaller', 'KeyBoard.spec', '--clean'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("exe success")
        return True
    else:
        print("exe fail")
        print("result:",result.stderr)
        return False

def copy_user_folder():
    """複製資料夾"""
    if os.path.exists('user'):
        dist_user_path = os.path.join('dist', 'user')
        if os.path.exists(dist_user_path):
            shutil.rmtree(dist_user_path)
        shutil.copytree('user', dist_user_path)
        print("已複製")
    else:
        print("跳過複製")

def create_readme():
    """在 dist 目錄創建說明檔案"""
    readme_content = """KeyBoard 鍵盤偵測工具

使用說明：
1. 程式會自動偵測鍵盤按鍵
2. 在 user 資料夾中放入自訂按鍵圖片
3. 圖片名稱必須與按鍵列表中的名稱相符
4. 放入新圖片後需要重啟程式
5. 圖片最小建議為 60px * 60px

檔案結構：
- KeyBoard.exe：主程式
- user/：自訂按鍵圖片資料夾
- README.txt：本說明檔案

注意事項：
- 請確保 user 資料夾中的圖片為 PNG 格式
- 程式可能需要管理員權限才能監聽全域鍵盤事件
- 如遇到問題，請檢查防毒軟體是否阻擋程式執行

"""
    
    readme_path = os.path.join('dist', 'README.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    """main"""
    
    check_dependencies()
    
    clean_build_dirs()
    
    create_spec_file()
    
    if build_exe():

        # 複製資料夾
        copy_user_folder()
        
        # 建readme
        create_readme()
        
        print("打包完成")
        
    else:
        print("打包失敗")

if __name__ == "__main__":
    main()
