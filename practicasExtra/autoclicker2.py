import pyautogui
import time
import threading

class AutoClicker:
    def __init__(self, interval=0.1):
        self.interval = interval
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True
        self._click_thread = threading.Thread(target=self._click)
        self._click_thread.start()

    def stop_clicking(self):
        self.running = False
        self._click_thread.join()

    def _click(self):
        while self.running:
            pyautogui.click()
            time.sleep(self.interval)

    def exit(self):
        self.stop_clicking()
        self.program_running = False

if __name__ == "__main__":
    clicker = AutoClicker(interval=0.1)  

    def on_press(key):
        if key == 's':
            if clicker.running:
                clicker.stop_clicking()
            else:
                clicker.start_clicking()
        elif key == 'q':
            clicker.exit()
            return False

    print("Press 's' to start/stop clicking and 'q' to quit.")
    while clicker.program_running:
        key = input("Enter command: ").strip().lower()
        on_press(key)
