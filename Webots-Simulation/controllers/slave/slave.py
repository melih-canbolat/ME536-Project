from controller import Robot


class Slave (Robot):
    timeStep = 32

    def boundSpeed(self, speed):
        return max(-self.maxSpeed, min(self.maxSpeed, speed))

    def __init__(self):
        super(Slave, self).__init__()
        
        self.camera = self.getDevice('camera')
        self.camera.enable(1 * self.timeStep)
        
        self.receiver = self.getDevice('receiver')
        self.receiver.enable(self.timeStep)

    def run(self):
        while True:
            # Read the supervisor order.
            if self.receiver.getQueueLength() > 0:
                message = self.receiver.getData().decode('utf-8')
                self.receiver.nextPacket()
                if message == 'avoid obstacles':
                    pass

            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            if self.step(self.timeStep) == -1:
                break


controller = Slave()
controller.run()
