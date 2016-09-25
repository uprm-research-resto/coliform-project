Coliform Project
=================
Python module for the UPRM BioMEMS Research Laboratory water quality project.
Written for Raspberry Pi(RPi) in Python 3.

Table of contents
=================
* [Coliform Project](#coliform-project)
  * [Table of contents](#table-of-contents)
  * [Installation](#installation)
  * [Requirements](#requirements)
  * [Usage](#usage)
    * [STDIN](#stdin)
    * [Local files](#local-files)
    * [Remote files](#remote-files)
    * [Multiple files](#multiple-files)
    * [Combo](#combo)
  * [Tests](#tests)
  * [Dependency](#dependency)

Installation
=================
In Raspberry Pi, or Linux Type the following into terminal:
```bash
sudo pip install Coliform
```
If you are running the code on Linux, Windows or Mac PC, for testing or other purposes, you need to run the following code in terminal, or CMD depending on your OS:
Linux/Mac:
```bash
sudo pip install Coliform
sudo pip install fakeRPiGPIO
```
Windows:
```bash
python -m pip install fakeRPiGPIO
python -m pip install Coliform
```
The reason is you need fakeRPiGPIO module in order to "emulate" the RPi.GPIO module of the Raspberry Pi.

Requirements
=================
