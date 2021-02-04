from controller import Supervisor


class Driver (Supervisor):
    timeStep = 32

    def __init__(self):
        super(Driver, self).__init__()
        self.emitter = self.getDevice('emitter')
        robot = self.getFromDef('RobotCam')
        self.translationField = robot.getField('translation')
        self.translation = self.translationField.getSFVec3f()
        self.keyboard.enable(Driver.timeStep)
        self.keyboard = self.getKeyboard()

    def run(self):
        print("Simulation has started.")
        print("S: Save the current image")
        print("P: Display the current position")


        # Main loop.
        while True:
            message = ''
            k = self.keyboard.getKey()  # Get the pressed keyboard key.
            #print(k)
            if k == 314:  # Move Left
                self.translation[0] -= 0.01
                self.translationField.setSFVec3f(self.translation)
                
            elif k == 315:  # Move Up
                self.translation[2] -= 0.01
                self.translationField.setSFVec3f(self.translation)

            elif k == 316:  # Move Right
                self.translation[0] += 0.01
                self.translationField.setSFVec3f(self.translation)

            elif k == 317:  # Move Down
                self.translation[2] += 0.01
                self.translationField.setSFVec3f(self.translation)
            elif k == ord('S'): # S - save image
                message = "capture"
            elif k == ord('P'):  # Get translation information of the robot
                translationValues = self.translationField.getSFVec3f()
                print(translationValues)

                
            # Deternmine the new message to be sent
            # Send a new message to the RobotCam through the emitter device.
            if message != "":
                self.emitter.send(message.encode('utf-8'))
                message = ""

            # Perform a simulation step, 
            # quit the loop when Webots is about to quit.
            if self.step(self.timeStep) == -1:
                break


controller = Driver()
controller.run()