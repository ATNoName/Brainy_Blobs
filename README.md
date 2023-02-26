# Brainy_Blobs
Using Evolutionary Neural Network and Distributive Programming in order to simulate a strategy game.

Rules of the strategy game: \
- The game is played on board with *a* by *b* spaces. 
- The game starts with 2 ≤ *n* ≤ ab players. 
- Each space has an owner that is either a player, or none. Each space can contain an amount of blobs. 
- There are 2 types of spaces, a base space or a normal space. 
- There is 1 base space at a random position on the board for each player in the game. 
- Every turn, each player's base space is given an income of blobs, and each player can move an amount of their blobs on a space to the direction up, down, left, or right.
- If the space moved into is owned by the player, the blobs are added to that space.
- Every time a blob or a group of blobs is moved by a player a space not owned by the player or in the visual output "coloured by the player", the blob expends itself to conquer the space or "colour it", and change the owner to the player.
- If a base space is conquered by a player, it is changed back to a normal space. 
- Whenever a blob or a group of blob meet an opposing blob either by moving towards each other or meeting at a space, each blob expends itself to take out an opposing. In the case of 3 opposing blob moving to a space, then each blob expend itself to take out each other, same with 4 or 5. What this effectively means the highest blob group in the collision wins.
- When blobs (that are the same owner) "surround" (read as occupy neighbouring space) another group of blobs, that group of blob is wiped out and conquered by the surrounding blobs.

The goal of the game is to conquer enemy base by moving a group of blobs into that space. This will eliminate the player and remove everything owner by the deleted player.

The simulation is designed into three phases: the learning phase, the test phase and the ending phase.

Learning phase is the standard phase of the game where removed player respawn with their weight adjusted. To give time for the respawning player to grow, income is 1 blob per turn.

Test phase is when respawn are removed and income is increased. This is effectively fight for which player is the last one standing.

End phase is when income is removed. If all blobs are expended or the time for end phase runs out, then the simulation ends.

Each player is given neural networks which will make the decisions for them and additionally, the simulation will have a custom genetic algorithm designed to reward player elimination and in the long run survivability.

The neural network consist of 2 phases: the thinking phase (in the code it is named bignet) which should take the board information and should in theory output which areas of the board is most important to attack (in reality this could be something different since the only representation the neural network is given is the state of the board as the input neurons).The moving phase (named smallnet) which is used to decide how many blobs to move, to move or not move and which direction.

DCP is used to do all of the Neural Network calculation which consists for multiple matrix-vector multiplication per player. The size of the matrix depends on the size of the board and how many hidden layer (default is 3) in the network.

## Running
 - Install node.js 16
 - ```pip install git+https://github.com/Distributive-Network/Bifrost```
 - Move .dcp directory to your home directory
 - ```pip install numpy```
 - ```pip install pygame```
 - Run ```main.py```
Remember that the framerate depends on the size of your compute group.
