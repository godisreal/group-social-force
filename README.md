# Multi-Agent Simulation For Collective Behavior

Group Social Force is implemented with Interactive Opinion Dynamics.  The fundamental idea is demonstrated as below. The model aims at investigating protypes of pedestrian behavior in a general sense. The current version of model especially contributes to simulating the crowd behavior in evacuation scenarios.

![](https://github.com/godisreal/Many-Particle-System/blob/master/FigNew.PNG)

In the repository there are several small examples to test protypes of the model.  The example is written in Python, and Pygame is required to run the code.  
How-To: Run simulator_XXX.py in a python console

The latest version of code is in Pre-Evac2  
Comment and suggestion are appreciated!

You can also check the video file pre-evac2.swf to browse the simulation result in the latest version.  
https://github.com/godisreal/group-social-force/blob/master/pre-evac2.swf

Thank Shen Shen for his original work on Social Force Model.  This repo was initially built up based on Shen Shen's code.  
https://github.com/dslwz2008/SocialForceModel

The source code runs well in Python 2.7.  The core computation runs OK in Python 3, but not sure about displaying the simulation result in Pygame with Python 3.    
Pull requests welcome!

### Current Version: 

![](https://github.com/godisreal/group-social-force/blob/master/Pre-Evac2/pre-evac2.PNG)

### Walls are abstracted in type of lines and specified in Wall_Data2018.csv
<Start X, Start Y>: 	Start Point 
<End X, End Y>: 		  End Point 


### Agents are specified in the Agent_Data2018.csv
<InitalX, InitialY>: 	Initial Positions  
<DestX, DestY>: 		  Destination Positions  
acclTime: 				    Relaxation Time in Social Force Model  
tpre: 					      The TPRE Time in the Pre-Evacuation Stage  


### Some boolean variables are used to set up the simulation (simulator_XXX.py)
THREECIRCLES = False  	# Use 3 circles to draw agents  
SHOWVELOCITY = False	# Show velocity and desired velocity of agents  
SHOWINDEX = True        # Show index of agents  
SHOWTIME = True         # Show a clock on the screen  
SHOWINTELINE = True     # Draw a line between interacting agents  
MODETRAJ = True        # Keep trajectory of agents' movement  

Several things to do to improve existing work!  
Maybe I should write a brief manual in the future.  Commets are much appreciated!
