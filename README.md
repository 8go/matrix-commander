[![PyPI - Python Version](
https://img.shields.io/pypi/pyversions/matrix-commander?color=red)](
https://www.python.org/)
[![Built with matrix-nio](
https://img.shields.io/badge/built%20with-matrix--nio-darkgreen)](
https://github.com/poljar/matrix-nio)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](
https://github.com/psf/black)
[![Docker Pulls](https://img.shields.io/docker/pulls/matrixcommander/matrix-commander)](
https://hub.docker.com/r/matrixcommander/matrix-commander/)
[![PyPI - Version](https://img.shields.io/pypi/v/matrix-commander?color=darkblue)](
https://pypi.org/project/matrix-commander)
[![PyPI - Downloads](
https://img.shields.io/pypi/dm/matrix-commander?color=darkblue&label=PyPi%20Downloads
)](https://pypi.org/project/matrix-commander)
[![Nix: package](https://img.shields.io/badge/Nix-package-6fa8dc.svg)](
https://search.nixos.org/packages?query=matrix-commander)

<p>
<img
src="https://raw.githubusercontent.com/8go/matrix-commander/master/logos/mc.svg"
alt="MC> logo" height="150">

<p>
<a href="https://matrix.org/docs/projects/client/matrix-commander">
<img src="https://matrix.org/docs/projects/images/made-for-matrix.png"
alt="made for Matrix" height="100"></a>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://pypi.org/project/matrix-commander/">
<img src="https://pypi.org/static/images/logo-large.6bdbb439.svg"
alt="get it on PyPi" height="100"></a>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://hub.docker.com/r/matrixcommander/matrix-commander">
<img src="https://www.unixtutorial.org/images/software/docker-hub.png"
alt="get it on Docker Hub" height="100"></a>
</p>

# :loudspeaker: :new: :boom: Latest News! :fire: :mega: :tada:

- `matrix-commander` now available on
  [Docker Hub](https://hub.docker.com/r/matrixcommander/matrix-commander)
  and hence easy to install as docker image (:clap: to @pataquets for his PR).
  Install via `docker pull matrixcommander/matrix-commander`.
- `matrix-commander` now available on
  [PyPi](https://pypi.org/project/matrix-commander/)
  and hence easy to install via `pip install matrix-commander`
- available as reproducible
  [Nix package](https://search.nixos.org/packages?query=matrix-commander)
  for NixOS, Debian, Fedora, etc.
- `matrix-commander` is now callable from a Python program as well.
  See [tests/test-send.py](
  https://github.com/8go/matrix-commander/blob/master/tests/test-send.py)
  for an example on how to do that.
- incompatibility: login (authentication) must now be done explicitly
  with `--login` on the first run of `matrix-commander`
- new option: `--login`, supports login methods `password` and `sso`
- new option: `--logout` to remove device and access-token validity
- new option: `--sync` to allow skipping sync when only sending
- new option: `--output` to produce output in different formats (text, JSON)
- new option: `--get-room-info` to get room info such as the
  room display name, room alias, etc. for a given room id
- new option: `--get-client-info` to get client info
- new option: `--verbose` to specify debugging verbosity
- announcing `matrix-commander-rs` :crab:, `matrix-commander` but in Rust.
  See [matrix-commander-rs](https://github.com/8go/matrix-commander-rs).
  Please :star: it if you like the idea. Please contribute if you can,
  please :pray: write some code to make this vision happen. Thank you!
  :heart:

# Summary, TLDR

This simple Matrix client written in Python allows you to send and
receive messages and files, verify other devices, and interact with
your Matrix account or other Matrix users in many ways.
You use it from the terminal (CLI) or integrate it into other simple
Python programs. Enjoy and please :star: star on Github.

# matrix-commander

Simple but convenient CLI-based Matrix client app for sending, receiving,
creating rooms, inviting, verifying, and so much more.

- `matrix-commander` is a simple command-line [Matrix](https://matrix.org/)
  client.
- It is a simple but convenient app to
    - send Matrix text messages as well as text, image, audio, video or
      other arbitrary files
    - listen to and receive Matrix messages, images, audio, video, etc.
    - download media files like images or audio
    - perform Matrix emoji verification
    - performs actions of rooms (create rooms, invite to rooms, etc.)
    - list rooms and room members
    - and much more
- It exclusively offers a command-line interface (CLI).
- Hence the word-play: matrix-command(lin)er
- There is no GUI and there are no windows (except for pop-up windows in
  OS notification)
- It uses the [matrix-nio](https://github.com/poljar/matrix-nio/) SDK
- Both `matrix-nio` and `matrix-commander` are written in Python 3
- Convenient to install via `pip`.

# What for? Why? For whom? Use cases?

Use cases for this program could be
- a bot or part of a bot,
- to automate sending via programs and scripts
- `matrix-nio show case`: as educational material that showcases the use
  of the `matrix-nio` SDK
- `alerter`: to send all sorts of alerts,
- `Gitlab CI automation tool`: some user uses it as Gitlab CI automation tool
   to report build success/failure to their internal Matrix room.
   See [Issue #81](https://github.com/8go/matrix-commander/issues/81).
- `admin tool` or `automation tool`: you needs to create 175 room for the
   roll-out within a company? You want to query some 9000 rooms for
   visibility data? You want to collect profile data of 7000 enterprise or
   public users? `matrix-commander` has many admin capabilities and can
   automate many tasks completely. Many admin jobs can be reduced to running
   a simple bash script or a simple Python program using `matrix-commander`.
- `reminder`: send yourself or others daily/weekly reminders via a cron job.
- `surf report`: an addict surfer uses `matrix-commander` combined with a
   `cron` job to publish daily early morning surf reports for his 3 favorite
   surfing spots to his Element app.
- `juke box`: a user told me he has a large collection of mp3 files on his
  server. He uses `matrix-commander` to send himself a random song from
  his music collection to brighten his day.
- `ticker`: many people send themselves stock prices from one of the many
  public ticker APIs. This is usually a single `curl` command piped into
  `matrix-commander`.
- `poor-man's Matrix client`: if you love the terminal and are too lazy to
   start up an Element desktop app or an Element webpage,
   `matrix-commander` is a a trivial way to fire off some instant
   messages to your friends from the terminal.
- `poor-man's importer or exporter`: you want to get things in and out of
   Matrix?
   Send those 39 holiday picture you have laying around in a holiday folder?
   Or, your best friend just sent you 57 wedding pictures on Element and
   you want to store them? `matrix-commander` can help with importing and
   exporting data.
- `poor man's blogger`: a "blogger" who frequently sends messages and
  images to the same public room(s) could use `matrix-commander` to keep
  his audience informed.
- `poor man's diary`: a person could write a diary or run a gratitude
  journal by sending messages to her/his own diary room or gratitude room.
- `ghost`: `matrix-commander` can be used in an ephemeral fashion, in a
  fire-and-forget style. A single batch command can log in, create a
  new device, send a message, and then log out and delete the device.

# Give it a Star

If you like it, use it, fork it, make a Pull Request or contribute.
Please give it a :star: on Github right now so others find it more easily.
:heart:


# Features

- CLI, Command Line Interface
- Python 3
- Simplicity
- Small footprint, small application (only around 250K)
- Uses `nio-template`
- End-to-end encryption
- Storage for End-to-end encryption
- Storage of credentials
- Supports access token instead of password
- Supports SSO (Single Sign-On)
- Sending messages
- Sending notices
- Sending formatted messages
- Sending MarkDown messages
- Message splitting before sending
- Sending Code-formatted messages
- Sending to one room
- Sending to multiple rooms
- Sending image files (photos, etc.)
- Sending of media files (music, videos, etc.)
- Sending of arbitrary files (PDF, xls, doc, txt, etc.)
- Sending events such as emoji reactions, or replies as threads
- Using events to edit sent messages
- Supports creating private DM rooms (thanks to PR from @murlock1000)
- Supports DM (direct messaging), sending DMs, listening for DMs
- Listing of joined rooms
- Listing of members of given room(s)
- Receiving messages forever
- Receiving messages once
- Receiving last messages
- Receiving or skipping its own messages
- Receiving and downloading media files
  - including automatic decryption
- Creating new rooms
- Joining rooms
- Leaving rooms
- Forgetting rooms
- Inviting other users to rooms
- Banning from rooms
- Unbanning from rooms
- Kicking from rooms
- Supports renaming of device
- Supports getting and setting display name
- Supports getting and setting presence
- Uploading, downloading, and deleting to/from resource depository
- Listing your devices
- Listing discovery info
- Listing available login methods supported by server
- Supports skipping SSL verification to use HTTP instead of HTTPS
- Supports providing local SSL certificate files
- Supports notification via OS of received messages
- Supports periodic execution via crontab
- Supports room aliases
- Supports multiple output formats like `text` (for human consumption)
  and `json` (for machine consumption and further processing)
- Provides PID files
- Logging (at various levels)
- In-source documentation
- Can be run as a service
- Smart tab completion for shells like bash (thanks to PR from @mizlan :clap:)
- More than 200 stars :stars: on Github
- Easy installation, available through `pip`, i.e. available in
  [PyPi](https://pypi.org/project/matrix-commander/) store
- Easy installation, available as docker image on
  [Docker Hub](https://hub.docker.com/r/matrixcommander/matrix-commander)
  (thanks to PR from @pataquets :clap:)
- Easy installation, available in Nix repository as reproducible
  [Nix package](https://search.nixos.org/packages?query=matrix-commander)
- Callable from the terminal, from shells like `bash`, etc.
- Callable from Python programs via the entry point (function) `main`.
- Open source
- Free, GPL3+ license

# First Run, Set Up, Credentials File, End-to-end Encryption

On the first run `matrix-commander` must be executed with the
`--login` argument and the corresponding secondary arguments.
This creates a credentials.json file.
The credentials.json file stores: homeserver, user id,
access token, device id, and default room id. On the first run,
the --login run, it asks some questions if not everything is
provided by arguments, creates the token and device id
and stores everything in the credentials.json file. If desired,
all arguments can be provided via arguments to that log in can
be performed fully in batch.

Since the credentials file holds an access token it
should be protected and secured. One can use different
credential files for different users or different rooms.

On creation the credentials file will always be created in the local
directory, so the users sees it right away. This is fine if you have
only one or a few credential files, but for better maintainability
it is suggested to place your credentials files into directory
$HOME/.config/matrix-commander/. When the program looks for
a credentials file it will first look in local directory and then
as secondary choice it will look in directory
$HOME/.config/matrix-commander/.

If you want to re-use an existing device id and an existing
access token, you can do so as well, just manually edit the
credentials file. However, for end-to-end encryption this will
NOT work.

End-to-end encryption (e2ee) is enabled by default. It cannot be turned off.
Wherever possible end-to-end encryption will be used. For e2ee to work
efficiently a `store` directory is needed to store e2ee data persistently.
The default location for the store directory is a local directory named
`store`. Alternatively, as a secondary choice the program looks for a store
directory in $HOME/.local/shared/matrix-commander/store/. The user can always
specify a different location via the --store argument. If needed the `store`
directory will be created on the first run.

From the second time the program is run, and on all
future runs it will use the homeserver, user id
and access token found in the credentials file to log
into the Matrix account. Now this program can be used
to easily send simple text messages, images, and so forth
to the just configured room.

# Verification

As second step after the `--login`, it is recommended to perform an
emoji verification by running `--verify`. Verification is always
interactive, bacause the emojis need to be confirmed via the keyboard.
If desired `--login` and `--verify` can be done in the same first run.
The program can accept verification request and verify other devices
via emojis. See `--verify` in help for more details.

# Room Operations, Actions on Rooms

The program can create rooms, join, leave and forget rooms.
It can also send invitations to join rooms to
others (given that user has the appropriate permissions) as
well as ban, unban and kick other users from rooms.

# Sending

Messages to send can be provided
1) in the command line (-m or --message)
2) as input from the keyboard (if there is no other input or command)
3) through a pipe from stdin (|), i.e. piped in from another program.

For sending messages the program supports various text formats:
1) text: default
2) html:  HTML formatted text
3) markdown: MarkDown formatted text
4) code: used a block of fixed-sized font, ideal for ASCII art or
   tables, bash outputs, etc.
5) notification
6) split: splits messages into multiple units at given pattern

Photos and images that can be sent. That includes files like
.jpg, .gif, .png or .svg.

Arbitrary files like .txt, .pdf, .doc, audio files like .mp3
or video files like .mp4 can also be sent.

Matrix events like sending an emoji reaction, replying as a thread,
message edits can be sent.

# Listening, Receiving

One can listen to one or multiple rooms. Received messages will be displayed
on the screen. If desired, optionally, you can be notified of incoming
messages through the operating system standard notification system, usually a
small pop-up window.

Messages can be received or listened to various ways:
1) Forever: the program runs forever, listens forever, and prints all
   messages as they arrive in real-time.
2) Once: the program prints all the messages that are waiting in the queue,
   i.e. all messages that have been sent in, and after printing them the
   program terminates.
3) Tail: prints the last N read or unread messages of one or multiple
   specified rooms and after printing them the program terminates.

When listening to messages you can also choose to download and decrypt
media. Say, someone is sending a song. The mp3 file can be downloaded
and automatically decrypted for you.

# Dependencies and Installation

- If you install via `pip`, then `pip` will take care of most of the
  dependencies.
  - See https://pypi.org/project/matrix-commander
  - Usually `pip install matrix-commander` will do the trick.
  - Note that even if you install via `pip` you must have a) Python 3.8+
    and b) `libolm` installed. See `PyPi-Instructions.md`.

- For macOS Monterey 12.4 (21F79) (Apple M1 Pro) and similar please follow
  the these steps for installation:

    - Install `libolm`, `dbus` and `libmagic` using Homebrew
    - Install `matrix-commander` using this command:
        - `pip3 install --global-option=build_ext --global-option="-I/opt/homebrew/include/" --global-option="-L/opt/homebrew/lib/" matrix-commander`
    - For more details see Issue #79. Thanks to @KizzyCode for the contribution.

- On macOS x86_64, follow these steps for installation:

    - `brew install libolm dbus libmagic`
    - `pip3 install poetry`
    - `pip3 install --global-option=build_ext --global-option="-I/usr/local/include/" --global-option="-L/usr/local/lib/" matrix-commander`
    - Notice that the Link and Include directories between ARM (M1, etc.) and x86-64 are different.
      So, check for example where file `olm.h` is located on your hard disk. That gives you a hind which Include directory to use.
    - For more details see Issue #103. Thanks to @@johannes87 for the contribution.

- If you install a docker image: `matrix-commander` is available on
  [Docker Hub](https://hub.docker.com/r/matrixcommander/matrix-commander)
  and hence easy to install as docker image (:clap: to @pataquets for his PR).
  Install via `docker pull matrixcommander/matrix-commander`.

- If you install it via `git` or via file download then these are the
  dependencies that you must take care of:

    - Python 3.8 or higher installed (3.7 will NOT work)
    - libolm-dev must be installed as it is required by matrix-nio
      - libolm-dev on Debian/Ubuntu, libolm-devel on Fedora, libolm on MacOS
    - matrix-nio must be installed, see https://github.com/poljar/matrix-nio
      - pip3 install --user --upgrade matrix-nio[e2e]
    - python3 package markdown must be installed to support MarkDown format
      - pip3 install --user --upgrade markdown
    - python3 package python_magic must be installed to support image sending
      - pip3 install --user --upgrade python_magic
    - if (and only if) you want OS notification support, then the python3
      package notify2 and dbus-python should be installed
      - pip3 install --user --upgrade dbus-python # optional
      - pip3 install --user --upgrade notify2 # optional
    - python3 package urllib must be installed to support media download
      - pip3 install --user --upgrade urllib
    - python3 package pyxdg must be installed to support `XDG_*` env vars.
      Be careful. Multiple packages install in the same directory `xdg` and
      overwrite each other. These packages can be conflicting. Specifically,
      packages `pyxdg` and `xdg` collide. If you already have `xdg` installed
      you cannot just simply install `pyxdg`; in this case you should opt
      for a separate Python environment.
      - pip3 install --user --upgrade pyxdg
    - `matrix_commander/matrix_commander.py` file must be installed, and should
      have execution permissions
      - chmod 755 matrix_commander.py
    - `matrix_commander/matrix-commander` file is recommended for the install,
      and should have execution permissions
      - chmod 755 matrix-commander
    - for a full list or requirements look at the `requirements.txt` file
      - run `pip install -r requirements.txt` to automatically install
        all required Python packages
      - if you e.g. run on a headless server and don't want dbus-python and
        notify2, please remove the corresponding 2 lines from
        the `requirements.txt` file

# Examples of calling `matrix-commander`

- Alternative 1: Usually `matrix-commander` is called from a terminal
  inside a shell like `bash`, `sh`, `zsh`, your Windows CMD terminal
  or similar. You will find plenty of examples how to use it within
  a terminal just a few lines down.
- Alternative 2: Sometimes, however, it might be more convenient to call
  `matrix-commander` from within a Python program. This is also possible.
  Import the Python module `matrix_commander` and use the provided
  entry point `main`. An example of how this can be done can be found
  in [tests/test-send.py](
  https://github.com/8go/matrix-commander/blob/master/tests/test-send.py).

```
$ matrix-commander --login password # first run; will configure everything
$ matrix-commander --login sso # alternative first run with Single Sign-On;
$   # this will configure everything on a headless server w/o a browser
$ # this created a credentials.json file, and a store directory.
$ # optionally, if you want you can move credentials to app config directory
$ mkdir $HOME/.config/matrix-commander # optional
$ mv -i credentials.json $HOME/.config/matrix-commander/
$ # optionally, if you want you can move store to the app share directory
$ mkdir $HOME/.local/share/matrix-commander # optional
$ mv -i store $HOME/.local/share/matrix-commander/
$ # Now you are ready to run program for a second time
$ # Let us verify the device/room to where we want to send messages
$ # The other device will issue a "verify by emoji" request
$ matrix-commander --verify
$ # Now program is both configured and verified, let us send the first message
$ matrix-commander -m "First message!"
$ matrix-commander --debug -m "First message!" # turn debugging on
$ # turn debugging on also for submodules
$ matrix-commander --debug --debug -m "First message!"
$ # turn debugging on, high verbosity
$ matrix-commander --debug --verbose -m "First message!"
$ # turn debugging on, very high verbosity
$ matrix-commander --debug --verbose --verbose -m "First message!"
$ # maximum debugging info
$ matrix-commander --debug --debug --verbose --verbose -m "First message!"
$ matrix-commander --help # print help
$ matrix-commander # this will ask user for message to send
$ matrix-commander --message "Hello World!" # sends provided message
$ echo "Hello World" | matrix-commander # pipe input msg into program
$ matrix-commander -m msg1 -m msg2 # sends 2 messages
$ matrix-commander -m msg1 msg2 msg3 # sends 3 messages
$ df -h | matrix-commander --code # formatting for code/tables
$ matrix-commander -m "<b>BOLD</b> and <i>ITALIC</i>" --html
$ matrix-commander -m "- bullet1" --markdown
$ # take input from an RSS feed and split large RSS entries into multiple
$ # Matrix messages wherever the pattern "\n\n\n" is found
$ rssfeed | matrix-commander --split "\n\n\n"
$ matrix-commander --credentials usr1room2.json # select credentials file
$ matrix-commander --store /var/storage/ # select store directory
$ # Send to a specific room
$ matrix-commander -m "hi" --room '!YourRoomId:example.org'
$ # some shells require the ! of the room id to be escaped with \
$ matrix-commander -m "hi" --room "\!YourRoomId:example.org"
$ # Send to multiple rooms
$ matrix-commander -m "hi" -r '!r1:example.org' '!r2:example.org'
$ # Send to multiple rooms, another way
$ matrix-commander -m "hi" -r '!r1:example.org' -r '!r2:example.org'
$ # Send to a specific user, DM, direct messaging, using full user id
$ matrix-commander -m "hi" --user '@MyFriend:example.org'
$ # Send to a specific user, DM, direct messaging, using partial user id
$ # It will be assumed that user @MyFriend is on same homeserver
$ matrix-commander -m "hi" --user '@MyFriend'
$ # Send to a specific user, DM, direct messaging, using display name
$ # Careful! Display names might not be unique. Don't DM the wrong person!
$ # To double-check the display names do a --joined-members "*"
$ matrix-commander -m "hi" -u 'Joe'
$ # Send to multiple users
$ matrix-commander -m "hi" -u '@Joe:example.org' '@Jane:example.org'
$ # Send to multiple users, another way
$ matrix-commander -m "hi" -u '@Joe:example.org' -u '@Jane:example.org'
$ # send 2 images and 1 text, text will be sent last
$ matrix-commander -i photo1.jpg photo2.img -m "Do you like my 2 photos?"
$ # send 1 image and no text
$ matrix-commander -i photo1.jpg
$ # pipe 1 image and no text
$ cat image1.jpg | matrix-commander -i -
$ # send 1 audio and 1 text to 2 rooms
$ matrix-commander -a song.mp3 -m "Do you like this song?" \
    -r '!someroom1:example.com' '!someroom2:example.com'
$ # send 2 audios, 1 via stdin pipe
$ audio-generator | matrix-commander -a intro.mp3 -
$ # send a .pdf file and a video with a text
$ matrix-commander -f example.pdf video.mp4 -m "Here are the promised files"
$ # send a .pdf file via stdin pipe
$ pdf-generator | matrix-commander -f -
$ # listen forever, get msgs in real-time and notify me via OS
$ matrix-commander --listen forever --os-notify
$ # listen forever, and show me also my own messages
$ matrix-commander --listen forever --listen-self
$ # listen once, get any new messages and quit
$ matrix-commander --listen once --listen-self
$ matrix-commander --listen once --listen-self | process-in-other-app
$ # listen to tail, get the last N messages and quit
$ matrix-commander --listen tail --tail 10 --listen-self
$ # listen to tail, another way of specifying it
$ matrix-commander --tail 10 --listen-self | process-in-other-app
$ # get the very last message
$ matrix-commander --tail 1 --listen-self
$ # listen to (get) all messages, old and new, and process them in another app
$ matrix-commander --listen all | process-in-other-app
$ # listen to (get) all messages, including own
$ matrix-commander --listen all --listen-self
$ # set, rename device-name, sometimes also called device display-name
$ matrix-commander --set-device-name "my new device name"
$ # set, rename display name for authenticated user
$ matrix-commander --set-display-name "Alex"
$ # get display name for authenticated user, for itself
$ matrix-commander --get-display-name
$ # get display name for other users
$ matrix-commander --get-display-name  \
    --user '@user1:example.com' '@user2:example.com'
$ # list all the rooms that I am a member of, all joined rooms
$ matrix-commander --joined-rooms
$ # list all the members of 2 specific rooms
$ matrix-commander --joined-members '!someroomId1:example.com' \
    '!someroomId2:example.com'
$ # list all the members of all rooms  that I am member of
$ matrix-commander --joined-members '*'
$ # set presence
$ matrix-commander --set-presence "unavailable"
$ # get presence of matrix-commander itself
$ matrix-commander --get-presence
$ # get presence of other users
$ matrix-commander --get-presence \
    --user '@user1:example.com' '@user2:example.com'
$ # upload file to resource repository
$ matrix-commander --upload "avatar.png"
$ # download file from resource repository via URI (MXC)
$ matrix-commander --download "mxc://example.com/SomeStrangeUriKey"
$ matrix-commander --delete-mxc mxc://... # delete image from database
$ matrix-commander --delete-mxc-before '20.01.2022 19:38:42' 1024000
$ # for more examples of --upload, --download, --delete-mxc,
$ # --delete-mxc-before, --mxc-to-http, see file tests/test-upload.sh
$ matrix-commander  --rest GET "" '__homeserver__/_matrix/client/versions'
$ # for more examples of --rest see file tests/test-rest.sh
$ matrix-commander --get-avatar # get its own avatar MXC URI
$ # get avatar MXC URIs of other users
$ matrix-commander --get-avatar '@user1:example.com' '@user2:example.com'
$ matrix-commander --set-avatar mxc://... # set its own avatar MXC URI
$ # for more examples of --set_avatar see tests/test-setget.sh
$ matrix-commander --get-profile # get its own user profile
$ matrix-commander --get-profile '@user1:example.com' '@user2:example.com'
$ matrix-commander --get-room-info # get its default room info
$ matrix-commander --get-room-info '\!room1:example.com' \
    '\!room2:example.com' # get room info for multiple rooms
$ # map from room id to room alias
$ matrix-commander --get-room-info '\!roomId1:example.com'
$ # map from room alias to room id
$ matrix-commander --get-room-info '#roomAlias1:example.com'
$ matrix-commander --get-client-info # get client info
$ matrix-commander --has-permission '!someroomId1:example.com' 'ban'
$ matrix-commander --export-keys mykeys "my passphrase" # export keys
$ matrix-commander --import-keys mykeys "my passphrase" # import keys
$ matrix-commander --get-openid-token # get its own OpenId token
$ # get OpenID tokens for other users
$ matrix-commander --get-openid-token '@user1:example.com' '@user2:example.com'
$ matrix-commander --room-get-visibility # get default room visibility
$ matrix-commander --room-get-visibility \
    '\!someroomId1:example.com' '\!someroomId2:example.com'
$ matrix-commander --room-set-alias '#someRoomAlias:matrix.example.org'
$ matrix-commander --room-set-alias 'someRoomAlias' \
    '\!someroomId1:example.com'
$ matrix-commander --room-resolve-alias '#someRoomAlias:matrix.example.org'
$ matrix-commander --room-resolve-alias '#someRoomAlias1:matrix.example.org' \
    'someRoomAlias2'
$ matrix-commander --room-delete-alias '#someRoomAlias:matrix.example.org'
$ matrix-commander --room-delete-alias '#someRoomAlias1:matrix.example.org' \
    'someRoomAlias2'
$ matrix-commander --room-get-state # get state of default room
$ matrix-commander --room-get-state \
    '\!someroomId1:example.com' '\!someroomId2:example.com'
$ matrix-commander --delete-device "QBUAZIFURK" --password 'mc-password'
$ matrix-commander --delete-device "QBUAZIFURK" "AUIECTSRND" \
    --user '@user1:example.com' --password 'user1-password'
$ # delete a message with event id 'someEventId'
# matrix-commander --room-redact '!someroomId1:example.com' 'someEventId'
$ # delete 2 images from 2 rooms
$ matrix-commander --room-redact \
    '\!someroomId1:example.com' '\$someEventId1' 'Image deleted, obsolete info'
    '\!someroomId2:example.com' '\$someEventId2' 'Image deleted, outdated'
$ # print its own user id
$ matrix-commander --whoami
$ # skip SSL certificate verification for a homeserver without SSL
$ matrix-commander --no-ssl -m "also working without Let's Encrypt SSL"
$ # use your own SSL certificate for a homeserver with SSL and local certs
$ matrix-commander --ssl-certificate mycert.crt -m "using my own cert"
$ # download and decrypt media files like images, audio, PDF, etc.
$ # and store downloaded files in directory "mymedia"
$ matrix-commander --listen forever --listen-self --download-media mymedia
$ # create rooms without name and topic, just with alias, use a simple alias
$ matrix-commander --room-create roomAlias1
$ # don't use a well formed alias like '#roomAlias1:example.com' as it will
$ # confuse the server!
$ # BAD: matrix-commander --room-create roomAlias1 '#roomAlias1:example.com'
$ matrix-commander --room-create roomAlias2
$ # create rooms with name and topic
$ matrix-commander --room-create roomAlias3 --name 'Fancy Room' \
    --topic 'All about Matrix'
$ matrix-commander --room-create roomAlias4 roomAlias5 \
    --name 'Fancy Room 4' -name 'Cute Room 5' \
    --topic 'All about Matrix 4' 'All about Nio 5'
$ # create DM rooms with user.
$ matrix-commander --room-dm-create '@user1:example.com'
$ # create DM rooms with name, topic, alias
$ matrix-commander --room-dm-create '@user1:example.com' '@user2:example.com' \
    --name 'Fancy DM room 4' -name 'Cute DM room 4' \
    --topic 'All about Matrix 4' 'All about Nio 5' \
    --alias roomAlias1 '#roomAlias2:example.com'
$ # join rooms
$ matrix-commander --room-join '!someroomId1:example.com' \
    '!someroomId2:example.com' '#roomAlias1:example.com'
$ # leave rooms
$ matrix-commander --room-leave '#roomAlias1:example.com' \
    '!someroomId2:example.com'
$ # forget rooms, you have to first leave a room before you forget it
$ matrix-commander --room-forget '#roomAlias1:example.com'
$ # invite users to rooms
$ matrix-commander --room-invite '#roomAlias1:example.com' \
    --user '@user1:example.com' '@user2:example.com'
$ # ban users from rooms
$ matrix-commander --room-ban '!someroom1:example.com' \
    '!someroom2:example.com' \
    --user '@user1:example.com' '@user2:example.com'
$ # unban users from rooms, remember after unbanning you have to invite again
$ matrix-commander --room-unban '!someroom1:example.com' \
    '!someroom2:example.com' \
    --user '@user1:example.com' '@user2:example.com'
$ # kick users from rooms
$ matrix-commander --room-kick '!someroom1:example.com' \
    '#roomAlias2:example.com' \
    --user '@user1:example.com' '@user2:example.com'
$ # set log levels, INFO for matrix-commander and ERROR for modules below
$ matrix-commander -m "test" --log-level INFO ERROR
$ # example of how to quote text correctly, e.g. JSON text
$ matrix-commander -m '{title: "hello", message: "here it is"}'
$ matrix-commander -m "{title: \"hello\", message: \"here it is\"}"
$ matrix-commander -m "{title: \"${TITLE}\", message: \"${MSG}\"}"
$ matrix-commander -m "Don't do this"
$ matrix-commander -m 'He said "No" to me.'
$ matrix-commander --separator " || " # customize column separator in outputs
$ matrix-commander --mxc-to-http mxc://example.com/abc... # get HTTP
$ matrix-commander --devices # to list devices of matrix-commander
$ matrix-commander --discovery-info # print discovery info of homeserver
$ matrix-commander --login-info # list login methods
$ matrix-commander --content-repository-config # list config of content repo
$ matrix-commander --sync off -m Test -i image.svg # a faster send
$ matrix-commander --joined-rooms --output json | jq # get json output in JSON
$ matrix-commander --joined-rooms --output json-max | jq # full details
$ matrix-commander --tail 10 --output json-spec | jq # as specification
$ matrix-commander --joined-rooms --output text # get human-readable output
$ # example of how to use stdin, how to pipe data into the program
$ echo "Some text" | matrix-commander # send a text msg via pipe
$ echo "Some text" | matrix-commander -m - # long form to send text via pipe
$ matrix-commander -m "\-" # send the literal minus sign as a text msg
$ cat image1.png | matrix-commander -i - # send an image via pipe
$ matrix-commander -i - < image1.png # send an image via pipe
$ cat image1.png | matrix-commander -i - -m "text" # send image and text
$ # send 3 images out of which the second will be read from stdin via pipe
$ cat im2.png | matrix-commander -i im1.jpg - im3.jpg # send 3 images
$ echo "text" | matrix-commander -i im1.png # first image, then piped text
$ echo "text" | matrix-commander -i im1.png -m - # same, long version
$ pdf-generator | matrix-commander -f - -m "Here is my PDF file."
$ audio-generator | matrix-commander -a - -m "Like this song?"
$ echo "junk" | matrix-commander -i - -m - # this will fail, not allowed
$ # remember, pipe or stdin, i.e. the "-" can be used at most once
$ cat im.png | matrix-commander -i im1.png - im3.png - im5.png # will fail
$ # sending an event: e.g. reacting with an emoji
$ JSON_REACT_MSC2677='{ "type": "m.reaction",
    "content": { "m.relates_to": { "rel_type": "m.annotation",
    "event_id": "%s", "key": "%s" } } }'
$ TARGET_EVENT="\$...a.valid.event.id" # event to which to react
$ REACT_EMOJI="😀" # how to react
$ printf "$JSON_REACT_MSC2677" "$TARGET_EVENT" "$REACT_EMOJI" |
    matrix-commander --event -
$ # for more examples of "matrix-commander --event" see tests/test-event.sh
```

# Usage
```
usage: matrix_commander.py [-h] [-d] [--log-level LOG_LEVEL [LOG_LEVEL ...]]
                           [--verbose] [--login LOGIN] [-v [VERIFY]]
                           [--logout LOGOUT] [-c CREDENTIALS] [-s STORE]
                           [-r ROOM [ROOM ...]] [--room-default ROOM_DEFAULT]
                           [--room-create ROOM_CREATE [ROOM_CREATE ...]]
                           [--room-dm-create ROOM_DM_CREATE [ROOM_DM_CREATE ...]]
                           [--room-join ROOM_JOIN [ROOM_JOIN ...]]
                           [--room-leave ROOM_LEAVE [ROOM_LEAVE ...]]
                           [--room-forget ROOM_FORGET [ROOM_FORGET ...]]
                           [--room-invite ROOM_INVITE [ROOM_INVITE ...]]
                           [--room-ban ROOM_BAN [ROOM_BAN ...]]
                           [--room-unban ROOM_UNBAN [ROOM_UNBAN ...]]
                           [--room-kick ROOM_KICK [ROOM_KICK ...]]
                           [-u USER [USER ...]] [--user-login USER_LOGIN]
                           [--name NAME [NAME ...]]
                           [--topic TOPIC [TOPIC ...]]
                           [--alias ALIAS [ALIAS ...]]
                           [-m MESSAGE [MESSAGE ...]] [-i IMAGE [IMAGE ...]]
                           [-a AUDIO [AUDIO ...]] [-f FILE [FILE ...]]
                           [-e EVENT [EVENT ...]] [-w] [-z] [-k] [-p SPLIT]
                           [--config CONFIG] [--proxy PROXY] [-n]
                           [--encrypted] [-l [LISTEN]] [-t [TAIL]] [-y]
                           [--print-event-id]
                           [--download-media [DOWNLOAD_MEDIA]] [-o]
                           [--set-device-name SET_DEVICE_NAME]
                           [--set-display-name SET_DISPLAY_NAME]
                           [--get-display-name] [--set-presence SET_PRESENCE]
                           [--get-presence] [--upload UPLOAD [UPLOAD ...]]
                           [--download DOWNLOAD [DOWNLOAD ...]]
                           [--delete-mxc DELETE_MXC [DELETE_MXC ...]]
                           [--delete-mxc-before DELETE_MXC_BEFORE [DELETE_MXC_BEFORE ...]]
                           [--joined-rooms]
                           [--joined-members JOINED_MEMBERS [JOINED_MEMBERS ...]]
                           [--mxc-to-http MXC_TO_HTTP [MXC_TO_HTTP ...]]
                           [--devices] [--discovery-info] [--login-info]
                           [--content-repository-config]
                           [--rest REST [REST ...]] [--set-avatar SET_AVATAR]
                           [--get-avatar [GET_AVATAR ...]]
                           [--get-profile [GET_PROFILE ...]]
                           [--get-room-info [GET_ROOM_INFO ...]]
                           [--get-client-info]
                           [--has-permission HAS_PERMISSION [HAS_PERMISSION ...]]
                           [--import-keys IMPORT_KEYS IMPORT_KEYS]
                           [--export-keys EXPORT_KEYS EXPORT_KEYS]
                           [--room-set-alias ROOM_SET_ALIAS [ROOM_SET_ALIAS ...]]
                           [--room-resolve-alias ROOM_RESOLVE_ALIAS [ROOM_RESOLVE_ALIAS ...]]
                           [--room-delete-alias ROOM_DELETE_ALIAS [ROOM_DELETE_ALIAS ...]]
                           [--get-openid-token [GET_OPENID_TOKEN ...]]
                           [--room-get-visibility [ROOM_GET_VISIBILITY ...]]
                           [--room-get-state [ROOM_GET_STATE ...]]
                           [--delete-device DELETE_DEVICE [DELETE_DEVICE ...]]
                           [--room-redact ROOM_REDACT [ROOM_REDACT ...]]
                           [--whoami] [--no-ssl]
                           [--ssl-certificate SSL_CERTIFICATE]
                           [--file-name FILE_NAME [FILE_NAME ...]]
                           [--key-dict KEY_DICT [KEY_DICT ...]] [--plain]
                           [--separator SEPARATOR]
                           [--access-token ACCESS_TOKEN] [--password PASSWORD]
                           [--homeserver HOMESERVER] [--device DEVICE]
                           [--sync SYNC] [--output OUTPUT] [--version]

Welcome to matrix-commander, a Matrix CLI client. ─── On first run use --login
to log in, to authenticate. On second run we suggest to use --verify to get
verified. Emoji verification is built-in which can be used to verify devices.
On further runs this program implements a simple Matrix CLI client that can
send messages, listen to messages, verify devices, etc. It can send one or
multiple message to one or multiple Matrix rooms and/or users. The text
messages can be of various formats such as "text", "html", "markdown" or
"code". Images, audio, arbitrary files, or events can be sent as well. For
receiving there are three main options: listen forever, listen once and quit,
and get the last N messages and quit. End-to-end encryption is enabled by
default and cannot be turned off. ─── Bundling several actions together into a
single call to matrix-commander is faster than calling matrix-commander
multiple times with only one action. If there are both 'set' and 'get' actions
present in the arguments, then the 'set' actions will be performed before the
'get' actions. Then send actions and at the very end listen actions will be
performed. ─── For even more explications and examples also read the
documentation provided in the on-line Github README.md file or the README.md
in your local installation.

options:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information. If used once, only the log
                        level of matrix-commander is set to DEBUG. If used
                        twice ("-d -d" or "-dd") then log levels of both
                        matrix-commander and underlying modules are set to
                        DEBUG. "-d" is a shortcut for "--log-level DEBUG". See
                        also --log-level. "-d" takes precedence over "--log-
                        level". Additionally, have a look also at the option "
                        --verbose".
  --log-level LOG_LEVEL [LOG_LEVEL ...]
                        Set the log level(s). Possible values are "DEBUG",
                        "INFO", "WARNING", "ERROR", and "CRITICAL". If
                        --log_level is used with one level argument, only the
                        log level of matrix-commander is set to the specified
                        value. If --log_level is used with two level argument
                        (e.g. "--log-level WARNING ERROR") then log levels of
                        both matrix-commander and underlying modules are set
                        to the specified values. See also --debug.
  --verbose             Set the verbosity level. If not used, then verbosity
                        will be set to low. If used once, verbosity will be
                        high. If used more than once, verbosity will be very
                        high. Verbosity only affects the debug information.
                        So, if '--debug' is not used then '--verbose' will be
                        ignored.
  --login LOGIN         Login to and authenticate with the Matrix homeserver.
                        This requires exactly one argument, the login method.
                        Currently two choices are offered: 'password' and
                        'sso'. Provide one of these methods. If you have
                        chosen 'password', you will authenticate through your
                        account password. You can optionally provide these
                        additional arguments: --homeserver to specify the
                        Matrix homeserver, --user-login to specify the log in
                        user id, --password to specify the password, --device
                        to specify a device name, --room-default to specify a
                        default room for sending/listening. If you have chosen
                        'sso', you will authenticate through Single Sign-On. A
                        web-browser will be started and you authenticate on
                        the webpage. You can optionally provide these
                        additional arguments: --homeserver to specify the
                        Matrix homeserver, --user-login to specify the log in
                        user id, --device to specify a device name, --room-
                        default to specify a default room for
                        sending/listening. See all the extra arguments for
                        further explanations. ----- SSO (Single Sign-On)
                        starts a web browser and connects the user to a web
                        page on the server for login. SSO will only work if
                        the server supports it and if there is access to a
                        browser. So, don't use SSO on headless homeservers
                        where there is no browser installed or accessible.
  -v [VERIFY], --verify [VERIFY]
                        Perform verification. By default, no verification is
                        performed. Possible values are: "emoji". If
                        verification is desired, run this program in the
                        foreground (not as a service) and without a pipe.
                        While verification is optional it is highly
                        recommended, and it is recommended to be done right
                        after (or together with) the --login action.
                        Verification is always interactive, i.e. it required
                        keyboard input. Verification questions will be printed
                        on stdout and the user has to respond via the keyboard
                        to accept or reject verification. Once verification is
                        complete, the program may be run as a service.
                        Verification is best done as follows: Perform a cross-
                        device verification, that means, perform a
                        verification between two devices of the *same* user.
                        For that, open (e.g.) Element in a browser, make sure
                        Element is using the same user account as the matrix-
                        commander user (specified with --user-login at
                        --login). Now in the Element webpage go to the room
                        that is the matrix-commander default room (specified
                        with --room-default at --login). OK, in the web-
                        browser you are now the same user and in the same room
                        as matrix-commander. Now click the round 'i' 'Room
                        Info' icon, then click 'People', click the appropriate
                        user (the matrix-commander user), click red 'Not
                        Trusted' text which indicated an untrusted device,
                        then click the square 'Interactively verify by Emoji'
                        button (one of 3 button choices). At this point both
                        web-page and matrix-commander in terminal show a set
                        of emoji icons and names. Compare them visually.
                        Confirm on both sides (Yes, They Match, Got it),
                        finally click OK. You should see a green shield and
                        also see that the matrix-commander device is now green
                        and verified in the webpage. In the terminal you
                        should see a text message indicating success. You
                        should now be verified across all devices and across
                        all users.
  --logout LOGOUT       Logout this or all devices from the Matrix homeserver.
                        This requires exactly one argument. Two choices are
                        offered: 'me' and 'all'. Provide one of these choices.
                        If you choose 'me', only the one device matrix-
                        commander is currently using will be logged out. If
                        you choose 'all', all devices of the user used by
                        matrix-commander will be logged out. While --logout
                        neither removes the credentials nor the store, the
                        logout action removes the device and makes the access-
                        token stored in the credentials invalid. Hence, after
                        a --logout, one must manually remove creditials and
                        store, and then perform a new --login to use matrix-
                        commander again. You can perfectly use matrix-
                        commander without ever logging out. --logout is a
                        cleanup if you have decided not to use this (or all)
                        device(s) ever again.
  -c CREDENTIALS, --credentials CREDENTIALS
                        On first run, information about homeserver, user, room
                        id, etc. will be written to a credentials file. By
                        default, this file is "credentials.json". On further
                        runs the credentials file is read to permit logging
                        into the correct Matrix account and sending messages
                        to the preconfigured room. If this option is provided,
                        the provided file name will be used as credentials
                        file instead of the default one.
  -s STORE, --store STORE
                        Path to directory to be used as "store" for encrypted
                        messaging. By default, this directory is "./store/".
                        Since encryption is always enabled, a store is always
                        needed. If this option is provided, the provided
                        directory name will be used as persistent storage
                        directory instead of the default one. Preferably, for
                        multiple executions of this program use the same store
                        for the same device. The store directory can be shared
                        between multiple different devices and users.
  -r ROOM [ROOM ...], --room ROOM [ROOM ...]
                        Optionally specify one or multiple rooms via room ids
                        or room aliases. --room is used by various send
                        actions and various listen actions. The default room
                        is provided in the credentials file (specified at
                        --login with --room-default). If a room (or multiple
                        ones) is (or are) provided in the --room arguments,
                        then it (or they) will be used instead of the one from
                        the credentials file. The user must have access to the
                        specified room in order to send messages there or
                        listen on the room. Messages cannot be sent to
                        arbitrary rooms. When specifying the room id some
                        shells require the exclamation mark to be escaped with
                        a backslash. As an alternative to specifying a room as
                        destination, one can specify a user as a destination
                        with the '--user' argument. See '--user' and the term
                        'DM (direct messaging)' for details. Specifying a room
                        is always faster and more efficient than specifying a
                        user. Not all listen operations allow setting a room.
                        Read more under the --listen options and similar. Most
                        actions also support room aliases instead of room ids.
                        Some even short room aliases.
  --room-default ROOM_DEFAULT
                        Optionally specify a room as the default room for
                        future actions. If not specified for --login, it will
                        be queried via the keyboard. --login stores the
                        specified room as default room in your credentials
                        file. This option is only used in combination with
                        --login. A default room is needed. Specify a valid
                        room either with --room-default or provide it via
                        keyboard.
  --room-create ROOM_CREATE [ROOM_CREATE ...]
                        Create one or multiple rooms. One or multiple room
                        aliases can be specified. For each alias specified a
                        room will be created. For each created room one line
                        with room id and alias will be printed to stdout. If
                        you are not interested in an alias, provide an empty
                        string like "".The alias provided must be in canocial
                        local form, i.e. if you want a final full alias like
                        "#SomeRoomAlias:matrix.example.com" you must provide
                        the string 'SomeRoomAlias'. The user must be permitted
                        to create rooms. Combine --room-create with --name and
                        --topic to add names and topics to the room(s) to be
                        created.
  --room-dm-create ROOM_DM_CREATE [ROOM_DM_CREATE ...]
                        Create one or multiple DM rooms with the specified
                        users. For each user specified a DM room will be
                        created and the user invited to it. For each created
                        room one line with room id and alias will be printed
                        to stdout. The user must be permitted to create rooms.
                        Combine --room-dm-create with --name, --topic and
                        --alias to add names, topics and aliases to the
                        room(s) to be created.
  --room-join ROOM_JOIN [ROOM_JOIN ...]
                        Join this room or these rooms. One or multiple room
                        aliases can be specified. The room (or multiple ones)
                        provided in the arguments will be joined. The user
                        must have permissions to join these rooms.
  --room-leave ROOM_LEAVE [ROOM_LEAVE ...]
                        Leave this room or these rooms. One or multiple room
                        aliases can be specified. The room (or multiple ones)
                        provided in the arguments will be left.
  --room-forget ROOM_FORGET [ROOM_FORGET ...]
                        After leaving a room you should (most likely) forget
                        the room. Forgetting a room removes the users' room
                        history. One or multiple room aliases can be
                        specified. The room (or multiple ones) provided in the
                        arguments will be forgotten. If all users forget a
                        room, the room can eventually be deleted on the
                        server.
  --room-invite ROOM_INVITE [ROOM_INVITE ...]
                        Invite one ore more users to join one or more rooms.
                        Specify the user(s) as arguments to --user. Specify
                        the rooms as arguments to this option, i.e. as
                        arguments to --room-invite. The user must have
                        permissions to invite users.
  --room-ban ROOM_BAN [ROOM_BAN ...]
                        Ban one ore more users from one or more rooms. Specify
                        the user(s) as arguments to --user. Specify the rooms
                        as arguments to this option, i.e. as arguments to
                        --room-ban. The user must have permissions to ban
                        users.
  --room-unban ROOM_UNBAN [ROOM_UNBAN ...]
                        Unban one ore more users from one or more rooms.
                        Specify the user(s) as arguments to --user. Specify
                        the rooms as arguments to this option, i.e. as
                        arguments to --room-unban. The user must have
                        permissions to unban users.
  --room-kick ROOM_KICK [ROOM_KICK ...]
                        Kick one ore more users from one or more rooms.
                        Specify the user(s) as arguments to --user. Specify
                        the rooms as arguments to this option, i.e. as
                        arguments to --room-kick. The user must have
                        permissions to kick users.
  -u USER [USER ...], --user USER [USER ...]
                        Specify one or multiple users. This option is
                        meaningful in combination with a) room actions like
                        --room-invite, --room-ban, --room-unban, etc. and b)
                        send actions like -m, -i, -f, etc. c) some listen
                        actions --listen, as well as d) actions like --delete-
                        device. In case of a) this option --user specifies the
                        users to be used with room commands (like invite, ban,
                        etc.). In case of b) the option --user can be used as
                        an alternative to specifying a room as destination for
                        text (-m), images (-i), etc. For send actions '--user'
                        is providing the functionality of 'DM (direct
                        messaging)'. For c) this option allows an alternative
                        to specifying a room as destination for some --listen
                        actions. For d) this gives the otion to delete the
                        device of a different user. ----- What is a DM?
                        matrix-commander tries to find a room that contains
                        only the sender and the receiver, hence DM. These
                        rooms have nothing special other the fact that they
                        only have 2 members and them being the sender and
                        recipient respectively. If such a room is found, the
                        first one found will be used as destination. If no
                        such room is found, the send fails and the user should
                        do a --room-create and --room-invite first. If
                        multiple such rooms exist, one of them will be used
                        (arbitrarily). For sending and listening, specifying a
                        room directly is always faster and more efficient than
                        specifying a user. So, if you know the room, it is
                        preferred to use --room instead of --user. For b) and
                        c) --user can be specified in 3 ways: 1) full user id
                        as in '@john:example.org', 2) partial user id as in
                        '@john' when the user is on the same homeserver
                        (example.org will be automatically appended), or 3) a
                        display name as in 'john'. Be careful, when using
                        display names as they might not be unique, and you
                        could be sending to the wrong person. To see possible
                        display names use the --joined-members '*' option
                        which will show you the display names in the middle
                        column.
  --user-login USER_LOGIN
                        Optional argument to specify the user for --login.
                        This gives the otion to specify the user id for login.
                        For '--login sso' the --user-login is not needed as
                        user id can be obtained from server via SSO. For '--
                        login password', if not provided it will be queried
                        via keyboard. A full user id like '@john:example.com',
                        a partial user name like '@john', and a short user
                        name like 'john' can be given. --user-login is only
                        used by --login and ignored by all other actions.
  --name NAME [NAME ...]
                        Specify one or multiple names. This option is only
                        meaningful in combination with option --room-create.
                        This option --name specifies the names to be used with
                        the command --room-create.
  --topic TOPIC [TOPIC ...]
                        Specify one or multiple topics. This option is only
                        meaningful in combination with option --room-create.
                        This option --topic specifies the topics to be used
                        with the command --room-create.
  --alias ALIAS [ALIAS ...]
                        Specify one or multiple aliases. This option is only
                        meaningful in combination with option --room-dm-
                        create. This option --alias specifies the aliases to
                        be used with the command --room-dm-create.
  -m MESSAGE [MESSAGE ...], --message MESSAGE [MESSAGE ...]
                        Send this message. Message data must not be binary
                        data, it must be text. If no '-m' is used and no other
                        conflicting arguments are provided, and information is
                        piped into the program, then the piped data will be
                        used as message. Finally, if there are no operations
                        at all in the arguments, then a message will be read
                        from stdin, i.e. from the keyboard. This option can be
                        used multiple times to send multiple messages. If
                        there is data piped into this program, then first data
                        from the pipe is published, then messages from this
                        option are published. Messages will be sent last, i.e.
                        after objects like images, audio, files, events, etc.
                        Input piped via stdin can additionally be specified
                        with the special character '-'. If you want to feed a
                        text message into matrix-commander via a pipe, via
                        stdin, then specify the special character '-'. If '-'
                        is specified as message, then the program will read
                        the message from stdin. If your message is literally
                        '-' then use '\-' as message in the argument. '-' may
                        appear in any position, i.e. '-m "start" - "end"' will
                        send 3 messages out of which the second one is read
                        from stdin. '-' may appear only once overall in all
                        arguments.
  -i IMAGE [IMAGE ...], --image IMAGE [IMAGE ...]
                        Send this image. This option can be used multiple
                        times to send multiple images. First images are sent,
                        then text messages are sent. If you want to feed an
                        image into matrix-commander via a pipe, via stdin,
                        then specify the special character '-'. If '-' is
                        specified as image file name, then the program will
                        read the image data from stdin. If your image file is
                        literally named '-' then use '\-' as file name in the
                        argument. '-' may appear in any position, i.e. '-i
                        image1.jpg - image3.png' will send 3 images out of
                        which the second one is read from stdin. '-' may
                        appear only once overall in all arguments. If the file
                        exists already, it is more efficient to specify the
                        file name than to pipe the file through stdin.
  -a AUDIO [AUDIO ...], --audio AUDIO [AUDIO ...]
                        Send this audio file. This option can be used multiple
                        times to send multiple audio files. First audios are
                        sent, then text messages are sent. If you want to feed
                        an audio into matrix-commander via a pipe, via stdin,
                        then specify the special character '-'. See
                        description of '-i' to see how '-' is handled.
  -f FILE [FILE ...], --file FILE [FILE ...]
                        Send this file (e.g. PDF, DOC, MP4). This option can
                        be used multiple times to send multiple files. First
                        files are sent, then text messages are sent. If you
                        want to feed a file into matrix-commander via a pipe,
                        via stdin, then specify the special character '-'. See
                        description of '-i' to see how '-' is handled.
  -e EVENT [EVENT ...], --event EVENT [EVENT ...]
                        Send an event that is formatted as a JSON object as
                        specified by the Matrix protocol. This allows the
                        advanced user to send additional types of events such
                        as reactions, send replies to previous events, or edit
                        previous messages. Specifications for events can be
                        found at https://spec.matrix.org/unstable/proposals/.
                        This option can be used multiple times to send
                        multiple events. First events are sent, then text
                        messages are sent. If you want to feed an event into
                        matrix-commander via a pipe, via stdin, then specify
                        the special character '-'. See description of '-i' to
                        see how '-' is handled. See tests/test-event.sh for
                        examples.
  -w, --html            Send message as format "HTML". If not specified,
                        message will be sent as format "TEXT". E.g. that
                        allows some text to be bold, etc. Only a subset of
                        HTML tags are accepted by Matrix.
  -z, --markdown        Send message as format "MARKDOWN". If not specified,
                        message will be sent as format "TEXT". E.g. that
                        allows sending of text formatted in MarkDown language.
  -k, --code            Send message as format "CODE". If not specified,
                        message will be sent as format "TEXT". If both --html
                        and --code are specified then --code takes priority.
                        This is useful for sending ASCII-art or tabbed output
                        like tables as a fixed-sized font will be used for
                        display.
  -p SPLIT, --split SPLIT
                        If set, split the message(s) into multiple messages
                        wherever the string specified with --split occurs.
                        E.g. One pipes a stream of RSS articles into the
                        program and the articles are separated by three
                        newlines. Then with --split set to "\n\n\n" each
                        article will be printed in a separate message. By
                        default, i.e. if not set, no messages will be split.
  --config CONFIG       Location of a config file. By default, no config file
                        is used. If this option is provided, the provided file
                        name will be used to read configuration from. Not
                        implemented.
  --proxy PROXY         Optionally specify a proxy for connectivity. By
                        default, i.e. if this option is not set, no proxy is
                        used. If this option is used a proxy URL must be
                        provided. The provided proxy URL will be used for the
                        HTTP connection to the server. The proxy supports
                        SOCKS4(a), SOCKS5, and HTTP (tunneling). Examples of
                        valid URLs are "http://10.10.10.10:8118" or
                        "socks5://user:password@127.0.0.1:1080". URLs with
                        "https" or "socks4a" are not valid. Only "http",
                        "socks4" and "socks5" are valid.
  -n, --notice          Send message as notice. If not specified, message will
                        be sent as text.
  --encrypted           Send message end-to-end encrypted. Encryption is
                        always turned on and will always be used where
                        possible. It cannot be turned off. This flag does
                        nothing as encryption is turned on with or without
                        this argument.
  -l [LISTEN], --listen [LISTEN]
                        The --listen option takes one argument. There are
                        several choices: "never", "once", "forever", "tail",
                        and "all". By default, --listen is set to "never". So,
                        by default no listening will be done. Set it to
                        "forever" to listen for and print incoming messages to
                        stdout. "--listen forever" will listen to all messages
                        on all rooms forever. To stop listening "forever", use
                        Control-C on the keyboard or send a signal to the
                        process or service. The PID for signaling can be found
                        in a PID file in directory "/home/user/.run". "--
                        listen once" will get all the messages from all rooms
                        that are currently queued up. So, with "once" the
                        program will start, print waiting messages (if any)
                        and then stop. The timeout for "once" is set to 10
                        seconds. So, be patient, it might take up to that
                        amount of time. "tail" reads and prints the last N
                        messages from the specified rooms, then quits. The
                        number N can be set with the --tail option. With
                        "tail" some messages read might be old, i.e. already
                        read before, some might be new, i.e. never read
                        before. It prints the messages and then the program
                        stops. Messages are sorted, last-first. Look at --tail
                        as that option is related to --listen tail. The option
                        "all" gets all messages available, old and new. Unlike
                        "once" and "forever" that listen in ALL rooms, "tail"
                        and "all" listen only to the room specified in the
                        credentials file or the --room options.
  -t [TAIL], --tail [TAIL]
                        The --tail option reads and prints up to the last N
                        messages from the specified rooms, then quits. It
                        takes one argument, an integer, which we call N here.
                        If there are fewer than N messages in a room, it reads
                        and prints up to N messages. It gets the last N
                        messages in reverse order. It print the newest message
                        first, and the oldest message last. If --listen-self
                        is not set it will print less than N messages in many
                        cases because N messages are obtained, but some of
                        them are discarded by default if they are from the
                        user itself. Look at --listen as this option is
                        related to --tail.
  -y, --listen-self     If set and listening, then program will listen to and
                        print also the messages sent by its own user. By
                        default messages from oneself are not printed.
  --print-event-id      If set and listening, then 'matrix-commander' will
                        print also the event id for each received message or
                        other received event. If set and sending, then
                        'matrix-commander' will print the event id of the sent
                        message or the sent object (audio, file, event) to
                        stdout. Other information like room id and reference
                        to what was sent will be printed too. For sending this
                        is useful, if after sending the user wishes to perform
                        further operations on the sent object, e.g.
                        redacting/deleting it after an expiration time, etc.
  --download-media [DOWNLOAD_MEDIA]
                        If set and listening, then program will download
                        received media files (e.g. image, audio, video, text,
                        PDF files). media will be downloaded to local
                        directory. By default, media will be downloaded to is
                        "./media/". You can overwrite default with your
                        preferred directory. If media is encrypted it will be
                        decrypted and stored decrypted. By default media files
                        will not be downloaded.
  -o, --os-notify       If set and listening, then program will attempt to
                        visually notify of arriving messages through the
                        operating system. By default there is no notification
                        via OS.
  --set-device-name SET_DEVICE_NAME
                        Set or rename the current device to the device name
                        provided. Send, listen and verify operations are
                        allowed when renaming the device.
  --set-display-name SET_DISPLAY_NAME
                        Set or rename the display name for the current user to
                        the display name provided. Send, listen and verify
                        operations are allowed when setting the display name.
                        Do not confuse this option with the option '--get-
                        room-info' which gets the room display name, not the
                        user display name.
  --get-display-name    Get the display name of matrix-commander (itself), or
                        of one or multiple users. Specify user(s) with the
                        --user option. If no user is specified get the display
                        name of itself. Send, listen and verify operations are
                        allowed when getting display name(s). Do not confuse
                        this option with the option '--get-room-info' which
                        gets the room display name, not the user display name.
  --set-presence SET_PRESENCE
                        Set presence of matrix-commander to the given value.
                        Must be one of these values: “online”, “offline”,
                        “unavailable”. Otherwise an error will be produced.
  --get-presence        Get presence of matrix-commander (itself), or of one
                        or multiple users. Specify user(s) with the --user
                        option. If no user is specified get the presence of
                        itself. Send, listen and verify operations are allowed
                        when getting presence(s).
  --upload UPLOAD [UPLOAD ...]
                        Upload one or multiple files to the content
                        repository. The files will be given a Matrix URI and
                        stored on the server. --upload allows the optional
                        argument --plain to skip encryption for upload. See
                        tests/test-upload.sh for an example.
  --download DOWNLOAD [DOWNLOAD ...]
                        Download one or multiple files from the content
                        repository. You must provide one or multiple Matrix
                        URIs (MXCs) which are strings like this
                        'mxc://example.com/SomeStrangeUriKey'. If found they
                        will be downloaded, decrypted, and stored in local
                        files. If file names are specified with --file-name
                        the downloads will be saved with these file names. If
                        --file-name is not specified the original file name
                        from the upload will be used. If neither specified nor
                        available on server, then the file name of last resort
                        'mxc-<mxc-id>' will be used. If a file name in --file-
                        name contains the placeholder __mxc_id__, it will be
                        replaced with the mxc-id. If a file name is specified
                        as empty string in --file-name, then also the name
                        'mxc-<mxc-id>' will be used. By default, the upload
                        was encrypted so a decryption dictionary must be
                        provided to decrypt the data. Specify one or multiple
                        decryption keys with --key-dict. If --key-dict is not
                        set, not decryption is attempted; and the data might
                        be stored in encrypted fashion, or might be plain-text
                        if the --upload skipped encryption with --plain. See
                        tests/test-upload.sh for an example.
  --delete-mxc DELETE_MXC [DELETE_MXC ...]
                        Delete one or multiple objects (e.g. files) from the
                        content repository. You must provide one or multiple
                        Matrix URIs (MXC) which are strings like this
                        'mxc://example.com/SomeStrangeUriKey'. Alternatively,
                        you can just provide the MXC id, i.e. the part after
                        the last slash. If found they will be deleted from the
                        server database. In order to delete objects one must
                        have server admin permissions. Having only room admin
                        permissions is not sufficient and it will fail. Read
                        https://matrix-org.github.io/synapse/latest/usage/admi
                        nistration/admin_api/ for learning how to set server
                        admin permissions on the server. Alternatively, and
                        optionally, one can specify an access token which has
                        server admin permissions with the --access-token
                        argument. See tests/test-upload.sh for an example.
  --delete-mxc-before DELETE_MXC_BEFORE [DELETE_MXC_BEFORE ...]
                        Delete objects (e.g. files) from the content
                        repository that are older than a given timestamp. It
                        is the timestamp of last access, not the timestamp
                        when the file was created. Additionally you can
                        specify a size in bytes to indicate that only files
                        older than timestamp and larger than size will be
                        deleted. You must provide a timestamp of the following
                        format: 'DD.MM.YYYY HH:MM:SS' like '20.01.2022
                        19:38:42' for January 20, 2022, 7pm 38min 42sec. Files
                        that are still used in image data (e.g user profile,
                        room avatar) will not be deleted from the server
                        database. In order to delete objects one must have
                        server admin permissions. Having only room admin
                        permissions is not sufficient and it will fail. Read
                        https://matrix-org.github.io/synapse/latest/usage/admi
                        nistration/admin_api/ for learning how to set server
                        admin permissions on the server. Alternatively, and
                        optionally, one can specify an access token which has
                        server admin permissions with the --access-token
                        argument. See tests/test-upload.sh for an example.
  --joined-rooms        Print the list of joined rooms. All rooms that you are
                        a member of will be printed, one room per line.
  --joined-members JOINED_MEMBERS [JOINED_MEMBERS ...]
                        Print the list of joined members for one or multiple
                        rooms. If you want to print the joined members of all
                        rooms that you are member of, then use the special
                        character '*'.
  --mxc-to-http MXC_TO_HTTP [MXC_TO_HTTP ...]
                        Convert one or more matrix content URIs to the
                        corresponding HTTP URLs. The MXC URIs to provide look
                        something like this
                        'mxc://example.com/SomeStrangeUriKey'. See tests/test-
                        upload.sh for an example.
  --devices, --get-devices
                        Print the list of devices. All device of this account
                        will be printed, one device per line.
  --discovery-info      Print discovery information about current homeserver.
                        Note that not all homeservers support discovery and an
                        error might be reported.
  --login-info          Print login methods supported by the homeserver. It
                        prints one login method per line.
  --content-repository-config
                        Print the content repository configuration, currently
                        just the upload size limit in bytes.
  --rest REST [REST ...]
                        Use the Matrix Client REST API. Matrix has several
                        extensive REST APIs. With the --rest argument you can
                        invoke a Matrix REST API call. This allows the user to
                        do pretty much anything, at the price of not being
                        very convenient. The APIs are described in
                        https://matrix.org/docs/api/,
                        https://spec.matrix.org/latest/client-server-api/,
                        https://matrix-org.github.io/synapse/latest/usage/admi
                        nistration/admin_api/, etc. Each REST call requires
                        exactly 3 arguments. So, the total number of arguments
                        used with --rest must be a multiple of 3. The argument
                        triples are: (a) the method, a string of GET, POST,
                        PUT, DELETE, or OPTIONS. (b) a string containing the
                        data (if any) in JSON format. (c) a string containing
                        the URL. All strings must be UTF-8. There are a few
                        placeholders. They are: __homeserver__ (like
                        https://matrix.example.org), __hostname__ (like
                        matrix.example.org), __access_token__, __user_id__
                        (like @mc:matrix.example.com), __device_id__, and
                        __room_id__. If a placeholder is found it is replaced
                        with the value from the local credentials file. An
                        example would be: --rest 'GET' ''
                        '__homeserver__/_matrix/client/versions'. If there is
                        no data, i.e. data (b) is empty, then use '' for it.
                        Optionally, --access-token can be used to overwrite
                        the access token from credentials (if needed). See
                        tests/test-rest.sh for an example.
  --set-avatar SET_AVATAR
                        Set the avatar MXC resource used by matrix-commander.
                        Provide one MXC URI that looks like this
                        'mxc://example.com/SomeStrangeUriKey'.
  --get-avatar [GET_AVATAR ...]
                        Get the avatar MXC resource used by matrix-commander,
                        or one or multiple other users. Specify zero or more
                        user ids. If no user id is specified, the avatar of
                        matrix-commander will be fetched. If one or more user
                        ids are given, the avatars of these users will be
                        fetched. As response both MXC URI as well as URL will
                        be printed.
  --get-profile [GET_PROFILE ...]
                        Get the user profile used by matrix-commander, or one
                        or multiple other users. Specify zero or more user
                        ids. If no user id is specified, the user profile of
                        matrix-commander will be fetched. If one or more user
                        ids are given, the user profiles of these users will
                        be fetched. As response display name and avatar MXC
                        URI as well as possible additional profile information
                        (if present) will be printed. One line per user will
                        be printed.
  --get-room-info [GET_ROOM_INFO ...]
                        Get the room information such as room display name,
                        room alias, room creator, etc. for one or multiple
                        specified rooms. The included room 'display name' is
                        also referred to as 'room name' or incorrectly even as
                        room title. If one or more room are given, the room
                        informations of these rooms will be fetched. If no
                        room is specified, the room information for the
                        default room configured for matrix-commander is
                        fetched. Rooms can be given via room id (e.g.
                        '\!SomeRoomId:matrix.example.com'), canonical (full)
                        room alias (e.g. '#SomeRoomAlias:matrix.example.com'),
                        or short alias (e.g. 'SomeRoomAlias' or
                        '#SomeRoomAlias'). As response room id, room display
                        name, room canonical alias, room topic, room creator,
                        and room encryption are printed. One line per room
                        will be printed. Since either room id or room alias
                        are accepted as input and both room id and room alias
                        are given as output, one can hence use this option to
                        map from room id to room alias as well as vice versa
                        from room alias to room id. Do not confuse this option
                        with the options '--get-display-name' and '--set-
                        display-name', which get/set the user display name,
                        not the room display name.
  --get-client-info     Print information kept in the client, i.e. matrix-
                        commander. Output is printed in JSON format.
  --has-permission HAS_PERMISSION [HAS_PERMISSION ...]
                        Inquire if user used by matrix-commander has
                        permission for one or multiple actions in one or
                        multiple rooms. Each inquiry requires 2 parameters:
                        the room id and the permission type. One or multiple
                        of these parameter pairs may be specified. For each
                        parameter pair there will be one line printed to
                        stdout. Values for the permission type are 'ban',
                        'invite', 'kick', 'notifications', 'redact', etc. See
                        https://spec.matrix.org/v1.2/client-server-
                        api/#mroompower_levels.
  --import-keys IMPORT_KEYS IMPORT_KEYS
                        Import Megolm decryption keys from a file. This is an
                        optional argument. If used it must be followed by two
                        values. (a) a file name from which the keys will be
                        read. (b) a passphrase with which the file can be
                        decrypted with. The keys will be added to the current
                        instance as well as written to the database. See also
                        --export-keys.
  --export-keys EXPORT_KEYS EXPORT_KEYS
                        Export all the Megolm decryption keys of this device.
                        This is an optional argument. If used it must be
                        followed by two values. (a) a file name to which the
                        keys will be written to. (b) a passphrase with which
                        the file will be encrypted with. Note that this does
                        not save other information such as the private
                        identity keys of the device.
  --room-set-alias ROOM_SET_ALIAS [ROOM_SET_ALIAS ...], --room-put-alias ROOM_SET_ALIAS [ROOM_SET_ALIAS ...]
                        Add an alias to a room, or aliases to multiple rooms.
                        Provide pairs of arguments. In each pair, the first
                        argument must be the alias you want to assign to the
                        room given via room id in the second argument of the
                        pair. E.g. the 4 arguments 'a1 r1 a2 r2' would assign
                        the alias 'a1' to room 'r1' and the alias 'a2' to room
                        'r2'. If you just have one single pair then the second
                        argument is optional. If just a single value is given
                        (an alias) then this alias is assigned to the default
                        room of matrix-commander (as found in credentials
                        file). In short, you can have just a single argument
                        or an even number of arguments forming pairs. You can
                        have multiple room aliases per room. So, you may add
                        multiple aliases to the same room. A room alias looks
                        like this: '#someRoomAlias:matrix.example.org'. Short
                        aliases like 'someRoomAlias' or '#someRoomAlias' are
                        also accepted. In case of a short alias, it will be
                        automatically prefixed with '#' and the homeserver
                        will be automatically appended. Adding the same alias
                        multiple times to the same room results in an error.
                        --room-put-alias is eqivalent to --room-set-alias.
  --room-resolve-alias ROOM_RESOLVE_ALIAS [ROOM_RESOLVE_ALIAS ...]
                        Resolves a room alias to the corresponding room id, or
                        multiple room aliases to their corresponding room ids.
                        Provide one or multiple room aliases. A room alias
                        looks like this: '#someRoomAlias:matrix.example.org'.
                        Short aliases like 'someRoomAlias' or '#someRoomAlias'
                        are also accepted. In case of a short alias, it will
                        be automatically prefixed with '#' and the homeserver
                        from the default room of matrix-commander (as found in
                        credentials file) will be automatically appended.
                        Resolving an alias that does not exist results in an
                        error. For each room alias one line will be printed to
                        stdout with the result.
  --room-delete-alias ROOM_DELETE_ALIAS [ROOM_DELETE_ALIAS ...]
                        Delete one or multiple rooms aliases. Provide one or
                        multiple room aliases. You can have multiple room
                        aliases per room. So, you may delete multiple aliases
                        from the same room or from different rooms. A room
                        alias looks like this:
                        '#someRoomAlias:matrix.example.org'. Short aliases
                        like 'someRoomAlias' or '#someRoomAlias' are also
                        accepted. In case of a short alias, it will be
                        automatically prefixed with '#' and the homeserver
                        from the default room of matrix-commander (as found in
                        credentials file) will be automatically appended.
                        Deleting an alias that does not exist results in an
                        error.
  --get-openid-token [GET_OPENID_TOKEN ...]
                        Get an OpenID token for matrix-commander, or for one
                        or multiple other users. It prints an OpenID token
                        object that the requester may supply to another
                        service to verify their identity in Matrix. See
                        http://www.openid.net/. Specify zero or more user ids.
                        If no user id is specified, an OpenID for matrix-
                        commander will be fetched. If one or more user ids are
                        given, the OpenID of these users will be fetched. As
                        response the user id(s) and OpenID(s) will be printed.
  --room-get-visibility [ROOM_GET_VISIBILITY ...]
                        Get the visibility of one or more rooms. Provide zero
                        or more room ids as arguments. If no argument is
                        given, then the default room of matrix-commander (as
                        found in credentials file) will be used. For each room
                        the visibility will be printed. Currently, this is
                        either the string 'private' or 'public'. As response
                        one line per room will be printed to stdout.
  --room-get-state [ROOM_GET_STATE ...]
                        Get the state of one or more rooms. Provide zero or
                        more room ids as arguments. If no argument is given,
                        then the default room of matrix-commander (as found in
                        credentials file) will be used. For each room the
                        state will be printed. The state is a long list of
                        events including events like 'm.room.create',
                        'm.room.encryption', 'm.room.guest_access',
                        'm.room.history_visibility', 'm.room.join_rules',
                        'm.room.member', 'm.room.power_levels', etc. As
                        response one line per room will be printed to stdout.
                        The line can be very long as the list of events can be
                        very large. To get output into a human readable form
                        pipe output through sed and jq as shown in an example
                        in tests/test-setget.sh.
  --delete-device DELETE_DEVICE [DELETE_DEVICE ...]
                        Delete one or multiple devices. By default devices
                        belonging to matrix-commander will be deleted. If the
                        devices belong to a different user, use the --user
                        argument to specify the user, i.e. owner. Only exactly
                        one user can be specified with the optional --user
                        argument. Device deletion requires the user password.
                        It must be specified with the --password argument. If
                        the server uses only HTTP (and not HTTPS), then the
                        password can be visible to attackers. Hence, if the
                        server does not support HTTPS this operation is
                        discouraged.
  --room-redact ROOM_REDACT [ROOM_REDACT ...], --room-delete-content ROOM_REDACT [ROOM_REDACT ...]
                        Strip information out of one or several events, e.g.
                        messages. Redact is used in the meaning of 'strip,
                        wipe, black-out', not in the meaning of 'edit'. This
                        action removes, deletes the content of an event while
                        not removing the event. You can wipe text from a
                        previous message, etc. Typical Matrix clients like
                        Element will delete messages, images and other objects
                        from the GUI once they have been redacted. So, --room-
                        redact is a way to delete a message, images, etc. The
                        content is wiped, the GUI deletes the message, but the
                        server keeps the event history. Note, while this
                        deletes from the client (GUI, e.g. Element), it does
                        not delete from the database on the server. So, this
                        call is not a way to clean up the server database.
                        Each redact (wipe, strip, delete) operation requires
                        exactly 3 arguments. The argument triples are: (a) the
                        room id. (b) the id of the event to be redacted. (c) a
                        string containing the reason for the redaction. Use ''
                        if you do not want to give a reason. So, the total
                        number of arguments used with --room-redact must be a
                        multiple of 3, but we also accept 2 in which case only
                        one redaction will be done without specifying a
                        reason. Room ids start with the dollar sign ($).
                        Depending on your shell, you might have to escape the
                        '$' to '\$'. --room-delete-content is an alias for
                        --room-redact. They can be used interchangeably.
  --whoami              Print the user id used by matrix-commander (itself).
                        One can get this information also by looking at the
                        credentials file.
  --no-ssl              Skip SSL verification. By default (if this option is
                        not used) the SSL certificate is validated for the
                        connection. But, if this option is used, then the SSL
                        certificate validation will be skipped. This is useful
                        for home-servers that have no SSL certificate. If used
                        together with the "--ssl-certificate" parameter, this
                        option is meaningless and an error will be raised.
  --ssl-certificate SSL_CERTIFICATE
                        Use this option to use your own local SSL certificate
                        file. This is an optional parameter. This is useful
                        for home servers that have their own SSL certificate.
                        This allows you to use HTTPS/TLS for the connection
                        while using your own local SSL certificate. Specify
                        the path and file to your SSL certificate. If used
                        together with the "--no-ssl" parameter, this option is
                        meaningless and an error will be raised.
  --file-name FILE_NAME [FILE_NAME ...]
                        Specify one or multiple file names for some actions.
                        This is an optional argument. Use this option in
                        combination with options like --download to specify
                        one or multiple file names. Ignored if used by itself
                        without an appropriate corresponding action.
  --key-dict KEY_DICT [KEY_DICT ...]
                        Specify one or multiple key dictionaries for
                        decryption. One or multiple decryption dictionaries
                        are provided by the --upload action as a result. A
                        decryption dictionary is a string like this: "{'v':
                        'v2', 'key': {'kty': 'oct', 'alg': 'A256CTR', 'ext':
                        True, 'k': 'somekey', 'key_ops': ['encrypt',
                        'decrypt']}, 'iv': 'someiv', 'hashes': {'sha256':
                        'someSHA'}}". If you have a list of key dictionaries
                        and want to skip one, use the empty string.
  --plain               Disable encryption for a specific action. By default,
                        everything is always encrypted. Actions that support
                        this option are: --upload.
  --separator SEPARATOR
                        Set a custom separator used for certain print outs. By
                        default, i.e. if --separator is not used, 4 spaces are
                        used as separator between columns in print statements.
                        You could set it to '\t' if you prefer a tab, but tabs
                        are usually replaced with spaces by the terminal. So,
                        that might not give you what you want. Maybe ' || ' is
                        an alternative choice.
  --access-token ACCESS_TOKEN
                        Set a custom access token for use by certain actions.
                        It is an optional argument. By default --access-token
                        is ignored and not used. It is used by the --delete-
                        mxc, --delete-mxc-before, and --rest actions.
  --password PASSWORD   Specify a password for use by certain actions. It is
                        an optional argument. By default --password is ignored
                        and not used. It is used by '--login password' and '--
                        delete-device' actions. If not provided for --login
                        the user will be queried via keyboard.
  --homeserver HOMESERVER
                        Specify a homeserver for use by certain actions. It is
                        an optional argument. By default --homeserver is
                        ignored and not used. It is used by '--login' action.
                        If not provided for --login the user will be queried
                        via keyboard.
  --device DEVICE       Specify a device name, for use by certain actions. It
                        is an optional argument. By default --device is
                        ignored and not used. It is used by '--login' action.
                        If not provided for --login the user will be queried
                        via keyboard. If you want the default value specify
                        ''. Multiple devices (with different device id) may
                        have the same device name. In short, the same device
                        name can be assigned to multiple different devices if
                        desired.
  --sync SYNC           This option decides on whether the program
                        synchronizes the state with the server before a 'send'
                        action. Currently two choices are offered: 'full' and
                        'off'. Provide one of these choices. The default is
                        'full'. If you want to use the default, then there is
                        no need to use this option. If you have chosen 'full',
                        the full state, all state events will be synchronized
                        between this program and the server before a 'send'.
                        If you have chosen 'off', synchronization will be
                        skipped entirely before the 'send' which will improve
                        performance.
  --output OUTPUT       This option decides on how the output is presented.
                        Currently offered choices are: 'text', 'json', 'json-
                        max', and 'json-spec'. Provide one of these choices.
                        The default is 'text'. If you want to use the default,
                        then there is no need to use this option. If you have
                        chosen 'text', the output will be formatted with the
                        intention to be consumed by humans, i.e. readable
                        text. If you have chosen 'json', the output will be
                        formatted as JSON. The content of the JSON object
                        matches the data provided by the matrix-nio SDK. In
                        some occassions the output is enhanced by having a few
                        extra data items added for convenience. In most cases
                        the output will be processed by other programs rather
                        than read by humans. Option 'json-max' is practically
                        the same as 'json', but yet another additional field
                        is added. The data item 'transport_response' which
                        gives information on how the data was obtained and
                        transported is also being added. For '--listen' a few
                        more fields are added. In most cases the output will
                        be processed by other programs rather than read by
                        humans. Option 'json-spec' only prints information
                        that adheres 1-to-1 to the Matrix Specification.
                        Currently only the events on '--listen' and '--tail'
                        provide data exactly as in the Matrix Specification.
                        If no data is available that corresponds exactly with
                        the Matrix Specification, no data will be printed. In
                        short, currently '--json-spec' only provides outputs
                        for '--listen' and '--tail'. All other arguments like
                        '--get-room-info' will print no output.
  --version             Print version information. After printing version
                        information program will continue to run. This is
                        useful for having version number in the log files.

You are running version 3.5.26 2022-11-21. Enjoy, star on Github and
contribute by submitting a Pull Request.
```

# Autocompletion

Tab completion is provided for shells (e.g. bash), courtesy of @mizlan).

Here is a sample snapshot of tab completion in action:

![tab completion screenshot](screenshots/tab_complete.png)

# Performance and Speed

- `matrix-commander` is written in Python and hence rather on the slow side
- It is not thread-safe. One cannot just simply run multiple instances
  at the same time. However, with very careful set-up one can run
  multiple instances, but that is not the target use case. See
  [Issue #31](https://github.com/8go/matrix-commander/issues/31).
- Where possible bundle several actions together into a single call.
  For example if one wants to send 8 images, then it is significantly faster
  to call `matrix-commander` once with `-i` specifying 8 images, than
  to call `matrix-commander` 8 times with one image each call. One needs
  to send 5 messages, 10 images, 5 audios, 3 PDF files and 7 events to
  the same user? Call `matrix-commander` once, not 30 times.
- If you are sending something, then try the `--sync off` option and see
  to what degree skipping the server sync for sending helps.
- Avoid using room aliases. Instead use room ids. For each room alias
  the corresponding id must be retrieved from the server creating overhead.

# For Developers

- Don't change tabbing, spacing, or formatting as file is automatically
  sorted, linted and formatted.
- `pylama:format=pep8:linters=pep8`
- first `isort` import sorter
- then `flake8` linter/formater
- then `black` linter/formater
- line length: 79
  - isort matrix_commander.py
  - flake8 matrix_commander.py
  - python3 -m black --line-length 79 matrix_commander.py
- There is a script called `lintmc.sh` in `scripts` directory for that.

# License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

When preparing to package `matrix-commander` for NIX the question
came up if `matrix-commander` is GPL3Only or GPL3Plus. GPL3PLus was
deemed to be better. As such the license was changed from GPL3Only
to GPL3Plus on May 25, 2021. Versions before this date are licensed
under GPL3. Versions on or after this date are GPL3Plus, i.e.
GPL3 or later.

See [GPL3 at FSF](https://www.fsf.org/licensing/).

# Things to do, Things missing

- see [Issues](https://github.com/8go/matrix-commander/issues) on Github

# Final Remarks

- Thanks to all of you who already have contributed! So appreciated!
  - :heart: and :thumbsup: to @fyfe, @berlincount, @ezwen, @Scriptkiddi,
    @pelzvieh, @mizlan, @edwinsage, @jschwartzentruber, @nirgal, @benneti,
    @opk12, @pataquets, @KizzyCode, @murlock1000, etc.
- Enjoy!
- Give it a :star: star on GitHub! Pull requests are welcome  :heart:

