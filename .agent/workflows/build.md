---
description: How to build openc2e on Windows
---

## Prerequisites

Install the following if not already present:

```powershell
winget install --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
winget install --id Kitware.CMake --accept-package-agreements --accept-source-agreements
winget install --id Microsoft.VisualStudio.2022.BuildTools --override "--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended --passive --wait" --accept-package-agreements --accept-source-agreements
```

After installing, refresh your PATH:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

## Configure (CMake)

// turbo
```powershell
cmake -S . -B build -G "Visual Studio 17 2022" -A x64 "-DCMAKE_BUILD_TYPE=RelWithDebInfo" "-DCMAKE_POLICY_VERSION_MINIMUM=3.5"
```

Note: `-DCMAKE_POLICY_VERSION_MINIMUM=3.5` is needed because the bundled SDL2 has an old `cmake_minimum_required` that CMake 4.x rejects.

## Build

```powershell
cmake --build build --config RelWithDebInfo --target openc2e -- /m
```

The `/m` flag enables parallel compilation with MSBuild.

The output binary will be at: `build\RelWithDebInfo\openc2e.exe`

## Run

```powershell
.\build\RelWithDebInfo\openc2e.exe -d "C:\path\to\GameDataFiles"
```

Replace `C:\path\to\GameDataFiles` with the path to a Creatures game's data directory (e.g. Creatures 2, Creatures 3, Docking Station).

## Run Tests

```powershell
cd build && ctest --build-config RelWithDebInfo
```
