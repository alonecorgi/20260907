import socket

HOST = "0.0.0.0"  # 監聽所有網路介面
PORT = 5000

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"=== Server 已啟動，等待樹莓派 Client 連線... (Port: {PORT}) ===")

    # 1. accept 放在迴圈外，連線一次後持續操作
    conn, addr = server_socket.accept()
    print(f"\n[成功連線] Client 已連入，來源：{addr[0]}:{addr[1]}")
    print("----------------------------------------")
    print("可用指令範例: LED_ON | LED_OFF | FAN_ON | FAN_OFF | exit")
    print("----------------------------------------\n")

    try:
        while True:
            cmd = input("請輸入指令: ").strip()
            if not cmd:
                continue
            
            # 2. 透過 Socket 發送資料 (轉為 utf-8 bytes)
            conn.sendall(cmd.encode('utf-8'))
            
            # 3. 忽略大小寫判斷 exit
            if cmd.lower() == "exit":
                print("發送 exit 指令，結束連線。")
                break
                
    except (BrokenPipeError, ConnectionResetError):
        print("\n[錯誤] 樹莓派 Client 已強制中斷連線！")
    except Exception as e:
        print(f"\n傳送發生錯誤: {e}")
    finally:
        conn.close()
        server_socket.close()
        print("Server 已安全關閉。")

if __name__ == "__main__":
    run_server()