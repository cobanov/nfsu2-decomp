<p align="center">
  <img src="assets/icon.svg" alt="nfsu2-decomp icon" width="88">
</p>

<h1 align="center">nfsu2-decomp</h1>

<p align="center">
  <strong>Need for Speed: Underground 2, rebuilt one function at a time.</strong><br>
  Match the original code first. Then make it a native PC game.
</p>

<p align="center">
  <a href="docs/getting-started.md"><strong>Get started</strong></a> ·
  <a href="docs/ROADMAP.md">Roadmap</a> ·
  <a href="CONTRIBUTING.md">Contribute</a> ·
  <a href="https://github.com/cobanov/nfsu2-decomp/issues">Issues</a>
</p>

A work-in-progress decompilation of Need for Speed: Underground 2 (EA Black Box, 2004),
made to learn how the game works. We write C++ that compiles back to the exact machine code of
the shipped game, then use that source for a native PC port. The repository holds no game
assets, code or executables: bring your own copy of the game.

<p align="center">
  <sub>Day zero: the build system is in place and no functions are matched yet.</sub>
</p>

## Read the game, not a guess of it

- **Byte for byte.** A function counts as done when objdiff shows it compiles to the same
  instructions as the original GameCube or PC binary.
- **The game's own names.** The GameCube release ships an unstripped `Speed.elf`, so functions keep
  the names Black Box gave them.
- **Playable at every step.** Matched code can be loaded back into the original PC executable and
  tested in the real game.
- **A road to a native port.** Once the platform layer is understood, it gets replaced: 64-bit,
  any resolution, then a modern renderer with ray tracing.
- **In the open from day one.** Code, notes, tooling and how we use AI tools are all public.

| Version | Platform | Status |
|---|---|---|
| `GUGE69` | GameCube, USA | Waiting for the first verified dump |
| `SPEED2_EXE_1_0` | PC, `SPEED2.EXE` v1.0 | Executable identified, splitting next |
| `SPEED2_EXE_1_2` | PC, `SPEED2.EXE` v1.2 | Wanted later: most community mods target it |

## Try it

1. Install Python 3 and [ninja](https://ninja-build.org), then `pip install -r requirements.txt`.
2. Put your own copy of the game in `orig/<version>/`. See [getting started](docs/getting-started.md).
3. Run `python configure.py` (add `-v SPEED2_EXE_1_0` for PC), then `ninja`.
4. Open the project in [objdiff](https://github.com/encounter/objdiff) and pick a function.

Compilers and tools download on the first build. On macOS and Linux the Windows compilers run
through [wibo](https://github.com/decompals/wibo).

## Want to tinker?

Python and ninja around [decomp-toolkit](https://github.com/encounter/decomp-toolkit),
[delink](https://github.com/HaydnTrigg/delink) and objdiff, adapted from the
[Need for Speed: Most Wanted decompilation](https://github.com/dbalatoni13/nfsmw). SN ProDG for
GameCube, MSVC 7.1 for PC.

[Getting started](docs/getting-started.md) ·
[Roadmap](docs/ROADMAP.md) ·
[Contributing](CONTRIBUTING.md) ·
[Credits](CREDITS.md)

---

[CC0 1.0](LICENSE) · [Credits](CREDITS.md) · An educational fan project, not affiliated with or
endorsed by Electronic Arts. Need for Speed is a trademark of Electronic Arts Inc.
