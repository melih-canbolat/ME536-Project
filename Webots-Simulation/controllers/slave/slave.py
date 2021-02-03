from controller import Robot, Receiver, Display, Camera
import numpy as np


class Slave (Robot):
    timeStep = 32

    def boundSpeed(self, speed):
        return max(-self.maxSpeed, min(self.maxSpeed, speed))

    def __init__(self):
        super(Slave, self).__init__()
        self.receiver = self.getDevice('receiver')
        self.receiver.enable(self.timeStep)
        self.display = self.getDevice('display')
        self.camera = self.getDevice('camera')
        self.camera.enable(2 * self.timeStep)

    def retrieveImage(self):  # Capture an image and return it as grayscale image
        image = self.camera.getImageArray()  # Get image from the camera as a nested list
        if image is None: return None  # Camera may return None at the beginning
        img = np.array(image)  # Convert to a numpy array
        gimg = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])  # Convert image to grayscale
        return gimg
    
    def displayImage(self, gray):  # Display grayscale image on 3D View
        if gray is None: return  # Don't proceed if the image is empty
        gimg = np.stack((gray,)*3, axis=-1)
        ir = self.display.imageNew(gimg.tolist(), Display.RGB, 200, 200)
        self.display.imagePaste(ir, 0, 0)
        self.display.imageDelete(ir)
        
    def run(self):
        while True:
            if self.receiver.getQueueLength() > 0:  # Read the supervisor order.
                message = self.receiver.getData().decode('utf-8')
                self.receiver.nextPacket()
                if message == 'avoid obstacles':
                    pass
            image = self.retrieveImage()
            #self.displayImage(image)
            
            
            # Send "image" appropriate medium to process.

        
            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            if self.step(self.timeStep) == -1:
                break


controller = Slave()
controller.run()
