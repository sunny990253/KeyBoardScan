import keyboard
import time
import json

def on_key_event(event):
    """處理鍵盤事件"""
    print(f"\n{'='*60}")
    print(f"按鍵事件: {event.event_type}")
    print(f"按鍵名稱: {event.name}")
    print(f"Scan Code: {event.scan_code}")
    print(f"設備: {event.device}")
    print(f"時間戳: {event.time}")
    print(f"是否為數字鍵盤: {event.is_keypad}")
    print(f"修飾鍵: {event.modifiers}")
    
    # 顯示所有可用屬性
    print(f"\n所有屬性:")
    for attr in dir(event):
        if not attr.startswith('_'):
            try:
                value = getattr(event, attr)
                if not callable(value):
                    print(f"  {attr}: {value}")
            except:
                pass
    
    print(f"{'='*60}")

def save_key_mapping():
    """保存按鍵映射到檔案"""
    key_mapping = {}
    
    def capture_key(event):
        if event.event_type == keyboard.KEY_DOWN:
            key_mapping[str(event.scan_code)] = {
                "name": event.name,
                "scan_code": event.scan_code,
                "device": event.device,
                "is_keypad": event.is_keypad
            }
            print(f"已記錄: Scan Code {event.scan_code} -> {event.name}")
    
    print("\n開始記錄按鍵映射...")
    print("請按下您想要記錄的按鍵")
    print("按 Ctrl+C 停止記錄")
    
    keyboard.hook(capture_key)
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        keyboard.unhook_all()
        
        # 保存到檔案
        with open("captured_keys.json", "w", encoding="utf-8") as f:
            json.dump(key_mapping, f, indent=2, ensure_ascii=False)
        
        print(f"\n已保存 {len(key_mapping)} 個按鍵映射到 captured_keys.json")
        return key_mapping

def main():
    """主函數"""
    print("按鍵識別工具")
    print("1. 即時監聽按鍵事件")
    print("2. 記錄按鍵映射")
    print("3. 退出")
    
    while True:
        choice = input("\n請選擇功能 (1-3): ").strip()
        
        if choice == "1":
            print("\n開始監聽按鍵事件...")
            print("請按下任意按鍵來查看資訊")
            print("按 Ctrl+C 停止監聽")
            
            keyboard.hook(on_key_event)
            
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                keyboard.unhook_all()
                print("\n已停止監聽")
                
        elif choice == "2":
            key_mapping = save_key_mapping()
            
        elif choice == "3":
            print("程式結束")
            break
            
        else:
            print("無效選擇，請重新輸入")

if __name__ == "__main__":
    main()
