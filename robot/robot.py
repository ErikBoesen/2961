import magicbot
import wpilib
import wpilib.drive
from wpilib.buttons import JoystickButton


class Robot(magicbot.MagicRobot):
    # TODO bad
    extended = False
    request_extended = False
    def createObjects(self):
        # For teleop auto
        self.robot = self

        self.controller = wpilib.XboxController(0)
        self.lf_motor = wpilib.Talon(2)
        self.lr_motor = wpilib.Talon(1)
        self.rf_motor = wpilib.Talon(4)
        self.rr_motor = wpilib.Talon(3)

        self.train = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                    wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

        self.hatch_solenoid = wpilib.DoubleSolenoid(1, 2)
        self.btn_hatch = JoystickButton(self.controller, 5)  # left bumper button

        wpilib.CameraServer.launch('camera/camera.py:main')
        wpilib.LiveWindow.disableAllTelemetry()

    def autonomous(self):
        """
        Prepare for and start autonomous mode.
        """
        # Call autonomous
        super().autonomous()

    def teleopPeriodic(self):
        self.train.tankDrive(self.controller.getY(hand=wpilib.interfaces.GenericHID.Hand.kLeft),
                             self.controller.getY(hand=wpilib.interfaces.GenericHID.Hand.kRight))

        self.extended = self.btn_hatch.get()

        if self.request_extended != self.extended:
            self.extended = self.request_extended
            self.hatch_solenoid.set(wpilib.DoubleSolenoid.Value.kForward if self.extended else wpilib.DoubleSolenoid.Value.kReverse)


if __name__ == '__main__':
    wpilib.run(Robot)
