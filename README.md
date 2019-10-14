# What is Piano Blochs?

Piano Blochs is a rhythm game based on popular existing titles such as osu! and Piano Tiles. It is meant to provide a simple and enjoyable introduction to quantum physics and the concept of a quantum state. Using a Bloch sphere as the play area, points appear on the surface of the sphere to the rhythm of the music. Apply quantum logic gates to bring your Bloch vector to the desired point! But remember, your system is constantly decaying back to the ground state :) 

# Getting Started

Simply clone or download the repository with the big green button and run `piano-blochs.py` with a Python 3 interpreter.

If you have no idea what `clone` means, start [here](https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop).

## System Requirements

The Python interpreter used to run Piano Blochs must have the following modules installed:
- `matplotlib`, available from `pip`
- `qiskit`, available from `pip`

If you have no idea what an interpreter or `pip` is, start [here](https://packaging.python.org/tutorials/installing-packages/).

# Instructions

The objective of the game is to produce, via measurement, a particular quantum state relative to some initial state. The axes on the Bloch sphere represent the coordinate system with respect to this initial state. and for simplicity will be referred to as `x'`, `y'` and `z'`. `x`, `y`, `z` will represent the directions on the screen itself, serving as a sort of lab frame. Initially, `x' = x`, `y' = y`, and `z' = 'z`. Applying the gates to the system will rotate the `x'y'z'` axes along the `xyz` axes, moving the state vector and the target points.

- `a` - apply the Rx gate to the system, rotating it 90 degrees clockwise along the x-axis.
- `s` - apply the Ry gate to the system, rotating it 90 degrees clockwise along the y-axis.
- `d` - apply the Rz gate to the system, rotating it 90 degrees clockwise along the z-axis.
- `<Enter>` - take a measurement and check if the state collapsed into the desired state.
- `f` - quit the game; at the game over screen, press `<Esc>` to exit, and press any other key to restart.
- `<Esc>` - exit the game and close the game window 

# For Developers

The game code has not been refactored and may be difficult to work with, and further development is currently (as 0f 14/10/2019) not a very high priority for the team. If you wish to work with Piano Blochs, contact project maintainer @aquohn (preferably via [email](mailto:john_khoo@u.nus.edu)) with any queries or to propose any arrangements.
