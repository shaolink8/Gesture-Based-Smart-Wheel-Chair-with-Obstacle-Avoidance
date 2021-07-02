# Gesture Based Smart Wheel Chair with Obstacle Avoidance

This is a Smart Assistant system for people suffering from Cerebral Palsy.

### For a detailed description of the project, you can refer to the "Smart Assistance System for people with Cerebral Palsy.pptx" file.

Here, you'll find two Javascript files, "Actuator.js" and "Gesture.js". 

## GESTURE RECOGNITION

In the "Gesture.js" file, we're taking the input from the user in the form of a gesture.

This is achieved thanks to the grove shield that includes the gesture sensor.
This grove shield is attached to our Microbit microcontroller.

This first Microbit, connected to the grove shield, works on the "Gesture.js" code.

As you can see in the code, for each gesture, right, left, up and down, there's a set of code that corresponds to the input.

For example, on the hexadecimal display of the Microbit, the letter "R" will be displayed if the gesture is right.
The variable x will be assigned as 2 and x will be sent over the radio channel to the second Microbit, the receiving Microbit which runs on the "Actuator.js" code.

This radio connection is made possible thanks to the line "radio.setGroup(8)".

## ACTUATORS

This receiving, second Microbit works on the "Actuator.js" code.

In the "Actuator.js" file, we're taking the input as x from the first Microbit, the transmitting Microbit which runs on the "Gesture.js" code.
The value of x corresponds to a movement. For example, x being 2 implies a right movement. So P1 has been assigned as 1 ( HIGH ) while the rest of the pins are still 0 ( LOW ).

P1 signifies forward movement of right wheel.

P11 signifies forward movement of left wheel.

P1 P11 signifies forward movement on both the wheels.

P13 P14 signifies reverse movement.

If 0, then the movement is restricted for a given pin.

So this is done to make the chair turn right based on the input received from the first Microbit which took the gesture as an input.

Similarly, for each input gesture, its corresponding x value is produced and transferred over the channel so that the receiving Microbit can accordingly power the required pins to run the motors.
In case of a down gesture, no pins are powered, hence, all pins have been set to LOW and the wheelchair stops.

## OBSTACLE AVOIDANCE

In the "Gesture.js" code, we have specified a distance threshold for the 3 ultrasonic sensors installed on the left, front and right of the wheelchair.
This is done to detect obstacle and prevent collision automatically. In case any threshold is breached, the same function as a "down" gesture which suggests the wheelchair to stop, is repeated and x is assigned as 3 and sent over the radio channel.
For our case, we used a small prototype. Hence the distance was made as short as 5 cms. This can be changed as per the prototype.

Different hexadecimal displays have been used to represent different gestures and movements.

The "microbit-Actuator.hex" and "microbit-Final-Gesture.hex" files are the compiled version of the code and can be directly uploaded to the Microbit.

## VOICE MEMO

The "memo through voice recognition.py" file is used to save voice memos for the patient to overcome the rare symptom of memory loss and store any crucial information in the form of a voice memo.

## VITALS MONITORING

The "Heartbeat Sensor with IoT Hub.py" file is used to monitor the patient's heartbeat, and send the values on IoT Hub at the same time. These values can be checked up on time to time by any assigned person.



