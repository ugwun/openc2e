# CAOS Audit & Diagnostic Tools

This directory contains tools used during the Phase 1 audit and verification of the openc2e engine.

## Files

### `CAOSTables.cpp`
Original CAOS command table definitions from the Creatures 3 engine. 
*Used as the source of truth for the audit.*

### `caos_audit.py`
A Python script that parses `CAOSTables.cpp` and compares its command definitions against openc2e's `commandinfo.json` (found in `build/generated`).
*Purpose: Identifies missing, mismatched, or stubbed commands.*

### `check_voices.py`
A diagnostic script that verifies the integrity of the `voices.catalogue` file in a game data directory.
*Purpose: Checks for empty strings, invalid hex values, and incorrect table sizes to prevent out-of-range crashes.*

### `openc2e_names.txt`
A machine-generated list of all CAOS command names currently supported or stubbed in openc2e.
*Used by the audit script for fast cross-referencing.*
