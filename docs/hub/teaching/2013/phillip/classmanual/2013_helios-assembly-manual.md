---
title: "Helios Assembly Manual"
year: 2013
drive_path: "Spokes Hub/Teaching/Previous Teaching Material/2013 Spokes/Phillip/ClassManual/Helios Assembly Manual.pdf"
drive_link: "local-zip:Spokes Hub/Teaching/Previous Teaching Material/2013 Spokes/Phillip/ClassManual/Helios Assembly Manual.pdf"
type: pdf
modified: "unknown"
relevance: medium
tags: [curriculum, gear]
summary: "28-page Helios (solar tracker) assembly manual by Phillip Daniel and A. Mitsos: tools, materials, hardware, electronics, software, purchasing links."
---
© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 1 of 28

Helios Assembly Manual

Phillip Daniel
Supervisor: Rockwell International Assistant Professor Alexander Mitsos
 Department of Mechanical Engineering
Massachusetts Institute of Technology

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 2 of 28

Table of Contents:
Table of Contents                                             Pg. 2
Abstract              Pg. 3
Introduction                       Pg. 3
Design                       Pg. 3
Tools                                    Pg. 4
Materials                       Pg. 5-6
Hardware Assembly Directions                Pg. 7-12
Electronics Setup               Pg. 13-14
Software Setup               Pg. 15-17
Purchasing Links                                           Pg. 18-19
Bibliography           Pg. 19
Supporter List           Pg. 20
Templates                Pg. 21-28

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 3 of 28

Introduction
We aim to introduce young students to engineering  and teach them about solar energy; by
having them build a Helios as part of their curriculum. There is an effor t in engineering to push energy
generation away from the use of fossil fuels and towards greener alternatives. One option for green er
energy is to use a device called a heliostat, which uses a mirror to dire ct the sun’s light onto a target
throughout the day. Such a device can be used for many applications , from concentrating solar energy
onto the heat reservoir of a power plant to illuminating areas that are blocked from the sun.
In addition to the  number of uses of this technology, there is also a diverse range of structures
that have been designed to enable solar tracking. The physical structure of Helios’s design, as with other
heliostat designs, functions to mount a mirror onto two controllable axes. The mechanism will track the
sun by using a program  to calculate the star’s location in the sky thought the day, based on the global
position of the Helios. An Arduino micro-controller will be used to run the program and control the two
servo motors.
Design Considerations
To ensure that this project is wi dely dispersed, considerable effort went into designi ng the
Helios to be built with common tools and cheap materials. The first design choice was to build the body
almost entirely out of foam core , which is rigid, affordable, easy to acquire, and easy to c ut. Also, for
maximum strength and rigidity, care was taken to design the body so that all of the foam parts are
either in tension or compression. This  was done to take advantage  of foam core’s stre ngth in tension
and compression, and because the adhesive  that was used  is more effective at supporting a load in
tension than in bending. Additionally, t he shaft that is attached to the mirror is powered through a
timing belt, which allows for a small  alignment error between the motor and the mirror, the  servo
motors are accurate to within 1 degree, and the platform runs on the open source Arduino platform.
These design choices, along with a few other considerations, make th e presented design a durable and
affordable, educational tool.
Our open-source promise
The goal of Helios is to promote engineering education. Because this is our main focus, our work
is licensed under the GNU FDL license. Users have full rights to reproduce and improve on what we have
done, as long as they continue to do so under the same l icense. We hope that users will improve the
design and continue to evolve Helios into a more effective learning tool.

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 4 of 28

Tools
Note: All of these tools can be purchased at local stores or at the links in the reference section. The total
cost of these materials is approximately $80, if they are all purchased online at the given links.

 Drill Bits15
.1258”, .18”, and .5” Diameter
Straight Edge
Large Vice Grips
Power Drill
Screwdriver Set
Box Cutter

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 5 of 28

Foam Core
(20” X 30”, ~.2in thick)

Rod
9.5” Long by 1/2” Diameter
Materials
Note: All of these materials can be purchased at local stores or at the links in the reference section. The
total cost of these materials is approximately $150, if they are all purchased online at the given links.

Timing-Belt 10”
Square Nut
(7/16” -14 Thread Size, 3/8” Thick)
Timing-Belt Pulleys (2), 1” OD
Krazy Glue
Tape
Templates
Vigor VS-2A
Servo
(39.2g/5kg/0.17 sec)
Washers

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 6 of 28

Krazy Glue Gel
8 Machine Screws
 (4-40, 25mm long)
8 Nuts (4-40)

What length
1 ½” Nails
Mirrored Acrylic Sheet (6” X 6”)
Starter Kit for Arduino Uno
 Real Time Clock Module
Wall Adapter Power Supply
(5VDC 1A)

9V battery

3.3 KOhm Resistor (2)

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 7 of 28

Hardware Assembly Directions
(Follow the drying times suggested by your glue’s manufacturer )
Step 1:
Print the templates at the end of this document.
Note: These have to be printed in full scale. Compare the printouts with the PDFs, to ensure that
your printer has not changed the scale.
Step 2:
Secure the templates to the poster board as shown in Figure 1 and, using the center lines as guides, drill
the .18 inch and .5 inch holes.
Note: Drill the .5 inch holes with the .18inch drill bit first for increased accuracy.

Step 3:
With a sharp box cutter, cut out the individual components.
Note: Cut the foam core with multiple passes of the box cutter, this will result in a much cleaner
cut. Don’t try to cut through the whole sheet in one pass.
.18 Inches
.5 Inches
Figure 1: This shows how the templates should be arranged on the poster board.

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 8 of 28

Figure 3: This is how the Helios should be
arranged at the end of step 5.
Step 4:
Glue the matching cutouts together as shown in Figure 2 ,
using the super glue . You should be able to look through
the cutouts and see that all of the holes are al igned, the
base of parts 1 and 2 should be flat , and one template on
part 3 should be facing out.
Note: After applying glue to one surface, join the parts
and press them together for 30 seconds. Then,  allow
the glue to set for five minutes.

Step 5:
Using the superglue gel, glue parts 1, 2 and 3 together as
shown in Figure 3 . Be sure that the parts are arranged so
that the .5” diameter holes are closest to the section of the
base that is  labeled short, also be sure that the template
on the base is facing down/out. Allow the glue to set for
five minutes. After the glue has set, insert  3 nails through
the base and into each of the uprights for added support.

Step 6:
Cut through the top layer of both cross beams and insert them into the Helios as shown in Figure 4.
Apply superglue gel to joints between the cross beams  and the walls of the Helios, and the surface
shared between the two cross beams, as indicated in blue. Allow the glue to set for five minutes.

Figure 2: This is how the parts should look after
they have been glued together.
2
3
1
Figure 4: This shows where to apply the glue to the cross beams and how to insert
them into the walls of the Helios.

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 9 of 28

Step 7:
Place a piece of tape along the cuts, as shown in Figure 5.

Step 8:
Superglue the spacer to the base, by lining it up with the
template as shown in Figure 6, and allow the glue to set for five
minutes.

Step 9:
Center the largest servo horn onto the bottom base and secure
it with the superglue, as shown in Figure 7. Allow the glue to set
for five minutes.

Figure 6: This shows the arrangement of the
spacer on Helios.
Figure 7: This is how the servo horn should be
arranged on the bottom base.
Figure 5: This shows where to place the tape on the cross beams, to keep them from flexing.

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 10 of 28

Step 10:
Bore out one of the timing belt-pulleys to a .5” diameter hole using the .5 inch drill bit, and check that it
fits onto the .5” diameter shaft. It should either press on, or have a gap small enough to fill with super
glue. If the drilled hole is too small, sand down the outer diameter of the shaft by hand.
Step 11:
Carefully bore out two square nuts to .5” diameter holes and check that they fit snuggly onto the shaft.
Note: Clamp the nut to a sacrificial surface, with a pair of vice grips, and progressively increase
the diameter of the hole with multiple bits until a .5” diameter hole is left. Remember to plunge
the drill bit into the nut slowly.
Step 12:
Attach a servo horn to the timing belt pulley as shown here, being careful to center the servo horn’s axis
with the pulley’s, as shown in Figure 8.

Figure 8: This shows the steps for how to attach a servo horn to a Delrin timing belt pulley, since superglue doesn’t
adhere well. First, select a servo horn that is approximately the same size as the pulley. Then, increase the diameter of
the pulley’s central axis to .3” with the drill, to at least .2” deep. Press the extended end of the servo horn into the pulley.
Next, drill through two opposing holes in the servo horn, and drill through the pulley as well, being sure not to drill
through its teeth. Now, turn the servo horn around and line up the two holes that were just drilled. Finally, insert two
1.5” long, 4-40 screws through the horn and the pulley and attach them together with nuts. If the pulley is made of ABS,
you can use glue to affix it to a servo horn

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 11 of 28

Step 13:
Assemble the shaft and servo, with no glue, and align the two timing belt pulleys as shown in Figure 9.
Some of the rod should be exposed from the wall opposite the pulley.
 Note: Screw the servo into the uprights, being careful not to force the screws through the foam
core, and screw the servo horn into the servo. You may use superglue instead of screws , however you
won’t be able to easily disassemble the unit.

Step 14:
Once the shaft’s pulley is aligned with the servo’s pulley, slide the inner set of washers against each wall
and glue them to the shaft using the superglue gel. They will keep the shaft from sliding out of
alignment. Also, glue the pulley to the shaft using the super glue. Let the glue set for five minutes.

Figure 9: These images show how to assemble the shaft and servo (left), and align the pullies (right).

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 12 of 28

Step 15:
Shorten the timing belt to the correct length,
around 7.2 inches, and use the superglue gel to
make a loop that connects the shaft’s pulley to
the servo’s pulley, as seen in Figure 10. First,
wrap the belt around both pulleys and take out
the slack. Now, cut the belt just after the teeth
on both ends, the ends of the belt to just reach
each other. Now cut around .5” of belt from the
piece you just removed. Finally, bring both ends
together and glue them with this extra length of
belt, image 2. Once the glue dries, place the
belt around the pulleys. It should be such a snug
fit that you will have to unattach the pulley
from the servo to fit the belt on. If it fits, place it
to the side for later.
Step 16:
Glue the mirror template onto the back of the mirror, or draw the center line by hand. Then, using the
line as a guide, glue the square nuts onto the mirror with the super glue gel. Make sure that the mirror is
able to rotate 180o from facing straight up to facing straight down without interfering with anything, and
then glue the square nuts to the shaft with the superglue gel.
 Note: The bottom edge of the square washers should be aligned with the dotted line on the
template.
Step 17:
Install the final servo, secure the bottom base to the final servo with a screw through the servo horn,
and place the timing belt onto the pulleys to complete the Helios.
 Note: Once you understand how the electronics and software work, by reading below, you can
adjust your Helios to increase its accuracy.

3
Figure 10: This shows the steps for making a belt of the
correct length.
4
1
2

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 13 of 28

Electronics Setup
Step 1:
Place the real time clock into the prototyping board and connect the pins according to Figure 11.
Note: You can solder pins onto the real time clock, use alligator clips to connect the clock to
your prototyping board, or tightly wrap wire around the connections in the clock. The last option
doesn’t require any additional purchases, however you could lose the connection if the clock is moved
relative to its wires.

Figure 11: The DS1307 timer clock wired into the prototyping board
with an Arduino, two 2.2 KOhm resistors, and a 9 Volt battery .
(Commons, Ethernet library, 2013)  (Commons, Real Time Clock
Module, 2010)  (sonlineshop, 2012)  (ElmarM, 2013)  (Gaze)
(Commons, DC Barrel Jack Adapter - Breadboard Compatible, 2011)

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 14 of 28

Step 2:
Connect the servos as shown, leaving the power disconnected from the DC jack. (Figure 12)

Note: Connect the 9 volt battery directly to the Arduino through the jack on the board and
connect the Arduino to your computer through its USB port. DO NOT connect the 9 volt battery to the
prototyping board, as this may damage your real time clock.

Figure 12: The VS-2A servos wired into the prototyping board.

Altitude
Servo
Azimuth
Servo

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 15 of 28

Software Setup
Step 1:
Download and Install Arduino Version 1.0.2 from here: (http://tinyurl.com/lx5tx72)
Note: This download includes the Helios control code and all the libraries that you will need to
run it. To install, download the folder and unzip it. The Arduino program runs directly out of its
directory, no formal installation is required. For general installation directions and directions on how to
install drivers for your Arduino, head here: http://arduino.cc/en/Guide/HomePage.
Step 2:
Run the Blink Arduino Sketch based on the directions here, (http://arduino.cc/en/Tutorial/Blink). Once
you get this short sketch to work, you can be sure that you have properly connected your Arduino to
your computer.
Step 3:
Open the control program (ArduinoCode >Helios_2013) to set the time and location of the Heliostat,
and to upload the program onto the Arduino.
1) Choose whether you want Helios to act like a solar panel and track the sun (set the variable
heliostat=0) or a heliostat (set the variable heliostat=1)
a. Note: We suggest that you try it as a solar panel first to make sure that it moves
how you expect. If one of the axis seems to be off, then you may have put in one of
the servos backwards.
2) Gently turn Helios clockwise all the way. Then point the whole machine east.
3) Enter the coordinates of your location.
a. Find the coordinates of a location by Google searching the address. Next, right click
the location and select “What’s here?”. The coordinates will appear in the search
box, with latitude and the longitude.
b. Change the default latitude and longitude values in the program to the latitude and
longitude values of Helios.
4) If you choose to use Helios as a solar panel, then skip this step. If you choose to use Helios
as a heliostat, then enter the altitude and azimuth angle of Helios’s target. The coordinate
system is defined in Figure 15.

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 16 of 28

Figure 15: The Coordinate system definition for Helios (4photos, 2112)
5)  To set the Real Time Clock, determine the current time in UTC and replace the
corresponding variables with these values, in military time. Then delete the “//” where
indicated, upload the sketch, and replace the “//” (Ex. 6:30pm EST is 10:30pm UTC. In the
program this would look like hour=22, minute=30, and second=0)
a. After the clock is set, unplug the servos and run the code in “solar panel” mode
(heliostat=0). Verify the calculated angles of the solar tracker with something like
the solar position calculator from sunearthtools.com
(http://www.sunearthtools.com/dp/tools/pos_sun.php). “dAzimuth” is the Azimuth
angle of the sun as predicted by Helios and “dElevation” is the elevation /altitude
angle of the sun. Both Helios’s and the website’s predictions should agree to within
around five degrees. Any discrepancy within this range is from the uploaded time
being off by a few minutes, and would cause an unnoticeable change in Helios’s
behavior.
b. Once Helios’s prediction for the sun’s location is accurate, then replace the “//” to
comment out the code that sets the clock. The real time clock only needs to be set
once, so it will not have to be updated as you upload new sketches or change
targets.
6) Remove the USB and power from the Arduino and connect the servo motors again.
90o
0
o

90
o

0
o

Altitude/Elevation
Azimuth
0
o

90
o

180
o

 0
o

90
o

180
o

 0
o

90
o

180
o

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 17 of 28

Step 4:
If Helios was assembled correctly, then it should point towards the target that you command and keep
the sun’s reflection stationary there when power is applied to the Arduino once again. Helios will correct
the sun’s reflection every degree. This means that the sun’s refection will shift until the sun has moved
one degree, at this point Helios will move to correct the reflection. Once you understand how the
program works, you may want to play with the variables “offset_Elv” (Elevation) and “offset_Az”
(Azimuth) to compensate for any assembly error. These variables control the orientation of Helios’s
coordinate system.

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 18 of 28

Purchasing Links
Foam core: http://www.amazon.com/Elmers-Acid-Free-Boards-16-Inch-
902015/dp/B003NS4HQY/ref=sr_1_4?s=office-products&ie=UTF8&qid=1340998492&sr=1-
4&keywords=20x30+foam+core
Rod: http://www.mcmaster.com/#cast-acrylic/=i6zw7m  (Part Number: 8528K32)
Box cutter: http://www.amazon.com/IRWIN-2082300-Utility-Standard-
Retractable/dp/B0001Q2EOS/ref=sr_1_2?ie=UTF8&qid=1340619344&sr=8 -2&keywords=box+cutter
Servo: http://www.hobbyking.com/hobbyking/store/__16641__Vigor_VS_2A_Servo_39_2g_5kg_0_17sec.html
Tape: http://www.amazon.com/Henkel-00-20843-4-Inch---500-Inch-
Invisible/dp/B000NHZ3IY/ref=sr_1_1?s=hi&ie=UTF8&qid=1340619520&sr=1 -1&keywords=invisible+tape
Templates: Print the pages at the end of this document. Paper can be purchased online at:
http://www.amazon.com/Inches-Letter-Bright-Sheets-
998067R/dp/B004WL0L9S/ref=sr_1_1?ie=UTF8&qid=1340864035&sr=8 -1&keywords=paper
Square nut: http://www.mcmaster.com/#machine-screw-square-nuts/=hflvij (Part Number: 98694A125)
Super glue: http://www.amazon.com/Krazy-Glue-KG92548R-Instant-0-18-
Ounce/dp/B000BQSFSM/ref=sr_1_2?ie=UTF8&qid=1340861717&sr=8-2&keywords=Krazy+Glue
Super glue gel: http://www.amazon.com/Krazy-Glue-KG86648R-Instant-0-07-
Ounce/dp/B000H5SFNW/ref=sr_1_4?ie=UTF8&qid=1340863003&sr=8 -
4&keywords=all+purpose+instant+krazy+glue
Straight Edge: http://www.amazon.com/The-Classics-12-Inch-Stainless-TPG-
152/dp/B002IXKD9U/ref=sr_1_1?ie=UTF8&qid=1340863091&sr=8-1&keywords=ruler
Power Drill: http://www.amazon.com/Black-Decker-9099KC-7-2-Volt-
Cordless/dp/B0002TXNX0/ref=sr_1_1?ie=UTF8&qid=1340863181&sr=8 -1&keywords=power+drill
Screws: http://www.mcmaster.com/#machine-screw-fasteners/=mumsm1 (Part Number: 90272A115)
Nuts:  http://www.mcmaster.com/#hex-nuts/=mums50 (Part Number: 90480A005)
Mirror: http://www.mcmaster.com/#catalog/118/3571/=i705h8 (Part Number: 1518T18)
Screwdriver Set: http://www.amazon.com/Stanley-66-052-6-Piece-Precision-
Screwdriver/dp/B00009OYGV/ref=sr_1_5?s=hi&ie=UTF8&qid=1340863503&sr=1 -5&keywords=screwdriver+set
2 Timing-Belt Pulleys: https://sdp-si.com/eStore/Direct.asp?GroupID=218 (Part Number: A 6M16-040DF25)
Timing-Belt: http://www.mcmaster.com/#timing-belts/=i723l2 (Part Number: 7887K82)
 Drill Bits: http://www.amazon.com/Bosch-TI18-18-Piece-Titanium-
Assortment/dp/B0000TZZWE/ref=sr_1_6?s=hi&ie=UTF8&qid=1340874037&sr=1 -6&keywords=drill+bits

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 19 of 28

Washers: http://www.mcmaster.com/#catalog/118/3226/=hzc366 (Part Number: 95630A246)
Large Vice Grips: http://www.amazon.com/7-Inch-Curved-Locking-Pliers-
Cutter/dp/B00004YO5L/ref=sr_1_10?ie=UTF8&qid=1340863806&sr=8-10&keywords=vise+grips
Nails: http://www.mcmaster.com/#standard-nails/=i708x6 (Part Number: 97850A228)
Arduino Kit: http://www.amazon.com/Starter-Kit-Newsite-Uno-
Breadboard/dp/B0051QHPJM/ref=sr_1_2?s=electronics&ie=UTF8&qid=1367794217&sr=1 -2&keywords=arduino
Real Time Clock Module: https://www.sparkfun.com/products/99
Power Supply: http://www.amazon.com/gp/product/B006GEPD6U/ref=oh_details_o01_s01_i00?ie=UTF8&psc=1
Battery: http://www.amazon.com/Duracell-Batteries-9Volt-size-battery/dp/B00009V2QT/ref=pd_sbs_hpc_9
Resistors: http://www.radioshack.com/product/index.jsp?productId=2062345

Works Cited
4photos. (2112, 07 07). 3d compass navigation. Retrieved June 6, 2013, from 4photos:
http://4photos.net/en/image:43-215776-3d_compass_navigation_images
Commons, C. (2010, January 1). Real Time Clock Module. Retrieved May 28, 2013, from Sparkfun:
https://www.sparkfun.com/products/99
Commons, C. (2011, January 1). DC Barrel Jack Adapter - Breadboard Compatible. Retrieved May 28,
2013, from Sparkfun: https://www.sparkfun.com/products/10811
Commons, C. (2013, May 16). Ethernet library. Retrieved May 28, 2013, from Arduino:
http://arduino.cc/en/Reference/Ethernet
ElmarM. (2013, March 24). Haunted Doll. Retrieved May 28, 2013, from instructables:
http://www.instructables.com/id/Now-the-fun-part-create-a-creepy-story-to-go-
wit/step17/Arduino-and-Breadboard-setup/
Gaze, M. (n.d.). STEPsss. Retrieved May 28, 2013, from kennyviper:
http://kennyviper.com/Temp/Chloe/electronic%20workshop%20final%20work/Male%20Gaze/
male%20gaze/Stepsss.html
sonlineshop. (2012, January 1). Resistor 2.2K Ohm. Retrieved May 28, 2013, from
http://sonlineshop.com/index.php?route=product/product&product_id=72

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 20 of 28

Thanks for your Support!!!
We would like to extend a huge thank you to Alexander Mitsos, our supportive advisor, and all of the
people that supported us throughout this project. We would like to especially thank all of our Kickstarter
Backers. Without your support, this would not have been possible: (Ordered by date of donation)

1. Whitney Meriwether
2. Benjamin Bangsberg
3. Walter Bryan
4. Radha Krishna Gorle
5. Matthew Miller
6. Katharina Wilkins
7. Garratt Gallagher
8. Rachel Nottelling
9. Randall Heath
10. Paul Shoemaker
11. Bruce Bock
12. Robert Davy
13. Nick Bolitho
14. Nick Bergeron
15. Paul English
16. Alexander Mitsos
17. Matt C
18. William Bryce
19. Nilton Lessa
20. Emerson Yearwood
21. Jost Jahn
22. Carl Men
23. Nina
24. Michael and Liz
25. Walter Lickteig
26. Andrew Heine
27. Rich Ramsland
28. Bryan Miller

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 21 of 28

Templates
Spacer

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 22 of 28

Base

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 23 of 28

sssbbB
Short
Base

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 24 of 28

Bottom
Bottom

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 25 of 28

s
Mirror
Mirror
2 Inches
(Attach above this line)

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 26 of 28

Wall (Print 3 copies of this page)

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 27 of 28

Wall (Print 3 copies of this page)

© P Daniel (docphil@mit.edu) and A Mitsos (amitsos@alum.mit.edu)               Helios                 Page 28 of 28

v
Cross Beams
Cut here
Cut here
