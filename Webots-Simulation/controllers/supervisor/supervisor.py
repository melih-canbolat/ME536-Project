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
        previous_message = ''
        print(self.translation)

        # Main loop.
        while True:
            # Deal with the pressed keyboard key.
            k = self.keyboard.getKey()
            message = ''

            if k == 314:  # Left
                print("left")
                self.translation[0] -= 0.01
                self.translationField.setSFVec3f(self.translation)
                
            elif k == 315:  # Up
                print("up")
                self.translation[2] -= 0.01
                self.translationField.setSFVec3f(self.translation)

            elif k == 316:  # Right
                print("Right")
                self.translation[0] += 0.01
                self.translationField.setSFVec3f(self.translation)

            elif k == 317:  # Down
                print("down")
                self.translation[2] += 0.01
                self.translationField.setSFVec3f(self.translation)

            elif k == ord('A'):
                message = 'avoid obstacles'
            elif k == ord('P'):  # Get translation information of the robot
                translationValues = self.translationField.getSFVec3f()
                print(translationValues)
            elif k == ord('R'):  # Teleport the robot to "self.translation"
                self.translationField.setSFVec3f(self.translation)

            # Send a new message through the emitter device.
            if message != '' and message != previous_message:
                previous_message = message
                self.emitter.send(message.encode('utf-8'))

            # Perform a simulation step, quit the loop when
            # Webots is about to quit.
            if self.step(self.timeStep) == -1:
                break


controller = Driver()
controller.run()