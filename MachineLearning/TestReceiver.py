import socket, struct

def read_udp_data():
    # add more variable arrays here
    host_ip = socket.gethostname()
    port = 4510
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host_ip, port))
    while True:
        packet = sock.recvfrom(65565)[0]
        # print repr(packet)
        try:
            print struct.unpack("4s", packet)[0]
            if struct.unpack("4s", packet)[0] == "STOP":
                break
        except struct.error:
            continue
    sock.close()
    print "Program Stopped"


if __name__=="__main__":
    read_udp_data()