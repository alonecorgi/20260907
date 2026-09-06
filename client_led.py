import socket
import time
import RPi.GPIO as GPIO

# --- 硬體腳位設定 ---
# 腳位號碼為 BCM 編號：GPIO 17 接 LED，GPIO 27 接風扇/繼電器
LED_PIN = 17
FAN_PIN = 41

# 1. 初始化 GPIO 設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)

# 預設狀態為關閉 (LOW)
GPIO.output(LED_PIN, GPIO.LOW)

# --- 網路設定 ---
SERVER_IP = "192.168.1.75"  # 請替換為 Server 的實際 IP
PORT = 5000

def process_command(command):
    """ 解析指令並執行相應動作 """
    cmd = command.strip().upper()
    print(f"[{time.strftime('%H:%M:%S')}] 執行指令: {cmd}")
    
    if cmd == "LED_ON":
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("  LED ON)")
    elif cmd == "LED_OFF":
        GPIO.output(LED_PIN, GPIO.LOW)
        print("  LED OFF")
    else:
        print("  WAIT SERVER ")

def run_client():
    while True:
        try:
            print(f"連線中... 目標：{SERVER_IP}:{PORT}")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, PORT))
            print("連線成功！等待 Server 發送指令...\n")

            while True:
                # 阻塞等待接收 Server 指令
                data = client_socket.recv(1024)
                if not data:
                    print("Server 已中斷連線。")
                    break
                
                command = data.decode('utf-8')
                process_command(command)

        except ConnectionRefusedError:
            print("連線被拒絕，請確認 Server 端是否已啟動程式。")
        except Exception as e:
            print(f"發生連線錯誤: {e}")
        finally:
            client_socket.close()
            print("連線已關閉，5 秒後嘗試重新連線...\n")
            time.sleep(5)

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\n使用者中斷程式")
    finally:
        # 結束程式時清理腳位設定，恢復安全狀態
        GPIO.cleanup()
        print("GPIO 已清理完畢。")