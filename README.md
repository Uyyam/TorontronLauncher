# Custom Torontron Launcher Documentation

## Setting Up A New Cabinet
### Installing the Launcher
The script for the launcher is a python script for Linux (using wine to run windows based games) or Windows - uses python processing library for GUI: https://py5coding.org/index.html 

Install the necessary packages by clicking on the correct file for the OS
* Make sure the system has Python and Java installed first (older windows versions may not have Python installed - 
  On Windows:
    Download Python https://www.python.org/downloads/windows/
    Download Java (must be >17) https://www.microsoft.com/openjdk 
  On Linux: built into the sh script - should install automatically
When python and java are installed run the following file
  linux.sh for Linux systemsl
    Run chmod -777 linux.sh
    Then ./linux.sh
  windows.bat for windows systems (click on it)

In the corresponding .py script change the name of the game variables to the correct file name (should be the same as the folder the game is in)
Ex. 
game1="CHROMA+ELEKTRON"
game2="Retroronto"

Start the launcher on Boot:
  On Windows
    Create a shortcut to the .bat file and copy it
    Go to Run (WINDOWS + R) and Type shell:startup
    Paste the shortcut 
  On Linux
    Run chmod +x ./linux.sh
    Open Startup Applications
    Click browse and add linux.sh script

### Setting Up Controllers
I use AntiMicroX to map custom joysticks to keyboard inputs for Linux. 
Download the .deb file here: https://github.com/AntiMicroX/antimicrox/releases
  The current cabinets run on Ubuntu version 24.04 but download the correct version
Install it using: 
sudo apt install ./antimicrox<version>.deb\
ie. sudo apt install ./antimicrox-3.5.1-ubuntu-24.04-x86_64.deb
Then launch it and map the correct buttons to keys
Add application to startup applications

On Windows I use JoyToKey
https://joytokey.net/en/download 
Add application to startup shell

### Adding or Removing Games
Inside the TorontronLauncher folder:
To add a game
  Create a folder named after the game (It must have the exact same name as the games .exe file in order for the launcher to work)
  Upload the executable files in this folder
  Navigate to the launcher script and change the game variable to equal the name of the file/folder (line 11 or 12)
Asset Folder
  Each game has it's own asset folder found in XXX Torontron Build/Assets/GAME NAME X
  These folders contain:
    A banner image of the game to be displayed on the launcher. named GAME NAME 2.png
    An image of the controller scheme for the game, named controls.png
    A text file containing the game info - Title, Description and Developer that will be displayed on the launcher page, named info.txt
    * You must follow these naming conventions so the launcher is able to find the files

### To Remove a Game
Simply delete the folder named after the game and the corresponding variable launcher script

