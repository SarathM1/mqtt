import threading
import paho.mqtt.client as mqtt

class sub(threading.Thread):
	def __init__(self,client):
		threading.Thread.__init__(self)
		self.client = client
	
	def run(self):
		self.client.loop_forever()

def sub_on_connect(client,userdata,rc):
	print "Sub Connected to broker. rc=%s" %(str(rc))
	client.subscribe("wa/thread1/publish")

def sub_on_message(client,userdata,msg):
	print "Topic: %s, Message: %s" %(msg.topic,msg.payload)

def subfn():
	client=mqtt.Client()
	client.on_connect=sub_on_connect
	client.on_message=sub_on_message
	client.connect("test.mosquitto.org",1883,60)

	sub_thread=sub(client)
	sub_thread.start()






class pub(threading.Thread):
	def __init__(self,client):
		threading.Thread.__init__(self)
		self.client = client

	def run(self):
		while True:
			self.client.loop()
			msg=raw_input("Data: ")
			self.client.publish("wa/thread2/publish",msg, 1)

def pub_on_connect(client,userdata,rc):
	print "Pub Connected to broker. rc=%s" %(str(rc))


def pub_on_disconnect(client,userdata,rc):
	print "Disconnected..rc=%s" %(str(rc))
	client.reconnect()

def pubfn():
	client=mqtt.Client()
	client.on_connect=pub_on_connect
	client.on_disconnect=pub_on_disconnect
	client.connect("test.mosquitto.org",1883,60)
	pub_thread=pub(client)
	pub_thread.start()


def main():
	subfn()
	pubfn()




if __name__ == '__main__':
	main()