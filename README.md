# Zertz 3D

Spring '20 15-112 Term Project

This project is a 3D implementation of the abstract strategy boardgame Zertz, designed by Kris Brum. Game information and rules are available [here]( http://www.gipf.com/zertz/index.html). 

[![Zertz 3D video](https://img.youtube.com/vi/yCdGfdmuBO4/0.jpg)](https://youtu.be/yCdGfdmuBO4)

### Code

The [Panda3D](https://www.panda3d.org/) module is required

`Zertz3d.py` Run this file <br>
`board.py` Class to create board and hold all the board state information

`player.py` Class to create players and store player specific information

`robot.py` Subclass of player that contains computer player logic

`turn.py` Class that interfaces between player, including robot, and board

`scene.py` Class to create board model

`ring.py` Class to create ring model

`marble.py` Class to create marble model

`menu.py` Class that holds GUI information

Data files:

`cellNeighbors.json` Dictionary of each board cell's neighbors listed in order

`cellPositions.json` Dictionary of each cell's X,Y,Z coordinates

Assets:
/myModels contains the .egg files for the marble, ring and scene.

/myModels/tex contains the textures for the .egg files

/myModesl/UI contains the textures for the GUI

