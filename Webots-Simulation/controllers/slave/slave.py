from controller import Robot, Receiver, Display, Camera
import paho.mqtt.client as mqtt
import numpy as np
import time

""" MQTT - Not Working
broker_address="test.mosquitto.org" # Broker Address
client_name = "ME536_RobotCam"   # Client ID
topic_pub = "ME536_RobotCam_Image"  # Topic to publish to
payload = "test"

client = mqtt.Client(client_name)  #Create a client instance
try:
    client.connect(broker_address)  #Try to connect to the broker
    print("Broker connection is established.")
except:
    print("Cannot connect to the broker")

client.publish(topic_pub, payload)
"""

class Slave (Robot):
    timeStep = 32

    def __init__(self):
        super(Slave, self).__init__()
        self.receiver = self.getDevice('receiver')
        self.receiver.enable(self.timeStep)
        self.display = self.getDevice('display')
        self.camera = self.getDevice('camera')
        self.camera.enable(1 * self.timeStep)

    def retrieveImage(self, grayscale=False):  # Capture an image and return it as numpy array
        image = self.camera.getImageArray()  # Get image from the camera as a nested list
        if image is None: return None  # Camera may return None at the beginning
        img = np.array(image)  # Convert to a numpy array
        if grayscale:
            img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])  # Convert image to grayscale
        return img
    
    def displayImage(self, img):  # Display grayscale image on 3D View
        if img is None: return  # Don't proceed if the image is empty
        if (img.ndim) == 2:  # If the image is grayscale
            img = np.stack((img,)*3, axis=-1)  # Add missing channels
        ir = self.display.imageNew(img.tolist(), Display.RGB, 200, 200)
        self.display.imagePaste(ir, 0, 0)
        self.display.imageDelete(ir)
        
    def run(self):
        count = 0
        while True:
            if self.receiver.getQueueLength() > 0:  # Read the supervisor order.
                message = self.receiver.getData().decode('utf-8')
                self.receiver.nextPacket()
                if message == "capture":
                    print("Image is saved: img"+str(count)+".jpg")
                    self.camera.saveImage("captures/img"+str(count)+".jpg",95)
                    count += 1
            image = self.retrieveImage(grayscale=False)
            # self.displayImage(image)
            
            
            # Send "image" appropriate medium to process.


        
            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            if self.step(self.timeStep) == -1:
                break


controller = Slave()
controller.run()
