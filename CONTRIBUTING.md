# Contributing

Thanks for helping. This is a learning project, so questions in issues are as welcome as code.

## Ground rules

- **Never commit game files.** No executables, disc images, extracted assets, text dumps or
  assembly. Everyone brings their own copy of the game; `orig/` and `build/` are ignored for that
  reason.
- **Matching means matching.** Mark an object `Matching` in `configure.py` only when objdiff shows
  every function in it at 100% for that version. Use `MatchingFor(...)` when it only matches some
  versions, and `NonMatching` for work in progress.
- **Original names win.** Use the names from the GameCube `Speed.elf` symbols whenever they exist.
  Invent names only for things the symbols don't cover, and keep them in the game's style.
- **Credit your sources.** If a fact comes from another project, say so in the PR and, for a new
  source, add it to [CREDITS.md](CREDITS.md).

## Code that reads like the original

Matching code can still be wrong in ways that hurt a port. Reviews reject:

- forcing registers or reordering statements only to fake a match;
- reaching into structs through pointer offsets instead of declared members;
- invented strings, floats or constants where the original values are known;
- renaming parameters and variables away from the symbols;
- the same function implemented twice, or functions redeclared at the top of a file instead of in
  a header;
- casts to the type a value already has.

This list is adapted from the
[Need for Speed: Most Wanted decompilation](https://github.com/dbalatoni13/nfsmw)'s rules.

## AI tools

AI tools are allowed, and we're open about using them. If a PR contains AI-written code, say so in
its description. The same review rules apply: a human has to understand and stand behind every
line, and objdiff decides whether it matches.

## Workflow

1. Follow [getting started](docs/getting-started.md) until `ninja` builds your version.
2. Pick an unmatched function in objdiff, or an open issue.
3. Keep PRs small: one translation unit or one subsystem at a time.
4. Run `python configure.py progress` and include the before and after in the PR.
