#!/usr/bin/env python3

###
# Generates build files for the project.
# This file also includes the project configuration,
# such as compiler flags and the object matching status.
#
# Usage:
#   python3 configure.py
#   ninja
#
# Append --help to see available options.
#
# Adapted from the Need for Speed: Most Wanted decompilation
# (https://github.com/dbalatoni13/nfsmw, CC0), which is itself based on
# encounter's dtk-template.
###

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

from tools.project import (
    Object,
    ProgressCategory,
    ProjectConfig,
    Platform,
    calculate_progress,
    generate_build,
    is_windows,
)

# Game versions
DEFAULT_VERSION = 0
VERSIONS = [
    "GUGE69",  # 0: GameCube, USA. Ships Speed.elf with symbols.
    "SPEED2_EXE_1_0",  # 1: PC, SPEED2.EXE v1.0 (4,788,224 bytes, CL 116661)
    "SPEED2_EXE_1_2",  # 2: PC, SPEED2.EXE v1.2 (4,800,512 bytes, CL 126890)
]

parser = argparse.ArgumentParser()
parser.add_argument(
    "mode",
    choices=["configure", "progress"],
    default="configure",
    help="script mode (default: configure)",
    nargs="?",
)
parser.add_argument(
    "-v",
    "--version",
    choices=VERSIONS,
    type=str.upper,
    default=VERSIONS[DEFAULT_VERSION],
    help="version to build",
)
parser.add_argument(
    "--build-dir",
    metavar="DIR",
    type=Path,
    default=Path("build"),
    help="base build directory (default: build)",
)
parser.add_argument(
    "--binutils",
    metavar="BINARY",
    type=Path,
    help="path to binutils (optional)",
)
parser.add_argument(
    "--compilers",
    metavar="DIR",
    type=Path,
    help="path to compilers (optional)",
)
parser.add_argument(
    "--map",
    action="store_true",
    help="generate map file(s)",
)
parser.add_argument(
    "--debug",
    action="store_true",
    help="build with debug info (non-matching)",
)
if not is_windows():
    parser.add_argument(
        "--wrapper",
        metavar="BINARY",
        type=Path,
        help="path to wibo or wine (optional)",
    )
parser.add_argument(
    "--dtk",
    metavar="BINARY | DIR",
    type=Path,
    help="path to decomp-toolkit binary or source (optional)",
)
parser.add_argument(
    "--delink",
    metavar="BINARY | DIR",
    type=Path,
    help="path to delink binary (optional)",
)
parser.add_argument(
    "--objdiff",
    metavar="BINARY | DIR",
    type=Path,
    help="path to objdiff-cli binary or source (optional)",
)
parser.add_argument(
    "--sjiswrap",
    metavar="EXE",
    type=Path,
    help="path to sjiswrap.exe (optional)",
)
parser.add_argument(
    "--verbose",
    action="store_true",
    help="print verbose output",
)
parser.add_argument(
    "--non-matching",
    dest="non_matching",
    action="store_true",
    help="builds equivalent (but non-matching) or modded objects",
)
parser.add_argument(
    "--no-progress",
    dest="progress",
    action="store_false",
    help="disable progress calculation",
)
args = parser.parse_args()

config = ProjectConfig()
config.version = str(args.version)
version_num = VERSIONS.index(config.version)

# Apply arguments
config.build_dir = args.build_dir
config.dtk_path = args.dtk
config.delink_path = args.delink
config.objdiff_path = args.objdiff
config.binutils_path = args.binutils
config.compilers_path = args.compilers
config.generate_map = args.map
config.non_matching = args.non_matching
config.sjiswrap_path = args.sjiswrap
config.progress = args.progress
if not is_windows():
    config.wrapper = args.wrapper
# Don't build asm unless we're --non-matching
if not config.non_matching:
    config.asm_dir = None

# Tool versions
config.compilers_tag = "20260903"

if version_num == 0:
    config.platform = Platform.GC_WII
    config.dtk_tag = "v1.8.32"
    config.binutils_tag = "2.42-1"
    config.wibo_tag = "1.1.0"  # sjiswrap segfaults on newer wibo
elif version_num in [1, 2]:
    config.platform = Platform.WIN32
    config.delink_tag = "v0.16.4"
    config.wibo_tag = "1.2.0"

config.objdiff_tag = "v3.7.0"
config.sjiswrap_tag = "v1.2.2"

# Project
config.config_path = Path("config") / config.version / "config.yml"
config.check_sha_path = Path("config") / config.version / "build.sha1"

compilers_path = (
    Path(config.compilers_path) if config.compilers_path else Path("build/compilers")
)

if config.platform == Platform.GC_WII:
    config.asflags = [
        "-mgekko",
        "--strip-local-absolute",
        "-I include",
        f"-I build/{config.version}/include",
        f"--defsym BUILD_VERSION={version_num}",
    ]

    ldscript_path = Path("config") / config.version / "ldscript.ld"
    keep_list_path = Path("config") / config.version / "keep.lst"
    config.ldflags = [
        "-strip-unused-data",
        "-keep",
        str(keep_list_path),
        "-T",
        str(ldscript_path),
    ]

    # Optional numeric ID for decomp.me preset
    config.scratch_preset_id = 176
elif config.platform == Platform.WIN32:
    config.ldflags = [
        "/nologo",
        "/MACHINE:X86",
        "/SUBSYSTEM:WINDOWS,4.0",
        "/ENTRY:entry",
        "/NODEFAULTLIB",
        "/FIXED",
        "/INCREMENTAL:NO",
        "/BASE:0x400000",
        "/FILEALIGN:0x1000",
        f"/PDB:./build/{config.version}/{config.version}.pdb",
    ]

# Use for any additional files that should cause a re-configure when modified
config.reconfig_deps = []

# The toolchains below are the ones Black Box used for Most Wanted (2005).
# Underground 2 (2004) most likely used the same ones, but that is unverified:
# check the .comment section of Speed.elf (GameCube) before trusting a match.
# The PC v1.0 Rich header confirms MSVC 7.1 (build 3077) for most objects.
if config.platform == Platform.GC_WII:
    config.linker_version = "ProDG/3.9.3"

    cflags_base_mwcc = [
        "-nodefaults",
        "-proc gekko",
        "-align powerpc",
        "-enum int",
        "-fp hardware",
        "-Cpp_exceptions off",
        "-O4,p",
        "-inline auto",
        '-pragma "cats off"',
        '-pragma "warn_notinlined off"',
        "-maxerrors 1",
        "-nosyspath",
        "-RTTI off",
        "-fp_contract off",
        "-str reuse",
        "-multibyte",
        "-D__GEKKO__",
        f"-DVERSION={version_num}",
    ]

    cflags_base_prodg = [
        "-O1",
        "-gdwarf+",
        "-Wno-ctor-dtor-privacy",
        "-Woverloaded-virtual",
        "-Wno-multichar",
        "-I src/Packages",
        "-I src",
        "-DEA_PLATFORM_GAMECUBE",
        "-DEA_REGION_AMERICA",
        "-DGEKKO",
        "-D_USE_MATH_DEFINES",
        f"-I build/{config.version}/include",
        f"-DBUILD_VERSION={version_num}",
        f"-DVERSION_{config.version}",
    ]

    config.context_defines = [
        "EA_PLATFORM_GAMECUBE",
        "EA_REGION_AMERICA",
        "GEKKO",
        "_USE_MATH_DEFINES",
        "__SN__",
        "SN_TARGET_NGC",
    ]

    if config.non_matching:
        cflags_base_prodg.append("-DNON_MATCHING")

    if args.debug:
        cflags_base_prodg.append("-DDEBUG=1")
    else:
        cflags_base_prodg.append("-DNDEBUG=1")

    # Library include paths (snd, realcore, rcmp, ...) get added here once
    # their versions are known from Speed.elf's line info.
    cflags_game = [
        *cflags_base_prodg,
        "-mps-nodf",
        "-G0",
        "-fno-static-dtors",
        "-ffast-math",
        "-fforce-addr",
        "-fcse-follow-jumps",
        "-fcse-skip-blocks",
        "-fforce-mem",
        "-fgcse",
        "-frerun-cse-after-loop",
        "-fschedule-insns",
        "-fschedule-insns2",
        "-fexpensive-optimizations",
        "-frerun-loop-opt",
        "-fmove-all-movables",
    ]

    config.extra_clang_flags = [
        "-std=gnu++11",
        "-DSN_TARGET_NGC",
        "-D__SN__",
        "-DCLANGD_DAMNIT",
        "-D__HONOR_STD",
        "-Wno-writable-strings",
    ]

    # Metrowerks flags, for the Dolphin SDK and runtime
    cflags_runtime = [*cflags_base_mwcc]

elif config.platform == Platform.WIN32:
    config.linker_version = "Win32/7.1"

    cflags_base_prodg = [
        "/nologo",
        "/c",  # compile without linking
        "/wd4996",  # string deprecation warnings
        "/wd4355",  # 'this' used in base member initializer
        "/Ox",
        "/Z7",  # debug info per object file
        "/EHsc",
        f"/I {compilers_path / config.linker_version / 'Include'}",
        "/I src/Packages",
        "/I src",
        "/DEA_PLATFORM_WIN32",
        "/D_USE_MATH_DEFINES",
        f"/I build/{config.version}/include",
        f"/DBUILD_VERSION={version_num}",
        f"/DVERSION_{config.version}",
    ]

    config.context_defines = [
        "EA_PLATFORM_WIN32",
        "EA_REGION_AMERICA",
        "_USE_MATH_DEFINES",
        "_WIN32",
    ]

    cflags_game = [*cflags_base_prodg]

    config.extra_clang_flags = [
        "-std=c++98",
        "-DCLANGD_DAMNIT",
        "-D_WIN32",
        "-D_WCHAR_T_DEFINED",
        "-fms-extensions",
    ]

Matching = True  # Object matches and should be linked
NonMatching = False  # Object does not match and should not be linked
Equivalent = (
    config.non_matching
)  # Object should be linked when configured with --non-matching


# Object is only matching for specific versions
def MatchingFor(*versions):
    return config.version in versions


config.warn_missing_config = True
config.warn_missing_source = False

# Objects are added here as the binaries are split into translation units.
config.libs = [
    {
        "lib": "Game",
        "toolchain_version": config.linker_version,
        "cflags": cflags_game,
        "host": False,
        "progress_category": "game",
        "objects": [],
    },
]


# Optional callback to adjust link order.
def link_order_callback(module_id: int, objects: List[str]) -> List[str]:
    return objects


config.progress_categories = [
    ProgressCategory("game", "Game Code"),
    ProgressCategory("sdk", "SDK Code"),
    ProgressCategory("libc", "STD Code"),
    ProgressCategory("libs", "Library Code"),
]
config.progress_each_module = args.verbose

if args.mode == "configure":
    # Write build.ninja and objdiff.json
    generate_build(config)
elif args.mode == "progress":
    # Print progress information
    calculate_progress(config)
else:
    sys.exit("Unknown mode: " + args.mode)
