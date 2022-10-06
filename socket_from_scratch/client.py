#!/usr/bin/python3
import socket
import time as t
import threading

is_valid_ipv4 = lambda ip: len(ip.split(".")) == 4 and all(0 <= int(i) <= 255 for i in ip.split("."))
sleep = lambda seconds: t.sleep(seconds)


def send_message(conn):
    while True:
        msg = input()
        conn.send(msg.encode("utf-8"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Validate IP address and port
    ip = ''
    while not is_valid_ipv4(ip):
        ip = input("Server IP: ")
    
    threads = []
    port = int(input("Server Port: "))

    # Connect to server
    s.connect((ip, port))
    name = input("Enter your name: ")
    s.send(name.encode("utf-8"))
    threads.append(threading.Thread(target=send_message, args=(s,)))
    threads[-1].start()

    while True:
        try:
            data = s.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'), end='')
        except KeyboardInterrupt:
            # disable threads
            for thread in threads:
                thread.do_run = False
            # close socket
            s.close()
            break

