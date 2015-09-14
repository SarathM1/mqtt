import threading
import paho.mqtt.client as mqtt

class sub(threading.Thread):
	def __init__(self,client):
		threading.Thread.__init__(self)
		self.client = client
	
	def run(self):
		self.client.loop_forever()

def sub_on_connect(client,userdata,rc):
	print "\nSub Connected to broker. rc=%d\n\n" %(rc)
	client.subscribe("wa/thread1/publish")

def sub_on_message(client,userdata,msg):
	print "\t%s" %(msg.payload)

def subfn():
	client=mqtt.Client()
	client.on_connect=sub_on_connect
	client.on_message=sub_on_message
	client.connect("192.168.1.22",1883,60)

	sub_thread=sub(client)
	sub_thread.start()






class pub(threading.Thread):
	def __init__(self,client):
		threading.Thread.__init__(self)
		self.client = client

	def run(self):
		while True:
			self.client.loop()
			msg=raw_input()
			self.client.publish("wa/thread2/publish",msg, 1)

def pub_on_connect(client,userdata,rc):
	print "\nPub Connected to broker. rc=%d\n\n" %(rc)


def pub_on_disconnect(client,userdata,rc):
	print "Disconnected..rc=%d" %(rc)
	client.reconnect()

def pubfn():
	client=mqtt.Client()
	client.on_connect=pub_on_connect
	client.on_disconnect=pub_on_disconnect
	client.connect("192.168.1.22",1883,60)
	pub_thread=pub(client)
	pub_thread.start()


def main():
	subfn()
	pubfn()




if __name__ == '__main__':
	main()
