import threading 
import paho.mqtt.client as mqtt 

class sub(threading.Thread):

	def __init__(self,client,stopThread):
		threading.Thread.__init__(self)
		self.client = client
		self.stopThread = stopThread

	def run(self):
		while not self.stopThread.isSet():
			#self.client.loop_forever()
			self.client.loop()
			self.stopThread.wait(0.001)

	def join(self,timeout = None):
		print "\n\t\tKilling thread Sub!!"
		self.stopThread.set()
		threading.Thread.join(self,timeout)
		print "\n\tKilled Thread Sub"

def sub_on_connect(client,userdata,rc):
	print "\nSub connected to broker. rc=%d\n\n" %(rc)
	client.subscribe("wa/thread2/publish")

def sub_on_message(client,userdata,msg):
	print "\t%s" %(msg.payload)


def subfn():
	client=mqtt.Client()
	client.on_connect=sub_on_connect
	client.on_message=sub_on_message
	client.connect("192.168.1.22", 1883,60)
	
	sub_thread=sub(client,stopThread)
	threadPool.append(sub_thread)
	
	sub_thread.start()


class pub(threading.Thread):
	
	def __init__(self,client,stopThread):
		threading.Thread.__init__(self)
		self.client = client
		self.stopThread = stopThread

	def run(self):
		while not self.stopThread.isSet():
			self.client.loop()
			msg=raw_input()
			self.client.publish("wa/thread1/publish",msg,1)
			self.stopThread.wait(0.001)

	def join(self,timeout = None):
		print "\n\t\tKilling thread Pub!!"
		self.stopThread.set()
		threading.Thread.join(self,timeout)
		print "\n\tKilled Pub"
		
		
	
def pub_on_connect(client,userdata,rc):
	print "\nPub Connected to broker..rc=%d\n\n" %(rc)
	

def pub_on_disconnect(client,userdata,rc):
	print "Disconnected..rc=%d" %(rc)
	client.reconnect()

def pubfn():
	client=mqtt.Client()
	client.on_connect= pub_on_connect
	client.on_disconnect= pub_on_disconnect
	client.connect("192.168.1.22", 1883,60)


	pub_thread=pub(client,stopThread)
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
		for each_thread in threadPool:
			each_thread.join()
		print "\n\tKilling all Threads !!"









