## Welcome to pyTWANG

This is a "port" or rather a rewrite of the 1D dungeon crawler called TWANG.

The original game is written for Arduino and is inspired by the game wobbler.

### Dependencies
* Python 3 (I guess? I do not even know Python 2)
* pyGame

### Goals
* Implement all the features of the Arduino implementation
* Allow simulation on the pc, for easier development and maintainability.
* Eventually port to run in circuit/micro python.
* Eventually port onto the iCEBreaker FPGA running RISC-V and some custom LED string PPU.

### Current status
Here is a basic todo list for the 1-1 port of the game.
I bet it is not even a complete list.

* [x] pygame LED string emulation
* [ ] Screensavers
  * [x] Mode 0: Marching green <> orange
  * [x] Mode 1: Random flashes
  * [x] Mode 2: Dots in bowl
  * [ ] Mode 3
  * [ ] Mode 4
* [ ] Controls
* [ ] Player
  * [ ] Player attack/shield
* [ ] Enemy
* [ ] Particle
* [ ] Spawner
* [ ] Lava
* [ ] Conveyor
* [ ] Boss
* [ ] Settings

