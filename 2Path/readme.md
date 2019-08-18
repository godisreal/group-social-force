Current Version:
1. Group force is integrated into the social force model.    
2. Opinion dynamics is modeled, or often considered as herding effect.   
3. Wall force is tested

![](https://github.com/godisreal/group-social-force/blob/master/2Path/0708.PNG)

### Walls are all abstracted in type of lines and are specified in Wall_Data2018.csv
<Start X, Start Y>: 	Start Points  
<End X, End Y>: 		End Points  


### Agents are specified in the Agent_Data2018.csv
<InitalX, InitialY>: 	Initial Positions   
<DestX, DestY>: 		Destination Positions    
acclTime: 				  Relaxation Time in Social Force Model   
tpre: 					    The TPRE Time in the Pre-Evacuation Stage   
p: 						      The Following Parameter in Opinion Dynamics   
mass: 					    Individual Mass of Agent  


### Below are boolean variables for users to set up the simulation 
SHOWVELOCITY = False	  # Show velocity and desired velocity of agents  
SHOWINDEX = True        # Show index of agents    
SHOWTIME = True         # Show a clock on the screen    
SHOWINTELINE = True     # Draw a line between interacting agents  
MODETRAJ = False        # Keep trajectory of agents' movement   
COHESION = True		      # Enable the Group social force   
SELFREPULSION = True	  # Enable self repulsion   
WALLBLOCKHERDING = True   
SHOWWALLDATA = True   
