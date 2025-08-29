#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按鍵圖片產生器
產生 60x60 像素、黑框圓角、透明背景的按鍵圖片
"""

from PIL import Image, ImageDraw, ImageFont
import json
import os
import argparse

class KeyImageGenerator:
    def __init__(self, output_dir="generated_keys"):
        """初始化圖片產生器"""
        self.output_dir = output_dir
        self.image_size = (100, 100)
        self.corner_radius = 15  # 增加圓角半徑
        self.border_width = 4    # 增加邊框寬度
        self.border_color = (0, 0, 0)  # 黑色邊框
        self.background_color = (255, 255, 255, 0)  # 透明背景
        self.text_color = (0, 0, 0)  # 黑色文字
        
        # 創建輸出目錄
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 嘗試載入字體，如果沒有則使用預設
        try:
            self.font = ImageFont.truetype("arial.ttf", 50) #字形大小設置
        except:
            try:
                self.font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 50)
            except:
                self.font = ImageFont.load_default()
    
    def create_rounded_rectangle(self, size, corner_radius, fill_color, border_color, border_width):
        """創建圓角矩形"""
        # 創建透明背景的圖片
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # 計算圓角矩形的邊界
        left = border_width // 2
        top = border_width // 2
        right = size[0] - border_width // 2
        bottom = size[1] - border_width // 2
        
        # 繪製圓角矩形
        draw.rounded_rectangle(
            [left, top, right, bottom],
            radius=corner_radius,
            fill=fill_color,
            outline=border_color,
            width=border_width
        )
        
        return image
    
    def create_key_image(self, text, filename=None):
        """創建單個按鍵圖片"""
        if filename is None:
            # 清理文字以創建有效的檔案名稱
            safe_text = self._sanitize_filename(text)
            filename = f"{safe_text}.png"
        
        # 創建圓角矩形圖片
        image = self.create_rounded_rectangle(
            self.image_size,
            self.corner_radius,
            (255, 255, 255, 255),  # 白色背景
            self.border_color,
            self.border_width
        )
        
        # 添加文字
        draw = ImageDraw.Draw(image)
        
        # 計算文字位置（置中），考慮邊框寬度
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 考慮邊框寬度，讓文字在實際按鍵區域內置中
        x = (self.image_size[0] - text_width) // 2
        y = (self.image_size[1] - text_height) // 2
        
        # 微調Y軸位置，文字置中效果微調
        y_offset = 4  # 向上微調8像素
        y -= y_offset
        
        # 繪製文字
        draw.text((x, y), text, fill=self.text_color, font=self.font)
        
        # 保存圖片
        output_path = os.path.join(self.output_dir, filename)
        image.save(output_path, 'PNG')
        print(f"已創建: {output_path}")
        
        return output_path
    
    def _sanitize_filename(self, text):
        """清理檔案名稱，移除或替換無效字元"""
        import re
        
        # 替換特殊字元
        replacements = {
            '*': 'star',
            '?': 'question',
            '<': 'lt',
            '>': 'gt',
            '|': 'pipe',
            '"': 'quote',
            ':': 'colon',
            '/': 'slash',
            '\\': 'backslash',
            '↑': 'ArrowUp',
            '↓': 'ArrowDown',
            '←': 'ArrowLeft',
            '→': 'ArrowRight',
            # 移除無法顯示的 Unicode 符號映射
            # '⌫': 'Backspace',
            # '⇧': 'Shift', 
            # '⇪': 'CapsLk',
            # '⇥': 'Tab',
            # '⇤': 'BackTab'
        }
        
        # 應用替換
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        # 移除其他無效字元
        text = re.sub(r'[<>:"/\\|?*]', '', text)
        
        # 如果檔案名稱為空，使用預設名稱
        if not text.strip():
            text = "Key"
        
        return text
    
    def create_from_key_map(self, key_map_file="key_map.json"):
        """根據 key_map.json 創建所有按鍵圖片"""
        try:
            with open(key_map_file, 'r', encoding='utf-8') as f:
                key_map = json.load(f)
            
            print(f"從 {key_map_file} 載入 {len(key_map)} 個按鍵")
            
            for keycode, key_info in key_map.items():
                key_name = key_info.get("name", f"Key{keycode}")
                image_filename = key_info.get("png", f"{key_name}.png")
                
                # 創建按鍵圖片
                self.create_key_image(key_name, image_filename)
            
            print(f"完成！所有圖片已保存到 {self.output_dir} 目錄")
            
        except FileNotFoundError:
            print(f"錯誤：找不到 {key_map_file} 檔案")
        except Exception as e:
            print(f"錯誤：{e}")
    
    def create_custom_keys(self, keys_list):
        """根據自定義按鍵列表創建圖片"""
        print(f"創建 {len(keys_list)} 個自定義按鍵圖片")
        
        for key in keys_list:
            self.create_key_image(key)
        
        print(f"完成！所有圖片已保存到 {self.output_dir} 目錄")
    
    def create_common_keys(self):
        """創建特殊的按鍵圖片"""
        common_keys = [
            
            # 特殊鍵
             'CapsLk', 'Shift', 'Ctrl', 'Alt',
            'Enter', 'Space', 'Win', 'Menu',
            
            # 方向鍵
            '↑', '↓', '←', '→',
            
            # 符號鍵
            '*', '-', '+', '=', '/', '\\', '.', ',', ';', "'",
            '[', ']', '`', '~', '!', '@', '#', '$', '%', '^', '&',
            
            # 注意：以下符號因字體不支援已移除
            # '⌫', '⌦', '⌧', '⇧', '⇪', '⇥', '⇤',
            
            # 其他常用鍵
            'Ins', 'Del', 'Home', 'End', 'PGUP', 'PGDN',
            'PrtSc', 'ScrLk', 'Pause', 'Num'
        ]
        
        self.create_custom_keys(common_keys)

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='按鍵圖片產生器')
    parser.add_argument('--output', '-o', default='generated_keys', 
                       help='輸出目錄 (預設: generated_keys)')
    parser.add_argument('--keymap', '-k', action='store_true',
                       help='根據 key_map.json 創建圖片')
    parser.add_argument('--common', '-c', action='store_true',
                       help='創建常見按鍵圖片')
    parser.add_argument('--keys', nargs='+',
                       help='創建指定的按鍵圖片')
    
    args = parser.parse_args()
    
    # 創建圖片產生器
    generator = KeyImageGenerator(args.output)
    
    if args.keymap:
        # 根據 key_map.json 創建
        generator.create_from_key_map()
    elif args.common:
        # 創建常見按鍵
        generator.create_common_keys()
    elif args.keys:
        # 創建指定的按鍵
        generator.create_custom_keys(args.keys)
    else:
        # 互動模式
        print("按鍵圖片產生器")
        print("=" * 30)
        print("1. 根據 key_map.json 創建所有按鍵圖片")
        print("2. 創建常見按鍵圖片")
        print("3. 創建自定義按鍵圖片")
        print("4. 退出")
        
        while True:
            try:
                choice = input("\n請選擇選項 (1-4): ").strip()
                
                if choice == '1':
                    generator.create_from_key_map()
                    break
                elif choice == '2':
                    generator.create_common_keys()
                    break
                elif choice == '3':
                    keys_input = input("請輸入按鍵名稱，用空格分隔: ").strip()
                    if keys_input:
                        keys_list = keys_input.split()
                        generator.create_custom_keys(keys_list)
                    break
                elif choice == '4':
                    print("退出程式")
                    break
                else:
                    print("無效選項，請重新選擇")
                    
            except KeyboardInterrupt:
                print("\n\n程式被中斷")
                break
            except Exception as e:
                print(f"錯誤：{e}")

if __name__ == "__main__":
    main()
