# Creatures 3 Engine Migration Plan

This document outlines the strategy for migrating the original Creatures 3 (C3/DS) engine code to the modern `openc2e` architecture.

## 1. Architectural Overview

### Legacy Engine (creatures3)
- **Language**: C++ (Legacy, Visual Studio 6.0 era)
- **Core Loop**: `App::UpdateApp()` handles events, ticks, and display.
- **CAOS VM**: Centralized in `CAOSMachine.cpp`, with handlers in `FamilyHandlers.cpp`, `AgentHandlers.cpp`, etc. Command metadata is stored in `CAOSTables.cpp`.
- **Entities**: Modular `Agent` base class. Highly specialized `Creature` class using a "Faculty" system (Sensory, Motor, etc.).
- **Rendering**: Custom `DisplayEngine` managing `EntityImage`, `Background`, and `Camera`.

### Modern Engine (openc2e)
- **Language**: Modern C++ (C++17/20)
- **Core Loop**: `Engine::tick()` and `Engine::update()` using SDL2.
- **CAOS VM**: `caosVM.cpp` with handlers in `caosVM_*.cpp`. Uses metadata in comments for command registration.
- **Entities**: Mirroring legacy structure (`Agent`, `SimpleAgent`, etc.) but using smart pointers and modern STL.
- **Rendering**: SDL-based backend with an `imageManager`.

### Phase 0: AI Oversight Suite
> [!TIP]
> A modern oversight layer was added to facilitate the migration of complex subsystems.

- **JSON Telemetry**: Modified the engine to dump structured JSON snapshots of the entire world.
- **VM Inspection**: Real-time tracking of Instruction Pointers and agent relationship links.
- **AI Dashboard**: A visual tool (`tools/ai_dashboard/`) for inspecting the world state, enabling rapid parity verification between `openc2e` and the legacy engine.

## 2. Core Migration Entrypoints

### Phase 1: CAOS Parity
- **Status**: [IN PROGRESS] Foundational world commands (WNAM, WUID, NWLD, WRLD, WNTI, DELW) implemented.
- **Action**: Systematic porting of stubbed CAOS commands, prioritized by engine subsystem.
- **Tasks**:
    - [x] Implement world identification: `WNAM`, `WUID`.
    - [x] Implement world directory management: `NWLD`, `WRLD` (RV/Command), `WNTI`, `DELW`.
    - [/] Categorize remaining `stub` and `maybe` commands:
        - **Subsystem: Agent Interaction** (High Priority)
            - Port `caosVM_agent.cpp` and `caosVM_compound.cpp` stubs.
        - **Subsystem: Creature Life & Bio** (High Priority)
            - Port `caosVM_creatures.cpp`, `caosVM_genetics.cpp`, and `caosVM_history.cpp` stubs.
        - **Subsystem: Environment & Physics** (Medium Priority)
            - Port `caosVM_map.cpp` and `caosVM_motion.cpp` stubs.
        - **Subsystem: Multimedia & Input** (Medium Priority)
            - Port `caosVM_input.cpp`, `caosVM_sounds.cpp`, and `caosVM_camera.cpp` stubs.
    - [x] Establish automated verification suite in `CaosTest.cpp` for core VM commands [x].

### Phase 2: Creature Faculty System
> [!NOTE]
> The original engine's "Faculty" system is more modular than `openc2e`'s current implementation.

- **Action**: Port the Faculty architecture to `openc2e`.
- **Target Files**:
    - `creatures3/engine/Creature/SensoryFaculty.cpp` -> `openc2e/src/openc2e/creatures/SensoryFaculty.cpp`
    - `creatures3/engine/Creature/LinguisticFaculty.cpp` -> `openc2e/src/openc2e/creatures/LinguisticFaculty.cpp`
    - etc.
- **Benefit**: Allows for better debugging of specific creature behaviors (e.g., what exactly are they seeing/hearing).

### Phase 3: Physics and CA (Cellular Automata)
- **Action**: Migrate the environment logic.
- **Target Files**:
    - `creatures3/engine/Map/Map.cpp`
    - `creatures3/engine/Map/CA.cpp`
- **Focus**: Parity in room connectivity, air flow, and temperature simulation.

### Phase 4: Persistence and Archiving
- **Action**: Ensure `openc2e` can read/write the exact same world format as the original.
- **Target Files**:
    - `creatures3/engine/CreaturesArchive.cpp`
    - `openc2e/src/openc2e/ser/` (Serialization logic)

## 3. Migration Process

1.  **Selection**: Pick a specific CAOS command or a Creature faculty.
2.  **Analysis**: Study the original implementation in the `creatures3` repository.
3.  **Adaptation**: Rewrite the logic in modern C++, replacing legacy MFC/Win32 calls with `openc2e` equivalents (SDL, STL, custom types).
4.  **Integration**: Add the new code to `openc2e` and update appropriate headers.
5.  **Validation**: Use CAOS scripts to verify the behavior matches the original engine.

## 4. Testing and Validation Strategy
To ensure logical parity and prevent regressions, every migrated component must pass a rigorous testing suite.

### Unit Testing
- **Goal**: Verify individual functions (e.g., CAOS commands, biochemical reactions) behave exactly like the original.
- **Approach**: Create tests in `src/openc2e/tests/` using the existing testing framework. For CAOS commands, test edge cases (e.g., invalid agent handles, out-of-bounds parameters) to ensure error handling parity.

### Integration Testing (CAOS Scripts)
- **Goal**: Ensure complex interactions between agents and the world function correctly.
- **Approach**: Run original world scripts and verify world state changes. Compare `openc2e` debug output with the original engine's `C2eDebug` logs for the same scripts.

### Parity Testing
- **Goal**: Direct comparison of internal state.
- **Approach**: Use the **AI Oversight Suite** to dump state from both engines. By feeding snapshots into the `ai_dashboard`, developers can visually verify that agent positions, variables, and script execution paths match perfectly across engines.

## 5. Priority List

1.  **CAOS Core**: Flow control, variables, basic agent manipulation.
2.  **Sensory Faculty**: Vision and hearing logic (this is the most complex part of creature behavior).
3.  **Genome Translation**: Ensure all genes are expressed correctly.
4.  **Networking (P2P)**: Porting the "Babel" or Warp logic for world-to-world travel.

## 5. Potential Pitfalls

- **Endianness**: Original was x86/Win32. `openc2e` aims for cross-platform.
- **Frame Timing**: The original relied on 20fps or specific tick rates.
- **Integer Precision**: Some biochemistry and brain logic might rely on specific fixed-point or integer overflow behaviors.
