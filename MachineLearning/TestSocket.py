import socket, time, struct

def send_udp_data():
    host_ip = socket.gethostname()
    port = 4510
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host_ip, port))
    while True:
        msg = -25.54
        message = struct.pack("f", msg)
        print repr(message)
        sock.send(message)
        time.sleep(1)

if __name__=="__main__":
    send_udp_data()