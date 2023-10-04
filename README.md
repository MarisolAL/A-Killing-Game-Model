# A Killing Game Model

Inspired by the game _Danganronpa_ the project models a simpler killing game. For the simulation the
project uses Python 2 and [Processing.py](https://py.processing.org/) framework.

## Game rules

The game has a set of players (in the code also referred as particles), a board or mesh where they will interact, and 
three phases.

### Phase 0

In the phase 0 the players will just interact between each other, these interactions modify the affinity 
levels between the players, in some iterations an incentive will be sent making the despair levels increase until
changing to phase 1, this happens when a player reach the highest despair level.

### Phase 1

Because a player reached the highest despair level, it will start chasing a victim to kill it and try to get away
with the murder. The particle will move until it finds a particle in their vision field and will kill the neighbor, 
there will always be a neighbor who will witness the crime, this action will change the current phase to phase 2.

### Phase 2

Phase 2 is considered as the _Investigation phase_, here the witness of the crime will try to spread the culprit
to the particles it has near, and this other particles will do the same, to make the others believe 
the culprit the affinity should be high enough, this phase has a time limit of 35 iterations, if in those iterations
more than 50% of the alive players doesn't have the right culprit then the killer wins, in other case the killer is 
eliminated from the game and the game returns to phase 0.
