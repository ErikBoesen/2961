import magicbot
import wpilib
import wpilib.drive
from wpilib.buttons import JoystickButton
import time
import sys


class Robot(magicbot.MagicRobot):
    def createObjects(self):
        # For teleop autonomous, we have to do this so that the autonomous can call teleopPeriodic.
        self.robot = self

        # Create an object for the Xbox controller. You can now use self.controller elsewhere to get
        # data from the controller like buttons, axes, etc. just as you would imagine.
        self.controller = wpilib.XboxController(0)

        # Create objects for each Talon motor controller. You must pass in the number of the
        # PWM port being used so that the code knows which Talon you want.
        self.lf_motor = wpilib.Talon(1)
        self.lr_motor = wpilib.Talon(0)
        self.rf_motor = wpilib.Talon(3)
        self.rr_motor = wpilib.Talon(2)

        # Create a drivetrain object. What this line is essentially doing is making a grouping of
        # all the motors on the left, one for all the motors on the right, and then passing both
        # of them in to wpilib.drive.DifferentialDrive, which handles all the calculations for driving
        # using tank drive so you don't have to do tons of unnecessary math yourself.
        self.drivetrain = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                         wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

        # Create object for the solenoid you're using to extend out the hatch grabber, and another
        # for the solenoid you're using to actually grab the hatch.
        self.extend_solenoid = wpilib.DoubleSolenoid(0, 1)
        self.grab_solenoid = wpilib.DoubleSolenoid(2, 3)

        # Create two objects for the buttons you're using to control extending and grabbing.
        # You can technically use functions like self.controller.getAButton() to check whether
        # a certain button is pressed, but I prefer this method because then you can name your
        # buttons and it is a little bit clearer what button is what.
        self.button_extend = JoystickButton(self.controller, 5)  # left bumper button
        self.button_grab = JoystickButton(self.controller, 1)  # A
        # If you need to check what button is what on your controller, reference this page in the RobotPy
        # documentation: https://robotpy.readthedocs.io/projects/wpilib/en/latest/wpilib/XboxController.html

        # Start sending your camera feed to the driverstation
        # This basically runs the file you give it with the function you specify.
        wpilib.CameraServer.launch('camera/camera.py:main')

    def robotInit(self):
        """
        This method runs when the robot starts running.
        """
        self.extended = self.extend_solenoid.get()
        self.grab = self.grab_solenoid.get()
        self.request_extended = self.extended
        self.request_grab = self.grab

    def autonomous(self):
        """
        Prepare for and start autonomous mode. Executed when auto starts.
        """
        # Call autonomous; use the autonomous modes listed in robot/autonomous/. This will either be
        # whatever mode you have chosen or the one for which you set DEFAULT = True.
        super().autonomous()

    def teleopPeriodic(self):
        """
        This method executes every 20 milliseconds during teleoperated mode. This is where you will
        want to take input from your controller/buttons and use that information to actually do things
        on your robot.
        """
        # Run the drivetrain with tank drive. This basically gets the Y of the two toggles (using some
        # weird constants from wpilib) and then inverts them so that the robot doesn't go backward.
        self.drivetrain.tankDrive(-self.controller.getY(hand=wpilib.interfaces.GenericHID.Hand.kLeft),
                                  -self.controller.getY(hand=wpilib.interfaces.GenericHID.Hand.kRight))

        # Get values from buttons for whether we WANT to extend the pistons this time around.
        # Use constants for whether solenoids are extended. You could technically just use 1 and 3,
        # but this is just a bit more clear what you're doing.
        self.request_extended = wpilib.DoubleSolenoid.Value.kForward if self.button_extend.get() else wpilib.DoubleSolenoid.Value.kReverse
        self.request_grab = wpilib.DoubleSolenoid.Value.kForward if self.button_grab.get() else wpilib.DoubleSolenoid.Value.kReverse

        # If we want to change whether the pistons are in or out, do that.
        # Otherwise don't do anything.
        # In theory you could just set the position of the piston using the button value every single time.
        # But then it would send the signal every time, even when it's not needed. This causes a lot of slowness,
        # and it was making our drivetrain jam up because it was taking so much time for the loop to run.
        if self.request_extended != self.extended:
            self.extended = self.request_extended
            self.extend_solenoid.set(self.extended)

        # Just the same thing, but for the grabbing pistons this time.
        if self.request_grab != self.grab:
            self.grab = self.request_grab
            self.grab_solenoid.set(self.grab)


# Just make the robot run when the file is run
if __name__ == '__main__':
    wpilib.run(Robot)
