# PRE-INSTALLATION

Before you install `matrix-commander` with `pip install matrix-commander`
you *must* have followed these prerequisites steps! Otherwise `pip` will fail.

- Note that even if you install via `pip` you must have a) Python 3.8+
  and b) `libolm` installed.
- Run `python -V` to get your Python version number and assure that it is
  3.8+.
- For e2ee support, python-olm is needed which requires the libolm C
  library (version 3.x). See also https://gitlab.matrix.org/matrix-org/olm.
  Make sure that version 3 is installed. Version 2 will not work.
  To install `libolm` do this:
  - On Debian, Ubuntu and Debian/Ubuntu derivative distributions: `sudo apt install libolm-dev`
  - On Fedora or Fedora derivative distributions do: `sudo dnf install libolm-devel`
  - On MacOS use brew: `brew install libolm`

- For macOS Monterey 12.4 (21F79) (Apple M1 Pro) and similar please follow
  these steps for installation:

  - Install `libolm`, `dbus` and `libmagic` using Homebrew:
      - `brew install libolm dbus libmagic`
  - Install `matrix-commander` using this command:
      - `pip3 install --global-option=build_ext --global-option="-I/opt/homebrew/include/" --global-option="-L/opt/homebrew/lib/" matrix-commander`
  - For more details see Issue #79. Thanks to @KizzyCode for the contribution.

- For macOS x86_64 and similar please follow these steps for installation:

  - `brew install libolm dbus libmagic`
  - `pip3 install poetry`
  - `pip3 install --global-option=build_ext --global-option="-I/usr/local/include/" --global-option="-L/usr/local/lib/" matrix-commander`
  - Notice that the Link and Include directories between ARM (M1, etc.)
    and x86-64 are different.
    So, check for example where file `olm.h` is located on your hard disk.
    That gives you a hint which Include directory to use.
  - For more details see Issue #103. Thanks to @johannes87 for the contribution.

- Installing dependencies of `matrix-commander-tui`
  - `matrix-commander-tui` requires that you install `vipe` from the packge `moreutils`.
    - Read https://www.putorius.net/moreutils.html for installation instructions.
    - As an alternative you could also install `vipe.sh` from https://github.com/0mp/vipe.sh/blob/master/vipe.sh.
  - `matrix-commander-tui` requires that you install `fzf`.
    - Read https://github.com/junegunn/fzf#installation for installation instructions.
