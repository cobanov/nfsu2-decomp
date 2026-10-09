# Roadmap

The goal is a full understanding of the game, then a native PC port, then a remaster with native
4K rendering and ray tracing. One source tree serves two builds:

- **Matching build:** compiled with the original toolchains and compared byte for byte against the
  GameCube and PC binaries.
- **Hook build:** matched functions loaded into the original PC executable through a DLL, replacing
  the originals one by one, so the game stays playable at every step.

## Phase 0: materials

- [x] PC executables to work on: v1.0 (Perforce change 116661) and v1.2 (change 126890). See
      [getting started](getting-started.md).
- [ ] A verified dump of the GameCube USA disc (`GUGE69`).
- [ ] Inspect `Speed.elf`: which symbols it has, how much DWARF, which compiler versions
      (`.comment` section).
- [x] Identify the PC compiler from the `SPEED2.EXE` Rich header: MSVC 7.1, build 3077.
- [ ] Check other builds for symbols: PAL GameCube (`GUGP69`), the PS2 Alpha 10R prototype, Xbox.
      The PS2 EU v2.00 retail ELF (`SLES_527.25`) is stripped: only section names survive.

## Phase 1: skeleton

- [x] Build system adapted from nfsmw: GameCube (ProDG) and PC v1.0 and v1.2 (MSVC 7.1).
- [ ] GameCube: `symbols.txt` and `splits.txt` generated from `Speed.elf`; the unmodified split
      rebuilds to the original DOL hash.
- [ ] PC: disassembler database seeded with GameCube names and the facts from yugecin/nfsu2-re;
      `symbols.json` and `splits.json` exported; the split relinks to the original executable.
- [ ] CI that builds both versions and publishes progress.
- [ ] The first matched function.

## Phase 2: matching

- [ ] Libraries shared with Most Wanted (bWare, EA libraries, Dolphin SDK, runtime), compared
      against nfsmw's matched code.
- [ ] Game systems, in the order the port needs them: main loop and memory, file and chunk loading,
      world streaming, rendering, cars and physics, AI, frontend, audio.

## Phase 3: hook build

- [ ] A DLL that replaces original PC functions with matched ones, switchable per function.
- [ ] The game playable with every matched function replaced.

## Phase 4: port and remaster

- [ ] A new platform layer: 64-bit, SDL, modern input and audio.
- [ ] A new renderer backend: native resolutions and widescreen first, then ray tracing.
- [ ] Runs from source with only the original game data.
