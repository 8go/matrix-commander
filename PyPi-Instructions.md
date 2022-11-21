# PRE-INSTALLATION

Before you install `matrix-commander` with `pip install matrix-commander`
you *must* have `libolm` installed. `pip` installation will fail otherwise!

For e2ee support, python-olm is needed which requires the
[libolm](https://gitlab.matrix.org/matrix-org/olm) C library (version 3.x).

- On Debian, Ubuntu and Debian or Ubuntu derivate distributions do `sudo apt install libolm-dev` to install the `libolm` package.
- On Fedora or Fedora derivate distributions do `sudo dnf install libolm-devel` to install the `libolm` package.
- On MacOS one can use [brew](https://brew.sh/) to install package `libolm`.

Make sure that version 3 is installed. Version 2 will not work.

For macOS Monterey 12.4 (21F79) (Apple M1 Pro) and similar please follow
the these steps:
- Install `libolm`, `dbus` and `libmagic` using Homebrew
- Install `matrix-commander` using this command:
  - `pip3 install --global-option=build_ext --global-option="-I/opt/homebrew/include/" --global-option="-L/opt/homebrew/lib/" matrix-commander`
- For more details see Issue #79. Thanks to @KizzyCode for the contribution.

On macOS x86_64, do these steps for installation:
- `brew install libolm dbus libmagic`
- `pip3 install poetry`
- `pip3 install --global-option=build_ext --global-option="-I/usr/local/include/" --global-option="-L/usr/local/lib/" matrix-commander`
- Notice that the Link and Include directories between ARM (M1, etc.) and x86-64 are different.
  So, check for example where file `olm.h` is located on your hard disk. That gives you a hind which Include directory to use.
- For more details see Issue #103. Thanks to @johannes87 for the contribution.
