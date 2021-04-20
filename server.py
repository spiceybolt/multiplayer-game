import socket
import threading
import pickle
import json

playerdata = []
playerdata_lock = threading.Lock()

#modify lock logic pls

count = 0
count_lock = threading.Lock()

colours = ['r','g','b']
colours_lock = threading.Lock()

def player_thread(client, addr, name:str):
	global count

	count_lock.acquire()
	colours_lock.acquire()
	playerdata_lock.acquire()
	# assigning colours to dudes in the order they joined(needs work later)
	print(f"{threading.active_count()} is number of threads active rn")
	#assigning unassigned colour to new client
	for i in colours:
		if i not in [j[-1] for j in playerdata]:
			client.send(i.encode())
			thiscolour = i
			print(i)
			break
	count_lock.release()
	playerdata_lock.release()
	colours_lock.release()
	

	#client loop
	while True:
		#getting message from client
		msg = client.recv(1024)

		#quit if msg == b'' its the quit message
		if msg == b'':
			break

		#if it isnt a " b'' " then it must be a pickle obj. pickle-it
		pickle_obj = pickle.loads(msg)

		count_lock.acquire()
		playerdata_lock.acquire()

		#if this is the first time this loop is running, then there is no 
		#data of this colour in the playerdata 
		#so if the colour aint in playerdata append this obj(tuple)
		#to our playerdata list
		if not pickle_obj[-1] in [j[-1] for j in playerdata]:
			playerdata.append(pickle_obj)
		#else playerdata[function to get index of the data we need to update] = obj
		# a try to catch an error ive been getting to find the cause
		else:
			try:
				playerdata[playerdata.index(next(i for i in playerdata if pickle_obj[-1] in i))] = pickle_obj
			except StopIteration:
				print(playerdata)
		#sending board info to client
		client.send(pickle.dumps(playerdata))

		
		playerdata_lock.release()
		count_lock.release()
	
	#closing thread after b''->break was called	
	print("closed client")
	#removing the data of player from playerdata
	playerdata.pop(playerdata.index(next(i for i in playerdata if thiscolour in i)))
	

#opening file and init socket
with open('config.json','r') as f:
	data = json.load(f)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = data['port']

server.bind((socket.gethostname(), port))
print(server.getsockname())

server.listen(5)

#mainloop listens to connections and starts thread(need to remove count)
while True:
	client, addr = server.accept()
	count += 1
	print(f"player {threading.active_count()} has connected")
	threading.Thread(target=player_thread, args=(client, addr, f'player {threading.active_count()}',)).start()
	print(threading.active_count())

