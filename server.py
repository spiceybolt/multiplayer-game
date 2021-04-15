import socket
import threading
import pickle
import json

playerdata = []
playerdatalock = threading.Lock()


count = 0
countlock = threading.Lock()

colours = ['r','g','b']
colourlock = threading.Lock()

def playerthread(client, addr, name:str):
	global count

	countlock.acquire()
	colourlock.acquire()
	# assigning colours to dudes in the order they joined(needs work later)
	client.send(colours[count - 1].encode())

	countlock.release()
	colourlock.release()
	
	while True:
		msg = client.recv(1024)
		if msg == b'':
			break
		pickleobj = pickle.loads(msg)

		countlock.acquire()
		playerdatalock.acquire()
		if not pickleobj[-1] in [j[-1] for j in playerdata]:
			playerdata.append(pickleobj)
		else:
			playerdata[playerdata.index(next(i for i in playerdata if pickleobj[-1] in i))] = pickle.loads(msg)
		print(playerdata)
		playerdatalock.release()
		countlock.release()
		
		# client.send(b'got')
	print("closed client")
	
	countlock.acquire()
	count -= 1
	countlock.release()


with open('config.json','r') as f:
	data = json.load(f)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = data['port']

server.bind((socket.gethostname(), port))
print(server.getsockname())

server.listen(5)

while True:
	client, addr = server.accept()
	count += 1
	print(client)
	threading.Thread(target=playerthread, args=(client, addr, f'player {count}',)).start()

