# What is Piano Blochs?

Piano Blochs is a rhythm game based on popular existing titles such as osu! and Piano Tiles. It is meant to provide a simple and enjoyable introduction to quantum physics and the concept of a quantum state. Using a Bloch sphere as the play area, points appear on the surface of the sphere to the rhythm of the music. Apply quantum logic gates to bring your Bloch vector to the desired point! But remember, your system is constantly decaying back to the ground state :) 

This Bloch sphere represents a quantum system with two energy levels, such as the spin of an electron in a magnetic field. The ground state `|0>` is at the top of the sphere, and the system constantly decays towards the ground state, precessing as it does so.

# Getting Started

Simply clone or download the repository with the big green button and run `piano-blochs.py` with a Python 3 interpreter.

If you have no idea what `clone` means, start [here](https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop).

## System Requirements

The Python interpreter used to run Piano Blochs must have the following modules installed, all available from `pip`:
- `matplotlib`
- `qiskit`
- `numpy`
- `pygame`

If you have no idea what an interpreter or `pip` is, start [here](https://packaging.python.org/tutorials/installing-packages/).

# Instructions

The objective of the game is to produce, via measurement, a particular quantum state relative to some initial state. The axes on the Bloch sphere represent the coordinate system with respect to this initial state. and for simplicity will be referred to as `x'`, `y'` and `z'`. `x`, `y`, `z` will represent the directions on the screen itself, serving as a sort of lab frame. Initially, `x' = x`, `y' = y`, and `z' = 'z`. Applying the gates to the system will rotate the `x'y'z'` axes along the `xyz` axes, moving the state vector and the target points, and measurement is always performed along the z-axis (up-down on the screen).

- `a` - apply the Rx gate to the system, rotating it 90 degrees clockwise along the x-axis.
- `s` - apply the Ry gate to the system, rotating it 90 degrees clockwise along the y-axis.
- `d` - apply the Rz gate to the system, rotating it 90 degrees clockwise along the z-axis.
- `<Enter>` - take a measurement in the basis defined by the z-axis, and check if the state has collapsed into the desired state.
- `f` - quit the game; at the game over screen, press `<Esc>` to exit, and press any other key to restart.
- `<Esc>` - exit the game and close the game window 

# For Developers

The game code has not been refactored and may be difficult to work with, and further development is currently (as 0f 14/10/2019) not a very high priority for the team. If you wish to work with Piano Blochs, contact project maintainer [@aquohn](https://github.com/aquohn) (preferably via [email](mailto:john_khoo@u.nus.edu)) with any queries or to propose any arrangements.

# Credits

This game was created at [Qiskit Hackathon 2019](https://github.com/qiskit-community/qiskit-hackathon-singapore-19) in Singapore. Special thanks to [@HuangJunye](https://github.com/HuangJunye) and [Naoki Kanazawa](https://researcher.watson.ibm.com/researcher/view.php?person=jp-KNZWNAO) for their invaluable mentorship!

The song featured is _Kalimba_ by Mr. Scruff - a copy of which you may be able to find in the Music folder of any Windows 7 computer. The song is from his album [Ninja Tuna](https://open.spotify.com/album/0m1RgvoI6QyGACkazXV5Th).
