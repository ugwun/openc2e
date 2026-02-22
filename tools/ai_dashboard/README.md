# AI Oversight Dashboard (v2.1)

This folder contains a web-based visualization tool for real-time monitoring and debugging of the `openc2e` engine. It provides a birds-eye view of the game world, agent relationships, and Virtual Machine (VM) execution states.

## 🚀 System Architecture

The oversight system consists of two primary components:

1.  **Engine Telemetry (C++)**:
    *   **Source**: `src/openc2e/World.cpp` (`World::dumpStateJSON`)
    *   **Action**: The engine serializes the entire world state into a structured JSON snapshot (`world_snapshot.json`).
    *   **Data Included**:
        *   **Metarooms**: Physical dimensions and background identifiers.
        *   **Agents**: Positions, classifiers (F/G/S), attributes, and local variables (`OVxx`/`NAME`).
        *   **VM State**: Instruction pointers (CIP/NIP), current script, and internal registers (`TARG`, `OWNR`, `IT`).
        *   **Relationships**: Links for `carrying`, `carriedby`, and `invehicle`.

2.  **Visualization Layer (HTML5/JS)**:
    *   **File**: `ai_dashboard.html`
    *   **Action**: A standalone web application that parses the JSON snapshot and renders it to a coordinate-accurate `<canvas>`.
    *   **Features**:
        *   **Auto-Fitting Viewport**: Dynamically adjusts to show all metarooms (e.g., C3 Ship + Docking Station).
        *   **Exploration**: Supports smooth panning (click-and-drag) and zooming (mouse wheel).
        *   **Deep Inspection**: Clicking any agent opens a sidebar with their full internal state and variable values.
        *   **Navigation**: "Jump to Area" dropdown for rapid travel between metarooms.

## �️ How to Capture a Snapshot

To capture the current state of your world and view it in the dashboard:

1.  **Open the CAOS Console**: While the game is running, press `CTRL + SHIFT + C` on your keyboard.
2.  **Trigger the Snapshot**: Type the following command and press Enter:
    ```caos
    dbg: snap
    ```
3.  **Locate the File**: The engine will generate a file named `world_snapshot.json`. You can find it in your build output directory, typically:
    *   `<project_root>/build/RelWithDebInfo/world_snapshot.json`
    *   *Note: If you are running from a different directory, it will be in the Current Working Directory (CWD) of the process.*
4.  **Open in Dashboard**: Click "Choose File" in `ai_dashboard.html` and select the generated JSON.

## 🛠️ Developer Workflow

## 🚀 Future Roadmap

The oversight system is evolving. Planned enhancements for the snapshot and dashboard include:

*   **Brain Activity**: Add serialization for the Norn/Grendel/Ettin brain state (neurons, dendrites, and firing states).
*   **Biochemistry**: Track chemical concentrations (Loci) per creature.
*   **Genome Mapping**: Visualize expressed genes and their current influence on behavior.
*   **Heatmaps**: Render room-based CA (Cellular Automata) data like air quality, temperature, and light levels.
*   **Live Mode**: Establish a WebSocket connection between the engine and the dashboard for real-time streaming updates without manual snapshots.

## 🤖 AI Agent Oversight

This dashboard is designed to be machine-readable. AI agents can utilize the JSON structure to:
- Perform spatial analysis of agent distribution.
- Identify "stuck" scripts by monitoring static IPs across snapshots.
- Verify relationship logic parity by comparing `carrying` states against CAOS expectations.

---
*Created as part of the Creatures 3 Engine Migration effort.*
