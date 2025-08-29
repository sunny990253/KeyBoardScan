import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import keyboard
import os
import json
import time

root = tk.Tk()
root.title("KeyBoard")

# 從內建資源檔案讀取預設設定
try:
    from resources import DEFAULT_CONFIG
    print("已載入內建資源檔案")
except ImportError:
    # 如果無法載入資源檔案，使用硬編碼的預設值
    DEFAULT_CONFIG = {
        "image_size": [64, 48],
        "display_mode": "float",
        "default_dir": "default",
        "user_dir": "user",
        "key_w": 8,
        "key_h": 3,
        "window_width": 1700,
        "window_height": 530,
        "realtime_image_size": [80,80],
        "max_keys_per_row": 10,
        "max_rows": 3,
        "realtime_background": "default"
    }
    print("使用硬編碼預設設定")

# 讀取設定檔
CONFIG_FILE = "config.json"
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        print("已載入外部設定檔")
    except Exception as e:
        print(f"讀取外部設定檔失敗: {e}，使用內建設定")
        config = {}
else:
    # 如果沒有 config.json，使用空的配置字典
    config = {}
    print("使用內建設定檔")

# 從 config 讀取所有設定，如果 config 中沒有該項目，則使用 DEFAULT_CONFIG 的預設值
IMAGE_SIZE = tuple(config.get("image_size", DEFAULT_CONFIG["image_size"]))
DEFAULT_DIR = config.get("default_dir", DEFAULT_CONFIG["default_dir"])
USER_DIR = config.get("user_dir", DEFAULT_CONFIG["user_dir"])
KEY_W = config.get("key_w", DEFAULT_CONFIG["key_w"])
KEY_H = config.get("key_h", DEFAULT_CONFIG["key_h"])
WINDOW_WIDTH = config.get("window_width", DEFAULT_CONFIG["window_width"])
WINDOW_HEIGHT = config.get("window_height", DEFAULT_CONFIG["window_height"])
REALTIME_IMAGE_SIZE = tuple(config.get("realtime_image_size", DEFAULT_CONFIG["realtime_image_size"]))
MAX_KEYS_PER_ROW = config.get("max_keys_per_row", DEFAULT_CONFIG["max_keys_per_row"])
MAX_ROWS = config.get("max_rows", DEFAULT_CONFIG["max_rows"])
REALTIME_BACKGROUND = config.get("realtime_background", DEFAULT_CONFIG["realtime_background"])

# 全域變數
pressed_keys = {}   # {key: Label物件}
key_images = {}     # {key: ImageTk物件}
image_mtime = {}    # {path: 最後修改時間}
tooltip = None      # 工具提示視窗

# 從內建資源檔案讀取預設按鍵映射
try:
    from resources import DEFAULT_KEY_MAP
    print("已載入內建按鍵映射")
except ImportError:
    # 如果無法載入資源檔案，使用硬編碼的預設值
    DEFAULT_KEY_MAP = {
    "1:False": {"key_id": "1", "name": "Esc", "png": "Esc.png"},
    "2:False": {"key_id": "2", "name": "1", "png": "1.png"},
    "3:False": {"key_id": "3", "name": "2", "png": "2.png"},
    "4:False": {"key_id": "4", "name": "3", "png": "3.png"},
    "5:False": {"key_id": "5", "name": "4", "png": "4.png"},
    "6:False": {"key_id": "6", "name": "5", "png": "5.png"},
    "7:False": {"key_id": "7", "name": "6", "png": "6.png"},
    "8:False": {"key_id": "8", "name": "7", "png": "7.png"},
    "9:False": {"key_id": "9", "name": "8", "png": "8.png"},
    "10:False": {"key_id": "10", "name": "9", "png": "9.png"},
    "11:False": {"key_id": "11", "name": "0", "png": "0.png"},
    "12:False": {"key_id": "12", "name": "-", "png": "Minus.png"},
    "13:False": {"key_id": "13", "name": "=", "png": "Equal.png"},
    "14:False": {"key_id": "14", "name": "Backspace", "png": "Backspace.png"},
    "15:False": {"key_id": "15", "name": "Tab", "png": "Tab.png"},
    "16:False": {"key_id": "16", "name": "Q", "png": "Q.png"},
    "17:False": {"key_id": "17", "name": "W", "png": "W.png"},
    "18:False": {"key_id": "18", "name": "E", "png": "E.png"},
    "19:False": {"key_id": "19", "name": "R", "png": "R.png"},
    "20:False": {"key_id": "20", "name": "T", "png": "T.png"},
    "21:False": {"key_id": "21", "name": "Y", "png": "Y.png"},
    "22:False": {"key_id": "22", "name": "U", "png": "U.png"},
    "23:False": {"key_id": "23", "name": "I", "png": "I.png"},
    "24:False": {"key_id": "24", "name": "O", "png": "O.png"},
    "25:False": {"key_id": "25", "name": "P", "png": "P.png"},
    "26:False": {"key_id": "26", "name": "[", "png": "BracketLeft.png"},
    "27:False": {"key_id": "27", "name": "]", "png": "BracketRight.png"},
    "28:False": {"key_id": "28", "name": "Enter", "png": "Enter.png"},
    "29:False": {"key_id": "29", "name": "CtrlLeft", "png": "CtrlLeft.png"},
    "30:False": {"key_id": "30", "name": "A", "png": "A.png"},
    "31:False": {"key_id": "31", "name": "S", "png": "S.png"},
    "32:False": {"key_id": "32", "name": "D", "png": "D.png"},
    "33:False": {"key_id": "33", "name": "F", "png": "F.png"},
    "34:False": {"key_id": "34", "name": "G", "png": "G.png"},
    "35:False": {"key_id": "35", "name": "H", "png": "H.png"},
    "36:False": {"key_id": "36", "name": "J", "png": "J.png"},
    "37:False": {"key_id": "37", "name": "K", "png": "K.png"},
    "38:False": {"key_id": "38", "name": "L", "png": "L.png"},
    "39:False": {"key_id": "39", "name": ";", "png": "Semicolon.png"},
    "40:False": {"key_id": "40", "name": "'", "png": "Quote.png"},
    "41:False": {"key_id": "41", "name": "`", "png": "Grave.png"},
    "42:False": {"key_id": "42", "name": "ShiftLeft", "png": "ShiftLeft.png"},
    "43:False": {"key_id": "43", "name": "\\", "png": "Backslash.png"},
    "44:False": {"key_id": "44", "name": "Z", "png": "Z.png"},
    "45:False": {"key_id": "45", "name": "X", "png": "X.png"},
    "46:False": {"key_id": "46", "name": "C", "png": "C.png"},
    "47:False": {"key_id": "47", "name": "V", "png": "V.png"},
    "48:False": {"key_id": "48", "name": "B", "png": "B.png"},
    "49:False": {"key_id": "49", "name": "N", "png": "N.png"},
    "50:False": {"key_id": "50", "name": "M", "png": "M.png"},
    "51:False": {"key_id": "51", "name": ",", "png": "Comma.png"},
    "52:False": {"key_id": "52", "name": ".", "png": "Period.png"},
    "53:False": {"key_id": "53", "name": "/", "png": "Slash.png"},
    "54:False": {"key_id": "54", "name": "ShiftRight", "png": "ShiftRight.png"},
    "55:True": {"key_id": "55", "name": "*", "png": "NumMultiply.png"},
    "56:False": {"key_id": "56", "name": "AltLeft", "png": "AltLeft.png"},
    "57:False": {"key_id": "57", "name": "Space", "png": "Space.png"},
    "58:False": {"key_id": "58", "name": "CapsLock", "png": "CapsLock.png"},
    "59:False": {"key_id": "59", "name": "F1", "png": "F1.png"},
    "60:False": {"key_id": "60", "name": "F2", "png": "F2.png"},
    "61:False": {"key_id": "61", "name": "F3", "png": "F3.png"},
    "62:False": {"key_id": "62", "name": "F4", "png": "F4.png"},
    "63:False": {"key_id": "63", "name": "F5", "png": "F5.png"},
    "64:False": {"key_id": "64", "name": "F6", "png": "F6.png"},
    "65:False": {"key_id": "65", "name": "F7", "png": "F7.png"},
    "66:False": {"key_id": "66", "name": "F8", "png": "F8.png"},
    "67:False": {"key_id": "67", "name": "F9", "png": "F9.png"},
    "68:False": {"key_id": "68", "name": "F10", "png": "F10.png"},
    "69:True": {"key_id": "69", "name": "NumLock", "png": "Num.png"},
    "70:False": {"key_id": "70", "name": "ScrLk", "png": "ScrollLock.png"},
    "71:True": {"key_id": "71", "name": "Num7", "png": "Num7.png"},
    "72:True": {"key_id": "72", "name": "Num8", "png": "Num8.png"},
    "73:True": {"key_id": "73", "name": "Num9", "png": "Num9.png"},
    "74:True": {"key_id": "74", "name": "-", "png": "NumSubtract.png"},
    "75:True": {"key_id": "75", "name": "Num4", "png": "Num4.png"},
    "76:True": {"key_id": "76", "name": "Num5", "png": "Num5.png"},
    "77:True": {"key_id": "77", "name": "Num6", "png": "Num6.png"},
    "78:True": {"key_id": "78", "name": "+", "png": "NumAdd.png"},
    "79:True": {"key_id": "79", "name": "Num1", "png": "Num1.png"},
    "80:True": {"key_id": "80", "name": "Num2", "png": "Num2.png"},
    "81:True": {"key_id": "81", "name": "Num3", "png": "Num3.png"},
    "82:True": {"key_id": "82", "name": "Num0", "png": "Num0.png"},
    "83:True": {"key_id": "83", "name": ".", "png": "NumDecimal.png"},
    "87:False": {"key_id": "87", "name": "F11", "png": "F11.png"},
    "88:False": {"key_id": "88", "name": "F12", "png": "F12.png"},
    "91:False": {"key_id": "91", "name": "Win", "png": "Win.png"},
    "92:False": {"key_id": "92", "name": "WinRight", "png": "Win.png"},
    "93:False": {"key_id": "93", "name": "Menu", "png": "Menu.png"},
    "95:False": {"key_id": "95", "name": "Fn", "png": "Fn.png"},
    "28:True": {"key_id": "96", "name": "Enter", "png": "NumEnter.png"},
    "97:False": {"key_id": "97", "name": "CtrlRight", "png": "CtrlRight.png"},
    "53:True": {"key_id": "98", "name": "/", "png": "NumDivide.png"},
    "55:False": {"key_id": "99", "name": "PrtSc", "png": "PrintScreen.png"},
    "100:False": {"key_id": "100", "name": "AltRight", "png": "AltRight.png"},
    "71:False": {"key_id": "101", "name": "Home", "png": "Home.png"},
    "72:False": {"key_id": "102", "name": "ArrowUp", "png": "ArrowUp.png"},
    "73:False": {"key_id": "103", "name": "PageUp", "png": "PageUp.png"},
    "75:False": {"key_id": "104", "name": "ArrowLeft", "png": "ArrowLeft.png"},
    "77:False": {"key_id": "106", "name": "ArrowRight", "png": "ArrowRight.png"},
    "79:False": {"key_id": "107", "name": "End", "png": "End.png"},
    "80:False": {"key_id": "108", "name": "ArrowDown", "png": "ArrowDown.png"},
    "81:False": {"key_id": "109", "name": "PageDown", "png": "PageDown.png"},
    "82:False": {"key_id": "110", "name": "Ins", "png": "Insert.png"},
    "83:False": {"key_id": "111", "name": "Del", "png": "Delete.png"},
    "69:False": {"key_id": "119", "name": "Pause", "png": "Pause.png"}
}

    print("使用硬編碼按鍵映射")

# 讀取key_map.json
def load_key_map():
    """載入按鍵映射檔案"""
    try:
        with open("key_map.json", "r", encoding="utf-8") as f:
            key_map_data = json.load(f)
            print("已載入外部按鍵映射檔")
            return key_map_data
    except FileNotFoundError:
        print("找不到 key_map.json 檔案，使用內建按鍵映射")
        return DEFAULT_KEY_MAP.copy()
    except Exception as e:
        print(f"讀取 key_map.json 失敗: {e}，使用內建按鍵映射")
        return DEFAULT_KEY_MAP.copy()

# 載入 key_map（全域變數）
key_map = load_key_map()

def create_rounded_image_label(parent, image_tk, width_mult=1, height_mult=1):
    """創建帶有圓角邊框的圖片標籤"""
    # 計算按鍵大小
    keyboard_key_width = KEY_W * 9 * width_mult
    keyboard_key_height = KEY_H * 18 * height_mult
    
    # 創建 Canvas 來繪製圓角邊框
    canvas = tk.Canvas(parent, width=keyboard_key_width, height=keyboard_key_height,
                      bg='white', highlightthickness=0, relief='flat')
    
    # 繪製圓角矩形邊框
    border_width = 2  # 減少邊框寬度，讓邊線更細
    corner_radius = 8  # 保持圓角半徑
    
    # 外框（黑色）
    canvas.create_rounded_rectangle(
        border_width//2, border_width//2, 
        keyboard_key_width - border_width//2, keyboard_key_height - border_width//2,
        radius=corner_radius, fill='white', outline='black', width=border_width
    )
    
    # 創建圖片標籤
    label = tk.Label(canvas, image=image_tk, bg='white', relief='flat', borderwidth=0)
    
    # 將圖片標籤放置在 Canvas 中央
    canvas.create_window(keyboard_key_width//2, keyboard_key_height//2, window=label)
    
    return canvas

def create_key_image_label(parent, key_id, width_mult=1, height_mult=1, columnspan=1, rowspan=1):
    """創建按鍵圖片標籤"""
    if key_id == '':
        # 空按鍵
        return tk.Label(parent, text='', width=KEY_W*width_mult, height=KEY_H*height_mult, 
                       borderwidth=0, highlightthickness=0)
    else:
        # 根據 key_id 從 key_map 獲取按鍵資訊
        # 需要遍歷 key_map 找到對應的 key_id
        key_info = None
        for composite_key, info in key_map.items():
            if info["key_id"] == key_id:
                key_info = info
                break
        
        if key_info:
            key_name = key_info["name"]
            image_filename = key_info["png"]
            
            # 檢查圖片是否已載入
            if image_filename in key_images:
                # 檢查圖片來源（user 或 default 資料夾）
                user_path = os.path.join(USER_DIR, image_filename)
                is_user_image = os.path.exists(user_path)
                
                if is_user_image:
                    # 使用者圖片：使用固定的 48x48 大小，在按鍵內置中顯示
                    try:
                        # 創建 48x48 的圖片
                        img = Image.open(user_path).resize((48, 48), Image.Resampling.LANCZOS)
                        img_tk = ImageTk.PhotoImage(img)
                        
                        # 創建帶有圓角邊框的圖片標籤
                        canvas = create_rounded_image_label(parent, img_tk, width_mult, height_mult)
                        
                        # 保存圖片引用以防止垃圾回收
                        canvas.image = img_tk
                        
                        # 設定工具提示顯示按鍵名稱
                        canvas.bind('<Enter>', lambda e, name=key_name: show_tooltip(e, name))
                        canvas.bind('<Leave>', lambda e: hide_tooltip())
                        
                        return canvas
                        
                    except Exception as e:
                        print(f"創建使用者按鍵圖片失敗 {key_id}: {e}")
                        # 降級為文字標籤
                        return create_rounded_text_label(parent, key_name, width_mult, height_mult, key_id)
                else:
                    # 預設圖片：根據按鍵大小進行縮放
                    try:
                        # 計算鍵盤配置中按鍵的實際像素大小
                        keyboard_key_width = KEY_W * 8  # 8 是 Tkinter 文字單位的像素轉換
                        keyboard_key_height = KEY_H * 16  # 16 是 Tkinter 文字單位的像素轉換
                        
                        # 調整圖片大小以匹配按鍵大小
                        img = Image.open(os.path.join(DEFAULT_DIR, image_filename))
                        img_resized = img.resize((keyboard_key_width * width_mult, keyboard_key_height * height_mult), Image.Resampling.LANCZOS)
                        img_tk = ImageTk.PhotoImage(img_resized)
                        
                        # 創建帶有圓角邊框的圖片標籤
                        canvas = create_rounded_image_label(parent, img_tk, width_mult, height_mult)
                        
                        # 保存圖片引用以防止垃圾回收
                        canvas.image = img_tk
                        
                        # 設定工具提示顯示按鍵名稱
                        canvas.bind('<Enter>', lambda e, name=key_name: show_tooltip(e, name))
                        canvas.bind('<Leave>', lambda e: hide_tooltip())
                        
                        return canvas
                        
                    except Exception as e:
                        print(f"創建預設按鍵圖片失敗 {key_id}: {e}")
                        # 降級為文字標籤
                        return create_rounded_text_label(parent, key_name, width_mult, height_mult)
            else:
                # 圖片未載入，使用文字標籤
                print(f"圖片未載入: {image_filename}")
                return create_rounded_text_label(parent, key_name, width_mult, height_mult)
        else:
            # 找不到按鍵資訊，使用 ID 作為文字
            print(f"找不到按鍵資訊: {key_id}")
            return create_rounded_text_label(parent, key_id, width_mult, height_mult)

def create_rounded_text_label(parent, text, width_mult=1, height_mult=1):
    """創建帶有圓角邊框的文字標籤"""
    # 計算按鍵大小
    keyboard_key_width = KEY_W * 8 * width_mult
    keyboard_key_height = KEY_H * 16 * height_mult
    
    # 創建 Canvas 來繪製圓角邊框
    canvas = tk.Canvas(parent, width=keyboard_key_width, height=keyboard_key_height,
                      bg='white', highlightthickness=0, relief='flat')
    
    # 繪製圓角矩形邊框
    border_width = 1  # 減少邊框寬度，讓邊線更細
    corner_radius = 8  # 保持圓角半徑
    
    # 外框（黑色）
    canvas.create_rounded_rectangle(
        border_width//2, border_width//2, 
        keyboard_key_width - border_width//2, keyboard_key_height - border_width//2,
        radius=corner_radius, fill='white', outline='black', width=border_width
    )
    
    # 創建文字標籤
    label = tk.Label(canvas, text=text, bg='white', fg='black', relief='flat', borderwidth=0,
                     font=('Arial', 10), anchor='center')
    
    # 將文字標籤放置在 Canvas 中央
    canvas.create_window(keyboard_key_width//2, keyboard_key_height//2, window=label)
    
    return canvas

# 為 Canvas 添加圓角矩形繪製方法
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    """在 Canvas 上繪製圓角矩形"""
    # 使用更平滑的圓角繪製方法
    # 創建圓角的弧線
    points = []
    
    # 上邊線
    points.extend([x1 + radius, y1])
    points.extend([x2 - radius, y1])
    
    # 右上角
    points.extend([x2, y1])
    points.extend([x2, y1 + radius])
    
    # 右邊線
    points.extend([x2, y2 - radius])
    
    # 右下角
    points.extend([x2, y2])
    points.extend([x2 - radius, y2])
    
    # 下邊線
    points.extend([x1 + radius, y2])
    
    # 左下角
    points.extend([x1, y2])
    points.extend([x1, y2 - radius])
    
    # 左邊線
    points.extend([x1, y1 + radius])
    
    # 左上角
    points.extend([x1, y1])
    
    # 創建平滑的圓角矩形
    return canvas.create_polygon(points, smooth=True, **kwargs)

# 將方法添加到 Canvas 類
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

def show_tooltip(event, text):
    """顯示工具提示"""
    global tooltip
    tooltip = tk.Toplevel()
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
    
    label = tk.Label(tooltip, text=text, justify='left',
                     background="#ffffe0", relief='solid', borderwidth=1)
    label.pack()

def hide_tooltip():
    """隱藏工具提示"""
    global tooltip
    if 'tooltip' in globals():
        tooltip.destroy()

def load_images():
    """載入key_map.json中定義的所有圖片"""
    # 使用全域的 key_map
    
    # 從key_map載入所有圖片
    for composite_key, key_info in key_map.items():
        image_filename = key_info["png"]
        
        # 優先嘗試user資料夾
        user_path = os.path.join(USER_DIR, image_filename)
        default_path = os.path.join(DEFAULT_DIR, image_filename)
        
        if os.path.exists(user_path):
            path = user_path
            print(f"載入使用者圖片: {image_filename}")
        elif os.path.exists(default_path):
            path = default_path
            print(f"載入預設圖片: {image_filename}")
        else:
            print(f"找不到圖片檔案: {image_filename}，跳過載入")
            continue
        
        try:
            img = Image.open(path).resize(IMAGE_SIZE)
            # 使用圖片檔案名稱作為key_images的鍵
            key_images[image_filename] = ImageTk.PhotoImage(img)
            image_mtime[path] = os.path.getmtime(path)
        except Exception as e:
            print(f"載入圖片 {path} 失敗: {e}")
    
    print(f"總共載入 {len(key_images)} 張圖片")

def reload_if_changed():
    """檢查圖片是否變更，有變就重新載入"""
    updated = False
    # 使用全域的 key_map
    
    for composite_key, key_info in key_map.items():
        image_filename = key_info["png"]
        user_path = os.path.join(USER_DIR, image_filename)
        default_path = os.path.join(DEFAULT_DIR, image_filename)
        
        # 檢查路徑是否存在
        if os.path.exists(user_path):
            path = user_path
        elif os.path.exists(default_path):
            path = default_path
        else:
            continue  # 跳過不存在的圖片
        
        try:
            mtime = os.path.getmtime(path)
            if path not in image_mtime or mtime != image_mtime[path]:
                img = Image.open(path).resize(IMAGE_SIZE)
                key_images[image_filename] = ImageTk.PhotoImage(img)
                image_mtime[path] = mtime
                updated = True
                print(f"重新載入圖片: {image_filename}")
        except Exception as e:
            print(f"重新載入圖片失敗: {e}")
    
    root.after(1000, reload_if_changed)  # 每秒檢查一次

def _rearrange_keys():
    """重新排列所有按鍵"""
    if not pressed_keys:
        return
    
    # 獲取所有按鍵標籤和對應的鍵名
    items = list(pressed_keys.items())
    
    # 清空pressed_keys字典
    pressed_keys.clear()
    
    # 重新排列（使用 config 中的設定）
    max_keys_per_row = MAX_KEYS_PER_ROW
    max_rows = MAX_ROWS
    
    for i, (unique_id, label) in enumerate(items):
        if i >= max_keys_per_row * max_rows:  # 超過限制的按鍵不顯示
            label.destroy()
            continue
            
        row = i // max_keys_per_row
        col = i % max_keys_per_row
        label.grid(row=row, column=col, padx=2, pady=2, sticky='nw')
        pressed_keys[unique_id] = label

def show_key(event):
    """顯示按下的按鍵圖片"""
    # 使用複合鍵值來區分數字鍵盤和主鍵盤的按鍵
    # 格式: "scan_code:is_keypad" (例如: "55:False" 表示主鍵盤的按鍵)
    keycode = str(event.scan_code)
    is_keypad = event.is_keypad
    composite_key = f"{keycode}:{is_keypad}"
    
    # 首先嘗試使用複合鍵值查找
    if composite_key in key_map:
        key_info = key_map[composite_key]
        key_name = key_info["name"]
        image_filename = key_info["png"]
        
        # 檢查該按鍵是否已經被按下（防止長按時重複累積）
        if key_name in root.currently_pressed:
            return  # 如果按鍵已經被按下，不重複處理
        
        # 標記按鍵為已按下
        root.currently_pressed.add(key_name)
        
        # 檢查圖片是否已載入
        if image_filename in key_images:
            # 在即時按鍵分頁中顯示圖片
            if hasattr(root, 'key_display_frame'):
                # 檢查圖片來源（user 或 default 資料夾）
                user_path = os.path.join(USER_DIR, image_filename)
                is_user_image = os.path.exists(user_path)
                
                if is_user_image:
                    # 使用者圖片：使用可配置的大小
                    try:
                        img = Image.open(user_path).resize(REALTIME_IMAGE_SIZE, Image.Resampling.LANCZOS)
                        img_tk = ImageTk.PhotoImage(img)
                        # 根據背景設定設定標籤背景顏色
                        if REALTIME_BACKGROUND == "blue":
                            key_label = tk.Label(root.key_display_frame, image=img_tk, borderwidth=0, bg='#0000FF')
                        elif REALTIME_BACKGROUND == "green":
                            key_label = tk.Label(root.key_display_frame, image=img_tk, borderwidth=0, bg='#00FF00')
                        else:  # default
                            default_bg = root.cget('bg')
                            key_label = tk.Label(root.key_display_frame, image=img_tk, borderwidth=0, bg=default_bg)
                        # 保存圖片引用以防止垃圾回收
                        key_label.image = img_tk
                    except Exception as e:
                        print(f"創建使用者即時按鍵圖片失敗 {key_name}: {e}")
                        # 降級為文字標籤
                        if REALTIME_BACKGROUND == "blue":
                            key_label = tk.Label(root.key_display_frame, text=key_name, borderwidth=0, font=('Arial', 10), bg='#0000FF', fg='white')
                        elif REALTIME_BACKGROUND == "green":
                            key_label = tk.Label(root.key_display_frame, text=key_name, borderwidth=0, font=('Arial', 10), bg='#00FF00', fg='black')
                        else:  # default
                            default_bg = root.cget('bg')
                            key_label = tk.Label(root.key_display_frame, text=key_name, borderwidth=0, font=('Arial', 10), bg=default_bg)
                else:
                    # 預設圖片：使用可配置的大小
                    try:
                        img = Image.open(os.path.join(DEFAULT_DIR, image_filename)).resize(REALTIME_IMAGE_SIZE, Image.Resampling.LANCZOS)
                        img_tk = ImageTk.PhotoImage(img)
                        # 根據背景設定設定標籤背景顏色
                        if REALTIME_BACKGROUND == "blue":
                            key_label = tk.Label(root.key_display_frame, image=img_tk, borderwidth=0, bg='#0000FF')
                        elif REALTIME_BACKGROUND == "green":
                            key_label = tk.Label(root.key_display_frame, image=img_tk, borderwidth=0, bg='#00FF00')
                        else:  # default
                            default_bg = root.cget('bg')
                            key_label = tk.Label(root.key_display_frame, image=img_tk, borderwidth=0, bg=default_bg)
                        # 保存圖片引用以防止垃圾回收
                        key_label.image = img_tk
                    except Exception as e:
                        print(f"創建預設即時按鍵圖片失敗 {key_name}: {e}")
                        # 降級為文字標籤
                        if REALTIME_BACKGROUND == "blue":
                            key_label = tk.Label(root.key_display_frame, text=key_name, borderwidth=0, font=('Arial', 10), bg='#0000FF', fg='white')
                        elif REALTIME_BACKGROUND == "green":
                            key_label = tk.Label(root.key_display_frame, text=key_name, borderwidth=0, font=('Arial', 10), bg='#00FF00', fg='black')
                        else:  # default
                            default_bg = root.cget('bg')
                            key_label = tk.Label(root.key_display_frame, text=key_name, borderwidth=0, font=('Arial', 10), bg=default_bg)
                
                # 計算位置（依序排列，限制在可見範圍內）
                keys_count = len(pressed_keys)
                max_keys_per_row = MAX_KEYS_PER_ROW  # 使用 config 中的設定
                max_rows = MAX_ROWS  # 使用 config 中的設定
                max_total_keys = max_keys_per_row * max_rows+1  # 總共按鍵數量
                
                if keys_count < max_total_keys:  # 限制總按鍵數量為 23×5 = 115 個
                    row = keys_count // max_keys_per_row
                    col = keys_count % max_keys_per_row
                    
                    # 使用grid佈局來排列按鍵
                    key_label.grid(row=row, column=col, padx=2, pady=2, sticky='nw')
                    
                    # 保存引用（使用唯一標識符）
                    unique_id = f"{key_name}_{keys_count}"
                    pressed_keys[unique_id] = key_label
                    
                    # 檢查是否剛好達到115個按鍵
                    if len(pressed_keys) == max_total_keys:
                        # 當達到115個按鍵時，清空所有按鍵
                        clear_all_keys()
                else:
                    # 如果超過限制，移除最早的按鍵
                    oldest_key = list(pressed_keys.keys())[0]
                    oldest_label = pressed_keys[oldest_key]
                    oldest_label.destroy()
                    del pressed_keys[oldest_key]
                    
                    # 重新排列剩餘的按鍵
                    _rearrange_keys()
                    
                    # 添加新按鍵到最後位置
                    keys_count = len(pressed_keys)
                    row = keys_count // max_keys_per_row
                    col = keys_count % max_keys_per_row
                    key_label.grid(row=row, column=col, padx=2, pady=2, sticky='nw')
                    
                    # 保存引用（使用唯一標識符）
                    unique_id = f"{key_name}_{keys_count}"
                    pressed_keys[unique_id] = key_label
                return
            else:
                print(f"圖片 {image_filename} 未載入")
        else:
            print(f"按鍵 {key_name} 在key_map中未定義")
    else:
        print(f"按鍵 keycode {keycode} 未定義對應關係")

def clear_all_keys():
    """清空所有顯示的按鍵圖片"""
    global pressed_keys
    
    # 銷毀所有按鍵標籤
    for label in pressed_keys.values():
        if label and hasattr(label, 'destroy'):
            label.destroy()
    
    # 清空按鍵字典
    pressed_keys.clear()
    
    # 清空當前按下的按鍵集合
    if hasattr(root, 'currently_pressed'):
        root.currently_pressed.clear()
    
    #print("已清空所有按鍵圖片")

def hide_key(event):
    """隱藏釋放的按鍵圖片"""
    # 使用複合鍵值來區分數字鍵盤和主鍵盤的按鍵
    keycode = str(event.scan_code)
    is_keypad = event.is_keypad
    composite_key = f"{keycode}:{is_keypad}"
    
    # 使用複合鍵值查找
    if composite_key in key_map:
        key_info = key_map[composite_key]
        key_name = key_info["name"]
        
        # 從當前按下的集合中移除（允許該按鍵再次被按下）
        if key_name in root.currently_pressed:
            root.currently_pressed.remove(key_name)
    
    # 注意：我們不應該移除圖片，只移除currently_pressed標記
    # 這樣圖片就能累積顯示

# 鍵盤按鍵配置
# 載入圖片（在設定載入之後）
load_images()
reload_if_changed()  # 啟動背景檢查

# 主鍵區（Esc~F12）
main_keys_row1 = ["1", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "87", "88"]
main_keys_row2 = ["41", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
main_keys_row3 = ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "43"]
# CapsLock與Enter佔1.5鍵位（columnspan=2），其餘正常
main_keys_row4 = ["58", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "28"]
main_keys_row5 = ["42", "", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54"]
main_keys_row6 = ["29", "91", "56", "57", "", "", "", "", "", "", "100", "92", "93", "97"]

# 次鍵區
sub_keys_row1 = ["99", "70", "119"]
sub_keys_row2 = ["110", "101", "103"]
sub_keys_row3 = ["111", "107", "109"]
sub_keys_row4 = ["", "", ""]
sub_keys_row5 = ["", "102", ""]
sub_keys_row6 = ["104", "108", "106"]

# 數字鍵區
num_keys_row1 = ["", "", "", ""]
num_keys_row2 = ["69", "98", "55", "74"]
num_keys_row3 = ["71", "72", "73", "78"]
num_keys_row4 = ["75", "76", "77", ""]
num_keys_row5 = ["79", "80", "81", "96"]
num_keys_row6 = ["82", "83", "52", ""]

# 創建標籤頁容器
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# 分頁一：顯示即時按鍵
realtime_tab = ttk.Frame(notebook)
notebook.add(realtime_tab, text="即時按鍵")

# 分頁二：鍵盤配置
keyboard_tab = ttk.Frame(notebook)
notebook.add(keyboard_tab, text="鍵盤配置")

# 分頁三：按鍵列表
keys_list_tab = ttk.Frame(notebook)
notebook.add(keys_list_tab, text="按鍵列表")

# 分頁四：關於
about_tab = ttk.Frame(notebook)
notebook.add(about_tab, text="關於")

# 分頁一：即時按鍵標籤頁內容
realtime_frame = tk.Frame(realtime_tab)
realtime_frame.pack(expand=True, fill='both', padx=20, pady=20)

# 創建一個 Canvas 和 Scrollbar 來實現滾輪功能
keys_canvas = tk.Canvas(realtime_frame)
keys_scrollbar = ttk.Scrollbar(realtime_frame, orient="vertical", command=keys_canvas.yview)
keys_scrollable_frame = tk.Frame(keys_canvas)

keys_scrollable_frame.bind(
    "<Configure>",
    lambda e: keys_canvas.configure(scrollregion=keys_canvas.bbox("all"))
)

keys_canvas.create_window((0, 0), window=keys_scrollable_frame, anchor="nw")
keys_canvas.configure(yscrollcommand=keys_scrollbar.set)

# 按鍵顯示區域（整個區塊都是顯示範圍）
key_display_frame = tk.Frame(keys_scrollable_frame, relief='flat', borderwidth=0)
key_display_frame.pack(expand=True, fill='both')

# 根據設定應用背景顏色
if REALTIME_BACKGROUND == "blue":
    key_display_frame.configure(bg='#0000FF')  # 藍幕
elif REALTIME_BACKGROUND == "green":
    key_display_frame.configure(bg='#00FF00')  # 綠幕
else:  # default - 透明（使用系統預設背景）
    # 使用系統預設的背景顏色
    default_bg = root.cget('bg')
    key_display_frame.configure(bg=default_bg)

# 配置滾輪功能
keys_canvas.pack(side="left", fill="both", expand=True)
keys_scrollbar.pack(side="right", fill="y")

# 在即時按鍵頁面底部添加清空按鈕
clear_button_frame = tk.Frame(realtime_tab)
clear_button_frame.pack(side='bottom', fill='x', padx=20, pady=(0, 20))

clear_button = tk.Button(clear_button_frame, text="清空所有按鍵", 
                        command=clear_all_keys,
                        font=('Arial', 12),
                        bg='white', fg='black',
                        relief='raised', borderwidth=2,
                        padx=20, pady=8)
clear_button.pack(pady=10)

# 保存引用到root，供show_key函數使用
root.key_display_frame = key_display_frame
root.keys_canvas = keys_canvas
root.keys_scrollable_frame = keys_scrollable_frame

# 用於追蹤當前按下的按鍵（防止按住時重複累積）
root.currently_pressed = set()

# 應用即時按鍵區域的背景設定
def apply_realtime_background():
    """應用即時按鍵區域的背景設定"""
    if hasattr(root, 'key_display_frame'):
        # 設定按鍵顯示區域的背景
        if REALTIME_BACKGROUND == "blue":
            root.key_display_frame.configure(bg='#0000FF')  # 藍幕
        elif REALTIME_BACKGROUND == "green":
            root.key_display_frame.configure(bg='#00FF00')  # 綠幕
        else:  # default - 透明（使用系統預設背景）
            # 使用系統預設的背景顏色
            default_bg = root.cget('bg')
            root.key_display_frame.configure(bg=default_bg)
        
        # 設定滾輪區域和可滾動框架的背景，確保整個區域背景一致
        if hasattr(root, 'keys_canvas') and hasattr(root, 'keys_scrollable_frame'):
            if REALTIME_BACKGROUND == "blue":
                root.keys_canvas.configure(bg='#0000FF')
                root.keys_scrollable_frame.configure(bg='#0000FF')
            elif REALTIME_BACKGROUND == "green":
                root.keys_canvas.configure(bg='#00FF00')
                root.keys_scrollable_frame.configure(bg='#00FF00')
            else:  # default - 透明（使用系統預設背景）
                # 使用系統預設的背景顏色
                default_bg = root.cget('bg')
                root.keys_canvas.configure(bg=default_bg)
                root.keys_scrollable_frame.configure(bg=default_bg)
        
        # 更新現有按鍵的背景顏色
        update_existing_keys_background()

def update_existing_keys_background():
    """更新現有按鍵的背景顏色以匹配當前背景設定"""
    global pressed_keys
    
    for unique_id, label in pressed_keys.items():
        if label and hasattr(label, 'configure'):
            if REALTIME_BACKGROUND == "blue":
                label.configure(bg='#0000FF')
                if hasattr(label, 'cget') and label.cget('text'):  # 如果是文字標籤
                    label.configure(fg='white')  # 藍幕上使用白色文字
            elif REALTIME_BACKGROUND == "green":
                label.configure(bg='#00FF00')
                if hasattr(label, 'cget') and label.cget('text'):  # 如果是文字標籤
                    label.configure(fg='black')  # 綠幕上使用黑色文字
            else:  # default
                default_bg = root.cget('bg')
                label.configure(bg=default_bg)
                if hasattr(label, 'cget') and label.cget('text'):  # 如果是文字標籤
                    label.configure(fg='black')  # 預設背景上使用黑色文字

# 初始化時應用背景設定
apply_realtime_background()

# 分頁二：鍵盤配置標籤頁內容
keyboard_frame = tk.Frame(keyboard_tab)
keyboard_frame.pack(fill='both', expand=True, padx=10, pady=10)

# 在鍵盤配置上方加入空白區域
top_spacer = tk.Frame(keyboard_frame, height=20)
top_spacer.pack(fill='x')

main_frame = tk.Frame(keyboard_frame)
sub_frame = tk.Frame(keyboard_frame)
num_frame = tk.Frame(keyboard_frame)

main_frame.pack(side='left', padx=10, pady=10)
sub_frame.pack(side='left', padx=10, pady=10)
num_frame.pack(side='left', padx=10, pady=10)

# 主鍵區前3列
main_rows = [main_keys_row1, main_keys_row2, main_keys_row3]
for row_idx, row in enumerate(main_rows):
    for col_idx, key_id in enumerate(row):
        label = create_key_image_label(main_frame, key_id)
        label.grid(row=row_idx, column=col_idx, padx=2, pady=2)

# 主鍵區第4列（CapsLock/Enter佔1.5格，但使用標準佈局）
row_idx = 3
col_idx = 0
while col_idx < len(main_keys_row4):
    key_id = main_keys_row4[col_idx]
    if key_id == "28":  # Enter
        label = create_key_image_label(main_frame, key_id, width_mult=2)
        label.grid(row=row_idx, column=col_idx, padx=2, pady=2, columnspan=2)
        col_idx += 2
    else:
        label = create_key_image_label(main_frame, key_id)
        label.grid(row=row_idx, column=col_idx, padx=2, pady=2)
        col_idx += 1

# 主鍵區第5列（Shift佔兩格，Z往右移一格）
row_idx = 4
col_idx = 0
while col_idx < len(main_keys_row5):
    key_id = main_keys_row5[col_idx]
    if key_id == "42" and col_idx == 0:  # 第一個 Shift
        label = create_key_image_label(main_frame, key_id, width_mult=2)
        label.grid(row=row_idx, column=col_idx, padx=2, pady=2, columnspan=2)
        col_idx += 2
    elif key_id == "54" and col_idx == len(main_keys_row5)-1:  # 最後一個 Shift
        label = create_key_image_label(main_frame, key_id, width_mult=2)
        label.grid(row=row_idx, column=col_idx, padx=2, pady=2, columnspan=2)
        col_idx += 2
    elif key_id == '':
        col_idx += 1
    else:
        label = create_key_image_label(main_frame, key_id)
        label.grid(row=row_idx, column=col_idx, padx=2, pady=2)
        col_idx += 1

# 主鍵區第6列（Space佔7格）
row_idx = 5
col_idx = 0
while col_idx < len(main_keys_row6):
    key_id = main_keys_row6[col_idx]
    if key_id == "57":  # Space
        label = create_key_image_label(main_frame, key_id, width_mult=7)
        label.grid(row=row_idx, column=col_idx, padx=2, pady=2, columnspan=7)
        col_idx += 7
    elif key_id == '':
        col_idx += 1
    else:
        label = create_key_image_label(main_frame, key_id)
        label.grid(row=row_idx, column=col_idx, padx=2, pady=2)
        col_idx += 1

# 次鍵區按鍵（六列）
sub_rows = [sub_keys_row1, sub_keys_row2, sub_keys_row3, sub_keys_row4, sub_keys_row5, sub_keys_row6]
for row_idx, row in enumerate(sub_rows):
    for col_idx, key_id in enumerate(row):
        label = create_key_image_label(sub_frame, key_id)
        label.grid(row=row_idx, column=col_idx, padx=2, pady=2)

# 數字鍵區按鍵（六列，+與Enter合併，0佔兩格，跳過被合併格）
num_rows = [num_keys_row1, num_keys_row2, num_keys_row3, num_keys_row4, num_keys_row5, num_keys_row6]
skip_cells = set()  # (row, col) 需跳過的格子
for row_idx, row in enumerate(num_rows):
    col_idx = 0
    while col_idx < len(row):
        key_id = row[col_idx]
        # 跳過被合併的格子
        if (row_idx, col_idx) in skip_cells:
            col_idx += 1
            continue
        # + 按鍵合併第三、四列
        if key_id == "78" and row_idx == 2:  # NumAdd
            label = create_key_image_label(num_frame, key_id, height_mult=2)
            label.grid(row=2, column=col_idx, rowspan=2, padx=2, pady=2)
            skip_cells.add((3, col_idx))
            col_idx += 1
        # Enter合併第五、六列
        elif key_id == "96" and row_idx == 4:  # NumEnter
            label = create_key_image_label(num_frame, key_id, height_mult=2)
            label.grid(row=4, column=col_idx, rowspan=2, padx=2, pady=2)
            skip_cells.add((5, col_idx))
            col_idx += 1
        # 0佔兩格
        elif key_id == "82" and row_idx == 5 and col_idx == 0:  # Num0
            label = create_key_image_label(num_frame, key_id, width_mult=2)
            label.grid(row=row_idx, column=col_idx, padx=2, pady=2, columnspan=2)
            skip_cells.add((row_idx, 1))
            col_idx += 2
        elif key_id == '' or (key_id == "78" and row_idx == 3) or (key_id == "96" and row_idx == 5):
            label = create_key_image_label(num_frame, key_id)
            label.grid(row=row_idx, column=col_idx, padx=2, pady=2)
            col_idx += 1
        else:
            label = create_key_image_label(num_frame, key_id)
            label.grid(row=row_idx, column=col_idx, padx=2, pady=2)
            col_idx += 1

# 分頁三：按鍵列表標籤頁內容
# 這裡可以重新設計按鍵列表的佈局

def get_key_map_info(key_id):
    """根據按鍵 ID 查找對應的 key_map 資訊"""
    if not key_id or key_id == '':
        return "空白", ""
    
    # 在 key_map 中查找對應的 key_id
    for composite_key, key_info in key_map.items():
        if key_info["key_id"] == key_id:
            return key_info["name"], key_info["png"]
    
    # 如果找不到，返回原始 ID 和空字串
    return key_id, ""

def get_display_name_for_empty_key(row_name, col_index):
    """為空字串按鍵提供更有意義的顯示名稱"""
    if row_name == "第五列" and col_index == 1:
        return "Shift間隔", ""
    elif row_name == "第六列" and col_index in [4, 5, 6, 7, 8, 9]:
        return "Space間隔", ""
    else:
        return "空白", ""

def create_key_column(parent_frame, title, row_keys):
    """創建按鍵列的通用函數"""
    # 創建列標題
    tk.Label(parent_frame, text=title, font=('Arial', 12, 'bold')).pack(pady=(0, 1))
    
    # 創建按鍵列表
    for key_id in row_keys:
        # 創建按鍵名稱和圖片檔名的容器
        key_container = tk.Frame(parent_frame)
        key_container.pack(anchor='w', pady=2)
        
        # 使用 get_key_map_info 函數獲取按鍵資訊
        key_name, image_filename = get_key_map_info(key_id)
        
        # 按鍵名稱（顯示 key_map 的 name）
        tk.Label(key_container, text=key_name, font=('Arial', 10), width=10, anchor='w').pack(side='left')
        
        # 圖片檔案名稱（可選擇但不能編輯）
        png_entry = tk.Entry(key_container, font=('Arial', 9), width=15, state='readonly')
        png_entry.pack(side='left', padx=(5, 0))
        
        # 設定唯讀模式的文字內容
        png_entry.config(state='normal')
        png_entry.insert(0, image_filename)
        png_entry.config(state='readonly')

# 創建主鍵區按鍵列表框架
keys_list_frame = tk.Frame(keys_list_tab)
keys_list_frame.pack(fill='both', expand=True, padx=10, pady=10)

# 創建分頁容器
keys_notebook = ttk.Notebook(keys_list_frame)
keys_notebook.pack(fill='both', expand=True)

# 主鍵區分頁
main_keys_tab = ttk.Frame(keys_notebook)
keys_notebook.add(main_keys_tab, text="主鍵區")

# 次鍵區分頁
sub_keys_tab = ttk.Frame(keys_notebook)
keys_notebook.add(sub_keys_tab, text="次鍵區")

# 主鍵區內容
main_keys_frame = tk.Frame(main_keys_tab)
main_keys_frame.pack(fill='both', expand=True, padx=10, pady=10)

# 創建水平排列的容器框架
horizontal_frame = tk.Frame(main_keys_frame)
horizontal_frame.pack(fill='x', expand=True)

# 定義各列的 ID 陣列
first_row_keys = ["1", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "87", "88"]
second_row_keys = ["41", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
third_row_keys = ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "43"]
fourth_row_keys = ["58", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "28"]
fifth_row_keys = ["42", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54"]
sixth_row_keys = ["29", "91", "56", "57", "100", "92", "93", "97"]

# 創建各列
col1_frame = tk.Frame(horizontal_frame)
col1_frame.pack(side='left', fill='y', padx=(0, 30))
create_key_column(col1_frame, "第一列", first_row_keys)

# 添加垂直分隔線
separator_line = tk.Frame(horizontal_frame, width=2, bg='lightgray')
separator_line.pack(side='left', fill='y', padx=(0, 40))

col2_frame = tk.Frame(horizontal_frame)
col2_frame.pack(side='left', fill='y', padx=(0, 40))
create_key_column(col2_frame, "第二列", second_row_keys)

# 添加垂直分隔線
separator_line = tk.Frame(horizontal_frame, width=2, bg='lightgray')
separator_line.pack(side='left', fill='y', padx=(0, 40))

col3_frame = tk.Frame(horizontal_frame)
col3_frame.pack(side='left', fill='y', padx=(0, 40))
create_key_column(col3_frame, "第三列", third_row_keys)

# 添加垂直分隔線
separator_line = tk.Frame(horizontal_frame, width=2, bg='lightgray')
separator_line.pack(side='left', fill='y', padx=(0, 40))

col4_frame = tk.Frame(horizontal_frame)
col4_frame.pack(side='left', fill='y', padx=(0, 40))
create_key_column(col4_frame, "第四列", fourth_row_keys)

# 添加垂直分隔線
separator_line = tk.Frame(horizontal_frame, width=2, bg='lightgray')
separator_line.pack(side='left', fill='y', padx=(0, 40))

col5_frame = tk.Frame(horizontal_frame)
col5_frame.pack(side='left', fill='y', padx=(0, 40))
create_key_column(col5_frame, "第五列", fifth_row_keys)

# 添加垂直分隔線
separator_line = tk.Frame(horizontal_frame, width=2, bg='lightgray')
separator_line.pack(side='left', fill='y', padx=(0, 30))

col6_frame = tk.Frame(horizontal_frame)
col6_frame.pack(side='left', fill='y', padx=(0, 30))
create_key_column(col6_frame, "第六列", sixth_row_keys)

# 次鍵區內容
sub_keys_frame = tk.Frame(sub_keys_tab)
sub_keys_frame.pack(fill='both', expand=True, padx=10, pady=10)

# 創建次鍵區的水平排列容器
sub_horizontal_frame = tk.Frame(sub_keys_frame)
sub_horizontal_frame.pack(fill='x', expand=True)

# 定義次鍵區的 ID 陣列（合併所有次鍵）
sub_keys_all = ["99", "70", "119", "110", "101", "103", "111", "107", "109", "102", "104", "108", "106"]  # PrtSc, ScrLk, Pause, Ins, Home, PageUp, Del, End, PageDown, ↑, ←, ↓, →

# 定義數字鍵區的 ID 陣列
num_keys_first_row = ["82", "79", "80", "81", "75", "76", "77", "71", "72", "73"]  # Num0, Num1, Num2, Num3, Num4, Num5, Num6, Num7, Num8, Num9
num_keys_second_row = ["69", "98", "55", "74","78", "83", "96"]  # NumEnter, Num/, Num*, Num-, Num+, Num., Num/  

# 創建次鍵區
sub_col_frame = tk.Frame(sub_horizontal_frame)
sub_col_frame.pack(side='left', fill='y', padx=(0, 40))
create_key_column(sub_col_frame, "次鍵區", sub_keys_all)

# 添加垂直分隔線
separator_line = tk.Frame(sub_horizontal_frame, width=2, bg='lightgray')
separator_line.pack(side='left', fill='y', padx=(0, 40))

# 創建數字鍵區（分成兩行並排顯示）
num_col_frame = tk.Frame(sub_horizontal_frame)
num_col_frame.pack(side='left', fill='y', padx=(0, 30))

# 創建水平排列的容器
num_horizontal_frame = tk.Frame(num_col_frame)
num_horizontal_frame.pack(fill='x', expand=True, anchor='n')

# 第一行：數字鍵
num_keys_frame = tk.Frame(num_horizontal_frame)
num_keys_frame.pack(side='left', fill='y', padx=(0, 20), anchor='n')
create_key_column(num_keys_frame, "數字鍵", num_keys_first_row)

# 第二行：功能鍵
num_func_frame = tk.Frame(num_horizontal_frame)
num_func_frame.pack(side='left', fill='y', padx=(0, 0), anchor='n')
create_key_column(num_func_frame, "功能鍵", num_keys_second_row)

# 關於分頁內容
# 創建關於頁面的框架
about_frame = tk.Frame(about_tab)
about_frame.pack(fill='both', expand=True, padx=20, pady=20)

# 創建水平排列的容器框架
about_horizontal_frame = tk.Frame(about_frame)
about_horizontal_frame.pack(fill='both', expand=True)

# 左側：關於區域
about_left_frame = tk.Frame(about_horizontal_frame)
about_left_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))

# 標題
title_label = tk.Label(about_left_frame, text="鍵盤偵測工具", 
                       font=('Arial', 24, 'bold'), fg='#333333')
title_label.pack(pady=(20, 0))

# 版本資訊
version_label = tk.Label(about_left_frame, text="版本: 1.0.0", 
                         font=('Arial', 14), fg='#666666')
version_label.pack(pady=(0, 10))

# 功能說明
features_text = """使用說明：
1. 程式會自動偵測鍵盤按鍵
2. 在 user 資料夾中放入自訂按鍵圖片
3. 圖片名稱必須與按鍵列表中的名稱相符
4. 放入新圖片後需要重啟程式
5. 圖片最小建議為 60px * 60px

注意事項：
- 請確保 user 資料夾中的圖片為 PNG 格式
- 程式可能需要管理員權限才能監聽全域鍵盤事件
- 如遇到問題，請檢查防毒軟體是否阻擋程式執行
- 更改設置後必須點擊儲存，才能生效(包含點恢復預設後)
- 即時按鍵尺寸設定，必須按照格式: 寬度x高度
"""

features_label = tk.Label(about_left_frame, text=features_text, 
                         font=('Arial', 12), fg='#444444',
                         justify='left', anchor='w')
features_label.pack(pady=(0, 20))

# 版權資訊（移到左側功能說明下方）
copyright_label = tk.Label(about_left_frame, text="Copyright © 2025 shanshan 版權所有", 
                           font=('Arial', 10), fg='#888888')
copyright_label.pack(pady=(0, 30))

# 右側：設置區域
about_right_frame = tk.Frame(about_horizontal_frame)
about_right_frame.pack(side='right', fill='both', expand=True, padx=(20, 0))

# 設置標題
settings_title_label = tk.Label(about_right_frame, text="設置", 
                               font=('Arial', 24, 'bold'), fg='#333333')
settings_title_label.pack(pady=(10, 10))

# 創建設置框架
settings_frame = tk.Frame(about_right_frame)
settings_frame.pack(fill='both', expand=True, padx=10, pady=20)

def create_setting_item(parent, label_text, value_text, row, config_key):
    """創建單個設置項目"""
    # 標籤 - 使用 'e' 對齊並置中
    label = tk.Label(parent, text=label_text, font=('Arial', 12, 'bold'), 
                     fg='#444444', anchor='e')
    label.grid(row=row, column=0, sticky='e', padx=(0, 10), pady=5)
    
    # 輸入框 - 使用 'w' 對齊並置中
    entry = tk.Entry(parent, font=('Arial', 12), fg='#333333', width=15)
    entry.insert(0, str(value_text))
    entry.grid(row=row, column=1, sticky='w', pady=5, padx=(0, 10))
    
    # 保存輸入框引用
    if not hasattr(parent, 'entries'):
        parent.entries = {}
    parent.entries[config_key] = entry

def create_setting_dropdown(parent, label_text, options, current_value, row, config_key):
    """創建下拉式選單設置項目"""
    # 標籤 - 使用 'e' 對齊並置中
    label = tk.Label(parent, text=label_text, font=('Arial', 12, 'bold'), 
                     fg='#444444', anchor='e')
    label.grid(row=row, column=0, sticky='e', padx=(0, 10), pady=5)
    
    # 下拉式選單 - 使用 'w' 對齊並置中
    dropdown = ttk.Combobox(parent, values=options, state='readonly', width=12, font=('Arial', 12))
    dropdown.set(current_value)
    dropdown.grid(row=row, column=1, sticky='w', pady=5, padx=(0, 10))
    
    # 保存下拉式選單引用
    if not hasattr(parent, 'entries'):
        parent.entries = {}
    parent.entries[config_key] = dropdown

def create_setting_items(parent):
    """創建設置項目"""
    # 配置grid權重，讓設置項目在容器內置中
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    
    # 顯示config設定
    create_setting_item(parent, "自訂圖片目錄:", config.get('user_dir', DEFAULT_CONFIG['user_dir']), 0, "user_dir")
    create_setting_item(parent, "視窗寬度:", config.get('window_width', DEFAULT_CONFIG['window_width']), 1, "window_width")
    create_setting_item(parent, "視窗高度:", config.get('window_height', DEFAULT_CONFIG['window_height']), 2, "window_height")
    create_setting_item(parent, "即時按鍵尺寸:", f"{config.get('realtime_image_size', DEFAULT_CONFIG['realtime_image_size'])[0]} x {config.get('realtime_image_size', DEFAULT_CONFIG['realtime_image_size'])[1]}", 3, "realtime_image_size")
    create_setting_item(parent, "每行按鍵數量:", config.get('max_keys_per_row', DEFAULT_CONFIG['max_keys_per_row']), 4, "max_keys_per_row")
    create_setting_item(parent, "最大行數:", config.get('max_rows', DEFAULT_CONFIG['max_rows']), 5, "max_rows")
    
    # 即時按鍵背景設定
    background_options = ["預設", "藍幕", "綠幕"]
    current_background = config.get('realtime_background', DEFAULT_CONFIG['realtime_background'])
    # 將英文值轉換為中文顯示
    if current_background == "default":
        current_background = "預設"
    elif current_background == "blue":
        current_background = "藍幕"
    elif current_background == "green":
        current_background = "綠幕"
    create_setting_dropdown(parent, "即時按鍵背景:", background_options, current_background, 6, "realtime_background")

def create_settings_buttons(parent):
    """創建設置按鈕"""
    # 按鈕框架
    button_frame = tk.Frame(parent)
    button_frame.grid(row=8, column=0, columnspan=2, pady=20, sticky='ew')
    
    # 配置按鈕框架的grid權重，讓按鈕在框架內置中
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    
    # 恢復預設按鈕
    reset_button = tk.Button(button_frame, text="恢復預設", 
                             command=lambda: reset_to_default(parent),
                             font=('Arial', 12, 'bold'),
                             bg='#f0f0f0', fg='black',
                             relief='raised', borderwidth=2,
                             padx=20, pady=8)
    reset_button.grid(row=0, column=0, padx=(0, 10))
    
    # 儲存按鈕
    save_button = tk.Button(button_frame, text="儲存設定", 
                            command=lambda: save_config(parent),
                            font=('Arial', 12, 'bold'),
                            bg='white', fg='black',
                            relief='raised', borderwidth=2,
                            padx=20, pady=8)
    save_button.grid(row=0, column=1, padx=(10, 0))

# 創建設置項目
create_setting_items(settings_frame)

# 創建狀態標籤並保存引用到settings_frame（移到按鈕上方）
save_status_label = tk.Label(settings_frame, text="", font=('Arial', 10), fg="green")
save_status_label.grid(row=7, column=0, columnspan=2, pady=(0, 0), sticky='ew')
settings_frame.save_status_label = save_status_label

# 創建按鈕
create_settings_buttons(settings_frame)

# 添加垂直分隔線
separator_line = tk.Frame(about_horizontal_frame, width=2, bg='lightgray')
separator_line.pack(side='left', fill='y', padx=(0, 0))


# 設置管理相關函數

def save_config(parent):
    """儲存設定到config.json"""
    try:
        # 獲取所有輸入框的值
        new_config = config.copy()
        
        # 更新設定值
        new_config['user_dir'] = parent.entries['user_dir'].get()
        new_config['window_width'] = int(parent.entries['window_width'].get())
        new_config['window_height'] = int(parent.entries['window_height'].get())
        
        # 處理即時圖片尺寸（格式：寬度 x 高度）
        size_text = parent.entries['realtime_image_size'].get()
        if 'x' in size_text:
            width, height = map(int, size_text.split('x'))
            new_config['realtime_image_size'] = [width, height]
        
        # 更新按鍵排列設定
        new_config['max_keys_per_row'] = int(parent.entries['max_keys_per_row'].get())
        new_config['max_rows'] = int(parent.entries['max_rows'].get())
        
        # 處理背景設定
        background_text = parent.entries['realtime_background'].get()
        if background_text == "預設":
            new_config['realtime_background'] = "default"
        elif background_text == "藍幕":
            new_config['realtime_background'] = "blue"
        elif background_text == "綠幕":
            new_config['realtime_background'] = "green"
        
        # 寫入config.json
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(new_config, f, indent=2, ensure_ascii=False)
        
        # 顯示成功訊息
        parent.save_status_label.config(text="設定已儲存！", fg="green")
        parent.save_status_label.after(2000, lambda: parent.save_status_label.config(text="", fg="green"))
        
        # 更新全域變數
        global WINDOW_WIDTH, WINDOW_HEIGHT, REALTIME_IMAGE_SIZE, MAX_KEYS_PER_ROW, MAX_ROWS, REALTIME_BACKGROUND
        WINDOW_WIDTH = new_config['window_width']
        WINDOW_HEIGHT = new_config['window_height']
        REALTIME_IMAGE_SIZE = tuple(new_config['realtime_image_size'])
        MAX_KEYS_PER_ROW = new_config['max_keys_per_row']
        MAX_ROWS = new_config['max_rows']
        REALTIME_BACKGROUND = new_config['realtime_background']
        
        # 重新設定視窗大小
        set_window_size()
        
        # 應用新的背景設定
        apply_realtime_background()
        
    except Exception as e:
        parent.save_status_label.config(text=f"儲存失敗: {str(e)}", fg="red")
        parent.save_status_label.after(3000, lambda: parent.save_status_label.config(text="", fg="red"))

def reset_to_default(parent):
    """恢復到預設設定"""
    try:
        # 獲取預設設定
        default_config = DEFAULT_CONFIG.copy()
        default_config['realtime_image_size'] = [80, 80]
        default_config['max_keys_per_row'] = 10
        default_config['max_rows'] = 3
        default_config['realtime_background'] = "default"
        
        # 更新輸入框的值
        parent.entries['user_dir'].delete(0, tk.END)
        parent.entries['user_dir'].insert(0, default_config['user_dir'])
        
        parent.entries['window_width'].delete(0, tk.END)
        parent.entries['window_width'].insert(0, default_config['window_width'])
        
        parent.entries['window_height'].delete(0, tk.END)
        parent.entries['window_height'].insert(0, default_config['window_height'])
        
        parent.entries['realtime_image_size'].delete(0, tk.END)
        parent.entries['realtime_image_size'].insert(0, f"{default_config['realtime_image_size'][0]} x {default_config['realtime_image_size'][1]}")
        
        parent.entries['max_keys_per_row'].delete(0, tk.END)
        parent.entries['max_keys_per_row'].insert(0, default_config['max_keys_per_row'])
        
        parent.entries['max_rows'].delete(0, tk.END)
        parent.entries['max_rows'].insert(0, default_config['max_rows'])
        
        # 更新背景設定
        parent.entries['realtime_background'].set("預設")
        
        # 顯示成功訊息
        parent.save_status_label.config(text="已恢復預設設定！", fg="blue")
        parent.save_status_label.after(2000, lambda: parent.save_status_label.config(text="", fg="blue"))
        
    except Exception as e:
        parent.save_status_label.config(text=f"恢復預設失敗: {str(e)}", fg="red")
        parent.save_status_label.after(3000, lambda: parent.save_status_label.config(text="", fg="red"))

def set_window_size():
    """設定頁面大小固定為鍵盤配置的大小"""
    # 計算鍵盤配置所需的最小尺寸
    keyboard_width = WINDOW_WIDTH  # 主鍵區 + 次鍵區 + 數字鍵區的寬度
    keyboard_height = WINDOW_HEIGHT  # 鍵盤配置的高度
    root.geometry(f"{keyboard_width}x{keyboard_height}")
    root.resizable(False, False)  # 固定視窗大小
    
set_window_size()

# 鍵盤監聽
def keyboard_event_handler(event):
    """統一的鍵盤事件處理函數"""
    if event.event_type == keyboard.KEY_DOWN:
        show_key(event)
    elif event.event_type == keyboard.KEY_UP:
        hide_key(event)

keyboard.hook(keyboard_event_handler)

# 設定焦點到根視窗以接收鍵盤事件
root.focus_set()

root.mainloop()