import threading
import paho.mqtt.client as mqtt

class sub(threading.Thread):
	def __init__(self,client):
		threading.Thread.__init__(self)
		self.client = client
		
	
	def run(self):
		while not stopThread.isSet():
			self.client.loop()
			stopThread.wait(0.001)

	def join(self,timeout = None):
		self.client.disconnect()
		threading.Thread.join(self,timeout)
		print "\n\t\tKilled thread sub!!"
		

def sub_on_connect(client,userdata,rc):
	print "\nSub Connected to broker. rc=%d\n\n" %(rc)
	client.subscribe("wa/thread1/publish")

def on_message(client,userdata,msg):
	print "\t%s" %(msg.payload)

def subfn():
	client=mqtt.Client()
	client.on_connect=sub_on_connect
	client.on_message=on_message
	client.on_disconnect = on_disconnect
	client.connect("192.168.1.22",1883,60)

	sub_thread=sub(client)
	threadPool.append(sub_thread)
	sub_thread.start()


class pub(threading.Thread):
	def __init__(self,client):
		threading.Thread.__init__(self)
		self.client = client
		

	def run(self):
		while not stopThread.isSet():
			self.client.loop()
			msg=raw_input()
			self.client.publish("wa/thread2/publish",msg, 1)
			stopThread.wait(0.001)

	def join(self,timeout = None):
		self.client.disconnect()
		print "\n\twaiting for KEYBOARD INPUT"
		threading.Thread.join(self,timeout)
		print "\n\t\tKilled thread thread pub!!"
		

def pub_on_connect(client,userdata,rc):
	print "\nPub Connected to broker. rc=%d\n\n" %(rc)


def on_disconnect(client,userdata,rc):
	print "Disconnected..rc=%d" %(rc)
	if not stopThread.isSet():
		client.reconnect()
		print "Reconnected to broker. ."

def pubfn():
	client=mqtt.Client()
	client.on_connect=pub_on_connect
	client.on_disconnect=on_disconnect
	client.connect("192.168.1.22",1883,60)
	
	pub_thread=pub(client)
	threadPool.append(pub_thread)
	pub_thread.start()


def main():
	subfn()
	pubfn()



threadPool = []
stopThread = threading.Event()
if __name__ == '__main__':
	main()

	try:
		while True:
			pass
	except KeyboardInterrupt as e:
		print e
		stopThread.set()
		for each_thread in threadPool:
			each_thread.join()
		
