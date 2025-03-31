# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       alebritt                                                     #
# 	Created:      2/4/2025, 1:59:40 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

import vex
from vex import *

# Competition Object (Handles Autonomous & Driver Control)
# competition = vex.Competition()

# Initialize the devices that will be used
brain = Brain()
brain.screen.clear_screen()
brain.screen.print("Program Started")
vex.wait(1000, vex.TimeUnits.MSEC)

controller = Controller()

# Initialize the movement motors, since the motors get flipped when put on either side of
# the frame, we need to set some of the motors to be reversed.

# ========================= MOTOR SETUP FOR BIG ROBOT =================================
left_front_motor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
left_rear_motor = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
right_front_motor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
right_rear_motor = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)

belt_motor = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)

roller_motor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)

lever_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)

# ========================== FUNCTIONS FOR AUTONOMOUS ===================================


def autonomous():
    # Move forward 1000mm (1 meter)
    left_front_motor.spin_for(DirectionType.FORWARD, 1000, DistanceUnits.MM)
    left_rear_motor.spin_for(DirectionType.FORWARD, 1000, DistanceUnits.MM)
    right_front_motor.spin_for(DirectionType.FORWARD, 1000, DistanceUnits.MM)
    right_rear_motor.spin_for(DirectionType.FORWARD, 1000, DistanceUnits.MM)

    # Interrupt if the DOWNN button is pressed
    if controller.buttonDown.pressing():
        brain.screen.print("Autonomous Stopped")
        return

    # Turn 180 degrees (by running motors in opposite directions)
    left_front_motor.spin_for(DirectionType.REVERSE, 500, RotationUnits.DEGREES)
    left_rear_motor.spin_for(DirectionType.REVERSE, 500, RotationUnits.DEGREES)
    right_front_motor.spin_for(DirectionType.FORWARD, 500, RotationUnits.DEGREES)
    right_rear_motor.spin_for(DirectionType.FORWARD, 500, RotationUnits.DEGREES)

    # Interrupt if the DOWNN button is pressed
    if controller.buttonDown.pressing():
        brain.screen.print("Autonomous Stopped")
        return

    # Raise lever arm
    lever_motor.spin_for(-40, RotationUnits.DEG, True)

    # Interrupt if the DOWNN button is pressed
    if controller.buttonDown.pressing():
        brain.screen.print("Autonomous Stopped")
        return

    # Reverse 500mm
    left_front_motor.spin_for(DirectionType.REVERSE, 500, DistanceUnits.MM)
    left_rear_motor.spin_for(DirectionType.REVERSE, 500, DistanceUnits.MM)
    right_front_motor.spin_for(DirectionType.REVERSE, 500, DistanceUnits.MM)
    right_rear_motor.spin_for(DirectionType.REVERSE, 500, DistanceUnits.MM)

    # Interrupt if the DOWNN button is pressed
    if controller.buttonDown.pressing():
        brain.screen.print("Autonomous Stopped")
        return

    # Lower lever arm
    lever_motor.spin_for(40, RotationUnits.DEG, True)

    # Interrupt if the DOWNN button is pressed
    if controller.buttonDown.pressing():
        brain.screen.print("Autonomous Stopped")
        return

    # Drive forward 1000mm (1 meter) again
    left_front_motor.spin_for(DirectionType.FORWARD, 1000, DistanceUnits.MM)
    left_rear_motor.spin_for(DirectionType.FORWARD, 1000, DistanceUnits.MM)
    right_front_motor.spin_for(DirectionType.FORWARD, 1000, DistanceUnits.MM)
    right_rear_motor.spin_for(DirectionType.FORWARD, 1000, DistanceUnits.MM)

    # Interrupt if the DOWNN button is pressed
    if controller.buttonDown.pressing():
        brain.screen.print("Autonomous Stopped")
        return


# =========================== FUNCTIONS FOR DRIVER CONTROL ===========================
def scale_input(value):
    if abs(value) < 20:  # First 25% of the joystick range
        return value * 0.5  # Reduce the speed to 50%
    return value


# ===================== MAIN PROGRAM LOOP FOR DRIVER CONTROL ============================
# Driver Control Function
def driver_control():
    """
    Main driver control loop that allows for commands from the controller to be sent to the motors
    """
    # Print to Brain screen to indicate that driver control is active
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Driver Control Active")
    vex.wait(3000, vex.TimeUnits.MSEC)

    # Default belt motor speed
    belt_speed = 75

    # Roller toggle state
    roller_running = False
    roller_speed = 60
    roller_motor.set_velocity(roller_speed, vex.VelocityUnits.PERCENT)

    # Lever toggle state --- 0=up, 1=down
    lever_position = 1
    lever_speed = 80
    lever_motor.set_velocity(lever_speed, vex.VelocityUnits.PERCENT)
    
    while True:
        # Get input values for the motors from the controller joysticks
        left_speed = scale_input(controller.axis3.position()) * .8
        right_speed = scale_input(controller.axis2.position()) * .8

        # Print values to Brain screen for debugging
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("L:", left_speed, " R:", right_speed)

        # Left side motors
        left_rear_motor.set_velocity(left_speed, vex.VelocityUnits.PERCENT)
        left_front_motor.set_velocity(left_speed, vex.VelocityUnits.PERCENT)

        # Right side motors
        right_rear_motor.set_velocity(right_speed, vex.VelocityUnits.PERCENT)
        right_front_motor.set_velocity(right_speed, vex.VelocityUnits.PERCENT)

        # Tell the motors to spin after setting the velocity
        left_front_motor.spin(vex.DirectionType.FORWARD)
        left_rear_motor.spin(vex.DirectionType.FORWARD)
        right_front_motor.spin(vex.DirectionType.FORWARD)
        right_rear_motor.spin(vex.DirectionType.FORWARD)

        # Belt control using the left bumper buttons for forward and reverse
        if controller.buttonL1.pressing():
            belt_motor.spin(vex.DirectionType.FORWARD, belt_speed, vex.VelocityUnits.PERCENT)
        elif controller.buttonL2.pressing():
            belt_motor.spin(vex.DirectionType.REVERSE, belt_speed, vex.VelocityUnits.PERCENT)
        else:
            belt_motor.stop()

        # Roller control toggling using the A button
        if controller.buttonA.pressing():
            if not roller_running:
                roller_motor.spin(vex.DirectionType.FORWARD, roller_speed, vex.VelocityUnits.PERCENT)
                roller_running = True
            else:
                roller_motor.stop()
                roller_running = False
            vex.wait(300, vex.TimeUnits.MSEC)

        # Lever control using the right bumper buttons
        if controller.buttonR1.pressing() and lever_position == 0:
            lever_motor.spin_for(40, vex.RotationUnits.DEG, True)
            lever_position = 1
            vex.wait(300, vex.TimeUnits.MSEC)

        if controller.buttonR2.pressing() and lever_position == 1:
            lever_motor.spin_for(-40, vex.RotationUnits.DEG, True)
            lever_position = 0
            vex.wait(300, vex.TimeUnits.MSEC)

        # Allow the program to continuously update motor speeds
        vex.wait(20, vex.TimeUnits.MSEC)
        

# ======================================= MAIN PROGRAM ======================================
# Run the autonomous program
# autonomous()

# Run the driver control program
driver_control()