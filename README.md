# DCP_games
Using Evolutionary Neutral Network and Distributive Programming in order to simulate a prototypical strategy game.

Rules of the strategy games: \
You start with a base and 10 blobs in a randomly generated position of the board. These blobs represents attack bot really. Within the board there are many rules and objective to follow:
1) You may move a blob in any direction for the turn. This means you can not move for multiple turn, move a group of blob in one direction or split the group up and move in multiple directions.
2) Two group of blob owned by you may merge in a space
3) Every time a blob or a group of blobs enter a space not owned by you or in the visual output "coloured by you", the blob expends itself to conquer the space or "colour it"
4) Whenever a blob or a group of blob meet an opposing blob either by moving towards each other or meeting at a space, each blob expends itself to take out an opposing. In the case of 3 opposing blob moving to a space, then each blob expend itself to take out each other, same with 4 or 5. What this effectively means the highest blob group in the collision wins.
5) When blobs (that are the same owner) "surround" (read as occupy neighbouring space) another group of blobs, that group of blob is wiped out and conquered by the surrounding blobs.
6) At the end of the turn, each base gets an income of blobs depending on the phase of the game

The goal of the game is to conquer enemy base by moving a group of blobs into that space. This will eliminate the player and remove everything owner by the deleted player.\

The simulation is designed into three phases: the learning phase, the test phase and the ending phase.

Learning phase is the standard phase of the game where removed player respawn with their weight adjusted. To give time for the respawning player to grow, income is 1 blob per turn.

Test phase is when respawn are removed and income is increased. This is effectively fight for which player is the last one standing.

End phase is when income is removed. If all blobs are expended or the time for end phase runs out, then the simulation ends.

Each player is given neural networks which will make the decisions for them and additionally, the simulation will have a custom genetic algorithm designed to reward player elimination and in the long run survivability. \

DCP is used to do all of the ANN calculation which consists for multiple matrix multiplication per player. On a single core, this would take years, but on DCP, this is reduce the time to minutes or even seconds.

TODO: \
Figure out the ANN setup for each player \
Configure DCP to calculate ANN \
Clean up game_data \
Implement the fitness function (for every player eliminated, new player is created whose ANN weight are based off of the eliminator's weights and a random player's weights) \
Implement output
