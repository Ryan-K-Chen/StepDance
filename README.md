# StepDance
## Inspiration
What might a piano look like in the year 2050? For Step Dance, we looked towards the future to see what changes we might make to a 350 year-old instrument in the digital age. Piano wires became stepper motors, ivory keys became 3d printed ABS, and with the use of computer vision, we gave the piano the one feature it was always missing: vibrato!

## What it does
Step Dance has three main features:
- **MIDI mode**: Upload a MIDI file and watch in amazement as our array of 10 stepper motors reproduce those tones magically!
- **Free-play mode**: Step Dance can be used like a regular piano, but with some extra features! Tilt your head to the side and you can sustain chords. Pinch your thumb and index fingers and wiggle them in the air for some impressive vibrato. Our computer vision script will dynamically analyze your pose and hand gestures in the background!
- **Learning mode**: Press the keys as they light up to play any song you want! Even an absolute beginner can learn to play simple songs with Step Dance's intuitive teaching system.

## How we built it
### The Hardware
Our custom designed 3d printed keys cleverly hide sophisticated circuitry all in the familiar form factor of a standard piano key. Hiding underneath each key is a button that signals the microcontroller to drive a stepper motor with a specific frequency. The laptop webcam similarly passes a series of values to the microcontroller to add vibrato and chord sustaining features.
### The Software
To parse the MIDI files, we used pretty-midi to translate each note and actuation time to frequencies and microseconds. This can directly be fed to the microcontroller, which will run a scheduling algorithm to assign notes to any available stepper motors.
For the gesture tracking, we used OpenCV to build a real-time skeleton of your hand and facial structure. Whenever certain gestures are detected, we convert these gestures to floating point values and send them to the microcontroller as a multiplier to adjust shift or sustain a chord.

## Challenges we ran into
We planned to use a bit counter to demux four signals for our stepper motor, but the clock signal from the Arduino was not stable enough to reliably clock the counter. After a couple hours of debugging, we decided it would not work and had to drive the motor manually. An hour after we gave up, we tried one last-ditch effort with a different approach that actually used less resources than our original proposition. And voila! It worked, drastically reducing the space on our circuit and the number of pins we need to output from the microcontroller.

_Also,_
#### Stack overflow was down for a couple hours!!!

## Accomplishments that we're proud of
Everyone in the team had a specialized skill that we all combined in equal parts to make Step Dance happen. Ryan was our electronics lead responsible for planning and wiring. Akash created all the embedded code running on our microprocessor and designed the communication protocol to interface between our python outputs. Andrew was our hardware specialist that CADed all our parts. And Jinwoo worked on our python scripts to perform the computer vision analysis. Everyone contributed to the success of the project, and we could not have been happier with how it all turned out.

## What we learned
OpenCV and pretty-midi were two python libraries that everyone in our group had very little experience working with, but thanks to extensive documentation and helpful tutorials, a lot of the python code was a fun experience.
We also learned a little about music technology in general with how MIDI files work and some general theory about acoustics on how to make sounds _sound_ good.

## What's next for Step Dance
We can always go bigger! Due to time and cost limitations, we only have 10 stepper motors and 24 keys we can use, but our dream would be to upgrade Step Dance to a full 88 key piano.
