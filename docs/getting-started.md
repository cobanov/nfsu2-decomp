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

### PC (`SPEED2_EXE_1_0`, `SPEED2_EXE_1_2`)

1. Install the game from your own discs. For v1.2, apply the official 1.2 patch.
2. Copy `SPEED2.EXE` to `orig/SPEED2_EXE_1_0/speed2.exe` or `orig/SPEED2_EXE_1_2/speed2.exe`.

The retail executable is wrapped in SafeDisc, which encrypts the code on disk. The splitter needs
the code in plain form. Tools that patch the executable (resolution patchers, for example) change
bytes too: undo them before you compare. A SafeDisc-free executable can also carry an extra section
and a rewritten PE timestamp left by the tool that removed the wrapper; neither affects the game's
code.

| Version | Size | PE timestamp | Notes |
|---|---|---|---|
| v1.0 | 4,788,224 bytes | 2004-10-25 23:37:44 | Perforce change 116661, entry point `0x75B9F1` |
| v1.2 | 4,800,512 bytes | | Perforce change 126890 (2005-02-09), entry point `0x75BCC7`; the build yugecin/nfsu2-re documents |

The v1.0 Rich header shows MSVC 7.1 (build 3077) for most objects, the same compiler as the
Most Wanted PC version. Its strings name realcore 6.23.00 and snd 9.03.04.

## Build

```sh
python configure.py                    # GameCube (default)
python configure.py -v SPEED2_EXE_1_0  # PC
ninja
```

The first `ninja` downloads the compilers, decomp-toolkit or delink, and objdiff into `build/`.

## Diff

Open the repository in [objdiff](https://github.com/encounter/objdiff). It reads the `objdiff.json`
that `configure.py` writes, rebuilds what you change, and shows each function side by side with the
original.
