# Fusion 360 Tongue and Groove Joint Automation

Python scripts for Autodesk Fusion 360 that automate the creation of tongue and groove joints. The scripts generate parametric geometry based on a selected face and adjustable dimension values, allowing for fast and consistent joint creation across multiple parts.



https://github.com/user-attachments/assets/48339d90-373f-42dc-b9bf-17cb1fbd0e7c



## Overview

The purpose of this project is to reduce repetitive modeling steps when designing assemblies that require tongue and groove connections. The scripts project face geometry, apply offset curves, and create either an extrusion (tongue) or a cut (groove) using the defined joint parameters. The resulting features are consistent and dimension-driven.

## Features

* Tongue generation script (`TongueCmd.py`)
* Groove generation script (`GroveCMD.py`)
* Works on any planar face in the active model
* Joint parameters can be modified directly inside the script


## Installation

1. Open Autodesk Fusion 360
2. Go to: Utilities → Add-Ins → Scripts
3. Click "Add" to include an existing script directory
4. Select the folder containing these Python files
5. Run the desired script from the Scripts panel

## Usage

1. Run `TongueCmd.py` or `GroveCMD.py`
2. When prompted, select the face where the joint should be created
3. The script automatically creates a sketch and feature based on the selected geometry
4. Select the profile when prompted to finalize the extrusion or cut

### Adjusting Parameters

Joint dimensions and offsets are defined near the top of each script. For example, in `TongueCmd.py`:

```python
thickness = 1
tongue_height = 0.4
distance_x_left = 0.5
distance_y_left = 0.5
```
Modify these to match material thickness and desired fit tolerance.

## Contributions

Suggestions and improvements are welcome.
Please open an issue or submit a pull request to propose enhancements.
