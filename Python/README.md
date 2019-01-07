# IC Scanner in Python

Similarly to PHP and C++ version, this version is developed in Python.

## Prerequisite
1. Python 2.X or 3.X
2. [Pyscard package](https://pypi.org/project/pyscard/)
  1. [Swigwin](http://www.swig.org/download.html)
  2. If Python 2.7: [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)

## Python
Download [Python](https://www.python.org/downloads/windows/) and install normally.
Set the environment path so that command **'pip'** can be used to install packages.

Before installing pyscard, **swigwin** is required to be download and set in environment
to run **swig.exe**. And if you're using Python 2.7, **Microsoft Visual C++ Compiler
for Python 2.7** is required to install the packages properly.

Afterward, run **"pip install pyscard"** and wait for installation.

In the script, add the following to import the package to start using its call:

`from smartcard.System import readers`<br>
`from smartcard.util import toHexString`

**Important call**
1. `readers()` - find all available readers
2. `createConnection()` - initialise pc-smart reader communication
3. `transmit(param)` - send a message to the reader which return data, sw1, sw2
4. `disconnect()` - disconnect reader properly

Since this package is based on C++, it work similarly to C++ and PHP implementation.
Likewise, it will be using TLV (Tag-Length-Value) to send and receive data - refer
to previous instruction.

**A python version source is attached as example.**
