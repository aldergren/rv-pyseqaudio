#!/bin/sh

# This will create a package in a temporary support area, install it
# and then run RV.

RVHOME=/Applications/RV64.app/Contents
RVBIN=$RVHOME/MacOS/RV64
RVPKG=$RVHOME/MacOS/rvpkg

mkdir -p build/Packages
zip -j build/Packages/seqaudio-1.0.1.rvpkg rv-pyseqaudio/*

export RV_SUPPORT_PATH=build

$RVPKG -uninstall build/Packages/seqaudio-1.0.1.rvpkg
$RVPKG -install build/Packages/seqaudio-1.0.1.rvpkg
$RVBIN
