# s2practice

## Background

One thing I've had on my list to do is learn to [speedrun Sonic the Hedgehog 2](https://www.speedrun.com/s2).

This tends to require lots of using the level-select code to pick stages,
and also dying a lot. Dealing with re-entering the level select code every
time I want to pick it up is tedious and annoying, so I built a small
ROM-patching system to let me easily modify sections of the original ROM
so that I can practice on [a flash cart](https://krikzz.com/store/home/45-mega-everdrive-x3.html).

## So what's all this

This is a system for being able to write annotated assembly using the
[GNU Assembler](https://www.gnu.org/software/binutils/). The GNU Assembler
isn't designed to patch arbitrary binaries, so this requires a second
script to utilize those annotations so replace sections of the original ROM.

## Changes

- Level-select code is pre-applied; starting a new game takes you to it.
- You start the game with 99 lives, so it takes longer to game over

## TODO

- can we add basic save-state support (as the Mega Everdrive X3 lacks this feature)
