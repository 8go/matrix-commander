#!/usr/bin/env python3

r"""matrix_commander.py.

0123456789012345678901234567890123456789012345678901234567890123456789012345678
0000000000111111111122222222223333333333444444444455555555556666666666777777777

[![Built with matrix-nio](
https://img.shields.io/badge/built%20with-matrix--nio-brightgreen)](
https://github.com/poljar/matrix-nio)

![MC> logo](logos/matrix-commander-logo.svg)

# :loudspeaker: :new: :boom: Latest News! :fire: :mega: :tada:

- `matrix-commander` new available on
  [PyPi](https://pypi.org/project/matrix-commander/)
  and hence easy to install via `pip install matrix-commander`
- Slight incompatibility: From now on instead of using `matrix-commander.py`
  please call `matrix-commander`. `matrix-commander` is from now on the
  preferred way to execute the program.
- `matrix-commander` is now callable from a Python program as well.
  See [tests/test-send.py](
  https://github.com/8go/matrix-commander/blob/master/tests/test-send.py)
  for an example on how to do that.
- new option `--joined-rooms` to list rooms you are a member of
- new option `--joined-members` to list members of the specified rooms
- new feature "DM" or "direct message" which allows you to send to
  (or listen from) a room whose members are only you (the sender) and the
  recipient by specifying the recipients name.
- Minor incompatibility: From now `-u` is assigned to `--user` and no
  longer to `--download-media`
- new option `--whoami`
- Minor incompatibility: `--rename-device` has been renamed to
  `--set-device-name` and `-x` is no longer supported as shortcut.
- new otion `--get_displayname` for itself, or one or multiple users
- new options `--set-presence` and `--get-presence` to set/get presence
  of itself, or one or multiple users

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
- to send alerts,
- combine it with `cron` to publish periodic data,
- send yourself daily/weekly reminders via a cron job
- send yourself a daily song from your music collection
- a trivial way to fire off some instant messages from the command line
- a trivial way to read messages in the terminal
- to automate sending via programs and scripts
- a "blogger" who frequently sends messages and images to the same
  room(s) could use it
- a person could write a diary or run a gratitude journal by
  sending messages to her/his own room
- as educational material that showcases the use of the `matrix-nio` SDK

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
- Supports skipping SSL verification to use HTTP instead of HTTPS
- Supports providing local SSL certificate files
- Supports notification via OS of received messages
- Supports periodic execution via crontab
- Supports room aliases
- Provides PID files
- Logging (at various levels)
- In-source documentation
- Can be run as a service
- Smart tab completion for shells like bash (thanks to PR from @mizlan :clap:)
- More than 200 stars :stars: on Github
- Easy installation, available through `pip`, i.e. available in PyPi store
- Callable from the terminal, from shells like `bash`, etc.
- Callable from Python programs via the entry point (function) `main`.
- Open source
- Free, GPL3+ license

# First Run, Set Up, Credentials File, End-to-end Encryption

This program on the first run creates a credentials.json file.
The credentials.json file stores: homeserver, user id,
access token, device id, and room id. On the first run
it asks some questions, creates the token and device id
and stores everything in the credentials.json file.

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
to the preconfigured room.

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

# Verification

The program can accept verification request and verify other devices
via emojis. Do do so use the --verify option and the program will
await incoming verification request and act accordingly.

# Room Operations, Actions on Rooms

The program can create rooms, join, leave and forget rooms.
It can also send invitations to join rooms to
others (given that user has the appropriate permissions) as
well as ban, unban and kick other users from rooms.

# Dependencies and Installation

- If you install via `pip`, then `pip` will take care of most of the
  dependencies.
  - See https://pypi.org/project/matrix-commander
  - Usually `pip install matrix-commander` will do the trick.
  - Note that even if you install via `pip` you must have a) Python 3.8+
    and b) `libolm` installed. See `PyPi-Instructions.md`.

If you install vit `git` or via file download then these are the
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
$ matrix-commander # first run; this will configure everything
$ matrix-commander --no-sso # alternative first run without Single Sign-On;
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
$ matrix-commander --debug # turn debugging on
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
                           [-c CREDENTIALS] [-r ROOM [ROOM ...]]
                           [--room-create ROOM_CREATE [ROOM_CREATE ...]]
                           [--room-join ROOM_JOIN [ROOM_JOIN ...]]
                           [--room-leave ROOM_LEAVE [ROOM_LEAVE ...]]
                           [--room-forget ROOM_FORGET [ROOM_FORGET ...]]
                           [--room-invite ROOM_INVITE [ROOM_INVITE ...]]
                           [--room-ban ROOM_BAN [ROOM_BAN ...]]
                           [--room-unban ROOM_UNBAN [ROOM_UNBAN ...]]
                           [--room-kick ROOM_KICK [ROOM_KICK ...]]
                           [-u USER [USER ...]] [--name NAME [NAME ...]]
                           [--topic TOPIC [TOPIC ...]]
                           [-m MESSAGE [MESSAGE ...]] [-i IMAGE [IMAGE ...]]
                           [-a AUDIO [AUDIO ...]] [-f FILE [FILE ...]]
                           [-e EVENT [EVENT ...]] [-w] [-z] [-k] [-p SPLIT]
                           [-j CONFIG] [--proxy PROXY] [-n] [--encrypted]
                           [-s STORE] [-l [LISTEN]] [-t [TAIL]] [-y]
                           [--print-event-id]
                           [--download-media [DOWNLOAD_MEDIA]] [-o]
                           [-v [VERIFY]] [--set-device-name SET_DEVICE_NAME]
                           [--set-display-name SET_DISPLAY_NAME]
                           [--get-display-name] [--set-presence SET_PRESENCE]
                           [--get-presence] [--no-ssl]
                           [--ssl-certificate SSL_CERTIFICATE] [--no-sso]
                           [--joined-rooms]
                           [--joined-members JOINED_MEMBERS [JOINED_MEMBERS ...]]
                           [--whoami] [--version]

Welcome to matrix-commander, a Matrix CLI client. ─── On first run this
program will configure itself. On further runs this program implements a
simple Matrix CLI client that can send messages, listen to messages, verify
devices, etc. It can send one or multiple message to one or multiple Matrix
rooms and/or users. The text messages can be of various formats such as
"text", "html", "markdown" or "code". Images, audio, arbitrary files, or
events can be sent as well. For receiving there are three main options: listen
forever, listen once and quit, and get the last N messages and quit. Emoji
verification is built-in which can be used to verify devices. End-to-end
encryption is enabled by default and cannot be turned off. ─── Bundling
several actions together into a single call to {PROG_WITHOUT_EXT} is faster
than calling {PROG_WITHOUT_EXT} multiple times with only one action. If there
are both 'set' and 'get' actions present in the arguments, then the 'set'
actions will be performed before the 'get' actions. ─── For even more
explications and examples also read the documentation provided in the on-line
Github README.md file or the README.md in your local installation.

options:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information. If used once, only the log
                        level of matrix-commander is set to DEBUG. If used
                        twice ("-d -d" or "-dd") then log levels of both
                        matrix-commander and underlying modules are set to
                        DEBUG. "-d" is a shortcut for "--log-level DEBUG". See
                        also --log-level. "-d" takes precedence over "--log-
                        level".
  --log-level LOG_LEVEL [LOG_LEVEL ...]
                        Set the log level(s). Possible values are "DEBUG",
                        "INFO", "WARNING", "ERROR", and "CRITICAL". If
                        --log_level is used with one level argument, only the
                        log level of matrix-commander is set to the specified
                        value. If --log_level is used with two level argument
                        (e.g. "--log-level WARNING ERROR") then log levels of
                        both matrix-commander and underlying modules are set
                        to the specified values. See also --debug.
  -c CREDENTIALS, --credentials CREDENTIALS
                        On first run, information about homeserver, user, room
                        id, etc. will be written to a credentials file. By
                        default, this file is "credentials.json". On further
                        runs the credentials file is read to permit logging
                        into the correct Matrix account and sending messages
                        to the preconfigured room. If this option is provided,
                        the provided file name will be used as credentials
                        file instead of the default one.
  -r ROOM [ROOM ...], --room ROOM [ROOM ...]
                        Send to or receive from this room or these rooms.
                        None, one or multiple rooms can be specified. The
                        default room is provided in credentials file. If a
                        room (or multiple ones) is (or are) provided in the
                        arguments, then it (or they) will be used instead of
                        the one from the credentials file. The user must have
                        access to the specified room in order to send messages
                        there or listen on the room. Messages cannot be sent
                        to arbitrary rooms. When specifying the room id some
                        shells require the exclamation mark to be escaped with
                        a backslash. As an alternative to specifying a room as
                        destination, one can specify a user as a destination
                        with the '--user' argument. See '--user' and the term
                        'DM (direct messaging)' for details. Specifying a room
                        is always faster and more efficient than specifying a
                        user. Not all listen operations allow setting a room.
                        Read more under the --listen options and similar.
  --room-create ROOM_CREATE [ROOM_CREATE ...]
                        Create this room or these rooms. One or multiple room
                        aliases can be specified. The room (or multiple ones)
                        provided in the arguments will be created. The user
                        must be permitted to create rooms. Combine --room-
                        create with --name and --topic to add names and topics
                        to the room(s) to be created.
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
                        send actions like -m, -i, -f, etc. as well as c) some
                        listen actions --listen. In case of a) this option
                        --user specifies the users to be used with room
                        commands (like invite, ban, etc.). In case of b) the
                        option --user can be used as an alternative to
                        specifying a room as destination for text (-m), images
                        (-i), etc. For send actions '--user' is providing the
                        functionality of 'DM (direct messaging)'. For c) this
                        option allows an alternative to specifying a room as
                        destination for some --listen actions. What is a DM?
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
                        as in '@user:example.org', 2) partial user id as in
                        '@user' when the user is on the same homeserver
                        (example.org will be automatically appended), or 3) a
                        display name. Be careful, when using display names as
                        they might not be unique, and you could be sending to
                        the wrong person. To see possible display names use
                        the --joined-members '*' option which will show you
                        the display names in the middle column.
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
  -m MESSAGE [MESSAGE ...], --message MESSAGE [MESSAGE ...]
                        Send this message. Message data must not be binary
                        data, it must be text. If no '-m' is used and no other
                        conflictingarguments are provided, and information is
                        piped into the program, then the piped data will be
                        used as message. Finally, if there are no operations
                        at all in the arguemnts, then a message will be read
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
                        literally named '-' then use '\-' as filename in the
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
                        see how '-' is handled.
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
  -j CONFIG, --config CONFIG
                        Location of a config file. By default, no config file
                        is used. If this option is provided, the provided file
                        name will be used to read configuration from.
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
                        credentials file or the --room options. Furthermore,
                        when listening to messages, no messages will be sent.
                        Hence, when listening, --message must not be used and
                        piped input will be ignored.
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
                        related to --tail.Furthermore, when tailing messages,
                        no messages will be sent. Hence, when tailing or
                        listening, --message must not be used and piped input
                        will be ignored.
  -y, --listen-self     If set and listening, then program will listen to and
                        print also the messages sent by its own user. By
                        default messages from oneself are not printed.
  --print-event-id      If set and listening, then program will print also the
                        event id foreach message or other event.
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
  -v [VERIFY], --verify [VERIFY]
                        Perform verification. By default, no verification is
                        performed. Possible values are: "emoji". If
                        verification is desired, run this program in the
                        foreground (not as a service) and without a pipe.
                        Verification questions will be printed on stdout and
                        the user has to respond via the keyboard to accept or
                        reject verification. Once verification is complete,
                        stop the program and run it as a service again. Don't
                        send messages or files when you verify.
  --set-device-name SET_DEVICE_NAME
                        Set or rename the current device to the device name
                        provided. Send, listen and verify operations are
                        allowed when renaming the device.
  --set-display-name SET_DISPLAY_NAME
                        Set or rename the display name for the current user to
                        the display name provided. Send, listen and verify
                        operations are allowed when setting the display name.
  --get-display-name    Get the display name of matrix-commander (itself), or
                        of one or multiple users. Specify user(s) with the
                        --user option. If no user is specified get the display
                        name of itself. Send, listen and verify operations are
                        allowed when getting display name(s).
  --set-presence SET_PRESENCE
                        Set presence of {PROG_WITHOUT_EXT} to the given value.
                        Must be one of these values: “online”, “offline”,
                        “unavailable”. Otherwise an error will be produced.
  --get-presence        Get presence of {PROG_WITHOUT_EXT} (itself), or of one
                        or multiple users. Specify user(s) with the --user
                        option. If no user is specified get the presence of
                        itself. Send, listen and verify operations are allowed
                        when getting presence(s).
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
  --no-sso              This argument is optional. If it is not used, the
                        default login method will be used. This default login
                        method is: SSO (Single Sign-On). SSO starts a web
                        browser and connects the user to a webpage on the
                        server for login. SSO will only work if the server
                        supports it and if there is access to a browser. If
                        this argument is used, then SSO will be avoided. This
                        is useful on headless homeservers where there is no
                        browser installed or accessible. It is also useful if
                        the user prefers to login via a password. So, if SSO
                        should be avoided and a password login is preferred
                        then set this option. This option is only meaningful
                        on the first run that initializes matrix-commander.
                        Once credentials are established this option is
                        irrelevant and it will simply be ignored.
  --joined-rooms        Print the list of joined rooms. All rooms that you are
                        a member of will be printed, one room per line.
  --joined-members JOINED_MEMBERS [JOINED_MEMBERS ...]
                        Print the list of joined members for one or multiple
                        rooms. If you want to print the joined members of all
                        rooms that you are member of, then use the special
                        character '*'.
  --whoami              Print the user id used by matrix-commander (itself).
                        One can get this information also by looking at the
                        credentials file.
  --version             Print version information. After printing version
                        information program will continue to run. This is
                        useful for having version number in the log files.

You are running version 2.23.0 2022-06-02. Enjoy, star on Github and
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
  multiple instances, but that is not the target use case.
- Where possible bundle several actions together into a single call.
  For example if one wants to send 8 images, then it is significatly faster
  to call `matrix-commander` once with `-i` specifying 8 images, than
  to call `matrix-commander` 8 times with one image each call. One needs
  to send 5 messages, 10 images, 5 audios, 3 PDF files and 7 events to
  the same user? Call `matrix-commander` once, not 30 times.

# For Developers

- Don't change tabbing, spacing, or formating as file is automatically
  sorted, linted and formatted.
- `pylama:format=pep8:linters=pep8`
- first `isort` import sorter
- then `flake8` linter/formater
- then `black` linter/formater
- linelength: 79
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
    @opk12, etc.
- Enjoy!
- Give it a :star: star on GitHub! Pull requests are welcome  :heart:

"""

# automatically sorted by isort,
# then formatted by black --line-length 79
import argparse
import asyncio
import datetime
import errno
import getpass
import json
import logging
import os
import re  # regular expression
import select
import shutil
import ssl
import subprocess
import sys
import tempfile
import textwrap
import traceback
import urllib.request
import uuid
from os import R_OK, access
from os.path import isfile
from ssl import SSLContext
from typing import Union
from urllib.parse import urlparse

import aiofiles
import aiofiles.os
import magic
from aiohttp import ClientConnectorError, ClientSession, TCPConnector, web
from markdown import markdown
from nio import (AsyncClient, AsyncClientConfig, EnableEncryptionBuilder,
                 JoinedMembersError, JoinedRoomsError, JoinError,
                 KeyVerificationCancel, KeyVerificationEvent,
                 KeyVerificationKey, KeyVerificationMac, KeyVerificationStart,
                 LocalProtocolError, LoginResponse, MatrixRoom,
                 MessageDirection, PresenceGetError, PresenceSetError,
                 ProfileGetAvatarResponse, ProfileGetDisplayNameError,
                 ProfileSetDisplayNameError, RedactedEvent, RedactionEvent,
                 RoomAliasEvent, RoomBanError, RoomCreateError,
                 RoomEncryptedAudio, RoomEncryptedFile, RoomEncryptedImage,
                 RoomEncryptedMedia, RoomEncryptedVideo, RoomEncryptionEvent,
                 RoomForgetError, RoomInviteError, RoomKickError,
                 RoomLeaveError, RoomMemberEvent, RoomMessage,
                 RoomMessageAudio, RoomMessageEmote, RoomMessageFile,
                 RoomMessageFormatted, RoomMessageImage, RoomMessageMedia,
                 RoomMessageNotice, RoomMessagesError, RoomMessageText,
                 RoomMessageUnknown, RoomMessageVideo, RoomNameEvent,
                 RoomReadMarkersError, RoomResolveAliasError, RoomUnbanError,
                 SyncError, SyncResponse, ToDeviceError, UnknownEvent,
                 UpdateDeviceError, UploadResponse, crypto)
from PIL import Image

try:
    import notify2

    HAVE_NOTIFY = True
except ImportError:
    HAVE_NOTIFY = False

# version number
VERSION = "2022-06-02"
VERSIONNR = "2.23.0"
# matrix-commander; for backwards compitability replace _ with -
PROG_WITHOUT_EXT = os.path.splitext(os.path.basename(__file__))[0].replace(
    "_", "-"
)
# matrix-commander.py; for backwards compitability replace _ with -
PROG_WITH_EXT = os.path.basename(__file__).replace("_", "-")
# file to store credentials in case you want to run program multiple times
CREDENTIALS_FILE_DEFAULT = "credentials.json"  # login credentials JSON file
# e.g. ~/.config/matrix-commander/
CREDENTIALS_DIR_LASTRESORT = os.path.expanduser(
    "~/.config/"
) + os.path.splitext(os.path.basename(__file__))[0].replace("_", "-")
# directory to be used by end-to-end encrypted protocol for persistent storage
STORE_DIR_DEFAULT = "./store/"
# e.g. ~/.local/share/matrix-commander/
# the STORE_PATH_LASTRESORT will be concatenated with a directory name
# like store to result in a final path of
# e.g. ~/.local/share/matrix-commander/store/ as actual persistent store dir
STORE_PATH_LASTRESORT = os.path.normpath(
    (
        os.path.expanduser("~/.local/share/")
        + os.path.splitext(os.path.basename(__file__))[0].replace("_", "-")
    )
)
# e.g. ~/.local/share/matrix-commander/store/
STORE_DIR_LASTRESORT = os.path.normpath(
    (os.path.expanduser(STORE_PATH_LASTRESORT + "/" + STORE_DIR_DEFAULT))
)
# directory to be used for downloading media files
MEDIA_DIR_DEFAULT = "./media/"
# usually there are no permissions for using: /run/matrix-commander.pid
# so instead local files like ~/.run/matrix-commander.some-uuid-here.pid will
# be used for storing the PID(s) for sending signals.
# There might be more than 1 process running in parallel, so there might be
# more than 1 PID at a given point in time.
PID_DIR_DEFAULT = os.path.normpath(os.path.expanduser("~/.run/"))
PID_FILE_DEFAULT = os.path.normpath(
    PID_DIR_DEFAULT + "/" + PROG_WITHOUT_EXT + "." + str(uuid.uuid4()) + ".pid"
)
EMOJI = "emoji"  # verification type
ONCE = "once"  # listening type
NEVER = "never"  # listening type
FOREVER = "forever"  # listening type
ALL = "all"  # listening type
TAIL = "tail"  # listening type
SEP = "    "  # separator used for sperating columns in print outputs
LISTEN_DEFAULT = NEVER
TAIL_UNUSED_DEFAULT = 0  # get 0 if --tail is not specified
TAIL_USED_DEFAULT = 10  # get the last 10 msgs by default with --tail
VERIFY_UNUSED_DEFAULT = None  # use None if --verify is not specified
VERIFY_USED_DEFAULT = "emoji"  # use emoji by default with --verify
SET_DEVICE_NAME_UNUSED_DEFAULT = None  # use None if -x is not specified
SET_DISPLAY_NAME_UNUSED_DEFAULT = None  # use None option not used
NO_SSL_UNUSED_DEFAULT = None  # use None if --no-ssl is not given
SSL_CERTIFICATE_DEFAULT = None  # use None if --ssl-certificate is not given
NO_SSO_UNUSED_DEFAULT = None  # use None if --no-sso is not given


class MatrixCommanderError(RuntimeError):
    def __init__(
        self,
        errmsg: str,
        traceback: bool = False,  # is traceback printing desired?
        level: str = "error",
    ):
        self.errmsg = errmsg
        self.traceback = traceback
        self.level = level  # debug, info, warning, error

    def __str__(self):
        return self.errmsg


class GlobalState:
    """Keep global variables.

    Trivial class to help keep some global state.
    """

    def __init__(self):
        """Store global state."""
        self.log: logging.Logger = None  # logger object
        self.pa: argparse.Namespace = None  # parsed arguments
        # to which logic (message, image, audio, file, event) is
        # stdin pipe assigned?
        self.stdin_use: str = "none"
        # 1) ssl None means default SSL context will be used.
        # 2) ssl False means SSL certificate validation will be skipped
        # 3) ssl a valid SSLContext means that the specified context will be
        #    used. This is useful to using local SSL certificate.
        self.ssl: Union[None, SSLContext, bool] = None
        self.send_action = False  # argv contains send action
        self.room_action = False  # argv contains room action
        self.setget_action = False  # argv contains set or get action


def choose_available_filename(filename):
    """Return next available filename.

    If filename (includes path) does not exist,
    then it returns filename. If file already
    exists it adds a counter at end, before
    extension, and increases counter until it
    finds a filename that does not yet exist.
    This avoids overwritting files when sources
    have same name.
    """
    if os.path.exists(filename):
        try:
            start, ext = filename.rsplit(".", 1)
        except ValueError:
            start, ext = (filename, "")
        i = 0
        while os.path.exists(f"{start}_{i}.{ext}"):
            i += 1
        return f"{start}_{i}.{ext}"
    else:
        return filename


async def download_mxc(client: AsyncClient, url: str):
    """Download MXC resource."""
    mxc = urlparse(url)
    response = await client.download(mxc.netloc, mxc.path.strip("/"))
    return response.body


class Callbacks(object):
    """Class to pass client to callback methods."""

    def __init__(self, client):
        """Store AsyncClient."""
        self.client = client

    # according to pylama: function too complex: C901 # noqa: C901
    async def message_callback(self, room: MatrixRoom, event):  # noqa: C901
        """Handle all events of type RoomMessage.

        Includes events like RoomMessageText, RoomMessageImage, etc.
        """
        try:
            gs.log.debug(
                f"message_callback(): for room {room} received this "
                f"event: type: {type(event)}, event_id: {event.event_id}, "
                f"event: {event}"
            )
            if not gs.pa.listen_self:
                if event.sender == self.client.user:
                    try:
                        gs.log.debug(
                            f"Skipping message sent by myself: {event.body}"
                        )
                    except AttributeError:  # does not have .body
                        gs.log.debug(
                            f"Skipping message sent by myself: {event}"
                        )
                    return

            # millisec since 1970
            gs.log.debug(f"event.server_timestamp = {event.server_timestamp}")
            timestamp = datetime.datetime.fromtimestamp(
                int(event.server_timestamp / 1000)
            )  # sec since 1970
            event_datetime = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            # e.g. 2020-08-06 17:30:18
            gs.log.debug(f"event_datetime = {event_datetime}")

            if isinstance(event, RoomMessageMedia):  # for all media events
                media_mxc = event.url
                media_url = await self.client.mxc_to_http(media_mxc)
                gs.log.debug(f"HTTP URL of media is : {media_url}")
                msg_url = " [" + media_url + "]"
                if gs.pa.download_media != "":
                    # download unencrypted media file
                    media_data = await download_mxc(self.client, media_mxc)
                    filename = choose_available_filename(
                        os.path.join(gs.pa.download_media, event.body)
                    )
                    async with aiofiles.open(filename, "wb") as f:
                        await f.write(media_data)
                        # Set atime and mtime of file to event timestamp
                        os.utime(
                            filename,
                            ns=((event.server_timestamp * 1000000,) * 2),
                        )
                    msg_url += f" [Downloaded media file to {filename}]"

            if isinstance(event, RoomEncryptedMedia):  # for all e2e media
                media_mxc = event.url
                media_url = await self.client.mxc_to_http(media_mxc)
                gs.log.debug(f"HTTP URL of media is : {media_url}")
                msg_url = " [" + media_url + "]"
                if gs.pa.download_media != "":
                    # download encrypted media file
                    media_data = await download_mxc(self.client, media_mxc)
                    filename = choose_available_filename(
                        os.path.join(gs.pa.download_media, event.body)
                    )
                    async with aiofiles.open(filename, "wb") as f:
                        await f.write(
                            crypto.attachments.decrypt_attachment(
                                media_data,
                                event.source["content"]["file"]["key"]["k"],
                                event.source["content"]["file"]["hashes"][
                                    "sha256"
                                ],
                                event.source["content"]["file"]["iv"],
                            )
                        )
                        # Set atime and mtime of file to event timestamp
                        os.utime(
                            filename,
                            ns=((event.server_timestamp * 1000000,) * 2),
                        )
                    msg_url += (
                        f" [Downloaded and decrypted media file to {filename}]"
                    )

            if isinstance(event, RoomMessageAudio):
                msg = "Received audio: " + event.body + msg_url
            elif isinstance(event, RoomMessageEmote):
                msg = "Received emote: " + event.body
            elif isinstance(event, RoomMessageFile):
                msg = "Received file: " + event.body + msg_url
            elif isinstance(event, RoomMessageFormatted):
                msg = event.body
            elif isinstance(event, RoomMessageImage):
                # Usually body is something like "image.svg"
                msg = "Received image: " + event.body + msg_url
            elif isinstance(event, RoomMessageNotice):
                msg = event.body  # Extract the message text
            elif isinstance(event, RoomMessageText):
                msg = event.body  # Extract the message text
            elif isinstance(event, RoomMessageUnknown):
                msg = "Received room message of unknown type: " + event.msgtype
            elif isinstance(event, RoomMessageVideo):
                msg = "Received video: " + event.body + msg_url
            elif isinstance(event, RoomEncryptedAudio):
                msg = "Received encrypted audio: " + event.body + msg_url
            elif isinstance(event, RoomEncryptedFile):
                msg = "Received encrypted file: " + event.body + msg_url
            elif isinstance(event, RoomEncryptedImage):
                # Usually body is something like "image.svg"
                msg = "Received encrypted image: " + event.body + msg_url
            elif isinstance(event, RoomEncryptedVideo):
                msg = "Received encrypted video: " + event.body + msg_url
            elif isinstance(event, RoomMessageMedia):
                # this should never be reached, this is a base class
                # it should be a audio, image, video, etc.
                # Put here at the end as defensive programming
                msg = "Received media: " + event.body + msg_url
            elif isinstance(event, RoomEncryptedMedia):
                # this should never be reached, this is a base class
                # it should be a audio, image, video, etc.
                # Put here at the end as defensive programming
                msg = "Received encrypted media: " + event.body + msg_url
            elif isinstance(event, RoomMemberEvent):
                msg = (
                    "Received room-member event: "
                    f"sender: {event.sender}, operation: {event.membership}"
                )
            elif isinstance(event, RoomEncryptionEvent):
                msg = (
                    "Received room-encryption event: "
                    f"sender: {event.sender}"
                )
            elif isinstance(event, RoomAliasEvent):
                msg = (
                    "Received room-alias event: sender: "
                    f"{event.sender}, alias: {event.canonical_alias}"
                )
            elif isinstance(event, RoomNameEvent):
                msg = (
                    "Received room-name event: sender: "
                    f"{event.sender}, room name: {event.name}"
                )
            elif isinstance(event, RedactedEvent):
                msg = (
                    "Received redacted event: "
                    f"sender: {event.sender}, "
                    f"type: {event.type}, redacter: {event.redacter}"
                )
            elif isinstance(event, RedactionEvent):
                msg = (
                    "Received redaction event: "
                    f"sender: {event.sender}, "
                    f"redacts: {event.redacts}"
                )
            elif isinstance(event, UnknownEvent):
                if event.type == "m.reaction":
                    msg = (
                        "Received a reaction, an emoji: "
                        f"{event.source['content']['m.relates_to']['key']}"
                    )
                else:
                    msg = f"Received unknown event: {event}"
            else:
                msg = f"Received unknown event: {event}"

            # if event['type'] == "m.room.message":
            #    if event['content']['msgtype'] == "m.text":
            #        content = event['content']['body']
            #    else:
            #        download_url = api.get_download_url(
            #            event['content']['url'])
            #        content = download_url
            # else:
            #    content = "\n{{ " + event['type'] + " event }}\n"
            gs.log.debug(f"type(msg) = {type(msg)}. msg is a string")
            sender_nick = room.user_name(event.sender)
            if not sender_nick:  # convert @foo:mat.io into foo
                sender_nick = event.sender.split(":")[0][1:]
            room_nick = room.display_name
            if not room_nick or room_nick == "Empty Room" or room_nick == "":
                room_nick = "Undetermined"
            if gs.pa.print_event_id:
                event_id_detail = f" | {event.event_id}"
            else:
                event_id_detail = ""
            # Prevent faking messages by prefixing each line of a multiline
            # message with space.
            fixed_msg = re.sub("\n", "\n    ", msg)
            complete_msg = (
                "Message received for room "
                f"{room_nick} [{room.room_id}] | "
                f"sender {sender_nick} "
                f"[{event.sender}] | {event_datetime}"
                f"{event_id_detail} | {fixed_msg}"
            )
            gs.log.debug(complete_msg)
            print(complete_msg, flush=True)
            if gs.pa.os_notify:
                avatar_url = await get_avatar_url(self.client, event.sender)
                notify(
                    f"From {room.user_name(event.sender)}",
                    msg[:160],
                    avatar_url,
                )

        except BaseException:
            gs.log.debug(traceback.format_exc())

    # according to linter: function is too complex, C901
    async def to_device_callback(self, event):  # noqa: C901
        """Handle events sent to device."""
        try:
            client = self.client

            if isinstance(event, KeyVerificationStart):  # first step
                """first step: receive KeyVerificationStart
                KeyVerificationStart(
                    source={'content':
                            {'method': 'm.sas.v1',
                             'from_device': 'DEVICEIDXY',
                             'key_agreement_protocols':
                                ['curve25519-hkdf-sha256', 'curve25519'],
                             'hashes': ['sha256'],
                             'message_authentication_codes':
                                ['hkdf-hmac-sha256', 'hmac-sha256'],
                             'short_authentication_string':
                                ['decimal', 'emoji'],
                             'transaction_id': 'SomeTxId'
                             },
                            'type': 'm.key.verification.start',
                            'sender': '@user2:example.org'
                            },
                    sender='@user2:example.org',
                    transaction_id='SomeTxId',
                    from_device='DEVICEIDXY',
                    method='m.sas.v1',
                    key_agreement_protocols=[
                        'curve25519-hkdf-sha256', 'curve25519'],
                    hashes=['sha256'],
                    message_authentication_codes=[
                        'hkdf-hmac-sha256', 'hmac-sha256'],
                    short_authentication_string=['decimal', 'emoji'])
                """

                if "emoji" not in event.short_authentication_string:
                    print(
                        "Other device does not support emoji verification "
                        f"{event.short_authentication_string}."
                    )
                    return
                resp = await client.accept_key_verification(
                    event.transaction_id
                )
                if isinstance(resp, ToDeviceError):
                    print(f"accept_key_verification failed with {resp}")

                sas = client.key_verifications[event.transaction_id]

                todevice_msg = sas.share_key()
                resp = await client.to_device(todevice_msg)
                if isinstance(resp, ToDeviceError):
                    print(f"to_device failed with {resp}")

            elif isinstance(event, KeyVerificationCancel):  # anytime
                """at any time: receive KeyVerificationCancel
                KeyVerificationCancel(source={
                    'content': {'code': 'm.mismatched_sas',
                                'reason': 'Mismatched authentication string',
                                'transaction_id': 'SomeTxId'},
                    'type': 'm.key.verification.cancel',
                    'sender': '@user2:example.org'},
                    sender='@user2:example.org',
                    transaction_id='SomeTxId',
                    code='m.mismatched_sas',
                    reason='Mismatched short authentication string')
                """

                # There is no need to issue a
                # client.cancel_key_verification(tx_id, reject=False)
                # here. The SAS flow is already cancelled.
                # We only need to inform the user.
                print(
                    f"Verification has been cancelled by {event.sender} "
                    f'for reason "{event.reason}".'
                )

            elif isinstance(event, KeyVerificationKey):  # second step
                """Second step is to receive KeyVerificationKey
                KeyVerificationKey(
                    source={'content': {
                            'key': 'SomeCryptoKey',
                            'transaction_id': 'SomeTxId'},
                        'type': 'm.key.verification.key',
                        'sender': '@user2:example.org'
                    },
                    sender='@user2:example.org',
                    transaction_id='SomeTxId',
                    key='SomeCryptoKey')
                """
                sas = client.key_verifications[event.transaction_id]

                print(f"{sas.get_emoji()}")

                yn = input("Do the emojis match? (Y/N) (C for Cancel) ")
                if yn.lower() == "y":
                    print(
                        "Match! The verification for this "
                        "device will be accepted."
                    )
                    resp = await client.confirm_short_auth_string(
                        event.transaction_id
                    )
                    if isinstance(resp, ToDeviceError):
                        print(f"confirm_short_auth_string failed with {resp}")
                elif yn.lower() == "n":  # no, don't match, reject
                    print(
                        "No match! Device will NOT be verified "
                        "by rejecting verification."
                    )
                    resp = await client.cancel_key_verification(
                        event.transaction_id, reject=True
                    )
                    if isinstance(resp, ToDeviceError):
                        print(f"cancel_key_verification failed with {resp}")
                else:  # C or anything for cancel
                    print("Cancelled by user! Verification will be cancelled.")
                    resp = await client.cancel_key_verification(
                        event.transaction_id, reject=False
                    )
                    if isinstance(resp, ToDeviceError):
                        print(f"cancel_key_verification failed with {resp}")

            elif isinstance(event, KeyVerificationMac):  # third step
                """Third step is to receive KeyVerificationMac
                KeyVerificationMac(
                    source={'content': {
                        'mac': {'ed25519:DEVICEIDXY': 'SomeKey1',
                                'ed25519:SomeKey2': 'SomeKey3'},
                        'keys': 'SomeCryptoKey4',
                        'transaction_id': 'SomeTxId'},
                        'type': 'm.key.verification.mac',
                        'sender': '@user2:example.org'},
                    sender='@user2:example.org',
                    transaction_id='SomeTxId',
                    mac={'ed25519:DEVICEIDXY': 'SomeKey1',
                         'ed25519:SomeKey2': 'SomeKey3'},
                    keys='SomeCryptoKey4')
                """
                sas = client.key_verifications[event.transaction_id]
                try:
                    todevice_msg = sas.get_mac()
                except LocalProtocolError as e:
                    # e.g. it might have been cancelled by ourselves
                    print(
                        f"Cancelled or protocol error: Reason: {e}.\n"
                        f"Verification with {event.sender} not concluded. "
                        "Try again?"
                    )
                else:
                    resp = await client.to_device(todevice_msg)
                    if isinstance(resp, ToDeviceError):
                        print(f"to_device failed with {resp}")
                    print(
                        f"sas.we_started_it = {sas.we_started_it}\n"
                        f"sas.sas_accepted = {sas.sas_accepted}\n"
                        f"sas.canceled = {sas.canceled}\n"
                        f"sas.timed_out = {sas.timed_out}\n"
                        f"sas.verified = {sas.verified}\n"
                        f"sas.verified_devices = {sas.verified_devices}\n"
                    )
                    print(
                        "Emoji verification was successful!\n"
                        "Hit Control-C to stop the program or "
                        "initiate another Emoji verification from "
                        "another device or room."
                    )
            else:
                print(
                    f"Received unexpected event type {type(event)}. "
                    f"Event is {event}. Event will be ignored."
                )
        except BaseException:
            print(traceback.format_exc())


def notify(title: str, content: str, image_url: str):
    """Notify OS of message receipt.

    If the system is running headless or any problem happens with
    operating system notifications, ignore it.
    """
    if not HAVE_NOTIFY:
        gs.log.warning(
            "notify2 or dbus is not installed. Notifications will not be "
            "displayed. "
            "Make sure that notify2 and dbus are installed or remove the "
            "--os-notify option."
        )
        return
    try:
        if image_url:
            notused, avatar_file = tempfile.mkstemp()
            urllib.request.urlretrieve(image_url, avatar_file)
            # TODO: cleanup temp files? in cleanup()?
        else:
            # Icon name "notification-message-IM" will work on Ubuntu
            # but not all platforms
            avatar_file = "notification-message-IM"
        notify2.init(PROG_WITHOUT_EXT)
        notify2.Notification(title, content, avatar_file).show()
        gs.log.debug(f"Showed notification for {title}.")
    except Exception:
        gs.log.debug(f"Showing notification for {title} failed.")
        print(traceback.format_exc())
        pass


def is_room_alias(room_id: str) -> bool:
    """Determine if room identifier is a room alias.

    Alias are of syntax: #somealias:someserver

    """
    if room_id and len(room_id) > 3 and room_id[0] == "#":
        return True
    else:
        return False


async def get_avatar_url(client: AsyncClient, user_id: str) -> str:
    """Get https avatar URL for user user_id.

    Returns URL or None if user has no avatar
    """
    avatar_url = None  # default
    resp = await client.get_avatar(user_id)
    if isinstance(resp, ProfileGetAvatarResponse):
        gs.log.debug(f"ProfileGetAvatarResponse. Response is: {resp}")
        avatar_mxc = resp.avatar_url
        gs.log.debug(f"avatar_mxc is {avatar_mxc}")
        if avatar_mxc:  # could be None if no avatar
            avatar_url = await client.mxc_to_http(avatar_mxc)
    else:
        gs.log.info(f"Failed getting avatar from server. {resp}")
    gs.log.debug(f"avatar_url is {avatar_url}")
    return avatar_url


def create_pid_file() -> None:
    """Write PID to disk.

    If possible create a PID file. This is not essential.
    So, if it fails there is no problem. The PID file can
    be helpful to send a kill signal or similar to the process.
    E.g. to stop listening.
    Because the user can start several processes at the same time,
    just having one PID file is not acceptable because a newly started
    process would overwrite the previous PID file. We use UUIDs to make
    each PID file unique.
    """
    try:
        if not os.path.exists(PID_DIR_DEFAULT):
            os.mkdir(PID_DIR_DEFAULT)
            gs.log.debug(f"Create directory {PID_DIR_DEFAULT} for PID file.")
        pid = os.getpid()
        gs.log.debug(f"Trying to create a PID file to store process id {pid}.")
        with open(PID_FILE_DEFAULT, "w") as f:  # overwrite
            f.write(str(pid))
            f.close()
        gs.log.debug(
            f'Successfully created PID file "{PID_FILE_DEFAULT}" '
            f"to store process id {pid}."
        )
    except Exception:
        gs.log.debug(
            f'Failed to create PID file "{PID_FILE_DEFAULT}" '
            f"to store process id {os.getpid()}."
        )


def delete_pid_file() -> None:
    """Remove PID file from disk.

    Clean up by removing PID file.
    It might not exist. So, ignore failures.
    """
    try:
        os.remove(PID_FILE_DEFAULT)
    except Exception:
        gs.log.debug(f'Failed to remove PID file "{PID_FILE_DEFAULT}".')


def cleanup() -> None:
    """Cleanup before quiting program."""
    gs.log.debug("Cleanup: cleaning up.")
    delete_pid_file()


def write_credentials_to_disk(
    homeserver, user_id, device_id, access_token, room_id, credentials_file
) -> None:
    """Write the required login details to disk.

    This file can later be used for logging in
    without using a password.

    Arguments:
    ---------
        homeserver : str
            URL of homeserver, e.g. "https://matrix.example.org"
        user_id : str
            full user id, e.g. "@user:example.org"
        device_id : str
            device id, 10 uppercase letters
        access_token : str
            access token, long cryptographic access token
        room_id : str
            name of room where message will be sent to,
            e.g. "!SomeRoomIdString:example.org"
            user must be member of the provided room
        credentials_file : str
            name/path of file where to store
            credentials information

    """
    # open the credentials file in write-mode
    with open(credentials_file, "w") as f:
        # write the login details to disk
        json.dump(
            {
                # e.g. "https://matrix.example.org"
                "homeserver": homeserver,
                # device ID, 10 uppercase letters
                "device_id": device_id,
                # e.g. "@user:example.org"
                "user_id": user_id,
                # e.g. "!SomeRoomIdString:example.org"
                "room_id": room_id,
                # long cryptographic access token
                "access_token": access_token,
            },
            f,
        )


def read_credentials_from_disk(credentials_file) -> dict:
    """Read the required login details from disk.

    It can then be used to log in without using a password.

    Arguments:
    ---------
    credentials_file : str
        name/path of file to read credentials information from

    """
    # open the file in read-only mode
    with open(credentials_file, "r") as f:
        return json.load(f)


def determine_credentials_file() -> str:
    """Determine the true filename of credentials file.

    Returns filename with full path or None.

    This function checks if a credentials file exists. If no, it will ask
    user questions regrading login, store the info in a newly created
    credentials file and exit.

    If a credentials file exists, it will read it, log into Matrix,
    send a message and exit.

    The credential file will be looked for the following way:
    a) if a path (e.g. "../cred.json") is specified with -t it will be looked
       for there. End of search.
    b) if only a filename without path (e.g. "cred.json") is specified
       first look in the current local directory, if found use it
    c) if only a filename without path (e.g. "cred.json") is specified
       and it cannot be found in the current local directory, then
       look for it in directory $HOME/.config/matrix-commander/
    TLDR: on first run it will be written to current local directory
       or to path specified with --credentials command line argument.
       On further reads, program will look in currently local directory
       or in path specified with --credentials command line argument.
       If not found there (and only filename without path given),
       as a secondary choice program will look for it in
       directory $HOME/.config/matrix-commander/

    """
    credentials_file = gs.pa.credentials  # default location
    if (not os.path.isfile(gs.pa.credentials)) and (
        gs.pa.credentials == os.path.basename(gs.pa.credentials)
    ):
        gs.log.debug(
            "Credentials file does not exist locally. "
            "File name has no path."
        )
        credentials_file = CREDENTIALS_DIR_LASTRESORT + "/" + gs.pa.credentials
        gs.log.debug(
            f'Trying path "{credentials_file}" as last resort. '
            "Suggesting to look for it there."
        )
        if os.path.isfile(credentials_file):
            gs.log.debug(
                "We found the file. It exists in the last resort "
                f'directory "{credentials_file}". '
                "Suggesting to use this one."
            )
        else:
            gs.log.debug(
                "File does not exists either in the last resort "
                "directory or the local directory. "
                "File not found anywhere. One will have to be "
                "created. So we suggest the local directory."
            )
            credentials_file = gs.pa.credentials
    else:
        if os.path.isfile(gs.pa.credentials):
            gs.log.debug(
                "Credentials file existed. "
                "So this is the one we suggest to use. "
                f"file: {credentials_file}"
            )
        else:
            gs.log.debug(
                "Credentials file was specified with full path. "
                "So we suggest that one. "
                f"file: {credentials_file}"
            )
    # The returned file (with or without path)  might or might not exist.
    # But if it does not exist, it is either a full path, or local.
    # We do not want to return the last resort path if it does not exist,
    # so that when it is created it is created where specifically specified
    # or in local dir (but not in last resort dir ~/.config/...)
    return credentials_file


def determine_store_dir() -> str:
    """Determine the true full directory name of store directory.

    Returns filename with full path (a dir) or None.

    For historic reasons:
    If --encrypted (encrypted) is NOT turned on, return None.

    The store path will be looked for the following way:
    gs.pa.store provides either default value or user specified value
    a) First looked at default/specified value. If dir exists,
       use it, end of search.
    b) if last-resort store dir exists, use it, end of search.
    c) if only a dirname without path (e.g. "store") is specified
       and it cannot be found in the current local directory, then
       look for it in last-resort path.
    TLDR: The program will look in path specified with --store
       command line argument. If not found there in default
       local dir. If not found there in last-resort dir.
       If not found there (and only dirname without path given),
       as a final choice, the program will look for it in
       last resort path.
    If not found anywhere, it will return default/specified value.

    """
    if not gs.pa.store:
        return None
    if not gs.pa.encrypted:
        return None
    pargs_store_norm = os.path.normpath(gs.pa.store)  # normailzed for humans
    if os.path.isdir(gs.pa.store):
        gs.log.debug(
            "Found an existing store in directory "
            f'"{pargs_store_norm}" (local or arguments). '
            "It will be used."
        )
        return pargs_store_norm
    text0 = "Could not find an existing store directory anywhere. "
    if gs.pa.store != STORE_DIR_DEFAULT and gs.pa.store != os.path.basename(
        gs.pa.store
    ):
        text0 = (
            f'Store directory "{pargs_store_norm}" was specified by '
            "user, it is a directory with a path, but the directory "
            "does not exist. "
        )
        # fall through towards ending of function to print and return value
        # create in the specified, directory with path
    if gs.pa.store == STORE_DIR_DEFAULT and os.path.isdir(
        STORE_DIR_LASTRESORT
    ):
        gs.log.debug(
            "Store was not found in default local directory. "
            "But found an existing store directory in "
            f'"{STORE_DIR_LASTRESORT}" directory. '
            "It will be used."
        )
        return STORE_DIR_LASTRESORT

    if gs.pa.store == os.path.basename(gs.pa.store):
        gs.log.debug(
            f'Store directory "{pargs_store_norm}" is just a name '
            "without a path. Already looked locally, but not found "
            "locally. So now looking for it in last-resort path."
        )
        last_resort = os.path.normpath(
            STORE_PATH_LASTRESORT + "/" + gs.pa.store
        )
        if os.path.isdir(last_resort):
            gs.log.debug(
                "Found an existing store directory in "
                f'"{last_resort}" directory. It will be used.'
            )
            return last_resort
    text1 = "There are 2 possibilities:"
    text2 = (
        f"1) This is the first time you use {PROG_WITHOUT_EXT} or you want "
        "to create a new store. "
        "In this first case just continue, and a new store will be created. "
        "It will need to be verified. "
        "The store directory will be created in the directory "
        f'"{pargs_store_norm}". '
        "Optionally, consider moving he persistant storage directory files "
        f'inside "{pargs_store_norm}" into '
        f'the directory "{STORE_DIR_LASTRESORT}" '
        "for a more consistent experience."
    )
    text3 = (
        "2) You specified the store location incorrectly or you started "
        f"{PROG_WITHOUT_EXT} from the wrong directory. "
        "In this second case abort, change you directory if needed or set the "
        f"store option correctly. Then start {PROG_WITHOUT_EXT} again."
    )
    gs.log.debug(text0 + "\n" + text1 + "\n" + text2 + "\n" + text3)
    print(
        textwrap.fill(
            text0,
            width=79,
            subsequent_indent=SEP,
        )
    )
    print(
        textwrap.fill(
            text1,
            width=79,
            subsequent_indent=SEP,
        )
    )
    print(
        textwrap.fill(
            text2,
            width=79,
            subsequent_indent=SEP,
        )
    )
    print(
        textwrap.fill(
            text3,
            width=79,
            subsequent_indent=SEP,
        )
    )
    return pargs_store_norm  # create in the specified, local dir without path


async def determine_dm_rooms(
    users: list, client: AsyncClient, credentials: dict
) -> list:
    """Determine the rooms to send to.

    Users can be specified with --user for send and listen operations.
    These rooms we label DM (direct messaging) rooms.
    By that we means rooms that only have 2 members, and these two
    members being the sender and the recipient in question.
    We do not care about 'is_group' or 'is_direct' flags (hints).

    If given a user and known the sender, we try to find a matching room.
    There might be 0, 1, or more matching rooms. If 0, then giver error
    and the user should run --room-invite first. if 1 found, use it.
    If more than 1 found, just use 1 of them arbitrarily.

    The steps are:
    - get all rooms where sender is member
    - get all members to these rooms
    - check if there is a room with just 2 members and them
      being sender and recipient (user from users arg)

    In order to match a user to a RoomMember we allow 3 choices:
    - user_id: perfect match, is unique, full user id, e.g. "@user:example.org"
    - user_id without homeserver domain: partial user id, e.g. "@user"
      this partial user will be completed by adding the homeserver of the
      sender to the end, i.e. assuming that sender and receiver are on the
      same homeserver.
    - display name: be careful, display names are NOT unique, you could be
      mistaken and by error send to the wrong person.
      '--joined-members "*"' shows you the display names in the middle column

    Arguments:
    ---------
        users: list(str): list of user_ids
            try to find a matching DM room for each user
        client: AsyncClient: client, allows as to query the server
        credentials: dict: allows to get the user_id of sender

    Returns a list of found DM rooms. List may be empty if no matches were
    found.

    """
    rooms = []
    if not users:
        gs.log.debug(f"Room(s) from --user: {rooms}, no users were specified.")
        return rooms
    sender = credentials["user_id"]  # who am i
    domain = sender.partition(":")[2]
    gs.log.debug(f"Trying to get members for all rooms of sender: {sender}")
    resp = await client.joined_rooms()
    if isinstance(resp, JoinedRoomsError):
        gs.log.error(
            f"joined_rooms failed with {resp}. Not able to "
            "get all rooms. "
            f"Not able to find DM rooms for sender {sender}. "
            f"Not able to send to receivers {users}."
        )
        senderrooms = []
    else:
        gs.log.debug(f"joined_rooms successful with {resp}")
        senderrooms = resp.rooms
    room_found_for_users = []
    for room in senderrooms:
        resp = await client.joined_members(room)
        if isinstance(resp, JoinedMembersError):
            gs.log.error(
                f"joined_members failed with {resp}. Not able to "
                f"get room members for room {room}. "
                f"Not able to find DM rooms for sender {sender}. "
                f"Not able to send to some of these receivers {users}."
            )
        else:
            # resp.room_id
            # resp.members = List[RoomMember] ; RoomMember
            # member.user_id
            # member.display_name
            # member.avatar_url
            gs.log.debug(f"joined_members successful with {resp}")
            if resp.members and len(resp.members) == 2:
                if resp.members[0].user_id == sender:
                    # sndr = resp.members[0]
                    rcvr = resp.members[1]
                elif resp.members[1].user_id == sender:
                    # sndr = resp.members[1]
                    rcvr = resp.members[0]
                else:
                    # sndr = None
                    rcvr = None
                    gs.log.error(f"Sender does not match {resp}")
                for user in users:
                    if (
                        rcvr
                        and user == rcvr.user_id
                        or user + ":" + domain == rcvr.user_id
                        or user == rcvr.display_name
                    ):
                        room_found_for_users.append(user)
                        rooms.append(resp.room_id)
    for user in users:
        if user not in room_found_for_users:
            gs.log.error(
                "Room(s) were specified for a DM (direct messaging) "
                "send operation via --room. But no DM room was "
                f"found for user '{user}'. "
                "Try setting up a room first via --room-create and "
                "--room-invite option."
            )
    rooms = list(dict.fromkeys(rooms))  # remove duplicates in list
    gs.log.debug(f"Room(s) from --user: {rooms}")
    return rooms


async def determine_rooms(
    room_id: str, client: AsyncClient, credentials: dict
) -> list:
    """Determine the room to send to.

    Arguments:
    ---------
    room_id : room from credentials file

    Look at room from credentials file and at rooms from command line
    and prepares a definite list of rooms.

    New: Also look at --user. For DM (direct messaging), destinations
    are specified via --user. For every user found, see if there is a
    "DM" room, a room with only 2 members (sender and recipient).
    If such a "DM" room is found, add it to the general rooms list
    that is returned.

    Mixing and matching of --room and --user is possible.
    --room R1 R2 --user U1 U2 might lead to 4 rooms in total.
    If no "DM" room is found then give error and tell user to do
    --room-invite first.

    Return list of rooms to send to. Returned list is never empty.

    """
    if not gs.pa.room and not gs.pa.user:
        gs.log.debug(
            "Room id was provided via credentials file. "
            "No rooms given in commands line. "
            "No users given in command line for DM rooms. "
            f'Setting rooms to "{room_id}".'
        )
        return [room_id]  # list of 1
    rooms = []
    if gs.pa.room:
        for room in gs.pa.room:
            room_id = room.replace(r"\!", "!")  # remove possible escape
            rooms.append(room_id)
        gs.log.debug(f"Room(s) from --room: {rooms}")
    rooms += await determine_dm_rooms(gs.pa.user, client, credentials)
    gs.log.debug(
        "Room(s) or user(s) were provided via command line. "
        "Overwriting room id from credentials file "
        f'with rooms "{rooms}" '
        "from command line."
    )
    return rooms


async def map_roomalias_to_roomid(client, alias) -> str:
    """Attempt to convert room alias to room_id.

    Arguments:
    ---------
    client : nio client
    alias : can be an alias in the form of '#someRoomALias:example.com'
        can also be a room_id in the form of '!someRoomId:example.com'

    room_id : room from credentials file

    If an alias try to get the corresponding room_id.
    If anything fails it returns the original input.

    Return corresponding room_id or on failure the original alias.

    """
    ret = alias
    if is_room_alias(alias):
        resp = await client.room_resolve_alias(alias)
        if isinstance(resp, RoomResolveAliasError):
            gs.log.error(
                f"room_resolve_alias for alias {alias} failed with {resp}. "
                f"Trying operation with input {alias} anyway. Might fail."
            )
        else:
            ret = resp.room_id
            gs.log.debug(
                f'Mapped room alias "{alias}" to room id "{ret}". '
                f"({resp.room_alias}, {resp.room_id})."
            )
    return ret


async def create_rooms(client, room_aliases, names, topics):
    """Create one or multiple rooms.

    Arguments:
    ---------
    client : nio client
    room_aliases : list of room aliases in the form of "sampleAlias"
            These aliases will then be used by the server and
            the server creates the definite alias in the form
            of "#sampleAlias:example.com" from it.
            Do not attempt to use "#sampleAlias:example.com"
            as it will confuse the server.
    names : list of names for rooms
    topics : list of room topics

    """
    try:
        index = 0
        gs.log.debug(
            f'Trying to create rooms with room aliases "{room_aliases}", '
            f'names "{names}", and topics "{topics}".'
        )
        for alias in room_aliases:
            alias = alias.replace(r"\!", "!")  # remove possible escape
            # alias is a true alias, not a room id
            # "alias1" will be converted into "#alias1:example.com"
            try:
                name = names[index]
            except (IndexError, TypeError):
                name = ""
            try:
                topic = topics[index]
            except (IndexError, TypeError):
                topic = ""
            gs.log.debug(
                f'Creating room with room alias "{alias}", '
                f'name "{name}", and topic "{topic}".'
            )
            resp = await client.room_create(
                alias=alias,
                name=name,  # room name
                topic=topic,  # room topic
                initial_state=[EnableEncryptionBuilder().as_dict()],
            )
            if isinstance(resp, RoomCreateError):
                gs.log.error(f"Room_create failed with {resp}")
            else:
                gs.log.info(f'Created room "{alias}".')
            index = index + 1
    except Exception:
        gs.log.error("Room creation failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def join_rooms(client, rooms):
    """Join one or multiple rooms."""
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            room_id = room_id.replace(r"\!", "!")  # remove possible escape
            gs.log.debug(f'Joining room with room alias "{room_id}".')
            room_id = await map_roomalias_to_roomid(client, room_id)
            resp = await client.join(room_id)
            if isinstance(resp, JoinError):
                gs.log.error(f"join failed with {resp}")
            else:
                gs.log.info(f'Joined room "{room_id}" successfully.')
    except Exception:
        gs.log.error("Joining rooms failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def leave_rooms(client, rooms):
    """Leave one or multiple rooms."""
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            room_id = room_id.replace(r"\!", "!")  # remove possible escape
            gs.log.debug(f'Leaving room with room alias "{room_id}".')
            room_id = await map_roomalias_to_roomid(client, room_id)
            resp = await client.room_leave(room_id)
            if isinstance(resp, RoomLeaveError):
                gs.log.error(f"Leave failed with {resp}")
            else:
                gs.log.info(f'Left room "{room_id}".')
    except Exception:
        gs.log.error("Room leave failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def forget_rooms(client, rooms):
    """Forget one or multiple rooms."""
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            room_id = room_id.replace(r"\!", "!")  # remove possible escape
            gs.log.debug(f'Forgetting room with room alias "{room_id}".')
            room_id = await map_roomalias_to_roomid(client, room_id)
            resp = await client.room_forget(room_id)
            if isinstance(resp, RoomForgetError):
                gs.log.error(f"Forget failed with {resp}")
            else:
                gs.log.info(f'Forgot room "{room_id}".')
    except Exception:
        gs.log.error("Room forget failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def invite_to_rooms(client, rooms, users):
    """Invite one or multiple users to one or multiple rooms."""
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            room_id = room_id.replace(r"\!", "!")  # remove possible escape
            room_id = await map_roomalias_to_roomid(client, room_id)
            for user in users:
                gs.log.debug(
                    f'Inviting user "{user}" to room with '
                    f'room alias "{room_id}".'
                )
                resp = await client.room_invite(room_id, user)
                if isinstance(resp, RoomInviteError):
                    gs.log.error(f"room_invite failed with {resp}")
                else:
                    gs.log.info(
                        f'User "{user}" was successfully invited '
                        f'to room "{room_id}".'
                    )
    except Exception:
        gs.log.error("User invite failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def ban_from_rooms(client, rooms, users):
    """Ban one or multiple users from one or multiple rooms."""
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            room_id = room_id.replace(r"\!", "!")  # remove possible escape
            room_id = await map_roomalias_to_roomid(client, room_id)
            for user in users:
                gs.log.debug(
                    f'Banning user "{user}" from room with '
                    f'room alias "{room_id}".'
                )
                resp = await client.room_ban(room_id, user)
                if isinstance(resp, RoomBanError):
                    gs.log.error(f"room_ban failed with {resp}")
                else:
                    gs.log.info(
                        f'User "{user}" was successfully banned '
                        f'from room "{room_id}".'
                    )
    except Exception:
        gs.log.error("User ban failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def unban_from_rooms(client, rooms, users):
    """Unban one or multiple users from one or multiple rooms."""
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            room_id = room_id.replace(r"\!", "!")  # remove possible escape
            room_id = await map_roomalias_to_roomid(client, room_id)
            for user in users:
                gs.log.debug(
                    f'Unbanning user "{user}" from room with '
                    f'room alias "{room_id}".'
                )
                resp = await client.room_unban(room_id, user)
                if isinstance(resp, RoomUnbanError):
                    gs.log.error(f"room_unban failed with {resp}")
                else:
                    gs.log.info(
                        f'User "{user}" was successfully unbanned '
                        f'from room "{room_id}".'
                    )
    except Exception:
        gs.log.error("User unban failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def kick_from_rooms(client, rooms, users):
    """Kick one or multiple users from one or multiple rooms."""
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            room_id = room_id.replace(r"\!", "!")  # remove possible escape
            room_id = await map_roomalias_to_roomid(client, room_id)
            for user in users:
                gs.log.debug(
                    f'Kicking user "{user}" from room with '
                    f'room alias "{room_id}".'
                )
                resp = await client.room_kick(room_id, user)
                if isinstance(resp, RoomKickError):
                    gs.log.error(f"room_kick failed with {resp}")
                else:
                    gs.log.info(
                        f'User "{user}" was successfully kicked '
                        f'from room "{room_id}".'
                    )
    except Exception:
        gs.log.error("User kick failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


# according to linter: function is too complex, C901
async def send_event(client, rooms, event):  # noqa: C901
    """Process event.

    Arguments:
    ---------
    client : Client
    rooms : list
        list of room_id-s
    event : str
        file name of event from --event argument

    """
    if not rooms:
        gs.log.info(
            "No rooms are given. This should not happen. "
            "Maybe your DM rooms specified via --user were not found. "
            "This file is being droppend and NOT sent."
        )
        return

    if event == "-":  # - means read as pipe from stdin
        jsondata = sys.stdin.buffer.read().decode()  # binary read
    else:
        with open(event, "r") as file:
            jsondata = file.read()
    gs.log.debug(
        f"{len(jsondata)} bytes of event data read from file {event}."
    )
    gs.log.debug(f"Event {event} contains this JSON data: {jsondata}")

    if not jsondata.strip():
        gs.log.debug(
            "Event is empty. This event is being droppend and NOT sent."
        )
        return

    try:
        content_json = json.loads(jsondata)
        message_type = content_json["type"]
        content = content_json["content"]
    except Exception:
        gs.log.warning(
            "Event is not a valid JSON object or not of Matrix JSON format. "
            "This event is being droppend and NOT sent."
        )
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())
        return

    try:
        for room_id in rooms:
            await client.room_send(
                room_id, message_type=message_type, content=content
            )
            gs.log.info(f'This event was sent: "{event}" to room "{room_id}".')
    except Exception:
        gs.log.error(f"Event send of file {event} failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


# according to linter: function is too complex, C901
async def send_file(client, rooms, file):  # noqa: C901
    """Process file.

    Upload file to server and then send link to rooms.
    Works and tested for .pdf, .txt, .ogg, .wav.
    All these file types are treated the same.

    Do not use this function for images.
    Use the send_image() function for images.

    Matrix has types for audio and video (and image and file).
    See: "msgtype" == "m.image", m.audio, m.video, m.file

    Arguments:
    ---------
    client : Client
    rooms : list
        list of room_id-s
    file : str
        file name of file from --file argument

    This is a working example for a PDF file.
    It can be viewed or downloaded from:
    https://matrix.example.com/_matrix/media/r0/download/
        example.com/SomeStrangeUriKey
    {
        "type": "m.room.message",
        "sender": "@someuser:example.com",
        "content": {
            "body": "example.pdf",
            "info": {
                "size": 6301234,
                "mimetype": "application/pdf"
                },
            "msgtype": "m.file",
            "url": "mxc://example.com/SomeStrangeUriKey"
        },
        "origin_server_ts": 1595100000000,
        "unsigned": {
            "age": 1000,
            "transaction_id": "SomeTxId01234567"
        },
        "event_id": "$SomeEventId01234567789Abcdef012345678",
        "room_id": "!SomeRoomId:example.com"
    }

    """
    if not rooms:
        gs.log.info(
            "No rooms are given. This should not happen. "
            "Maybe your DM rooms specified via --user were not found. "
            "This file is being droppend and NOT sent."
        )
        return

    # for more comments on how to treat pipe on stdin please read the
    # comments in send_image()

    if file == "-":  # - means read as pipe from stdin
        isPipe = True
        fin_buf = sys.stdin.buffer.read()
        len_fin_buf = len(fin_buf)
        file = "mc-" + str(uuid.uuid4()) + ".tmp"
        gs.log.debug(
            f"{len_fin_buf} bytes of file data read from stdin. "
            f'Temporary file "{file}" was created for file.'
        )
        fout = open(file, "wb")
        fout.write(fin_buf)
        fout.close()
    else:
        isPipe = False

    if not os.path.isfile(file):
        gs.log.debug(
            f"File {file} is not a file. Doesn't exist or "
            "is a directory. "
            "This file is being droppend and NOT sent."
        )
        return

    # # restrict to "txt", "pdf", "mp3", "ogg", "wav", ...
    # if not re.match("^.pdf$|^.txt$|^.doc$|^.xls$|^.mobi$|^.mp3$",
    #                os.path.splitext(file)[1].lower()):
    #    gs.log.debug(f"File {file} is not a permitted file type. Should be "
    #                 ".pdf, .txt, .doc, .xls, .mobi or .mp3 ... "
    #                 f"[{os.path.splitext(file)[1].lower()}]"
    #                 "This file is being droppend and NOT sent.")
    #    return

    # 'application/pdf' "plain/text" "audio/ogg"
    mime_type = magic.from_file(file, mime=True)
    # if ((not mime_type.startswith("application/")) and
    #        (not mime_type.startswith("plain/")) and
    #        (not mime_type.startswith("audio/"))):
    #    gs.log.debug(f"File {file} does not have an accepted mime type. "
    #                 "Should be something like application/pdf. "
    #                 f"Found mime type {mime_type}. "
    #                 "This file is being droppend and NOT sent.")
    #    return

    # first do an upload of file, see upload() documentation
    # http://matrix-nio.readthedocs.io/en/latest/nio.html#nio.AsyncClient.upload
    # then send URI of upload to room

    file_stat = await aiofiles.os.stat(file)
    async with aiofiles.open(file, "r+b") as f:
        resp, decryption_keys = await client.upload(
            f,
            content_type=mime_type,  # application/pdf
            filename=os.path.basename(file),
            filesize=file_stat.st_size,
            encrypt=True,
        )
    if isinstance(resp, UploadResponse):
        gs.log.debug(
            f"File was uploaded successfully to server. Response is: {resp}"
        )
    else:
        gs.log.info(
            f"The program {PROG_WITH_EXT} failed to upload. "
            "Please retry. This could be temporary issue on "
            "your server. "
            "Sorry."
        )
        gs.log.info(
            f'file="{file}"; mime_type="{mime_type}"; '
            f'filessize="{file_stat.st_size}"'
            f"Failed to upload: {resp}"
        )

    # determine msg_type:
    if mime_type.startswith("audio/"):
        msg_type = "m.audio"
    elif mime_type.startswith("video/"):
        msg_type = "m.video"
    else:
        msg_type = "m.file"

    content = {
        "body": os.path.basename(file),  # descriptive title
        "info": {"size": file_stat.st_size, "mimetype": mime_type},
        "msgtype": msg_type,
        "file": {
            "url": resp.content_uri,
            "key": decryption_keys["key"],
            "iv": decryption_keys["iv"],
            "hashes": decryption_keys["hashes"],
            "v": decryption_keys["v"],
        },
    }

    if isPipe:
        # rm temp file
        os.remove(file)

    try:
        for room_id in rooms:
            await client.room_send(
                room_id, message_type="m.room.message", content=content
            )
            gs.log.info(f'This file was sent: "{file}" to room "{room_id}".')
    except Exception:
        gs.log.error(f"File send of file {file} failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


# according to linter: function is too complex, C901
async def send_image(client, rooms, image):  # noqa: C901
    """Process image.

    Arguments:
    ---------
    client : Client
    rooms : list
        list of room_id-s
    image : str
        file name of image from --image argument

    This is a working example for a JPG image.
    It can be viewed or downloaded from:
    https://matrix.example.com/_matrix/media/r0/download/
        example.com/SomeStrangeUriKey
    {
        "type": "m.room.message",
        "sender": "@someuser:example.com",
        "content": {
            "body": "someimage.jpg",
            "info": {
                "size": 5420,
                "mimetype": "image/jpeg",
                "thumbnail_info": {
                    "w": 100,
                    "h": 100,
                    "mimetype": "image/jpeg",
                    "size": 2106
                },
                "w": 100,
                "h": 100,
                "thumbnail_url": "mxc://example.com/SomeStrangeThumbnailUriKey"
            },
            "msgtype": "m.image",
            "url": "mxc://example.com/SomeStrangeUriKey"
        },
        "origin_server_ts": 12345678901234576,
        "unsigned": {
            "age": 268
        },
        "event_id": "$skdhGJKhgyr548654YTr765Yiy58TYR",
        "room_id": "!JKHgyHGfytHGFjhgfY:example.com"
    }

    """
    if not rooms:
        gs.log.warning(
            "No rooms are given. This should not happen. "
            "Maybe your DM rooms specified via --user were not found. "
            "This image is being droppend and NOT sent."
        )
        return

    # how to treat pipe on stdin?
    # aiofiles.open(sys.stdin, "r+b") does not work, wrong type.
    # aiofiles.open(sys.stdin.buffer, "r+b") does not work, wrong type.
    # aiofiles.open('/dev/stdin', mode='rb') fails with error:
    #    io.UnsupportedOperation: File or stream is not seekable
    # stdin, _ = await aioconsole.get_standard_streams() also failes
    # Hence I see no way to directly hand stdin to aiofiles.
    # Problem: I cannot combine the 3 things:
    #    stdin + aiofiles + nio.AsyncClient.upload()
    # Since I could not overcome this problem I generate a temporary file

    if image == "-":  # - means read as pipe from stdin
        isPipe = True
        fin_buf = sys.stdin.buffer.read()
        len_fin_buf = len(fin_buf)
        image = "mc-" + str(uuid.uuid4()) + ".tmp"
        gs.log.debug(
            f"{len_fin_buf} bytes of image data read from stdin. "
            f'Temporary file "{image}" was created for image.'
        )
        fout = open(image, "wb")
        fout.write(fin_buf)
        fout.close()
    else:
        isPipe = False

    if not os.path.isfile(image):
        gs.log.warning(
            f"Image file {image} is not a file. Doesn't exist or "
            "is a directory. "
            "This image is being dropped and NOT sent."
        )
        return

    # "bmp", "gif", "jpg", "jpeg", "png", "pbm", "pgm", "ppm", "xbm", "xpm",
    # "tiff", "webp", "svg",

    if not isPipe and not re.match(
        "^.jpg$|^.jpeg$|^.gif$|^.png$|^.svg$",
        os.path.splitext(image)[1].lower(),
    ):
        gs.log.warning(
            f"Image file {image} is not an image file. Should be "
            ".jpg, .jpeg, .gif, or .png. "
            f"[{os.path.splitext(image)[1].lower()}] "
            "This image is being dropped and NOT sent."
        )
        return

    # 'application/pdf' "image/jpeg"
    mime_type = magic.from_file(image, mime=True)
    if not mime_type.startswith("image/"):
        gs.log.warning(
            f"Image file {image} does not have an image mime type. "
            "Should be something like image/jpeg. "
            f"Found mime type {mime_type}. "
            "This image is being droppend and NOT sent."
        )
        return

    im = Image.open(image)
    (width, height) = im.size  # im.size returns (width,height) tuple

    # first do an upload of image, see upload() documentation
    # http://matrix-nio.readthedocs.io/en/latest/nio.html#nio.AsyncClient.upload
    # then send URI of upload to room
    # Note that encrypted upload works even with unencrypted rooms; the
    # decryption keys will not be protected, obviously, but no special
    # treatment is required.

    file_stat = await aiofiles.os.stat(image)
    async with aiofiles.open(image, "r+b") as f:
        resp, decryption_keys = await client.upload(
            f,
            content_type=mime_type,  # image/jpeg
            filename=os.path.basename(image),
            filesize=file_stat.st_size,
            encrypt=True,
        )
    if isinstance(resp, UploadResponse):
        gs.log.debug(
            "Image was uploaded successfully to server. "
            f"Response is: {resp}"
        )
    else:
        gs.log.info(
            f"The program {PROG_WITH_EXT} failed to upload. "
            "Please retry. This could be temporary issue on "
            "your server. "
            "Sorry."
        )
        gs.log.info(
            f'file="{image}"; mime_type="{mime_type}"; '
            f'filessize="{file_stat.st_size}"'
            f"Failed to upload: {resp}"
        )

    # TODO compute thumbnail, upload thumbnail to Server
    # TODO add thumbnail info to `content`

    content = {
        "body": os.path.basename(image),  # descriptive title
        "info": {
            "size": file_stat.st_size,
            "mimetype": mime_type,
            "thumbnail_info": None,  # TODO
            "w": width,  # width in pixel
            "h": height,  # height in pixel
            "thumbnail_url": None,  # TODO
            # "thumbnail_file": None,
        },
        "msgtype": "m.image",
        "file": {
            "url": resp.content_uri,
            "key": decryption_keys["key"],
            "iv": decryption_keys["iv"],
            "hashes": decryption_keys["hashes"],
            "v": decryption_keys["v"],
        },
    }

    if isPipe:
        # rm temp file
        os.remove(image)

    try:
        for room_id in rooms:
            await client.room_send(
                room_id, message_type="m.room.message", content=content
            )
            gs.log.info(
                f'This image file was sent: "{image}" to room "{room_id}".'
            )
    except Exception:
        gs.log.error(f"Image send of file {image} failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


# according to linter: function is too complex, C901
async def send_message(client, rooms, message):  # noqa: C901
    """Process message.

    Format messages according to instructions from command line arguments.
    Then send all messages to all rooms.

    Arguments:
    ---------
    client : Client
    rooms : list
        list of room_id-s
    message : str
        message to send as read from -m, pipe or keyboard
        message is without mime formatting

    """
    if not rooms:
        gs.log.info(
            "No rooms are given. This should not happen. "
            "Maybe your DM rooms specified via --user were not found. "
            "This text message is being droppend and NOT sent."
        )
        return
    # remove leading AND trailing newlines to beautify
    message = message.strip("\n")

    if message == "" or message.strip() == "":
        gs.log.debug(
            "The message is empty. "
            "This message is being droppend and NOT sent."
        )
        return

    if gs.pa.notice:
        content = {"msgtype": "m.notice"}
    else:
        content = {"msgtype": "m.text"}

    if gs.pa.code:
        gs.log.debug('Sending message in format "code".')
        formatted_message = "<pre><code>" + message + "\n</code></pre>\n"
        content["format"] = "org.matrix.custom.html"  # add to dict
        content["formatted_body"] = formatted_message
        # next line: work-around for Element Android
        message = "```\n" + message + "\n```"  # to format it as code
    elif gs.pa.markdown:
        gs.log.debug(
            "Converting message from MarkDown into HTML. "
            'Sending message in format "markdown".'
        )
        # e.g. converts from "-abc" to "<ul><li>abc</li></ul>"
        formatted_message = markdown(message)
        content["format"] = "org.matrix.custom.html"  # add to dict
        content["formatted_body"] = formatted_message
    elif gs.pa.html:
        gs.log.debug('Sending message in format "html".')
        formatted_message = message  # the same for the time being
        content["format"] = "org.matrix.custom.html"  # add to dict
        content["formatted_body"] = formatted_message
    else:
        gs.log.debug('Sending message in format "text".')
    content["body"] = message

    try:
        for room_id in rooms:
            if is_room_alias(room_id):
                resp = await client.room_resolve_alias(room_id)
                if isinstance(resp, RoomResolveAliasError):
                    print(f"room_resolve_alias failed with {resp}")
                room_id = resp.room_id
                gs.log.debug(
                    f'Mapping room alias "{resp.room_alias}" to '
                    f'room id "{resp.room_id}".'
                )
            await client.room_send(
                room_id,
                message_type="m.room.message",
                content=content,
                ignore_unverified_devices=True,
            )
            gs.log.info(
                f'This message was sent: "{message}" to room "{room_id}".'
            )
    except Exception:
        gs.log.error("Message send failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


def get_messages_from_pipe() -> list:
    """Read input from pipe if available.

    Return [] if no input available on pipe stdin.
    Return ["some-msg"] if input is availble.
    Might also return [""] of course if "" was in pipe.
    Currently there is at most 1 msg in the returned list.
    """
    messages = []
    stdin_ready = select.select([sys.stdin,], [], [], 0.0)[  # noqa
        0
    ]  # noqa
    if not stdin_ready:
        gs.log.debug(
            "stdin is not ready. "
            "A pipe could be used, but pipe could be empty, "
            "stdin could also be a keyboard."
        )
    else:
        gs.log.debug(
            "stdin is ready. Something "
            "is definitely piped into program from stdin."
            "Reading message from stdin pipe."
        )
    if ((not stdin_ready) and (not sys.stdin.isatty())) or stdin_ready:
        if not sys.stdin.isatty():
            gs.log.debug(
                "Pipe was definitely used, but pipe might be empty. "
                "Trying to read from pipe in any case."
            )
        message = ""
        try:
            for line in sys.stdin:
                message += line
            gs.log.debug("Using data from stdin pipe as message.")
            messages.append(message)
        except EOFError:  # EOF when reading a line
            gs.log.debug(
                "Reading from stdin resulted in EOF. This can happen "
                "when a pipe was used, but the pipe is empty. "
                "No message will be generated."
            )
        except UnicodeDecodeError:
            gs.log.info(
                "Reading from stdin resulted in UnicodeDecodeError. This "
                "can happen if you try to pipe binary data for a text "
                "message. For a text message only pipe text via stdin, "
                "not binary data. No message will be generated."
            )
    return messages


def get_messages_from_keyboard() -> list:
    """Read input from keyboard but only if no other messages are available.

    If there is a message provided via --message argument, no message
    will be read from keyboard.
    If there are other send operations like --image, --file, etc. are
    used, no message will be read from keyboard.
    If there is a message provided via stdin input pipe, no message
    will be read from keyboard.
    In short, we only read from keyboard as last resort, if no messages are
    specified or provided anywhere and no other send-operations like
    --image, --event, etc. are performed.

    Return [] if no input available on keyboard.
    Return ["some-msg"] if input is availble on keyboard.
    Might also return [""] of course if "" keyboard entry was empty.
    Currently there is at most 1 msg in the returned list.
    """
    messages = []
    if gs.pa.message:
        gs.log.debug(
            "Don't read from keyboard because there are "
            "messages provided in arguments with -m."
        )
        return messages  # return empty list because mesgs in -m
    if (
        gs.pa.image
        or gs.pa.audio
        or gs.pa.file
        or gs.pa.event
        or gs.pa.version
    ):
        gs.log.debug(
            "Don't read from keyboard because there are "
            "other send operations or --version provided in arguments."
        )
        return messages  # return empty list because mesgs in -m
    stdin_ready = select.select([sys.stdin,], [], [], 0.0)[  # noqa
        0
    ]  # noqa
    if not stdin_ready:
        gs.log.debug(
            "stdin is not ready. "
            "A pipe could be used, but pipe could be empty, "
            "stdin could also be a keyboard."
        )
    else:
        gs.log.debug(
            "stdin is ready. Something "
            "is definitely piped into program from stdin."
            "Reading message from stdin pipe."
        )
    if (not stdin_ready) and (sys.stdin.isatty()):
        # because sys.stdin.isatty() is true
        gs.log.debug(
            "No pipe was used, so read input from keyboard. "
            "Reading message from keyboard"
        )
        try:
            message = input("Enter message to send: ")
            gs.log.debug("Using data from stdin keyboard as message.")
            messages.append(message)
        except EOFError:  # EOF when reading a line
            gs.log.debug(
                "Reading from stdin resulted in EOF. "
                "Reading from keyboard failed. "
                "No message will be generated."
            )
    return messages


async def send_messages_and_files(client, rooms, messages):
    """Send text messages and files.

    First images, audio, etc, then text messaged.

    Arguments:
    ---------
    client : Client
    rooms : list of room_ids
    messages : list of messages to send

    """
    if gs.pa.image:
        for image in gs.pa.image:
            await send_image(client, rooms, image)

    if gs.pa.audio:
        for audio in gs.pa.audio:
            # audio file can be sent like other files
            await send_file(client, rooms, audio)

    if gs.pa.file:
        for file in gs.pa.file:
            await send_file(client, rooms, file)

    if gs.pa.event:
        for event in gs.pa.event:
            await send_event(client, rooms, event)

    for message in messages:
        await send_message(client, rooms, message)


async def process_arguments_and_input(client, rooms):
    """Process arguments and all input.

    Process all input: text messages, etc.
    Prepare a list of messages from all sources and then send them.

    Arguments:
    ---------
    client : Client
    rooms : list of room_ids

    """
    messages_from_pipe = []
    if gs.stdin_use == "none":  # STDIN is unused
        messages_from_pipe = get_messages_from_pipe()
    messages_from_keyboard = get_messages_from_keyboard()
    if not gs.pa.message:
        messages_from_commandline = []
    else:
        messages_from_commandline = []
        for m in gs.pa.message:
            if m == "\\-":  # escaped -
                messages_from_commandline += ["-"]
            elif m == "-":  # stdin pipe
                messages_from_commandline += get_messages_from_pipe()
            else:
                messages_from_commandline += [m]

    gs.log.debug(f"Messages from pipe:         {messages_from_pipe}")
    gs.log.debug(f"Messages from keyboard:     {messages_from_keyboard}")
    gs.log.debug(f"Messages from command-line: {messages_from_commandline}")

    messages_all = (
        messages_from_commandline + messages_from_pipe + messages_from_keyboard
    )  # keyboard at end

    # loop thru all msgs and split them
    if gs.pa.split:
        # gs.pa.split can have escape characters, it has to be de-escaped
        decoded_string = bytes(gs.pa.split, "utf-8").decode("unicode_escape")
        gs.log.debug(f'String used for splitting is: "{decoded_string}"')
        messages_all_split = []
        for m in messages_all:
            messages_all_split += m.split(decoded_string)
    else:  # not gs.pa.split
        messages_all_split = messages_all

    await send_messages_and_files(client, rooms, messages_all_split)


# according to pylama: function too complex: C901 # noqa: C901
async def create_credentials_file(  # noqa: C901
    credentials_file: str, store_dir: str
) -> None:
    """Log in, create credentials file, log out and exit.

    Arguments:
    ---------
        credentials_file: str : location of credentials file
        store_dir: str : location of persistent storage store directory

    """
    text0 = f"""
            Credentials file \"{gs.pa.credentials}\" was not found.
            There are 2 possibilities for this."""
    text1 = f"""
            1) This is your first time use? Setting up new credentials?
            Then welcome to {PROG_WITHOUT_EXT}. Continue, and in the next
            step you will be asked for homeserver, user, password and
            room id to create a credentials file."""
    text2 = f"""
            2) You specified the credentials location incorrectly
            or you started {PROG_WITHOUT_EXT} from the wrong directory.
            Abort, change you directory if needed or set the credentials
            option correctly. Then start {PROG_WITHOUT_EXT} again."""
    print(
        textwrap.fill(
            textwrap.dedent(text0).strip(),
            width=79,
            subsequent_indent=SEP,
        )
    )
    print(
        textwrap.fill(
            textwrap.dedent(text1).strip(),
            width=79,
            subsequent_indent=SEP,
        )
    )
    print(
        textwrap.fill(
            textwrap.dedent(text2).strip(),
            width=79,
            subsequent_indent=SEP,
        )
    )
    confirm = input(
        "Continue to create new credentials? (Yes or Ctrl-C to abort) "
    )
    if confirm.lower() != "yes" and confirm.lower() != "y":
        print("")  # add newline to stdout to separate any log info
        raise MatrixCommanderError(
            "Aborting due to user request.",
            traceback=False,
            level="info",
        )
    homeserver = "https://matrix.example.org"
    homeserver = input(f"Enter URL of your homeserver: [{homeserver}] ")
    if not homeserver:
        homeserver = "https://matrix.example.org"  # better error msg later
    if not (
        homeserver.startswith("https://") or homeserver.startswith("http://")
    ):
        homeserver = "https://" + homeserver

    if gs.pa.proxy:
        gs.log.info(f"Proxy {gs.pa.proxy} will be used.")

    # check for password/SSO
    connector = TCPConnector(ssl=gs.ssl)  # setting sslcontext
    async with ClientSession(connector=connector) as session:
        async with session.get(
            f"{homeserver}/_matrix/client/r0/login",
            raise_for_status=True,
            proxy=gs.pa.proxy,
        ) as response:
            flow_types = {
                x["type"] for x in (await response.json()).get("flows", [])
            }
            gs.log.debug("Supported login flows: %r", flow_types)

            password = "m.login.password" in flow_types
            sso = "m.login.sso" in flow_types and "m.login.token" in flow_types

    # SSO: Single Sign-On:
    # see https://matrix.org/docs/guides/sso-for-client-developers
    if sso:
        gs.log.debug("Server supports SSO for login.")
        if gs.pa.no_sso:
            gs.log.debug('Due to "--no-sso" argument, SSO will be avoided.')
            sso = False  # override sso due to --no-sso flag set
    else:
        gs.log.debug(
            "Server does not support SSO for login. "
            "Hence, attempting to login with password."
        )

    if not sso and password:

        user_id = "@user:example.org"
        user_id = input(f"Enter your full user ID: [{user_id}] ")
    else:
        user_id = ""

    device_name = PROG_WITHOUT_EXT
    device_name = input(f"Choose a name for this device: [{device_name}] ")
    if device_name == "":
        device_name = PROG_WITHOUT_EXT  # default
    room_id = "!SomeRoomIdString:example.org"
    room_id = input(f"Enter your room ID: [{room_id}] ")

    if sso:
        # startup server to handle response
        stop_server_evt = asyncio.Event()
        login_token = None

        async def handle(request):
            nonlocal login_token
            login_token = request.query.get("loginToken")
            stop_server_evt.set()
            return web.Response(
                body="Login complete. You can now close this page."
            )

        app = web.Application()
        app.add_routes([web.get("/", handle)])

        logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", 38080)
        await site.start()

        try:
            print("Launching browser to complete SSO login.")
            if gs.pa.proxy:
                gs.log.warning(
                    f"Specified proxy {gs.pa.proxy} cannot "
                    "be configured for browser."
                )

            # launch web-browser
            if sys.platform.startswith("darwin"):
                cmd = [shutil.which("open")]
            elif sys.platform.startswith("win"):
                cmd = ["start"]
            else:
                cmd = [shutil.which("x-www-browser")]
            cmd.append(
                f"{homeserver}/_matrix/client/r0/login/sso/redirect"
                "?redirectUrl=http://localhost:38080/"
            )
            try:
                subprocess.check_output(cmd)
            except Exception:
                raise MatrixCommanderError(
                    "Browser could not be launched. "
                    "Hence SSO (Single Sign-On) login could not be "
                    "completed. Sorry. If you think the browser and "
                    "SSO should work then try again. If you do not have "
                    "a browser or don't want SSO or want to login with a "
                    "password instead, then use the '--no-sso' option in "
                    "the command line.",
                    traceback=False,
                    level="error",
                )

            # wait and shutdown server
            try:
                await asyncio.wait_for(stop_server_evt.wait(), 5 * 60)
            except asyncio.TimeoutError:
                raise MatrixCommanderError(
                    f"The program {PROG_WITH_EXT} failed. "
                    "No response was received from SSO provider. "
                    "Sorry.",
                    traceback=False,
                    level="error",
                )

        finally:
            await runner.cleanup()

    elif not password:
        raise MatrixCommanderError(
            "No supported login method found for homeserver. "
            "Neither SSO nor password are accepted login "
            "methods of the server.",
            traceback=False,
            level="error",
        )

    # Configuration options for the AsyncClient
    client_config = AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        store_sync_tokens=True,
        encryption_enabled=True,
    )

    if not os.path.exists(store_dir):
        os.makedirs(store_dir)
        gs.log.info(
            f"The persistent storage directory {store_dir} "
            "was created for you."
        )

    # Initialize the matrix client
    client = AsyncClient(
        homeserver,
        user_id,
        store_path=store_dir,
        config=client_config,
        ssl=gs.ssl,
        proxy=gs.pa.proxy,
    )
    try:

        txt = ""
        level = ""
        if sso:
            resp = await client.login(
                token=login_token, device_name=device_name
            )
            method = "SSO"

        else:
            pw = getpass.getpass()
            resp = await client.login(pw, device_name=device_name)
            method = "a password"

        # check that we logged in succesfully
        if isinstance(resp, LoginResponse):
            # when writing, always write to primary location (e.g. .)
            write_credentials_to_disk(
                homeserver,
                resp.user_id,
                resp.device_id,
                resp.access_token,
                room_id,
                gs.pa.credentials,
            )
            txt = f"""
                Log in using {method} was successful.
                Credentials were stored in file \"{gs.pa.credentials}\".
                Run program \"{PROG_WITH_EXT}\" again to
                login with credentials and to send a message.
                If you plan on having many credential files, consider
                moving them to directory \"{CREDENTIALS_DIR_LASTRESORT}\"."""
            txt = textwrap.fill(textwrap.dedent(txt).strip(), width=79)
            level = "info"
        else:
            txt = f"The program {PROG_WITH_EXT} failed. "
            "Most likely wrong credentials were entered. "
            "Sorry. \n"
            f'homeserver="{homeserver}"; user="{user_id}"; '
            f'room_id="{room_id}"; '
            f"failed to log in: {resp}"
            level = "error"
    finally:
        await client.close()
    if level == "error":
        raise MatrixCommanderError(txt, traceback=True, level=level)
    elif level == "info":
        raise MatrixCommanderError(txt, traceback=False, level=level)


def login_using_credentials_file(
    credentials_file: str, store_dir: str
) -> (AsyncClient, dict):
    """Log in by using available credentials file.

    Arguments:
    ---------
        credentials_file: str : location of credentials file
        store_dir: str : location of persistent storage store directory

    Returns
    -------
        AsyncClient : the created NIO client
        dict : the credentials dictionary from the credentials file

    """
    credentials = read_credentials_from_disk(credentials_file)

    # Configuration options for the AsyncClient
    client_config = AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        store_sync_tokens=True,
        encryption_enabled=True,
    )
    # Initialize the matrix client based on credentials from file
    client = AsyncClient(
        credentials["homeserver"],
        credentials["user_id"],
        device_id=credentials["device_id"],
        store_path=store_dir,
        config=client_config,
        ssl=gs.ssl,
        proxy=gs.pa.proxy,
    )

    client.restore_login(
        user_id=credentials["user_id"],
        device_id=credentials["device_id"],
        access_token=credentials["access_token"],
    )
    # room_id = credentials['room_id']
    gs.log.debug(
        "Logged in using stored credentials from "
        f'credentials file "{credentials_file}".'
    )
    if gs.pa.proxy:
        gs.log.debug(f"Proxy {gs.pa.proxy} will be used for connectivity.")
    gs.log.debug(f"Logged_in() = {client.logged_in}")
    return (client, credentials)


async def listen_forever(client: AsyncClient) -> None:
    """Listen forever or until Control-C."""
    # Set up event callbacks
    callbacks = Callbacks(client)
    client.add_event_callback(
        callbacks.message_callback,
        (
            RoomMessage,
            RedactedEvent,
            RedactionEvent,
        ),
    )
    print(
        "This program is ready and listening for its Matrix messages."
        " To stop program type Control-C on keyboard or send signal"
        f" to process {os.getpid()}. PID can also be found in "
        f'file "{PID_FILE_DEFAULT}".',
        flush=True,
    )
    # the sync_loop will be terminated by user hitting Control-C to stop
    await client.sync_forever(timeout=30000, full_state=True)


async def listen_once(client: AsyncClient) -> None:
    """Listen once, then quit.

    Get all the messages that are currently queued up and waiting.
    Print them. Then leave.
    """
    # Set up event callbacks
    callbacks = Callbacks(client)
    client.add_event_callback(callbacks.message_callback, (RoomMessage,))
    # We want to get out quickly, so we reduced timeout to 10 sec.
    # We want to get messages and quit, so we call sync() instead of
    # sync_forever().
    resp = await client.sync(timeout=10000, full_state=False)
    if isinstance(resp, SyncResponse):
        gs.log.debug(f"Sync successful. Response is: {resp}")
    else:
        gs.log.info(f"Sync failed. Error is: {resp}")
    # sync() forces the message_callback() to fire
    # for each new message presented in the sync().


async def listen_once_alternative(client: AsyncClient) -> None:
    """Listen once, then quit.

    Get all the messages that are currently queued up and waiting.
    Print them. Then leave.

    Alternative implementation of listen_once().
    We don't use any callbacks and we just call sync() and get all
    of the MessageEvents from the timeline of the reply provided by
    sync(). This is more work than listen_once() but it is interesting
    case study to understand sync().

    sync() response includes the member `rooms` (of class nio.responses.Rooms).
    Rooms have 3 top dicts.
    Rooms(invite={}, join={...}, leave={})
    join has a dict entry of type RoomInfo for
    each room. And the RoomInfo has a timeline (of class TimeLine) with
    all currently queued up events. So, timeline has a list of events
    such as RoomMessageText, RoomMessageNotice, etc. One can go through
    these timeline event lists and process each queued up message.

    This is an example Rooms object that is part of a sync() response.
    This example gives the details on 2 currently queued up messages.

    Rooms(
    invite={},
    join={'!SomeRoomId:example.org':
        RoomInfo(
        timeline=Timeline(
            events=[
                RoomMessageText(source={
                    'room_id': '!SomeRoomId:example.org',
                    'type': 'm.room.message',
                    'content': {'msgtype': 'm.text', 'body': 'Hi there'},
                    'event_id': 'SomeEventId1',
                    'sender': '@user1:example.org',
                    'origin_server_ts': 1591234896712},
                event_id='SomeEventId1',
                sender='@user1:example.org',
                server_timestamp=1591234896712,
                decrypted=True, verified=False,
                sender_key='SomeSenderKey1',
                session_id='SomeSessionId1',
                transaction_id=None,
                body='Hi there',
                formatted_body=None,
                format=None),

                RoomMessageNotice(source={'content': {'msgtype': 'm.notice',
                    'body': 'Hello',
                    'format': 'org.matrix.custom.html',
                    'formatted_body': '<p>Hello</p>'
                    },
                    'type': 'm.room.message',
                    'room_id': '!SomeRoomId:example.org',
                    'event_id': 'SomeEventId2',
                    'sender': '@user2:example.org',
                    'origin_server_ts': 1591234897079},
                event_id='SomeEventId2',
                sender='@user2:example.org',
                server_timestamp=1591234897079, decrypted=True, verified=False,
                sender_key='SomeSenderKey2',
                session_id='SomeSessionId2',
                transaction_id=None,
                body='<p>Hello</p>',
                format='org.matrix.custom.html')
            ],
            limited=False,
            prev_batch='s16650_264746_732_1234_8050_2_8260_439_1'),
        state=[],
        ephemeral=[TypingNoticeEvent(users=[]), ReceiptEvent(...)],
        account_data=[],
        summary=RoomSummary(...),
        unread_notifications=UnreadNotifications(...)
        )
    },
    leave={})

    """
    resp_s = await client.sync(timeout=10000, full_state=False)
    # this prints a summary of all new messages currently waiting in the queue
    gs.log.debug(f"sync response = {type(resp_s)} :: {resp_s}")
    gs.log.debug(f"sync next_batch = (str) {resp_s.next_batch}")
    gs.log.debug(f"sync rooms = (nio.responses.Rooms) {resp_s.rooms}")
    # Set up event callbacks
    callbacks = Callbacks(client)
    # Note: we are NOT registering a callback funtion!
    # Loop through the join dictionary
    for room_id, room_info in resp_s.rooms.join.items():
        event_list = room_info.timeline.events
        for event in event_list:
            gs.log.debug(f"sending event to callback = {event}.")
            # because of full_state=False in sync() the
            # rooms object is not fully populated and missing the
            # room names.
            room = client.rooms[room_id]
            await callbacks.message_callback(room, event)
        if event_list:  # list not empty
            last_event = event_list[-1]
            resp = await client.room_read_markers(
                room_id=room_id,
                fully_read_event=last_event.event_id,
                read_event=last_event.event_id,
            )
            if isinstance(resp, RoomReadMarkersError):
                gs.log.debug(
                    f"room_read_markers failed with response = {resp}."
                )


# according to pylama: function too complex: C901 # noqa: C901
async def listen_tail(  # noqa: C901
    client: AsyncClient, credentials: dict
) -> None:  # noqa: C901
    """Get the last N messages, then quit.

    Arguments:
    ---------
        client: AsyncClient : the created NIO client
        credentials: dict : credentials dictionary from the credentials file

    Get the last N messages. Some might be old, i.e. already
    read before, some might be new, i.e. never read before.
    Print them. Then leave.

    If there are less than N messages, get up to N.

    The function room_messages() is used to get
    the last N messages.

    """
    # we call sync() to get the next_batch marker
    # we set full_state=True to get all room_ids
    try:
        resp_s = await client.sync(timeout=10000, full_state=True)
    except ClientConnectorError:
        gs.log.info("sync() failed. Do you have connectivity to internet?")
        gs.log.debug(traceback.format_exc())
        return
    except Exception:
        gs.log.info("sync() failed.")
        gs.log.debug(traceback.format_exc())
        return
    if isinstance(resp_s, SyncError):
        gs.log.debug(f"sync failed with resp = {resp_s}")
        return
    # this prints a summary of all new messages currently waiting in the queue
    gs.log.debug(f"sync response = {type(resp_s)} :: {resp_s}")
    gs.log.debug(f"client.next_batch after = (str) {client.next_batch}")
    gs.log.debug(f"sync next_batch = (str) {resp_s.next_batch}")
    gs.log.debug(f"sync rooms = (nio.responses.Rooms) {resp_s.rooms}")
    gs.log.debug(f"client.rooms = {client.rooms}")
    if not resp_s.rooms.join:  # no Rooms!
        gs.log.debug(f"sync returned no rooms = {resp_s.rooms.join}")
        return

    # Set up event callbacks
    callbacks = Callbacks(client)
    # Note: we are NOT registering a callback funtion!

    # room_id = list(resp_s.rooms.join.keys())[0]  # first room_id from dict
    # alternative way of getting room_id, client.rooms is also a dict
    # room_id = list(client.rooms.keys())[0]  # first room_id from dict

    # get rooms as specified by the user thru args or credential file
    rooms = await determine_rooms(credentials["room_id"], client, credentials)
    gs.log.debug(f"Rooms are: {rooms}")

    limit = gs.pa.tail
    # To loop over all rooms, one can loop through the join dictionary. i.e.
    # for room_id, room_info in resp_s.rooms.join.items():  # loop all rooms
    for room_id in rooms:  # loop only over user specified rooms
        resp = await client.room_messages(
            room_id, start=resp_s.next_batch, limit=limit
        )
        if isinstance(resp, RoomMessagesError):
            gs.log.debug("room_messages failed with resp = {resp}")
            continue  # skip this room
        gs.log.debug(f"room_messages response = {type(resp)} :: {resp}.")
        gs.log.debug(f"room_messages room_id = {resp.room_id}.")
        gs.log.debug(f"room_messages start = (str) {resp.start}.")
        gs.log.debug(f"room_messages end = (str) :: {resp.end}.")
        gs.log.debug(f"room_messages chunk = (list) :: {resp.chunk}.")
        # chunk is just a list of RoomMessage events like this example:
        # chunk=[RoomMessageText(...)]

        for event in resp.chunk:
            gs.log.debug(f"sending event to callback = {event}.")
            if client.rooms and client.rooms[room_id]:
                room = client.rooms[room_id]
            else:
                room = MatrixRoom(room_id, None, True)  # dummy_room
            await callbacks.message_callback(room, event)
        if resp.chunk:  # list not empty
            # order is reversed, first element is timewise the newest
            first_event = resp.chunk[1]
            resp = await client.room_read_markers(
                room_id=room_id,
                fully_read_event=first_event.event_id,
                read_event=first_event.event_id,
            )
            if isinstance(resp, RoomReadMarkersError):
                gs.log.debug(
                    f"room_read_markers failed with response = {resp}."
                )


async def read_all_events_in_direction(
    client: AsyncClient,
    room_id: str,
    start_token: str,
    direction: MessageDirection = MessageDirection.back,
) -> list:
    """Read all events from a given room in certain direction.

    Arguments:
    ---------
        client: AsyncClient : The created NIO client
        room_id: str : The room id of the room for which we
            would like to fetch the messages.
        start_token: str :  The token to start returning events from.
            This token can be obtained from a prev_batch token returned for
            each room by the sync() API, or from a start or end token returned
            by a previous request to room_messages().
        direction: MessageDirection (optional): The direction to return
            events from. Defaults to MessageDirection.back.

    Returns
    -------
        list: list of RoomMessage events, could be empty

    Read all messages of a room beginning from the past_token
    to oldest or newest message (depending on the direction).

    """
    all_events = []
    current_start_token = start_token
    while True:
        resp = await client.room_messages(
            room_id, current_start_token, limit=500, direction=direction
        )
        if isinstance(resp, RoomMessagesError):
            gs.log.debug("room_messages failed with resp = {resp}")
            break  # skip to end of function
        gs.log.debug(f"Received {len(resp.chunk)} events.")
        gs.log.debug(f"room_messages response = {type(resp)} :: {resp}.")
        gs.log.debug(f"room_messages room_id = {resp.room_id}.")
        gs.log.debug(f"room_messages start = (str) {resp.start}.")
        gs.log.debug(f"room_messages end = (str) :: {resp.end}.")
        gs.log.debug(f"room_messages chunk = (list) :: {resp.chunk}.")
        # resp.chunk is just a list of RoomMessage events like this example:
        # chunk=[RoomMessageText(...)]
        current_start_token = resp.end
        if len(resp.chunk) == 0:
            break
        all_events = all_events + resp.chunk
    return all_events


# according to pylama: function too complex: C901 # noqa: C901
async def listen_all(  # noqa: C901
    client: AsyncClient, credentials: dict
) -> None:  # noqa: C901
    """Get all messages, then quit.

    Arguments:
    ---------
        client: AsyncClient : the created NIO client
        credentials: dict : credentials dictionary from the credentials file

    Get all messages. Some might be old, i.e. already
    read before, some might be new, i.e. never read before.
    Print them. Then leave.

    The function room_messages() is used to get all messages.

    """
    # we call sync() to get the next_batch marker
    # we set full_state=True to get all room_ids
    try:
        resp_s = await client.sync(timeout=10000, full_state=True)
    except ClientConnectorError:
        gs.log.info("sync() failed. Do you have connectivity to internet?")
        gs.log.debug(traceback.format_exc())
        return
    except Exception:
        gs.log.info("sync() failed.")
        gs.log.debug(traceback.format_exc())
        return
    if isinstance(resp_s, SyncError):
        gs.log.debug(f"sync failed with resp = {resp_s}")
        return
    # this prints a summary of all new messages currently waiting in the queue
    gs.log.debug(f"sync response = {type(resp_s)} :: {resp_s}")
    gs.log.debug(f"client.next_batch after = (str) {client.next_batch}")
    gs.log.debug(f"sync next_batch = (str) {resp_s.next_batch}")
    gs.log.debug(f"sync rooms = (nio.responses.Rooms) {resp_s.rooms}")
    gs.log.debug(f"client.rooms = {client.rooms}")
    if not resp_s.rooms.join:  # no Rooms!
        gs.log.debug(f"sync returned no rooms = {resp_s.rooms.join}")
        return

    # Set up event callbacks
    callbacks = Callbacks(client)
    # Note: we are NOT registering a callback funtion!

    # room_id = list(resp_s.rooms.join.keys())[0]  # first room_id from dict
    # alternative way of getting room_id, client.rooms is also a dict
    # room_id = list(client.rooms.keys())[0]  # first room_id from dict

    # get rooms as specified by the user thru args or credential file
    rooms = await determine_rooms(credentials["room_id"], client, credentials)
    gs.log.debug(f"Rooms are: {rooms}")

    # To loop over all rooms, one can loop through the join dictionary. i.e.
    # for room_id, room_info in resp_s.rooms.join.items():  # loop all rooms
    for room_id in rooms:  # loop only over user specified rooms
        prev_batch = resp_s.rooms.join[room_id].timeline.prev_batch
        back_events = await read_all_events_in_direction(
            client, room_id, prev_batch, MessageDirection.back
        )
        front_events = await read_all_events_in_direction(
            client, room_id, prev_batch, MessageDirection.front
        )

        # We have to reverse the first list since we are going backwards (but
        # we want to have a chronological order)
        all_events = back_events[::-1] + front_events

        for event in all_events:
            gs.log.debug(f"sending event to callback = {event}.")
            if client.rooms and client.rooms[room_id]:
                room = client.rooms[room_id]
            else:
                room = MatrixRoom(room_id, None, True)  # dummy_room
            await callbacks.message_callback(room, event)
        if all_events:  # list not empty
            last_event = all_events[-1]
            resp = await client.room_read_markers(
                room_id=room_id,
                fully_read_event=last_event.event_id,
                read_event=last_event.event_id,
            )
            if isinstance(resp, RoomReadMarkersError):
                gs.log.debug(
                    f"room_read_markers failed with response = {resp}."
                )


async def main_listen() -> None:
    """Use credentials to log in and listen."""
    credentials_file = determine_credentials_file()
    store_dir = determine_store_dir()
    if not os.path.isfile(credentials_file):
        raise MatrixCommanderError(
            f"""Credentials file was not found.
            Did you start {PROG_WITHOUT_EXT} in the wrong directory?
            Did you specify the credentials options incorrectly?
            Credentials file must be created first before one can listen.
            Aborting due to missing or not-found credentials file.""",
            traceback=False,
            level="error",
        )
    gs.log.debug("Credentials file does exist.")
    try:
        client, credentials = login_using_credentials_file(
            credentials_file, store_dir
        )
        # Sync encryption keys with the server
        # Required for participating in encrypted rooms
        if client.should_upload_keys:
            await client.keys_upload()
        gs.log.debug(f"Listening type: {gs.pa.listen}")
        if gs.pa.listen == FOREVER:
            await listen_forever(client)
        elif gs.pa.listen == ONCE:
            await listen_once(client)
            # could use 'await listen_once_alternative(client)'
            # as an alternative implementation
        elif gs.pa.listen == TAIL:
            await listen_tail(client, credentials)
        elif gs.pa.listen == ALL:
            await listen_all(client, credentials)
        else:
            gs.log.error(
                f'Unrecognized listening type "{gs.pa.listen}". '
                "Closing client."
            )
    finally:
        if client:
            await client.close()


async def action_set_device_name(
    client: AsyncClient, credentials: dict
) -> None:
    """Set, rename the device name of itself while already being logged in."""
    content = {"device_name": gs.pa.set_device_name}
    resp = await client.update_device(credentials["device_id"], content)
    if isinstance(resp, UpdateDeviceError):
        gs.log.error(f"update_device failed with {resp}")
    else:
        gs.log.debug(f"update_device successful with {resp}")


async def action_set_display_name(
    client: AsyncClient, credentials: dict
) -> None:
    """Set, rename the logged in user's display name. Change my own
    display name.
    Rename the user by changing display name.
    Assumes that user is already logged in.
    """
    resp = await client.set_displayname(gs.pa.set_display_name)
    if isinstance(resp, ProfileSetDisplayNameError):
        gs.log.error(f"set_displayname failed with {resp}")
    else:
        gs.log.debug(f"set_displayname successful with {resp}")


async def action_get_display_name(
    client: AsyncClient, credentials: dict
) -> None:
    """Get display name(s) while already logged in."""
    if not gs.pa.user:
        # get display name of myself
        whoami = credentials["user_id"]
        users = [whoami]
    else:
        users = gs.pa.user
    users = list(dict.fromkeys(users))  # remove duplicates in list
    for user in users:
        resp = await client.get_displayname(user)
        if isinstance(resp, ProfileGetDisplayNameError):
            gs.log.error(f"get_displayname failed with {resp}")
        else:
            gs.log.debug(f"get_displayname successful with {resp}")
            # resp.displayname is str or None (has no display name)
            if not resp.displayname:
                displayname = ""  # means no display name is set
            else:
                displayname = resp.displayname
            print(f"{user}{SEP}{displayname}")


async def action_set_presence(client: AsyncClient, credentials: dict) -> None:
    """Set the logged in user's presence. Change my own presence.
    Assumes that user is already logged in.
    """
    state = gs.pa.set_presence.strip().lower()
    gs.log.debug(f"Setting presence to {state} [{gs.pa.set_presence}].")
    resp = await client.set_presence(state)
    if isinstance(resp, PresenceSetError):
        gs.log.error(f"set_presence failed with {resp}")
    else:
        gs.log.debug(f"set_presence successful with {resp}")


async def action_get_presence(client: AsyncClient, credentials: dict) -> None:
    """Get presence(s) while already logged in."""
    if not gs.pa.user:
        # get presence name of myself
        whoami = credentials["user_id"]
        users = [whoami]
    else:
        users = gs.pa.user
    users = list(dict.fromkeys(users))  # remove duplicates in list
    for user in users:
        resp = await client.get_presence(user)
        if isinstance(resp, PresenceGetError):
            gs.log.error(f"get_presence failed with {resp}")
        else:
            gs.log.debug(f"get_presence successful with {resp}")
            if not resp.last_active_ago:
                last_active_ago = 0  # means currently_active is not set
            else:
                last_active_ago = resp.last_active_ago
            if not resp.currently_active:
                currently_active = False  # means currently_active is not set
            else:
                currently_active = resp.currently_active
            if not resp.status_msg:
                status_msg = ""  # means no status_msg is set
            else:
                status_msg = resp.status_msg
            print(
                f"{resp.user_id}{SEP}{resp.presence}{SEP}{last_active_ago}"
                f"{SEP}{currently_active}{SEP}{status_msg}"
            )


async def action_joined_rooms(client: AsyncClient, credentials: dict) -> None:
    """Get joined rooms while already logged in."""
    resp = await client.joined_rooms()
    if isinstance(resp, JoinedRoomsError):
        gs.log.error(f"joined_rooms failed with {resp}")
    else:
        gs.log.debug(f"joined_rooms successful with {resp}")
        print(*resp.rooms, sep="\n")  # one per line


async def action_joined_members(
    client: AsyncClient, credentials: dict
) -> None:
    """Get members of given rooms while already being logged in."""
    rooms = gs.pa.joined_members
    if not rooms:
        gs.log.warning(
            "No membership action(s) were performed because no rooms "
            "were specified. Use --joined-members option and specify rooms."
        )
        return

    # print(credentials["user_id"])  ## who am i, whoami
    gs.log.debug(f"Trying to get members for these rooms: {rooms}")
    if "*" in rooms:
        resp = await client.joined_rooms()
        if isinstance(resp, JoinedRoomsError):
            gs.log.error(
                f"joined_rooms failed with {resp}. Not able to "
                "get all rooms as specified by '*'. "
                "The member listing will be incomplete or missing."
            )
            # since we can't get all rooms leave room list as is
            rooms = filter(lambda val: val != "*", rooms)  # remove all *
        else:
            gs.log.debug(f"joined_rooms successful with {resp}")
            gs.log.debug(
                "Room list has been successfully overwritten with '*'"
            )
            rooms = resp.rooms  # overwrite args with full list
    for room in rooms:
        resp = await client.joined_members(room)
        if isinstance(resp, JoinedMembersError):
            gs.log.error(f"joined_members failed with {resp}")
        else:
            gs.log.debug(f"joined_members successful with {resp}")
            print(resp.room_id)
            # members = List[RoomMember] ; RoomMember
            print(
                *list(
                    map(
                        lambda member: SEP
                        + member.user_id
                        + SEP
                        + member.display_name
                        + SEP
                        + member.avatar_url,
                        resp.members,
                    )
                ),
                sep="\n",
            )


async def action_whoami(client: AsyncClient, credentials: dict) -> None:
    """Get user id while already logged in."""
    whoami = credentials["user_id"]
    gs.log.debug(f"whoami: user id: {whoami}")
    print(whoami)


async def main_roomsetget_action() -> None:
    """Use credentials to log in and perform actions on server."""
    credentials_file = determine_credentials_file()
    store_dir = determine_store_dir()
    if not os.path.isfile(credentials_file):
        raise MatrixCommanderError(
            f"""Credentials file was not found.
            Did you start {PROG_WITHOUT_EXT} in the wrong directory?
            Did you specify the credentials options incorrectly?
            Credentials file must be created first before one can
            perform any other actions.
            Aborting due to missing or not-found credentials file.""",
            traceback=False,
            level="error",
        )
    gs.log.debug("Credentials file does exist.")
    try:
        client, credentials = login_using_credentials_file(
            credentials_file, store_dir
        )
        # room_action
        # we already checked args at the beginning, no need to check
        # room and user argument combinations again.
        if gs.pa.room_create:
            await create_rooms(
                client, gs.pa.room_create, gs.pa.name, gs.pa.topic
            )
        if gs.pa.room_join:
            await join_rooms(client, gs.pa.room_join)
        if gs.pa.room_leave:
            await leave_rooms(client, gs.pa.room_leave)
        if gs.pa.room_forget:
            await forget_rooms(client, gs.pa.room_forget)
        if gs.pa.room_invite and gs.pa.user:
            await invite_to_rooms(client, gs.pa.room_invite, gs.pa.user)
        if gs.pa.room_ban and gs.pa.user:
            await ban_from_rooms(client, gs.pa.room_ban, gs.pa.user)
        if gs.pa.room_unban and gs.pa.user:
            await unban_from_rooms(client, gs.pa.room_unban, gs.pa.user)
        if gs.pa.room_kick and gs.pa.user:
            await kick_from_rooms(client, gs.pa.room_kick, gs.pa.user)
        if gs.room_action:
            gs.log.debug("Room action(s) were performed or attempted.")
        # set_action
        if gs.pa.set_display_name:
            await action_set_display_name(client, credentials)
        if gs.pa.set_device_name:
            await action_set_device_name(client, credentials)
        if gs.pa.set_presence:
            await action_set_presence(client, credentials)
        # get_action
        if gs.pa.get_display_name:
            await action_get_display_name(client, credentials)
        if gs.pa.get_presence:
            await action_get_presence(client, credentials)
        if gs.pa.joined_rooms:
            await action_joined_rooms(client, credentials)
        if gs.pa.joined_members:
            await action_joined_members(client, credentials)
        if gs.pa.whoami:
            await action_whoami(client, credentials)
        if gs.setget_action:
            gs.log.debug("Set or get action(s) were performed or attempted.")
    finally:
        if client:
            await client.close()


async def main_verify() -> None:
    """Use credentials to log in and verify."""
    credentials_file = determine_credentials_file()
    store_dir = determine_store_dir()
    if not os.path.isfile(credentials_file):
        raise MatrixCommanderError(
            f"""Credentials file was not found.
            Did you start {PROG_WITHOUT_EXT} in the wrong directory?
            Did you specify the credentials options incorrectly?
            Credentials file must be created first before one can verify.
            Aborting due to missing or not-found credentials file.""",
            traceback=False,
            level="error",
        )
    gs.log.debug("Credentials file does exist.")
    try:
        client, credentials = login_using_credentials_file(
            credentials_file, store_dir
        )
        # Set up event callbacks
        callbacks = Callbacks(client)
        client.add_to_device_callback(
            callbacks.to_device_callback, (KeyVerificationEvent,)
        )
        # Sync encryption keys with the server
        # Required for participating in encrypted rooms
        if client.should_upload_keys:
            await client.keys_upload()
        print(
            "This program is ready and waiting for the other party to "
            "initiate an emoji verification with us by selecting "
            '"Verify by Emoji"'
            "in their Matrix client."
        )
        # the sync_loop will be terminated by user hitting Control-C to stop
        await client.sync_forever(timeout=30000, full_state=True)
    finally:
        if client:
            await client.close()


async def main_send() -> None:
    """Create credentials, or use credentials to log in and send messages."""
    credentials_file = determine_credentials_file()
    store_dir = determine_store_dir()
    if not os.path.isfile(credentials_file):
        gs.log.debug("Credentials file does not exist.")
        await create_credentials_file(credentials_file, store_dir)
    gs.log.debug("Credentials file does exist.")
    try:
        client, credentials = login_using_credentials_file(
            credentials_file, store_dir
        )
        # a few more steps to prepare for sending messages
        rooms = await determine_rooms(
            credentials["room_id"], client, credentials
        )
        gs.log.debug(f"Rooms are: {rooms}")
        # Sync encryption keys with the server
        # Required for participating in encrypted rooms
        if client.should_upload_keys:
            await client.keys_upload()
        # must sync first to get room ids for encrypted rooms
        # since we only send a msg and then stop we can use sync() instead of
        # sync_forever() (await client.sync_forever(30000, full_state=True))
        await client.sync(timeout=30000, full_state=True)
        # Now we can send messages as the user
        await process_arguments_and_input(client, rooms)
        gs.log.debug("Messages were sent. We close the client and quit")
    finally:
        if client:
            await client.close()


def check_arg_files_readable() -> None:
    """Check if files from command line are readable."""
    arg_files = gs.pa.image if gs.pa.image else []
    arg_files += gs.pa.audio if gs.pa.audio else []
    arg_files += gs.pa.file if gs.pa.file else []
    arg_files += gs.pa.event if gs.pa.event else []
    r = True
    errtxt = (
        "These file specified in the command line were not found "
        "or are not readable: "
    )
    for fn in arg_files:
        if (fn != "-") and not (isfile(fn) and access(fn, R_OK)):
            if not r:
                errtxt += ", "
            errtxt += f'"{fn}"'
            r = False
            errfile = fn
    if not r:
        raise FileNotFoundError(errno.ENOENT, errtxt, errfile)


def check_download_media_dir() -> None:
    """Check if media download directory is correct."""
    if not gs.pa.download_media:
        return  # "": that means no download of media, valid value
    # normailzed for humans
    dl = os.path.normpath(gs.pa.download_media)
    gs.pa.download_media = dl
    if os.path.isfile(dl):
        raise NotADirectoryError(
            errno.ENOTDIR,
            f'"{dl}" cannot be used as media directory, because '
            f'"{dl}" is a file. Specify a different directory for downloading '
            "media.",
            dl,
        )
    if os.path.isdir(dl):
        if os.access(dl, os.W_OK):  # Check for write access
            return  # all OK
        else:
            raise PermissionError(
                errno.EPERM,
                "Found an existing media download directory "
                f'"{dl}". But this directory is lacking write '
                "permissions. Add write permissions to it.",
                dl,
            )
    else:
        # not a file, not a directory, create directory
        mode = 0o777
        try:
            os.mkdir(dl, mode)
        except OSError as e:
            raise OSError(
                e.errno,
                "Could not create media download directory "
                f"{dl} for you. ({e})",
                dl,
            )
        gs.log.debug(f'Created media download directory "{dl}" for you.')


def version() -> None:
    """Print version info."""
    version_info = (
        "\n"
        f"  _|      _|      _|_|_|    _|       {PROG_WITHOUT_EXT}\n"
        "  _|_|  _|_|    _|            _|     a Matrix CLI client\n"
        "  _|  _|  _|    _|              _|   \n"
        f"  _|      _|    _|            _|     version {VERSIONNR} {VERSION}\n"
        "  _|      _|      _|_|_|    _|       enjoy and submit PRs\n"
        "\n"
    )
    print(version_info)
    gs.log.debug(version_info)


def initial_check_of_log_args() -> None:
    """Check logging related arguments.

    Arguments:
    ---------
    None

    Returns: None

    Raises exception on error.
    """
    if not gs.pa.log_level:
        return  # all OK
    t = ""
    for i in range(len(gs.pa.log_level)):
        up = gs.pa.log_level[i].upper()
        gs.pa.log_level[i] = up
        if up not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            t = (
                '--log-level only allows values "DEBUG", "INFO", "WARNING", '
                '"ERROR", or "CRITICAL". --log-level argument incorrect. '
                f"({up})"
            )
    if t == "":
        return  # all OK
    else:
        raise MatrixCommanderError(t)


# according to pylama: function too complex: C901 # noqa: C901
def initial_check_of_args() -> None:  # noqa: C901
    """Check arguments."""
    # First, the adjustments
    if not gs.pa.encrypted:
        gs.pa.encrypted = True  # force it on
        gs.log.debug("Encryption is always enabled. It cannot be turned off.")
    if not gs.pa.encrypted:  # just in case we ever go back disabling e2e
        gs.pa.store = None
    if gs.pa.listen:
        gs.pa.listen = gs.pa.listen.lower()
    if gs.pa.listen == NEVER and gs.pa.tail != 0:
        gs.pa.listen = TAIL  # --tail turns on --listen TAIL
        gs.log.debug('--listen set to "tail" because "--tail" is used.')
    if (
        gs.pa.message
        or gs.pa.image
        or gs.pa.audio
        or gs.pa.file
        or gs.pa.event
    ):
        gs.send_action = True
    else:
        gs.send_action = False
    if (
        gs.pa.room_create
        or gs.pa.room_join
        or gs.pa.room_leave
        or gs.pa.room_forget
        or gs.pa.room_invite
        or gs.pa.room_ban
        or gs.pa.room_unban
        or gs.pa.room_kick
    ):
        gs.room_action = True
    else:
        gs.room_action = False
    if (
        gs.pa.set_device_name  # set
        or gs.pa.set_display_name
        or gs.pa.set_presence
        or gs.pa.get_display_name  # get
        or gs.pa.get_presence
        or gs.pa.joined_rooms
        or gs.pa.joined_members
        or gs.pa.whoami
    ):
        gs.setget_action = True
    else:
        gs.setget_action = False
    # only 2 SSL states allowed: None (SSL default on), False (SSL off)
    if gs.pa.no_ssl is not True:
        gs.pa.no_ssl = None
    if gs.pa.proxy == "":
        gs.pa.proxy = None

    # how often is "-" used to represent stdin
    # must be 0 or 1; cannot be used twice or more
    STDIN_MESSAGE = 0
    STDIN_IMAGE = 0
    STDIN_AUDIO = 0
    STDIN_FILE = 0
    STDIN_EVENT = 0
    STDIN_TOTAL = 0
    if gs.pa.image:
        for image in gs.pa.image:
            if image == "-":
                STDIN_IMAGE += 1
                gs.stdin_use = "image"
    if gs.pa.audio:
        for audio in gs.pa.audio:
            if audio == "-":
                STDIN_AUDIO += 1
                gs.stdin_use = "audio"
    if gs.pa.file:
        for file in gs.pa.file:
            if file == "-":
                STDIN_FILE += 1
                gs.stdin_use = "file"
    if gs.pa.event:
        for event in gs.pa.event:
            if event == "-":
                STDIN_EVENT += 1
                gs.stdin_use = "event"
    if gs.pa.message:
        for message in gs.pa.message:
            if message == "-":
                STDIN_MESSAGE += 1
                gs.stdin_use = "message"
    STDIN_TOTAL = (
        STDIN_MESSAGE + STDIN_IMAGE + STDIN_AUDIO + STDIN_FILE + STDIN_EVENT
    )

    # Secondly, the checks
    if gs.pa.config:
        t = (
            "This feature is not implemented yet. "
            "Please help me implement it. If you feel motivated "
            "please write code and submit a Pull Request. "
            "Your contribution is appreciated. Thnx!"
        )
    elif (
        gs.pa.listen == FOREVER or gs.pa.listen == ONCE or gs.pa.listen == ALL
    ) and gs.pa.tail != 0:
        t = (
            "Don't use --listen forever, --listen once or --listen all "
            "together with --tail. It's one or the other."
        )
    # this is set by default anyway, just defensive programming
    elif gs.pa.encrypted and ((not gs.pa.store) or (gs.pa.store == "")):
        t = (
            "If --encrypted is used --store must be set too. "
            "Specify --store and run program again."
        )
    elif gs.pa.verify and (gs.pa.verify.lower() != EMOJI):
        t = f'For --verify currently only "{EMOJI}" is allowed ' "as keyword."
    elif gs.pa.verify and (
        gs.send_action
        or gs.pa.room
        or gs.room_action
        or gs.pa.listen != NEVER
        or gs.setget_action
    ):
        t = (
            "If --verify is specified, only verify can be done. "
            "No messages, images, files or events can be sent."
            "No listening or tailing allowed. "
            "No other actions allowed."
        )
    elif gs.pa.listen != NEVER and (
        gs.send_action or gs.room_action or gs.pa.verify or gs.setget_action
    ):
        t = (
            "If --listen is specified, only listening can be done. "
            "No messages, images, files or events can be sent. "
            "No room or other actions allowed."
        )
    elif gs.send_action and (
        gs.room_action
        or gs.pa.listen != NEVER
        or gs.pa.verify
        or gs.setget_action
    ):
        t = (
            "If sending (-m, -i, -a, -f, -e) is specified, only sending can "
            "be done. No listening allowed. "
            "No room or other actions allowed."
        )
    elif gs.pa.set_device_name and (gs.pa.set_device_name.strip() == ""):
        t = "Don't use an empty name for --set-device-name."
    elif gs.pa.set_display_name and (gs.pa.set_display_name.strip() == ""):
        t = "Don't use an empty name for --set-display-name."
    elif (gs.pa.user) and not (
        gs.send_action
        or gs.room_action
        or gs.pa.get_display_name
        or gs.pa.get_presence
    ):
        t = (
            "If --user is specified, only a send action, a room action, "
            "--get-display-name, or --get-presence can be done. "
            "Adjust your arguments accordingly."
        )
    elif not gs.pa.user and (
        gs.pa.room_invite
        or gs.pa.room_ban
        or gs.pa.room_unban
        or gs.pa.room_kick
    ):
        t = (
            "User not specified for room action. "
            "Use --user option to specify user(s) for given room action."
        )
    elif (gs.pa.listen == ONCE or gs.pa.listen == FOREVER) and gs.pa.room:
        t = (
            "If --listen once or --listen forever are specified, "
            "--room must not be specified because "
            "these options listen in ALL rooms."
        )
    elif (
        gs.pa.listen != NEVER
        and gs.pa.listen != FOREVER
        and gs.pa.listen != ONCE
        and gs.pa.listen != TAIL
        and gs.pa.listen != ALL
    ):
        t = (
            "If --listen is specified, only these choices are "
            f"possible: {ONCE}, {NEVER}, {FOREVER}, {TAIL} or {ALL}. "
            f'Found "{gs.pa.listen}".'
        )
    elif gs.pa.listen == NEVER and gs.pa.listen_self:
        t = (
            "If neither --listen nor --tail are used, "
            "then --listen-self must not be used "
            "either. Specify --listen or --tail "
            "and run program again."
        )
    elif gs.pa.listen == NEVER and (gs.pa.download_media != ""):
        t = (
            "If neither --listen nor --tail are used, "
            "then --download-media must not be used "
            "either. Specify --listen or --tail "
            f"and run program again. ({gs.pa.download_media})"
        )
    elif gs.pa.proxy and not (
        gs.pa.proxy.startswith("http://")
        or gs.pa.proxy.startswith("socks4://")
        or gs.pa.proxy.startswith("socks5://")
    ):
        t = (
            "Proxy is not correct. Proxy should start with "
            '"http://", "socks4://" or "socks5://". '
            f' Your proxy is set to "{gs.pa.proxy}".'
        )
    elif STDIN_TOTAL > 1:
        t = (
            'The character "-" is used more than once '
            'to represent "stdin" for piping information '
            f'into "{PROG_WITHOUT_EXT}". Stdin pipe can '
            "be used at most once."
        )
    elif gs.pa.no_ssl and gs.pa.ssl_certificate != SSL_CERTIFICATE_DEFAULT:
        t = (
            "Options --no-ssl and --ssl-certificate cannot be used "
            "together. Use one or the other."
        )
    else:
        gs.log.debug("All arguments are valid. All checks passed.")
        return  # all OK
    raise MatrixCommanderError(t, traceback=False)


# according to linter: function is too complex, C901
def main(
    argv: Union[None, list] = None
) -> None:  # noqa: C901 # ignore mccabe if-too-complex
    """Run the program.

    main() is an entry point allowing other Python programs to
    easily call matrix-commander.

    Arguments:
    ---------
    argv : list of arguments as in sys.argv; first element is the
        program name, further elements are the arguments; every
        element must be of type "str".
        argv is optional and can be None.
        If argv is set then these arguments will be used as arguments for
        matrix-commander. If argv is not set (None or empty list), then
        sys.argv will be used as arguments for matrix-commander.

    Example input argv: ["matrix-commander"]
        ["matrix-commander" "--version"]
        ["matrix-commander" "--message" "Hello" --image "pic.jpg"]

    Returns nothing.

    Raises exception if an error is detected. Many exceptions are
        possible. One of them is: MatrixCommanderError.

    """
    if argv:
        sys.argv = argv
    # prepare the global state
    global gs
    gs = GlobalState()
    # Construct the argument parser
    ap = argparse.ArgumentParser(
        description=(
            f"Welcome to {PROG_WITHOUT_EXT}, a Matrix CLI client. ─── "
            "On first run this program will configure itself. "
            "On further runs this program implements a simple Matrix CLI "
            "client that can send messages, listen to messages, verify "
            "devices, etc. It can send one or multiple message to one or "
            "multiple Matrix rooms and/or users. The text messages can be "
            "of various "
            'formats such as "text", "html", "markdown" or "code". '
            "Images, audio, arbitrary files, or events can be sent as well. "
            "For receiving there are three main options: listen forever, "
            "listen once and quit, and get the last N messages "
            "and quit. Emoji verification is built-in which can be used "
            "to verify devices. End-to-end encryption is enabled by default "
            "and cannot be turned off.  ─── "
            "Bundling several actions together into a single call to "
            "{PROG_WITHOUT_EXT} is faster than calling {PROG_WITHOUT_EXT} "
            "multiple times with only one action. If there are both 'set' "
            "and 'get' actions present in the arguments, then the 'set' "
            "actions will be performed before the 'get' actions. ─── "
            "For even more explications and examples also read the "
            "documentation provided in the on-line Github README.md file "
            "or the README.md in your local installation."
        ),
        epilog="You are running "
        f"version {VERSIONNR} {VERSION}. Enjoy, star on Github and "
        "contribute by submitting a Pull Request. ",
    )
    # Add the arguments to the parser
    ap.add_argument(
        "-d",
        "--debug",
        action="count",
        default=0,
        help="Print debug information. If used once, only the log level of "
        f"{PROG_WITHOUT_EXT} is set to DEBUG. "
        'If used twice ("-d -d" or "-dd") then '
        f"log levels of both {PROG_WITHOUT_EXT} and underlying modules are "
        'set to DEBUG. "-d" is a shortcut for "--log-level DEBUG". '
        'See also --log-level. "-d" takes precedence over "--log-level". ',
    )
    ap.add_argument(
        "--log-level",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Set the log level(s). Possible values are "
        '"DEBUG", "INFO", "WARNING", "ERROR", and "CRITICAL". '
        "If --log_level is used with one level argument, only the log level "
        f"of {PROG_WITHOUT_EXT} is set to the specified value. "
        "If --log_level is used with two level argument "
        '(e.g. "--log-level WARNING ERROR") then '
        f"log levels of both {PROG_WITHOUT_EXT} and underlying modules are "
        "set to the specified values. "
        "See also --debug.",
    )
    ap.add_argument(
        "-c",
        "--credentials",
        required=False,
        type=str,
        default=CREDENTIALS_FILE_DEFAULT,
        help="On first run, information about homeserver, "
        "user, room id, etc. will be written to a credentials "
        "file. By default, this file "
        f'is "{CREDENTIALS_FILE_DEFAULT}". '
        "On further runs the credentials file is read to "
        "permit logging into the correct Matrix account "
        "and sending messages to the preconfigured room. "
        "If this option is provided, the provided file name "
        "will be used as credentials file instead of the "
        "default one. ",
    )
    ap.add_argument(
        "-r",
        "--room",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Send to or receive from this room or these rooms. "
        "None, one or "
        "multiple rooms can be specified. "
        "The default room is provided "
        "in credentials file. If a room (or multiple ones) "
        "is (or are) provided in the arguments, then it "
        "(or they) will be used "
        "instead of the one from the credentials file. "
        "The user must have access to the specified room "
        "in order to send messages there or listen on the room. "
        "Messages cannot "
        "be sent to arbitrary rooms. When specifying the "
        "room id some shells require the exclamation mark "
        "to be escaped with a backslash. "
        "As an alternative to specifying a room as destination, "
        "one can specify a user as a destination with the '--user' "
        "argument. See '--user' and the term 'DM (direct messaging)' "
        "for details. Specifying a room is always faster and more "
        "efficient than specifying a user. Not all listen operations "
        "allow setting a room. Read more under the --listen options "
        "and similar. ",
    )
    ap.add_argument(
        "--room-create",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Create this room or these rooms. One or multiple "
        "room aliases can be specified. The room (or multiple "
        "ones) provided in the arguments will be created. "
        "The user must be permitted to create rooms. "
        "Combine --room-create with --name and --topic to add "
        "names and topics to the room(s) to be created.",
    )
    ap.add_argument(
        "--room-join",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Join this room or these rooms. One or multiple "
        "room aliases can be specified. The room (or multiple "
        "ones) provided in the arguments will be joined. "
        "The user must have permissions to join these rooms.",
    )
    ap.add_argument(
        "--room-leave",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Leave this room or these rooms. One or multiple "
        "room aliases can be specified. The room (or multiple "
        "ones) provided in the arguments will be left. ",
    )
    ap.add_argument(
        "--room-forget",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="After leaving a room you should (most likely) forget the room. "
        "Forgetting a room removes the users' room history. "
        "One or multiple "
        "room aliases can be specified. The room (or multiple "
        "ones) provided in the arguments will be forgotten. "
        "If all users forget a room, the room can eventually be "
        "deleted on the server.",
    )
    ap.add_argument(
        "--room-invite",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Invite one ore more users to join one or more rooms. "
        "Specify the user(s) as arguments to --user. "
        "Specify the rooms as arguments to this option, i.e. "
        "as arguments to --room-invite. "
        "The user must have permissions to invite users.",
    )
    ap.add_argument(
        "--room-ban",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Ban one ore more users from one or more rooms. "
        "Specify the user(s) as arguments to --user. "
        "Specify the rooms as arguments to this option, i.e. "
        "as arguments to --room-ban. "
        "The user must have permissions to ban users.",
    )
    ap.add_argument(
        "--room-unban",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Unban one ore more users from one or more rooms. "
        "Specify the user(s) as arguments to --user. "
        "Specify the rooms as arguments to this option, i.e. "
        "as arguments to --room-unban. "
        "The user must have permissions to unban users.",
    )
    ap.add_argument(
        "--room-kick",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Kick one ore more users from one or more rooms. "
        "Specify the user(s) as arguments to --user. "
        "Specify the rooms as arguments to this option, i.e. "
        "as arguments to --room-kick. "
        "The user must have permissions to kick users.",
    )
    ap.add_argument(
        # starting with version 2.19 "-u" has been moved from
        # --download-media to --user!
        "-u",
        "--user",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Specify one or multiple users. This option is meaningful "
        "in combination with a) room actions like --room-invite, --room-ban, "
        "--room-unban, etc. and b) send actions like -m, -i, -f, etc. "
        "as well as c) some listen actions --listen. "
        "In case of a) this option --user specifies the users "
        "to be used with room commands (like invite, ban, etc.). "
        "In case of b) the option --user can be used as an alternative "
        "to specifying a room as destination for text (-m), images (-i), "
        "etc. For send actions '--user' is providing the functionality of "
        "'DM (direct messaging)'. For c) this option allows an alternative "
        "to specifying a room as destination for some --listen actions. "
        f"What is a DM? {PROG_WITHOUT_EXT} tries to find a "
        "room that contains only the sender and the receiver, hence DM. "
        "These rooms have nothing special other the fact that they only have "
        "2 members and them being the sender and recipient respectively. "
        "If such a room is found, the first one found will be used as "
        "destination. If no such room is found, the send fails and the user "
        "should do a --room-create and --room-invite first. If multiple "
        "such rooms exist, one of them will be used (arbitrarily). "
        "For sending and listening, specifying a room directly is always "
        "faster and more efficient than specifying a user. So, if you know "
        "the room, it is preferred to use --room instead of --user. "
        "For b) and c) --user can be specified in 3 ways: 1) full user id "
        "as in '@user:example.org', 2) partial user id as in '@user' when "
        "the user is on the same homeserver (example.org will be "
        "automatically appended), or 3) a display name. Be careful, when "
        "using display names as they might not be unique, and you could "
        "be sending to the wrong person. To see possible display names use "
        "the --joined-members '*' option which will show you the display "
        "names in the middle column.",
    )
    ap.add_argument(
        "--name",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Specify one or multiple names. This option is only meaningful "
        "in combination with option --room-create. "
        "This option --name specifies the names "
        "to be used with the command --room-create.",
    )
    ap.add_argument(
        "--topic",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Specify one or multiple topics. This option is only meaningful "
        "in combination with option --room-create. "
        "This option --topic specifies the topics "
        "to be used with the command --room-create.",
    )
    # allow multiple messages , e.g. -m "m1" "m2" or -m "m1" -m "m2"
    # message is going to be a list of strings
    # e.g. message=[ 'm1', 'm2' ]
    ap.add_argument(
        "-m",
        "--message",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Send this message. Message data must not be binary data, it "
        "must be text. If no '-m' is used and no other conflicting"
        "arguments are provided, and information is piped into the program, "
        "then the piped data will be used as message. "
        "Finally, if there are no operations at all in the arguemnts, then "
        "a message will be read from stdin, i.e. from the keyboard. "
        "This option can be used multiple times to send "
        "multiple messages. If there is data piped "
        "into this program, then first data from the "
        "pipe is published, then messages from this "
        "option are published. Messages will be sent last, "
        "i.e. after objects like images, audio, files, events, etc. "
        "Input piped via stdin can additionally be specified with the "
        "special character '-'. "
        f"If you want to feed a text message into {PROG_WITHOUT_EXT} "
        "via a pipe, via stdin, then specify the special "
        "character '-'. If '-' is specified as message, "
        "then the program will read the message from stdin. "
        "If your message is literally '-' then use '\\-' "
        "as message in the argument. "
        "'-' may appear in any position, i.e. '-m \"start\" - \"end\"' "
        "will send 3 messages out of which the second one is read from stdin. "
        "'-' may appear only once overall in all arguments. ",
    )
    # allow multiple messages , e.g. -i "i1.jpg" "i2.gif"
    # or -i "i1.png" -i "i2.jpeg"
    # image is going to be a list of strings
    # e.g. image=[ 'i1.jpg', 'i2.png' ]
    ap.add_argument(
        "-i",
        "--image",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Send this image. "
        "This option can be used multiple times to send "
        "multiple images. First images are sent, "
        "then text messages are sent. "
        f"If you want to feed an image into {PROG_WITHOUT_EXT} "
        "via a pipe, via stdin, then specify the special "
        "character '-'. If '-' is specified as image file name, "
        "then the program will read the image data from stdin. "
        "If your image file is literally named '-' then use '\\-' "
        "as filename in the argument. "
        "'-' may appear in any position, i.e. '-i image1.jpg - image3.png' "
        "will send 3 images out of which the second one is read from stdin. "
        "'-' may appear only once overall in all arguments. "
        "If the file exists already, it is more efficient to specify the "
        "file name than to pipe the file through stdin.",
    )
    # allow multiple audio files , e.g. -i "a1.mp3" "a2.wav"
    # or -i "a1.mp3" -i "a2.m4a"
    # audio is going to be a list of strings
    # e.g. audio=[ 'a1.mp3', 'a2.m4a' ]
    ap.add_argument(
        "-a",
        "--audio",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Send this audio file. "
        "This option can be used multiple times to send "
        "multiple audio files. First audios are sent, "
        "then text messages are sent. "
        f"If you want to feed an audio into {PROG_WITHOUT_EXT} "
        "via a pipe, via stdin, then specify the special "
        "character '-'. See description of '-i' to see how '-' is handled.",
    )
    # allow multiple files , e.g. -f "a1.pdf" "a2.doc"
    # or -f "a1.pdf" -f "a2.doc"
    # file is going to be a list of strings
    # e.g. file=[ 'a1.pdf', 'a2.doc' ]
    ap.add_argument(
        "-f",
        "--file",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Send this file (e.g. PDF, DOC, MP4). "
        "This option can be used multiple times to send "
        "multiple files. First files are sent, "
        "then text messages are sent. "
        f"If you want to feed a file into {PROG_WITHOUT_EXT} "
        "via a pipe, via stdin, then specify the special "
        "character '-'. See description of '-i' to see how '-' is handled.",
    )
    ap.add_argument(
        "-e",
        "--event",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Send an event that is formatted as a JSON object as "
        "specified by the Matrix protocol. This allows the advanced "
        "user to send additional types of events such as reactions, "
        "send replies to previous events, or edit previous messages. "
        "Specifications for events can be found "
        "at https://spec.matrix.org/unstable/proposals/. "
        "This option can be used multiple times to send "
        "multiple events. First events are sent, "
        "then text messages are sent. "
        f"If you want to feed an event into {PROG_WITHOUT_EXT} "
        "via a pipe, via stdin, then specify the special "
        "character '-'. See description of '-i' to see how '-' is handled.",
    )
    # -h already used for --help, -w for "web"
    ap.add_argument(
        "-w",
        "--html",
        required=False,
        action="store_true",
        help="Send message as format "
        '"HTML". If not specified, message will be sent '
        'as format "TEXT". E.g. that allows some text '
        "to be bold, etc. Only a subset of HTML tags are "
        "accepted by Matrix.",
    )
    # -m already used for --message, -z because there were no letters left
    ap.add_argument(
        "-z",
        "--markdown",
        required=False,
        action="store_true",
        help="Send message as format "
        '"MARKDOWN". If not specified, message will be sent '
        'as format "TEXT". E.g. that allows sending of text '
        "formatted in MarkDown language.",
    )
    #  -c is already used for --credentials, -k as it sounds like c
    ap.add_argument(
        "-k",
        "--code",
        required=False,
        action="store_true",
        help="Send message as format "
        '"CODE". If not specified, message will be sent '
        'as format "TEXT". If both --html and --code are '
        "specified then --code takes priority. This is "
        "useful for sending ASCII-art or tabbed output "
        "like tables as a fixed-sized font will be used "
        "for display.",
    )
    # -s is already used for --store, -i for sPlit
    ap.add_argument(
        "-p",
        "--split",
        required=False,
        type=str,
        help="If set, split the message(s) into multiple messages "
        "wherever the string specified with --split occurs. "
        "E.g. One pipes a stream of RSS articles into the "
        "program and the articles are separated by three "
        "newlines. "
        'Then with --split set to "\\n\\n\\n" each article '
        "will be printed in a separate message. "
        "By default, i.e. if not set, no messages will be split.",
    )
    # -c is already used for --credentials
    ap.add_argument(
        "-j",
        "--config",
        required=False,
        type=str,
        help="Location of a config file. By default, no "
        "config file is used. "
        "If this option is provided, the provided file name "
        "will be used to read configuration from. ",
    )
    # -p is already used for --split
    ap.add_argument(
        "--proxy",
        required=False,
        type=str,
        help="Optionally specify a proxy for connectivity. By default, "
        "i.e. if this option is not set, no proxy is used. "
        "If this option is used a proxy URL must be provided. "
        "The provided proxy URL "
        "will be used for the HTTP connection to the server. "
        "The proxy supports SOCKS4(a), SOCKS5, and HTTP (tunneling). "
        'Examples of valid URLs are "http://10.10.10.10:8118" '
        'or "socks5://user:password@127.0.0.1:1080". '
        'URLs with "https" or "socks4a" are not valid. Only '
        '"http", "socks4" and "socks5" are valid.',
    )
    ap.add_argument(
        "-n",
        "--notice",
        required=False,
        action="store_true",
        help="Send message as notice. "
        "If not specified, message will be sent as text.",
    )
    ap.add_argument(
        # no single char flag
        "--encrypted",
        required=False,
        action="store_true",
        help="Send message end-to-end "
        "encrypted. Encryption is always turned on and "
        "will always be used where possible. "
        "It cannot be turned off. This flag does nothing "
        "as encryption is turned on with or without this "
        "argument.",
    )
    ap.add_argument(
        "-s",
        "--store",
        required=False,
        type=str,
        default=STORE_DIR_DEFAULT,
        help="Path to directory to be "
        'used as "store" for encrypted messaging. '
        "By default, this directory "
        f'is "{STORE_DIR_DEFAULT}". '
        "Since encryption is always enabled, a store is "
        "always needed. "
        "If this option is provided, the provided directory name "
        "will be used as persistent storage directory instead of "
        "the default one. Preferably, for multiple executions "
        "of this program use the same store for the same device. "
        "The store directory can be shared between multiple "
        "different devices and users.",
    )
    ap.add_argument(
        "-l",
        "--listen",
        required=False,
        type=str,
        default=LISTEN_DEFAULT,  # when -l is not used
        nargs="?",  # makes the word optional
        const=FOREVER,  # when -l is used, but FOREVER is not added
        help="The --listen option takes one argument. There "
        f'are several choices: "{NEVER}", "{ONCE}", '
        f'"{FOREVER}", "{TAIL}", and "{ALL}". '
        f'By default, --listen is set to "{NEVER}".  So, by '
        "default no listening will be done. Set it to "
        f'"{FOREVER}" to listen for and print incoming messages '
        "to stdout. "
        f'"--listen {FOREVER}" will listen to all messages on '
        "all rooms forever. "
        f'To stop listening "{FOREVER}", use Control-C on '
        "the keyboard or send a signal to the process or service. "
        "The PID for signaling can be found in a PID file in "
        f'directory "{PID_DIR_DEFAULT}". '
        f'"--listen {ONCE}" will get all the messages from '
        "all rooms that are currently queued up. So, with "
        f'"{ONCE}" the program will start, print waiting '
        "messages (if any) and then stop. The timeout for "
        f'"{ONCE}" is set to 10 seconds. So, be patient, it '
        "might take up to that amount of time. "
        f'"{TAIL}" reads and prints the last N '
        "messages from the specified rooms, then quits. The "
        "number N can be set with the --tail option. With "
        f'"{TAIL}" some messages read might be old, '
        "i.e. already read before, some might be new, "
        "i.e. never read before. It prints the messages and then "
        f"the program stops. "
        "Messages are sorted, last-first. "
        "Look at --tail as that option is related "
        "to --listen tail. "
        f'The option "{ALL}" gets all messages available, '
        "old and new. "
        f'Unlike "{ONCE}" and '
        f'"{FOREVER}" that listen in ALL rooms, "{TAIL}" '
        f'and "{ALL}" listen '
        "only to the room specified in the credentials "
        "file or the --room options. "
        "Furthermore, when listening to messages, no messages "
        "will be sent. Hence, when listening, --message must not "
        "be used and piped input will be ignored. ",
    )
    ap.add_argument(
        "-t",
        "--tail",
        required=False,
        type=int,
        default=TAIL_UNUSED_DEFAULT,  # when -t is not used
        nargs="?",  # makes the word optional
        # when -t is used, but number is not added
        const=TAIL_USED_DEFAULT,
        help="The --tail option reads and prints up to the last N "
        "messages from the specified rooms, then quits. "
        "It takes one "
        "argument, an integer, "
        "which we call N here. If there are fewer than N messages "
        "in a room, it reads and prints up to N messages. "
        "It gets the last N messages in reverse order. "
        "It print the newest message first, and the "
        "oldest message last. "
        "If --listen-self is not set it will print less than "
        "N messages in many cases because N messages are "
        "obtained, but some of them are discarded by default if "
        "they are from the user itself. "
        "Look at --listen as this option is related to --tail."
        "Furthermore, when tailing messages, no messages "
        "will be sent. Hence, when tailing or listening, "
        "--message  must not be used and piped input will "
        "be ignored. ",
    )
    ap.add_argument(
        "-y",
        "--listen-self",
        required=False,
        action="store_true",
        help="If set and listening, "
        "then program will listen to and print also "
        "the messages sent by its own user. "
        "By default messages from oneself are not printed.",
    )
    ap.add_argument(
        # no single char flag
        "--print-event-id",
        required=False,
        action="store_true",
        help="If set and listening, "
        "then program will print also the event id for"
        "each message or other event.",
    )
    ap.add_argument(
        # starting with version 2.19 "-u" has been moved to --user!
        "--download-media",
        type=str,
        default="",  # if --download-media is not used
        action="store",
        nargs="?",  # makes the word optional
        const=MEDIA_DIR_DEFAULT,  # when option is used, but no dir added
        help="If set and listening, "
        "then program will download "
        "received media files (e.g. image, audio, video, text, PDF files). "
        "media will be downloaded to local directory. "
        "By default, media will be downloaded to "
        f'is "{MEDIA_DIR_DEFAULT}". '
        "You can overwrite default with your preferred directory. "
        "If media is encrypted it will be decrypted and stored decrypted. "
        "By default media files will not be downloaded.",
    )
    ap.add_argument(
        "-o",
        "--os-notify",
        required=False,
        action="store_true",
        help="If set and listening, "
        "then program will attempt to visually notify of "
        "arriving messages through the operating system. "
        "By default there is no notification via OS.",
    )
    ap.add_argument(
        "-v",
        "--verify",
        required=False,
        type=str,
        default=VERIFY_UNUSED_DEFAULT,  # when -t is not used
        nargs="?",  # makes the word optional
        # when -v is used, but text is not added
        const=VERIFY_USED_DEFAULT,
        help="Perform verification. By default, no "
        "verification is performed. "
        f'Possible values are: "{EMOJI}". '
        "If verification is desired, run this program in the "
        "foreground (not as a service) and without a pipe. "
        "Verification questions "
        "will be printed on stdout and the user has to respond "
        "via the keyboard to accept or reject verification. "
        "Once verification is complete, stop the program and "
        "run it as a service again. Don't send messages or "
        "files when you verify.",
    )
    ap.add_argument(
        # removed "-x", starting v2.21 -x is no longer supported
        "--set-device-name",
        required=False,
        type=str,
        default=SET_DEVICE_NAME_UNUSED_DEFAULT,  # when option isn't used
        help="Set or rename the current device to the "
        "device name provided. "
        "Send, listen and verify operations are allowed when "
        "renaming the device.",
    )
    ap.add_argument(
        "--set-display-name",
        required=False,
        type=str,
        default=SET_DISPLAY_NAME_UNUSED_DEFAULT,  # when option isn't used
        help="Set or rename the display name for the current user to the "
        "display name provided. "
        "Send, listen and verify operations are allowed when "
        "setting the display name.",
    )
    ap.add_argument(
        "--get-display-name",
        required=False,
        action="store_true",
        help=f"Get the display name of {PROG_WITHOUT_EXT} (itself), "
        "or of one or multiple users. Specify user(s) with the "
        "--user option. If no user is specified get the display name of "
        "itself. "
        "Send, listen and verify operations are allowed when "
        "getting display name(s).",
    )
    ap.add_argument(
        "--set-presence",
        required=False,
        type=str,
        # defaults to None if not used, is str if used
        help="Set presence of {PROG_WITHOUT_EXT} to the given value. "
        "Must be one of these values: “online”, “offline”, “unavailable”. "
        "Otherwise an error will be produced.",
    )
    ap.add_argument(
        "--get-presence",
        required=False,
        action="store_true",
        # defaults to False if not used
        help="Get presence of {PROG_WITHOUT_EXT} (itself), "
        "or of one or multiple users. Specify user(s) with the "
        "--user option. If no user is specified get the presence of "
        "itself. "
        "Send, listen and verify operations are allowed when "
        "getting presence(s).",
    )
    ap.add_argument(
        # no single char flag
        "--no-ssl",
        required=False,
        action="store_true",
        default=NO_SSL_UNUSED_DEFAULT,  # when option isn't used
        help="Skip SSL verification. By default (if this option is not used) "
        "the SSL certificate is validated for the connection. But, if this "
        "option is used, then the SSL certificate validation will be skipped. "
        "This is useful for home-servers that have no SSL certificate. "
        'If used together with the "--ssl-certificate" '
        "parameter, this option is meaningless and an error will be raised.",
    )
    ap.add_argument(
        # no single char flag
        "--ssl-certificate",
        required=False,
        type=str,
        default=SSL_CERTIFICATE_DEFAULT,  # when option isn't used
        help="Use this option to use your own local SSL certificate file. "
        "This is an optional parameter. This is useful for home servers that "
        "have their own "
        "SSL certificate. This allows you to use HTTPS/TLS for the connection "
        "while using your own local SSL certificate. Specify the path and "
        'file to your SSL certificate. If used together with the "--no-ssl" '
        "parameter, this option is meaningless and an error will be raised.",
    )
    ap.add_argument(
        # no single char flag
        "--no-sso",  # no Single Sign-On
        required=False,
        action="store_true",
        default=NO_SSO_UNUSED_DEFAULT,  # when option isn't used
        help="This argument is optional. If it is not used, the default "
        "login method will be used. This default login method is: "
        "SSO (Single Sign-On). SSO starts a web browser and connects the "
        "user to a webpage on the server for login. SSO will only work if "
        "the server supports it and if there is access to a browser. "
        "If this argument is used, then SSO will be avoided. This is useful "
        "on headless homeservers where there is no browser installed or "
        "accessible. It is also useful if the user prefers to login via a "
        "password. So, if SSO should be avoided and a password login is "
        "preferred then set this option. This option is only meaningful "
        f"on the first run that initializes {PROG_WITHOUT_EXT}. "
        "Once credentials are established this option is irrelevant and "
        "it will simply be ignored.",
    )
    ap.add_argument(
        # no single char flag
        "--joined-rooms",
        required=False,
        action="store_true",
        help="Print the list of joined rooms. All rooms that you are a "
        "member of will be printed, one room per line.",
    )
    ap.add_argument(
        # no single char flag
        "--joined-members",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        help="Print the list of joined members for one or multiple rooms. "
        "If you want to print the joined members of all rooms that you "
        "are member of, then use the special character '*'.",
    )
    ap.add_argument(
        # no single char flag
        "--whoami",
        required=False,
        action="store_true",
        help=f"Print the user id used by {PROG_WITHOUT_EXT} (itself). "
        "One can get "
        "this information also by looking at the credentials file.",
    )
    ap.add_argument(
        # no single char flag
        "--version",
        required=False,
        action="store_true",
        help="Print version information. After printing version information "
        "program will continue to run. This is useful for having version "
        "number in the log files.",
    )
    gs.pa = ap.parse_args()

    logging.basicConfig(  # initialize root logger, a must
        format="{asctime}: {levelname:>8}: {name:>16}: {message}", style="{"
    )
    # set log level on root
    if "DEBUG" in os.environ:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    gs.log = logging.getLogger(PROG_WITHOUT_EXT)

    if gs.pa.log_level:
        initial_check_of_log_args()
        if len(gs.pa.log_level) > 0:
            if len(gs.pa.log_level) > 1:
                # set log level for EVERYTHING
                logging.getLogger().setLevel(gs.pa.log_level[1])
            # set log level for matrix-commander
            gs.log.setLevel(gs.pa.log_level[0])
            gs.log.debug(
                f"Log level is set for module {PROG_WITHOUT_EXT}. "
                f"log_level={gs.pa.log_level[0]}"
            )
            if len(gs.pa.log_level) > 1:
                # only now that local log level is set, we can log prev. info
                gs.log.debug(
                    f"Log level is set for modules below {PROG_WITHOUT_EXT}. "
                    f"log_level={gs.pa.log_level[1]}"
                )
    if gs.pa.debug > 0:
        if gs.pa.debug > 1:
            # turn on debug logging for EVERYTHING
            logging.getLogger().setLevel(logging.DEBUG)
        # turn on debug logging for matrix-commander
        gs.log.setLevel(logging.DEBUG)
        gs.log.debug(f"Debug is turned on. debug count={gs.pa.debug}")
        if gs.pa.log_level and len(gs.pa.log_level) > 0:
            gs.log.warning("Debug option -d overwrote option --log-level.")

    initial_check_of_args()
    check_download_media_dir()
    try:
        check_arg_files_readable()
    except Exception as e:
        gs.log.error(e)
        raise MatrixCommanderError(
            f"{PROG_WITHOUT_EXT} forces an early abort. "
            "To avoid partial execution, no action has been performed at all. "
            "Nothing has been sent. Fix your arguments and run the command "
            "again."
        )

    if gs.pa.version:
        version()  # continue execution
        if not (
            gs.send_action
            or gs.room_action
            or gs.pa.listen != LISTEN_DEFAULT
            or gs.pa.tail != TAIL_UNUSED_DEFAULT
            or gs.pa.verify
            or gs.setget_action
        ):
            gs.log.debug("Only --version. Print and quit.")
            return  # just version, quit

    create_pid_file()

    gs.log.debug(f'Stdin pipe is assigned to "{gs.stdin_use}".')
    if gs.pa.ssl_certificate != SSL_CERTIFICATE_DEFAULT:
        gs.log.debug(
            "SSL will be used. A custom SSL certificate was provided. "
            f'Custom certificate from file "{gs.pa.ssl_certificate}" will '
            "be used for this connection."
        )
        try:
            # type SSLContext
            gs.ssl = ssl.create_default_context(cafile=gs.pa.ssl_certificate)
        except FileNotFoundError:
            raise MatrixCommanderError(
                f'SSL certificate file "{gs.pa.ssl_certificate}" was '
                "not found.",
                traceback=False,
            )
        except PermissionError:
            raise MatrixCommanderError(
                f'SSL certificate file "{gs.pa.ssl_certificate}" does '
                "not have read permissions.",
                traceback=False,
            )
        except ssl.SSLError:
            raise MatrixCommanderError(
                f'SSL certificate file "{gs.pa.ssl_certificate}" has '
                "invalid content. Does not seem to be a certificate.",
                traceback=False,
            )
    elif gs.pa.no_ssl:
        gs.log.debug(
            "SSL will be not be used. The SSL certificate validation "
            "will be skipped for this connection."
        )
        gs.ssl = False
    else:
        gs.log.debug(
            "SSL will be used. Default SSL certificate validation "
            "will be done for this connection."
        )
        gs.ssl = None

    try:
        if gs.pa.verify:
            asyncio.run(main_verify())
        elif (
            gs.pa.listen == FOREVER
            or gs.pa.listen == ONCE
            or gs.pa.listen == TAIL
            or gs.pa.listen == ALL
        ):
            asyncio.run(main_listen())
        elif gs.room_action or gs.setget_action:
            asyncio.run(main_roomsetget_action())
        else:  # send_action
            asyncio.run(main_send())
        # the next can be reached on success or failure
        gs.log.debug(f"The program {PROG_WITH_EXT} left the event loop.")
    except TimeoutError:
        cleanup()
        raise MatrixCommanderError(
            f"The program {PROG_WITH_EXT} ran into a timeout. "
            "Most likely connectivity to internet was lost. "
            "If this happens frequently consider running this "
            "program as a service so it will restart automatically. Sorry.",
            True,
        )
    except MatrixCommanderError as e:
        cleanup()
        raise MatrixCommanderError(
            f"{e}", traceback=e.traceback, level=e.level
        )
    except Exception as e:
        cleanup()
        raise MatrixCommanderError(
            f"The program {PROG_WITH_EXT} failed. Sorry.\n{e}",
            traceback=True,
        )
    except KeyboardInterrupt:
        gs.log.debug("Keyboard interrupt received.")
    cleanup()


if __name__ == "__main__":
    try:
        main()
    except MatrixCommanderError as e:
        tb = ""
        if e.traceback:
            tb = f"\nHere is the traceback.\n{traceback.format_exc()}"
        if e.level == "info":
            gs.log.info(f"{e}{tb}")
        else:
            gs.log.error(f"{e}{tb}")
        sys.exit(1)
    except Exception as e:
        tb = ""
        if gs.pa.debug > 0:
            tb = f"\nHere is the traceback.\n{traceback.format_exc()}"
        gs.log.error(f"{e}{tb}")
        sys.exit(1)
    sys.exit(0)
# EOF
