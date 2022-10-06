import socket
import threading as th
import re


class User:
    def __init__(self, conn, name):
        self.conn = conn
        self.name = name

    def get_name(self):
        return self.name

    def get_conn(self):
        return self.conn

class Room:
    def __init__(self, name):
        self.name = name
        self.room = []
        self.room_lock = th.Lock()
        self.room_cond = th.Condition(self.room_lock)
    
    def add_user(self, user, name):
        new_user = User(user, name)
        self.room_cond.acquire()
        self.room.append(new_user)
        self.room_cond.release()
    
    def remove_user(self, user):
        self.room_cond.acquire()
        for user_ in self.room:
            if user_.get_conn() == user:
                self.room.remove(user_)
                self.room_cond.release()
                return True
        self.room_cond.release()
        return False
    
    def get_user(self, user):
        self.room_cond.acquire()
        for user_ in self.room:
            if user_.get_conn() == user:
                self.room_cond.release()
                return True
        self.room_cond.release()
        return False
    
    def treat_message(self, message):
        return message.strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('\b', ' ').replace('\f', ' ')

    def is_valid_message(self, message):
        # 1-100 characters, accept spaces, acentuated characters, numbers, special characters, and punctuation
        match = re.match(r'^[\w\sáéíóúñÁÉÍÓÚÑãõÃÕàèìòùÀÈÌÒÙâêîôûÂÊÎÔÛçÇ.,;:!?¿¡()\[\]{}<>\-_+=/*"\'\\|%$#@&~`^]+$', message)
        if match:
            return True
        return False

    def send_message(self, name, msg):
        msg = self.treat_message(msg)
        if self.is_valid_message(msg):
            self.room_cond.acquire()
            for user_ in self.room:
                if user_.get_name() != name:
                    user_.conn.sendall(f"> {name}: {msg}\n".encode("utf-8"))
            self.room_cond.release()
        else:
            self.room_cond.acquire()
            for user_ in self.room:
                if user_.get_name() == name:
                    user_.conn.send(f"Invalid message\n".encode("utf-8"))
            self.room_cond.release()

    def close(self):
        self.room_cond.acquire()
        self.room_cond.notify_all()
        for user_ in room.room:
            user_.conn.close()
        self.room_cond.release()

class Server:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.rooms = {}
        self.rooms_lock = th.Lock()
        self.rooms_cond = th.Condition(self.rooms_lock)

        print(f"Trying to bind to port {port}...")
        self.socket.bind(('', port))
        self.socket.listen()
        print(f"Success! Listening on port {port}...")
        
        self.threads = []
        self.threads_lock = th.Lock()
        self.threads_cond = th.Condition(self.threads_lock)
        self.threads_cond.acquire()
        self.threads.append(th.Thread(target=self.accept_new_conns))
        self.threads[-1].start()
        self.threads_cond.release()


    def accept_new_conns(self):
        while True:
            conn, _ = self.socket.accept()
            if conn:
                self.threads_cond.acquire()
                self.threads.append(th.Thread(target=self.handle_connection,
                                              args=(conn, self.rooms['default'])))
                self.threads[-1].start()
                self.threads_cond.release()

    def add_room(self, room):
        self.rooms_cond.acquire()
        self.rooms[room.name] = room
        self.rooms_cond.release()

    def remove_room(self, room):
        del self.rooms[room.name]

    def close(self):
        self.rooms_cond.acquire()
        for room in self.rooms.values():
            room.close()
        self.rooms_cond.release()

        self.threads_cond.acquire()
        for thread in self.threads:
            thread.do_run = False
        self.threads_cond.release()
        self.socket.close()
        print("Server shutdown.")

    def handle_connection(self, user_conn, room: Room):
        user_name = user_conn.recv(1024).decode('utf-8')
        user_name = user_name.strip().rstrip('\n')
        print(f"{user_name} has connected.")
        room.add_user(user_conn, user_name)
        room.send_message('Server', f"Welcome to the chat, {user_name}!")
        while True:
            data = user_conn.recv(1024)
            if not data:
                break
            room.send_message(user_name, data.decode('utf-8'))
        room.remove_user(user_conn)
        room.send_message('Server', f"{user_name} has disconnected.")
        user_conn.close()
    
    def broadcast(self, room: Room, msg: str):
        room.send_message('Server', msg)
 

if __name__ == '__main__':
    ports = [8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089]
    room = Room('default')
    for port in ports:
        try: 
            server = Server(port)
            server.add_room(room)
        except Exception as e:
            print(f"ERROR: Failed to bind to port {port}.")
            print(e)
            continue
