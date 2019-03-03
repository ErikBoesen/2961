import magicbot
import wpilib
import wpilib.drive
from wpilib.buttons import JoystickButton
import time
import sys


class Robot(magicbot.MagicRobot):
    # TODO bad
    extended = False
    request_extended = False
    grab = False
    request_grab = False
    def createObjects(self):
        # For teleop auto
        self.robot = self

        self.controller = wpilib.XboxController(0)
        self.lf_motor = wpilib.Talon(1)
        self.lr_motor = wpilib.Talon(0)
        self.rf_motor = wpilib.Talon(3)
        self.rr_motor = wpilib.Talon(2)

        self.train = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                    wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

        self.extend_solenoid = wpilib.DoubleSolenoid(0, 1)
        self.grab_solenoid = wpilib.DoubleSolenoid(2, 3)

        self.button_hatch = JoystickButton(self.controller, 5)  # left bumper button
        self.button_grab = JoystickButton(self.controller, 1)  # A

        wpilib.CameraServer.launch('camera/camera.py:main')
        wpilib.LiveWindow.disableAllTelemetry()

    def autonomous(self):
        """
        Prepare for and start autonomous mode.
        """
        # Call autonomous
        super().autonomous()

    def teleopPeriodic(self):
        self.train.tankDrive(-self.controller.getY(hand=wpilib.interfaces.GenericHID.Hand.kLeft),
                             -self.controller.getY(hand=wpilib.interfaces.GenericHID.Hand.kRight))

        self.extended = self.button_hatch.get()
        self.grab = self.button_grab.get()

        if self.request_extended != self.extended:
            self.extended = self.request_extended
            self.extend_solenoid.set(wpilib.DoubleSolenoid.Value.kForward if self.extended else wpilib.DoubleSolenoid.Value.kReverse)

        if self.request_grab != self.grab:
            self.grab = self.request_grab
            self.grab_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse if self.grab else wpilib.DoubleSolenoid.Value.kReverse)


if __name__ == '__main__':
    wpilib.run(Robot)
