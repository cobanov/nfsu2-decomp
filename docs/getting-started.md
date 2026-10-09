# Getting started

## What you need

- Python 3.10 or newer and [ninja](https://ninja-build.org). `pip install -r requirements.txt`.
- Your own copy of the game, for the version you want to work on.
- On macOS and Linux, nothing else: [wibo](https://github.com/decompals/wibo) runs the Windows
  compilers and downloads on the first build.

## Game files

Nothing from the game is ever committed. Put your files in `orig/<version>/`; that folder is
ignored by git.

### GameCube, USA (`GUGE69`)

1. Dump your own disc, for example with CleanRip on a Wii.
2. Put the ISO or RVZ in `orig/GUGE69/`. decomp-toolkit reads files straight out of the image.
3. The disc carries `Speed.elf`, an unstripped build of the game with symbols. It's the source of
   our names.

The expected SHA-1 hashes will be listed here once the first dump is verified.

### PC, v1.2 (`SPEED2_EXE_1_2`)

1. Install the game from your own discs and apply the official 1.2 patch.
2. Copy `SPEED2.EXE` to `orig/SPEED2_EXE_1_2/speed2.exe`.

The splitter needs the v1.2 executable with its code in plain form (4,800,512 bytes). The retail
executable is wrapped in SafeDisc, which encrypts the code on disk. The expected SHA-1 will be
listed here once it's verified.

## Build

```sh
python configure.py                    # GameCube (default)
python configure.py -v SPEED2_EXE_1_2  # PC
ninja
```

The first `ninja` downloads the compilers, decomp-toolkit or delink, and objdiff into `build/`.

## Diff

Open the repository in [objdiff](https://github.com/encounter/objdiff). It reads the `objdiff.json`
that `configure.py` writes, rebuilds what you change, and shows each function side by side with the
original.
