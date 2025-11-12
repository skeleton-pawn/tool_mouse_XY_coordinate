# mouse_point.py
from pynput import mouse, keyboard

coords = []          # 저장된 좌표 리스트
shift_pressed = False
MAX_POINTS = 2       # 최대 2개까지만 저장

def on_press(key):
    global shift_pressed
    if key == keyboard.Key.shift:
        shift_pressed = True

def on_release(key):
    global shift_pressed
    if key == keyboard.Key.shift:
        shift_pressed = False

def on_click(x, y, button, pressed):
    global coords
    if pressed and shift_pressed:
        coords.append((int(x), int(y)))
        print(f"[SHIFT + Click] 좌표 {len(coords)}: X={int(x)}, Y={int(y)}")
        print(f"for pyautogui--->({int(x)}, {int(y)})")

        if len(coords) >= MAX_POINTS:
            save_coords()
            print(f"\n{MAX_POINTS}개 좌표 저장 완료 → coords.txt")
            print("프로그램을 종료합니다.")
            return False  # 클릭 리스너 종료

def save_coords():
    with open("coords.txt", "w", encoding="utf-8") as f:
        for i, (x, y) in enumerate(coords, start=1):
            f.write(f"{i}: X={x}, Y={y}\n")
            f.write(f"pyautogui.click({x}, {y})\n")
        f.write("\n")
    print(f"\n coords.txt 파일에 {len(coords)}개 좌표를 저장했습니다.")

# 리스너 실행
with keyboard.Listener(on_press=on_press, on_release=on_release) as kl, \
     mouse.Listener(on_click=on_click) as ml:
    print("왼쪽 Shift + 마우스 클릭 시 좌표를 기록합니다.")
    print(f"최대 {MAX_POINTS}개 좌표가 저장되면 자동 종료됩니다.\n")
    kl.join()
    ml.join()
