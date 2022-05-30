# PRE-INSTALLATION

Before you install `matrix-commander` with `pip install matrix-commander`
you *must* have `libolm` installed. `pip` installation will fail otherwise!

For e2ee support, python-olm is needed which requires the
[libolm](https://gitlab.matrix.org/matrix-org/olm) C library (version 3.x).

- On Debian, Ubuntu and Debian or Ubuntu derivate distributions do `sudo apt install libolm-dev` to install the `libolm` package.
- On Fedora or Fedora derivate distributions do `sudo dnf install libolm-devel` to install the `libolm` package.
- On MacOS one can use [brew](https://brew.sh/) to install package `libolm`.

Make sure that version 3 is installed. Version 2 will not work.
