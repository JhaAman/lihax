import socket, time, struct

def send_udp_data():
    host_ip = socket.gethostname()
    port = 4510
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host_ip, port))
    while True:
        message = struct.pack("f", 1.23)
        print repr(message)
        # print struct.unpack("4s", message)
        sock.send(message)
        time.sleep(1)

if __name__=="__main__":
    send_udp_data()