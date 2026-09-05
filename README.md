# smithchart_tool

A Python library for Smith Chart analysis, microwave impedance transformations, and matching-network synthesis using Möbius transformations.

## Overview

`smithchart_tool` is an open-source Python package for analyzing and visualizing microwave impedance and admittance transformations on the Smith Chart.

The library provides an object-oriented framework for representing common microwave network elements such as impedances, admittances, transmission lines, and open-circuit stubs.

Network elements can be connected sequentially to reproduce the impedance transformations of a matching network and visualize the corresponding trajectories directly on the Smith Chart.

The mathematical transformations implemented by the library are based on complex-number operations and Möbius transformations, providing an explicit computational representation of the transformations commonly performed by microwave CAD tools.

The project was originally developed as a computational framework for independently verifying matching-network synthesis performed using conventional microwave CAD software, particularly Keysight ADS.

## Features

- Smith Chart impedance and admittance visualization.
- Complex impedance and admittance representation.
- Reflection-coefficient visualization.
- Constant-resistance and constant-reactance circles.
- Constant-conductance and constant-susceptance circles.
- Transmission-line impedance transformations.
- Open-circuit stub transformations.
- Sequential connection of microwave network elements.
- Visualization of impedance trajectories between matching-network stages.
- Retrieval of impedance and admittance at each transformation stage.
- Object-oriented representation of microwave network elements.
- Independent reproduction of Smith Chart impedance transformations.
- Möbius transformation-based impedance mapping.
- Python-based numerical analysis and visualization.

## Supported Network Elements

The package currently provides classes for several microwave network elements, including:

- Impedance
- Admittance
- Transmission lines
- Open-circuit stubs
- Short-circuit stubs

These elements can be combined to construct and analyze matching networks step by step.

For example, a network can be represented conceptually as:

```text
Load
  │
  ▼
Transmission Line
  │
  ▼
Shunt Stub
  │
  ▼
Transmission Line
  │
  ▼
Input Impedance
```

The implementation was developed as part of the research presented in:

> **Design and Verification of a 500-W S-Band GaN Power Amplifier Using Möbius Transformations**


## Installation

Clone the repository:

```bash
git clone https://github.com/ZeroPole03/smithchart_tool.git
cd smithchart_tool
```

Install the package locally:

```bash
pip install .
```

For development, an editable installation can be used:

```bash
pip install -e .
```

The required dependencies are listed in `requirements.txt`.

## Package Structure

The main classes included in the package are:

| Class              | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| `SmithChart`       | Creates and plots impedance and admittance Smith Charts.               |
| `Impedance`        | Represents a complex impedance and its reflection coefficient.         |
| `Admittance`       | Represents the admittance associated with an impedance.                |
| `TransmissionLine` | Represents impedance transformations produced by transmission lines.   |
| `OpenStub`         | Represents impedance transformations produced by an open-circuit stub. |
| `ShortStub`         | Represents impedance transformations produced by an short-circuit stub. |

The classes can be imported directly from the main package:

```python
from smithchart_tool import *
```

## Smith Chart

The `SmithChart` class creates the coordinate system used to visualize impedance and admittance transformations.

```python
import numpy as np
from smithchart_tool import *

theta = np.linspace(0, 2*np.pi, 1000)

smith = SmithChart(theta, unitary=False)
smith.plotChart()
```

The `unitary` parameter controls the range of the resistance and reactance circles displayed on the chart.

The impedance and admittance Smith Charts can also be displayed simultaneously:

```python
smith.plotChart(admitance=True)
```

## Impedance

The `Impedance` class represents a complex load impedance referenced to a characteristic impedance.

```python
Z = Impedance(50.0, 70.561 + 1j*5.052)
```

The corresponding reflection coefficient can be represented on the Smith Chart:

```python
Z.addToSmithChart("Load impedance")
```

Constant-resistance and constant-reactance circles can be plotted using:

```python
Z.plotCircles(theta)
```

The impedance and admittance associated with the object can be obtained using:

```python
Z.getImpedance()
Z.getAdmitance()
```

The impedance value can also be labeled directly on the Smith Chart:

```python
Z.labelOnChart(True, x0, y0)
```

## Admittance

The `Admittance` class is constructed from an `Impedance` object.

```python
Z = Impedance(50.0, 70.561 + 1j*5.052)
Y = Admittance(50.0, Z)
```

The corresponding impedance and admittance can be retrieved using:

```python
Y.getImpedance()
Y.getAdmitance()
```

The constant-conductance and constant-susceptance circles can be visualized using:

```python
Y.addToSmithChart(theta)
```

The admittance can be labeled directly on the Smith Chart:

```python
Y.labelOnChart(True, x0, y0)
```

The class also provides functionality for representing admittance transformations associated with transmission lines:

```python
Y.transToAdmitance(TransmissionLine)
```

## Transmission Lines

The `TransmissionLine` class represents the impedance transformation produced by a transmission line.

It receives:

* `Z0`: characteristic impedance of the transmission line.
* `Impedance`: input impedance object.
* `deg`: electrical length of the transmission line in degrees.
* `f0`: operating frequency.

For example:

```python
f0 = 3e9

Z1 = Impedance(50.0, 70.561 + 1j*5.052)

TL1 = TransmissionLine(
    82.0,
    Z1,
    71.39,
    f0
)
```

The transformed impedance can be represented on the Smith Chart:

```python
TL1.addToSmithChart(theta, "Transmission Line")
```

The transformed impedance and admittance can be obtained using:

```python
TL1.getImpedance()
TL1.getAdmitance()
```

The corresponding transformed impedance circles can also be plotted:

```python
TL1.plotImpedanceCircles(theta, "Transmission Line")
```

The transformed impedance can be labeled on the Smith Chart:

```python
TL1.labelOnChart(True, x0, y0)
```

## Open-Circuit Stub

The `OpenStub` class represents an open-circuit transmission-line stub and its associated impedance transformation.

The constructor accepts:

* `z0`: characteristic impedance of the stub.
* `ZL`: input impedance associated with the previous network stage.
* `theta_deg`: electrical length of the stub in degrees.
* `f0`: operating frequency.

For example:

```python
stub = OpenStub(
    z0=77.0,
    ZL=50 + 1j*10,
    theta_deg=11.99,
    f0=3e9
)
```

The transformed reflection coefficient can be represented on the Smith Chart:

```python
stub.addToSmithChart("Open Stub")
```

The transformed impedance and admittance can be obtained using:

```python
stub.getImpedance()
stub.getAdmitance()
```

The associated impedance circles can be plotted using:

```python
stub.plotImpedanceCircles(theta)
```

and the corresponding admittance circles using:

```python
stub.plotAdmitanceCircles(theta)
```

##Short-Circuit Stub

The `ShortStub` class represents a short-circuit transmission-line stub and its associated impedance transformation.

The constructor accepts:

* `z0`: characteristic impedance of the stub.
* `ZL`: input impedance associated with the previous network stage.
* `theta_deg`: electrical length of the stub in degrees.
* `f0`: operating frequency.

For example:

```python
shortstub = ShortStub(
    z0=77.0,
    ZL=50 + 1j*10,
    theta_deg=11.99,
    f0=2.4e9
)
```

The transformed reflection coefficient can be represented on the Smith Chart:

```python
shortstub.addToSmithChart("Open Stub")
```

The transformed impedance and admittance can be obtained using:

```python
shortstub.getImpedance()
shortstub.getAdmitance()
```

The associated impedance circles can be plotted using:

```python
shortstub.plotImpedanceCircles(theta)
```

and the corresponding admittance circles using:

```python
shortstub.plotAdmitanceCircles(theta)
```

## Sequential Matching-Network Analysis

One of the main capabilities of `smithchart_tool` is the sequential representation of matching-network transformations.

The output impedance of one network element can be used as the input impedance of the following element. This allows transmission lines, reactive elements, and open stubs to be combined to reproduce a complete matching-network transformation.

A simplified example is:

```python
Z1 = Impedance(50.0, 70.561 + 1j*5.052)

TL1 = TransmissionLine(
    82.0,
    Z1,
    np.deg2rad(71.39),
    3e9
)

Z2 = TL1.getImpedance()

TL2 = TransmissionLine(
    77.0,
    Impedance(50.0, Z2),
    np.deg2rad(41.86),
    3e9
)

Z3 = TL2.getImpedance()

stub = OpenStub(
    77.0,
    Z3,
    11.99,
    3e9
)

Z4 = stub.getImpedance()
```

This sequential approach allows the impedance state to be tracked throughout the matching network.

The corresponding transformations can be plotted on the Smith Chart to visualize the complete impedance trajectory.

## Example: Input Matching Network

The `examples/` directory contains scripts demonstrating the application of the library to microwave matching networks.

The input matching example combines:

1. An initial complex load impedance.
2. A transmission-line transformation.
3. A lumped reactive element.
4. A second transmission-line transformation.
5. An open-circuit stub.
6. A final transmission-line transformation.

The resulting impedance states are plotted sequentially on the Smith Chart, allowing the complete matching-network trajectory to be visualized.

This workflow reproduces the type of impedance synthesis commonly performed using a conventional Smith Chart CAD environment while providing an independent computational implementation.

## Möbius Transformations

The impedance transformations represented by the library can be expressed mathematically using Möbius transformations.

For a transmission line, the impedance mapping can be written in the general form

[
Z_{\mathrm{in}} =
Z_0
\frac{Z_L + jZ_0\tan(\beta l)}
{Z_0 + jZ_L\tan(\beta l)}.
]

This transformation maps the complex load impedance (Z_L) to the input impedance (Z_{\mathrm{in}}) and provides the mathematical basis for the impedance trajectories represented on the Smith Chart.

The Python implementation provides an independent computational representation of these transformations, allowing impedance states obtained through the mathematical formulation to be compared with those produced by conventional microwave CAD tools.

## Application to Microwave Matching Networks

The library was developed to support independent verification of matching-network synthesis.

In the associated research work, `smithchart_tool` was used to reproduce the impedance transformations of the input and output matching networks of a 500-W S-band GaN HEMT power amplifier.

The impedance states obtained through the Python implementation were compared with those synthesized using the Keysight ADS Smith Chart Utility. The agreement between the intermediate and final impedance states provides an independent verification of the matching-network transformations.

The implementation therefore provides a reproducible computational framework for analyzing matching networks without relying exclusively on a proprietary CAD environment.

## Examples

Example scripts are provided in the `examples/` directory:

```text
examples/
├── inputmatching.py
└── outputmatching.py
└── taper_approx.py
```

These scripts demonstrate the use of transmission lines, reactive elements, open stubs, and Smith Chart visualization for matching-network analysis.

## Reproducibility

This repository provides the computational implementation associated with the matching-network verification methodology presented in the corresponding research work.

The source code is publicly available at:

https://github.com/ZeroPole03/smithchart_tool

The repository is intended to support reproducibility and further development of computational tools for microwave impedance matching.

## Citation

If you use `smithchart_tool` in academic research, please cite the associated research work and software repository.

The repository includes a `CITATION.cff` file containing the recommended citation information and the author's ORCID.

**Author:** Alan Rodríguez Bojorjes
**ORCID:** https://orcid.org/0009-0002-3418-6299

## License

This project is distributed under the MIT License. See the `LICENSE` file for details.

## Author

**Alan Rodríguez Bojorjes**

Universidad Autónoma de San Luis Potosí
San Luis Potosí, Mexico

ORCID: https://orcid.org/0009-0002-3418-6299

GitHub: https://github.com/ZeroPole03
