# PRE-INSTALLATION

Before you install `matrix-commander` with `pip3 --install matrix-commander`
you *must* have `libolm` installed. `pip3` installation will fail otherwise!

For e2ee
support, python-olm is needed which requires the
[libolm](https://gitlab.matrix.org/matrix-org/olm) C library (version 3.x).
On Debian and Ubuntu one can use `apt-get` to install package `libolm-dev`.
On Fedora one can use `dnf` to install package `libolm-devel`.
On MacOS one can use [brew](https://brew.sh/) to install package `libolm`.
Make sure version 3 is installed.
