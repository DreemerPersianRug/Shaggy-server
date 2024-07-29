import socket
import struct
import random

def createUDPResponse(length, pattern=True, small_pattern=True):
    header = struct.pack('>I', 0x02020304)
    header += struct.pack('>I', 0x0f000000)
    header += struct.pack('>I', 0x00000000)
    header += struct.pack('<I', length)
    
    blocks = b''
    if not pattern:
        for _ in range(length):
            if not small_pattern:
                blocks += struct.pack('<I', random.randint(0x3f9f0000, 0x3f9ff000))
            else:
                blocks += struct.pack('<I', 0x3f9f0000)
    else:
        data = [
            0x26000000, 0x1f000000, 0x1d000000, 0x15000000,
            0x14000000, 0x20000000, 0x19000000, 0x17000000,
            0x16000000, 0x32000000, 0x84ffffff, 0x8dffffff,
            0x91ffffff, 0x79ffffff, 0x87ffffff, 0x83ffffff,
            0x8dffffff, 0x94ffffff, 0x87ffffff, 0x90ffffff,
            0x09000000, 0x06000000, 0xfdffffff, 0x10000000,
            0x02000000, 0xf9ffffff, 0xe8ffffff, 0xf7ffffff,
            0xfdffffff, 0x06000000
        ]
    
        for d in data:
            blocks += struct.pack('>I', d)

    return header + blocks

def readUDPRequest(data):
    udp_preambule = struct.unpack('<I', data[0:4])[0]
    udp_pack_cnt = struct.unpack('<I', data[4:8])[0]
    sens_cmd_preambule = struct.unpack('<I', data[8:12])[0]
    sens_cmd_get_raw = struct.unpack('<I', data[12:16])[0]
    sensor = struct.unpack('<I', data[16:20])[0]
    n = struct.unpack('<I', data[20:24])[0]

    print(f"udp_preambule: {udp_preambule}")
    print(f"udp_pack_cnt: {udp_pack_cnt}")
    print(f"sens_cmd_preambule: {sens_cmd_preambule}")
    print(f"sens_cmd_get_raw: {sens_cmd_get_raw}")
    print(f"sensor: {sensor}")
    print(f"n: {n}")

    return (udp_preambule, udp_pack_cnt, sens_cmd_preambule, sens_cmd_get_raw, sensor, n)

def reciver(local_ip='192.168.0.102', local_port=50018, remote_ip='192.168.0.106', remote_port=50019):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, local_port))

    print("Waiting for data...")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print("Received message:", data)

            decode_data = readUDPRequest(data)
            response = createUDPResponse(decode_data[-1] * 3, False, False)
            print(response)
            sock.sendto(response, (remote_ip, remote_port))
            print(f"Response sent {response} {(remote_ip, remote_port)}")

        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    reciver('192.168.0.102', 50051, '192.168.0.106', 50052)