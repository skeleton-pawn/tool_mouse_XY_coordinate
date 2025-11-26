# mouse_point.py
from pynput import mouse, keyboard
import sys

coords = []          # 저장된 좌표 리스트
shift_pressed = False
MAX_POINTS = 2       # 최대 2개까지만 저장

# Listener 객체를 전역으로 보관하면 콜백에서 중지할 수 있습니다.
kl = None
ml = None

def on_press(key):
    """Shift 키가 눌렸는지 표시한다. 왼쪽/오른쪽 Shift 모두 처리."""
    global shift_pressed
    try:
        if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
            shift_pressed = True
    except AttributeError:
        # 특수키가 아닌 경우 무시
        pass

def on_release(key):
    """Shift 키가 해제되면 상태를 갱신."""
    global shift_pressed
    try:
        if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
            shift_pressed = False
    except AttributeError:
        pass

def on_click(x, y, button, pressed):
    """마우스 클릭 핸들러: Shift가 눌린 상태에서 클릭하면 좌표를 저장."""
    global coords, kl
    # 왼쪽 버튼 + Shift 조합만 기록
    if pressed and shift_pressed and button == mouse.Button.left:
        coords.append((int(x), int(y)))
        print(f"[SHIFT + Click] 좌표 {len(coords)}: X={int(x)}, Y={int(y)}")
        print(f"for pyautogui--->({int(x)}, {int(y)})")

        if len(coords) >= MAX_POINTS:
            save_coords()
            print(f"\n{MAX_POINTS}개 좌표 저장 완료 → coords.txt")
            print("프로그램을 종료합니다.")
            # 키보드 리스너도 중지시켜 전체 프로그램을 종료하게 함
            try:
                if kl is not None:
                    kl.stop()
            except Exception:
                pass
            return False  # 클릭 리스너 종료

def save_coords():
    with open("coords.txt", "w", encoding="utf-8") as f:
        for i, (x, y) in enumerate(coords, start=1):
            f.write(f"{i}: X={x}, Y={y}\n")
            f.write(f"pyautogui.click({x}, {y})\n")
        f.write("\n")
    print(f"\ncoords.txt 파일에 {len(coords)}개 좌표를 저장했습니다.")


def main():
    global kl, ml
    kl = keyboard.Listener(on_press=on_press, on_release=on_release)
    ml = mouse.Listener(on_click=on_click)

    kl.start()
    ml.start()

    print("왼쪽 Shift + 마우스 클릭 시 좌표를 기록합니다.")
    print(f"최대 {MAX_POINTS}개 좌표가 저장되면 자동 종료됩니다.\n")

    # 두 리스너가 종료될 때까지 대기
    try:
        kl.join()
        ml.join()
    except KeyboardInterrupt:
        # 사용자가 Ctrl+C로 중지할 때
        try:
            if kl is not None:
                kl.stop()
            if ml is not None:
                ml.stop()
        except Exception:
            pass
        sys.exit(0)


if __name__ == "__main__":
    main()
