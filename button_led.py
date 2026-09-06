import RPi.GPIO as GPIO
import time
# 1. 設定腳位編號模式為 BCM (對應 GPIO 號碼，如 GPIO 17)
GPIO.setmode(GPIO.BCM)

# 2. 定義腳位
LED_PIN = 17
BUTTON_PIN = 22

# 3. 設定腳位輸入/輸出模式
# LED 為輸出 (OUTPUT)
GPIO.setup(LED_PIN, GPIO.OUT)

# 按鈕為輸入 (INPUT)，並啟用內部拉高電阻 (PULL_UP)
# 這樣按鈕平常沒按是 1 (HIGH)，按下時接地變成 0 (LOW)
GPIO.setup(BUTTON_PIN, GPIO.IN)


try:
    while True:
        # 直觀地直接讀取按鈕當前狀態 (回傳 GPIO.HIGH 或 GPIO.LOW)
        button_state = GPIO.input(BUTTON_PIN)
        print (f"{button_state}")
        if button_state == GPIO.LOW:  # 按鈕被按下了（接地變成 LOW）
            GPIO.output(LED_PIN, GPIO.HIGH)  # 讓 LED 腳位輸出高電位（點亮）
            print("button click")
            
        else:                         # 按鈕沒被按下（平常是 HIGH）
            GPIO.output(LED_PIN, GPIO.LOW)   # 讓 LED 腳位輸出低電位（熄滅）
            print("button no click")
        # 稍微暫停 0.05 秒，避免 CPU 100% 滿載
        time.sleep(1)

except KeyboardInterrupt:
    print("\n程式結束")

finally:
    # 離開程式時清理 GPIO 設定，確保腳位恢復安全狀態
    GPIO.cleanup()
