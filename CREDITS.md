# Credits

This project stands on years of work by other people. Thank you.

## Code we build on

- **[dbalatoni13/nfsmw](https://github.com/dbalatoni13/nfsmw)**, "WIP 1:1 Decompilation of multiple
  versions of NFS:MW", by Dávid Balatoni and contributors. `configure.py`, `tools/` and `include/`
  are adapted from it (CC0 1.0). Most Wanted's source tree continues Underground 2's, so its
  research is the closest reference we have.
- **[encounter/dtk-template](https://github.com/encounter/dtk-template)**,
  **[decomp-toolkit](https://github.com/encounter/decomp-toolkit)** and
  **[objdiff](https://github.com/encounter/objdiff)** by Luke Street (encounter): the build system
  nfsmw grew from, the GameCube splitter and the diff tool.
- **[HaydnTrigg/delink](https://github.com/HaydnTrigg/delink)**, the PE splitter used for the PC
  version (through dbalatoni13's fork).
- **[decompals/wibo](https://github.com/decompals/wibo)**, which runs the Windows compilers on
  macOS and Linux.

## Research we learn from

- **[yugecin/nfsu2-re](https://github.com/yugecin/nfsu2-re)**, a "hobby reverse engineering project
  about need for speed underground 2" by Robin (yugecin), with
  [documentation](https://yugecin.github.io/nfsu2-re/) of the PC executable: functions, structs,
  enums, file formats and hashes. Our fork, [cobanov/nfsu2-re](https://github.com/cobanov/nfsu2-re),
  keeps his work as he left it. His repository has no license, so none of its code or docs are
  copied here. We use the facts it records (addresses, names, layouts) to seed our own symbol files.
- **[whoismept/OpenUG2](https://github.com/whoismept/OpenUG2)**, "An open, from-scratch
  reimplementation of the Need for Speed: Underground 2 engine.". Its format notes are the best
  current description of the game's files. OpenUG2 is clean-room and doesn't accept decompiled code,
  so we only link to it.
- **[antoxa2584x/nfsu2-sw](https://github.com/antoxa2584x/nfsu2-sw)**, a static recompilation of the
  Xbox release with [xboxrecomp](https://github.com/sp00nznet/xboxrecomp). It shows a native lift of
  the game is possible.
- **[Ekozmaster/NFSU2-RTX-Remix](https://github.com/Ekozmaster/NFSU2-RTX-Remix)**, "RTX Remix mod
  for Need for Speed Underground 2", prior art for the ray-traced remaster.
- **[nlgxzef/NFSU2Unlimiter](https://github.com/nlgxzef/NFSU2Unlimiter)**,
  **[ExOptsTeam/NFSU2ExOpts](https://github.com/ExOptsTeam/NFSU2ExOpts)** and
  **[xan1242](https://github.com/xan1242)**'s NFS tools: years of hook points, memory layouts and
  file format knowledge for the PC version.
- **[SpeedReflect/Binary](https://github.com/SpeedReflect/Binary)**, the editor for the game's
  BIN, BUN and LZC files.
- **[ThirteenAG](https://github.com/ThirteenAG)**'s Ultimate ASI Loader and widescreen fixes.
- The [Dolphin wiki](https://wiki.dolphin-emu.org), [TCRF](https://tcrf.net) and
  [Hidden Palace](https://hiddenpalace.org) for documenting releases, prototypes and debug symbols.

If your work helped and isn't listed, open an issue and we'll add it.
