### Current Version:
1. Group force is integrated into the social force model.    
2. Opinion dynamics is modeled, or often considered as herding effect.  
(When agents are interacting, a line between them is drawn as below.)     
3. Self-repulsion is tested

![](https://github.com/godisreal/group-social-force/blob/master/Pre-Evac2/pre-evac2.PNG)

### Walls are abstracted in type of lines and specified in Wall_Data2018.csv
<Start X, Start Y>: 	Start Points  
<End X, End Y>: 		  End Points  


### Agents are specified in the Agent_Data2018.csv
<InitalX, InitialY>: 	Initial Positions  
<DestX, DestY>: 		  Destination Positions  
acclTime: 				    Relaxation Time in Social Force Model  
tpre: 					      The TPRE Time in the Pre-Evacuation Stage  
p: 						The Following Parameter in Opinion Dynamics  
mass: 				Individual Mass of Agent  


### Some boolean variables are used to set up the simulation in the source code
THREECIRCLES = False  	# Use 3 circles to draw agents  
SHOWVELOCITY = False	# Show velocity and desired velocity of agents  
SHOWINDEX = True        # Show index of agents  
SHOWTIME = True         # Show a clock on the screen  
SHOWINTELINE = True     # Draw a line between interacting agents  
MODETRAJ = True        # Keep trajectory of agents' movement  


