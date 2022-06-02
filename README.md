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

