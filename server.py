import socket
import threading as th

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

    def send_message(self, name, msg):
        self.room_cond.acquire()
        for user_ in self.room:
            if user_.get_name() != name:
                user_.conn.sendall(f"> {name}: {msg}".encode("utf-8"))
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
        print(f"Trying to bind to port {port}...")
        self.socket.bind(('', port))
        self.socket.listen()
        print(f"Success! Listening on port {port}...")


        th.Thread(target=self.accept_new_conn).start()

    def accept_new_conn(self):
        while True:
            conn, _ = self.socket.accept()
            handle = th.Thread(target=self.handle_connection, args=(conn, room))
            handle.start()


    def add_room(self, room):
        self.rooms[room.name] = room

    def remove_room(self, room):
        del self.rooms[room.name]

    def close(self):
        for room in self.rooms.values():
            room.close()
        self.socket.close()
        print("Server shutdown.")

    def handle_connection(self, user_conn, room: Room):
        user_name = user_conn.recv(1024).decode('utf-8')
        print(user_name)
        room.add_user(user_conn, user_name)
        room.send_message('Server', f"Welcome to the chat, {user_name}!")
        while True:
            data = user_conn.recv(1024)
            if not data:
                break
            room.send_message(user_name, data.decode('utf-8'))
        room.remove_user(user_conn)
        user_conn.close()
    
    def broadcast(self, room: Room, msg: str):
        room.send_message('Server', msg)
 

if __name__ == '__main__':
    try: 
        room = Room("Main") # Default room for everyone

        roll = Server(4002)
        roll.add_room(room)

        ricked = Server(8922)
        ricked.add_room(room)

    except KeyboardInterrupt:
        exit()  
