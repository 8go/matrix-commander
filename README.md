[![Built with matrix-nio](
https://img.shields.io/badge/built%20with-matrix--nio-brightgreen)](
https://github.com/poljar/matrix-nio)

![logo](matrix-commander-logo.svg)

# matrix-commander

Simple but convenient CLI-based Matrix client app for sending and receiving.

- `matrix-commander` is a simple command-line [Matrix](https://matrix.org/)
  client.
- It is a simple but convenient app to
    - send Matrix text messages as well as text, image, audio, video or
      other arbitrary files
    - listen to and receive Matrix messages
    - perform Matrix emoji verification
- It exclusively offers a command-line interface (CLI).
- Hence the word-play: matrix-command(lin)er
- There is no GUI and there are no windows (except for pop-up windows in
  OS notification)
- It uses the [matrix-nio](https://github.com/poljar/matrix-nio/) SDK
- Both `matrix-nio` and `matrix-commander` are written in Python 3

# Summary

This program is a simple but convenient app to send and receive Matrix
messages from the CLI in various different ways.

Use cases for this program could be
- a bot or part of a bot,
- to send alerts,
- combine it with cron to publish periodic data,
- send yourself daily/weekly reminders via a cron job
- send yourself a daily song from your music collection
- a trivial way to fire off some instant messages from the command line
- to automate sending via programs and scripts
- a "blogger" who frequently sends messages and images to the same
  room(s) could use it
- a person could write a diary or run a gratitutde journal by
  sending messages to her/his own room
- as educational material that showcases the use of the `matrix-nio` SDK

# Give it a Star
If you like it, use it, fork it, make a Pull Request or contribute.
Please give it a :star: on GitHub right now so others find it more easily. :heart:

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
2) as input from the keyboard
3) through a pipe from stdin (|), i.e. piped in from another program.

For sending messages the program supports various text formats:
1) text: default
2) html:  HTML formated text
3) markdown: MarkDown formatted text
4) code: used a block of fixed-sized font, ideal for ASCII art or
   tables, bash outputs, etc.
5) notification
6) split: splits messages into multiple units at given pattern

Photos and images that can be sent. That includes files like
.jpg, .gif, .png or .svg.

Arbirtary files like .txt, .pdf, .doc, audio files like .mp3
or video files like .mp4 can also be sent.

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

# Summary, TLDR

This simple Matrix client written in Python allows you to send and
receive messages and verify other devices. End-to-end encryption is enabled
by default and cannot be turned off.

# Dependencies, Requirements

- Python 3.8 or higher (3.7 will NOT work) installed
- `libolm-dev` must be installed as it is required by `matrix-nio`
  - `libolm-devel` on Debian/Ubuntu, `libolm-dev` on Fedora, `libolm` on MacOS
- matrix-nio must be installed, see https://github.com/poljar/matrix-nio
  - pip3 install --user --upgrade matrix-nio[e2e]
- python3 package markdown must be installed to support MarkDown format
  - pip3 install --user --upgrade markdown
- python3 package python_magic must be installed to support image sending
  - pip3 install --user --upgrade python_magic
- python3 package notify2 must be installed to support OS notifications
  - pip3 install --user --upgrade notify2
- python3 package urllib must be installed to support media download
  - pip3 install --user --upgrade urllib
- the matrix-commander.py file must be installed, and should have execution permissions
  - chmod 755 matrix-commander.py
- for a full list or requirements look at the `requirements.txt` file
  - `pip install -r requirements.txt` to automatically install all required Python packages

# Examples of calling `matrix-commander`

```
$ matrix-commander.py #  first run; this will configure everything
$ # this created a credentials.json file, and a store directory
$ # optionally, if you want you can move credentials to app config directory
$ mkdir $HOME/.config/matrix-commander # optional
$ mv -i credentials.json $HOME/.config/matrix-commander/
$ # optionally, if you want you can move store to the app share directory
$ mkdir $HOME/.local/share/matrix-commander # optional
$ mv -i store $HOME/.local/share/matrix-commander/
$ # Now you are ready to run program for a second time
$ # Let us verify the device/room to where we want to send messages
$ # The other device will issue a "verify by emoji" request
$ matrix-commander.py --verify
$ # Now program is both configured and verified, let us send the first message
$ matrix-commander.py -m "First message!"
$ matrix-commander.py --debug # turn debugging on
$ matrix-commander.py --help # print help
$ matrix-commander.py # this will ask user for message to send
$ matrix-commander.py --message "Hello World!" # sends provided message
$ echo "Hello World" | matrix-commander.py # pipe input msg into program
$ matrix-commander.py -m msg1 -m msg2 # sends 2 messages
$ matrix-commander.py -m msg1 msg2 msg3 # sends 3 messages
$ df -h | matrix-commander.py --code # formatting for code/tables
$ matrix-commander.py -m "<b>BOLD</b> and <i>ITALIC</i>" --html
$ matrix-commander.py -m "- bullet1" --markdown
$ # take input from an RSS feed and split large RSS entries into multiple
$ # Matrix messages wherever the pattern "\n\n\n" is found
$ rssfeed | matrix-commander.py --split "\n\n\n"
$ matrix-commander.py --credentials usr1room2.json # select credentials file
$ matrix-commander.py --store /var/storage/ # select store directory
$ # Send to a specific room
$ matrix-commander.py -m "hi" --room '!YourRoomId:example.org'
$ # some shells require the ! of the room id to be escaped with \
$ matrix-commander.py -m "hi" --room "\!YourRoomId:example.org"
$ # Send to multiple rooms
$ matrix-commander.py -m "hi" -r '!r1:example.org' '!r2:example.org'
$ # Send to multiple rooms, another way
$ matrix-commander.py -m "hi" -r '!r1:example.org' -r '!r2:example.org'
$ # send 2 images and 1 text
$ matrix-commander.py -i photo1.jpg photo2.img -m "Do you like my 2 photos?"
$ # send 1 image and no text
$ matrix-commander.py -i photo1.jpg -m ""
$ # send 1 audio and 1 text to 2 rooms
$ matrix-commander.py -a song.mp3 -m "Do you like this song?" \
    -r "!someroom1:example.com" "!someroom2:example.com"
$ # send a .pdf file and a video with a text
$ matrix-commander.py -f example.pdf video.mp4 -m "Here are the promised files"
$ # listen forever, get msgs in real-time and notify me via OS
$ matrix-commander.py --listen forever --os-notify
$ # listen forever, and show me also my own messages
$ matrix-commander.py --listen forever --listen-self
$ # listen once, get any new messages and quit
$ matrix-commander.py --listen once --listen-self
$ matrix-commander.py --listen once --listen-self | process-in-other-app
$ # listen to tail, get the last N messages and quit
$ matrix-commander.py --listen tail --tail 10 --listen-self
$ # listen to tail, another way of specifying it
$ matrix-commander.py --tail 10 --listen-self | process-in-other-app
$ # get the very last message
$ matrix-commander.py --tail 1 --listen-self
$ # listen to (get) all messages, old and new, and process them in another app
$ matrix-commander.py --listen all | process-in-other-app
$ # listen to (get) all messages, including own
$ matrix-commander.py --listen all --listen-self
$ # rename device-name, sometimes also called display-name
$ matrix-commander.py --rename-device "my new name"
$ # download and decrypt media files like images, audio, PDF, etc.
$ # and store downloaded files in directory "mymedia"
$ matrix-commander.py --listen forever --listen-self --download-media mymedia

```

# Usage
```
usage: matrix-commander.py [-h] [-d] [-c CREDENTIALS] [-r ROOM [ROOM ...]]
                           [-m MESSAGE [MESSAGE ...]] [-i IMAGE [IMAGE ...]]
                           [-a AUDIO [AUDIO ...]] [-f FILE [FILE ...]] [-w]
                           [-z] [-k] [-p SPLIT] [-j CONFIG] [-n] [-e]
                           [-s STORE] [-l [LISTEN]] [-t [TAIL]] [-y]
                           [-u [DOWNLOAD_MEDIA]] [-o] [-v [VERIFY]]
                           [-x RENAME_DEVICE]

On first run this program will configure itself. On further runs this program
implements a simple Matrix CLI client that can send messages, listen to
messages and verify devices. It can send one or multiple message to one or
multiple Matrix rooms. The text messages can be of various formats such as
"text", "html", "markdown" or "code". Images, audio or arbitrary files can be
sent as well. For receiving there are three main options: listen forever,
listen once and quit, and get the last N messages and quit. Emoji verification
is built-in which can be used to verify devices. End-to-end encryption is
enabled by default and cannot be turned off. matrix-nio
(https://github.com/poljar/matrix-nio) and end-to-end encryption packages must
be installed. See dependencies in source code (or README.md). For even more
explications run this program with the --help option or read the full
documentation in the source code.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
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
                        Send to this room or these rooms. None, one or
                        multiple rooms can be specified. The default room is
                        provided in credentials file. If a room (or multiple
                        ones) is (or are) provided in the arguments, then it
                        (or they) will be used instead of the one from the
                        credentials file. The user must have access to the
                        specified room in order to send messages there.
                        Messages cannot be sent to arbitrary rooms. When
                        specifying the room id some shells require the
                        exclamation mark to be escaped with a blackslash.
  -m MESSAGE [MESSAGE ...], --message MESSAGE [MESSAGE ...]
                        Send this message. If not specified, and no input
                        piped in from stdin, then message will be read from
                        stdin, i.e. keyboard. This option can be used multiple
                        time to send multiple messages. If there is data is
                        piped into this program, then first data from the pipe
                        is published, then messages from this option are
                        published.
  -i IMAGE [IMAGE ...], --image IMAGE [IMAGE ...]
                        Send this image. This option can be used multiple time
                        to send multiple images. First images are send, then
                        text messages are send.
  -a AUDIO [AUDIO ...], --audio AUDIO [AUDIO ...]
                        Send this audio file. This option can be used multiple
                        time to send multiple audio files. First audios are
                        send, then text messages are send.
  -f FILE [FILE ...], --file FILE [FILE ...]
                        Send this file (e.g. PDF, DOC, MP4). This option can
                        be used multiple time to send multiple files. First
                        files are send, then text messages are send.
  -w, --html            Send message as format "HTML". If not specified,
                        message will be sent as format "TEXT". E.g. that
                        allows some text to be bold, etc. Only a subset of
                        HTML tags are accepted by Matrix.
  -z, --markdown        Send message as format "MARKDOWN". If not specified,
                        message will be sent as format "TEXT". E.g. that
                        allows sending of text formated in MarkDown language.
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
  -n, --notice          Send message as notice. If not specified, message will
                        be sent as text.
  -e, --encrypted       Send message end-to-end encrypted. Encryption is
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
  -u [DOWNLOAD_MEDIA], --download-media [DOWNLOAD_MEDIA]
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
  -x RENAME_DEVICE, --rename-device RENAME_DEVICE
                        Rename the current device to the new device name
                        provided. No other operations like sending, listening,
                        or verifying are allowed when renaming the device.

```

# Features

- CLI, Command Line Interface
- Python 3
- Uses nio-template
- End-to-end encryption
- Storage for End-to-end encryption
- Storage of credentials
- Supports access token instead of password
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
- Receiving messages forever
- Receiving messages once
- Receiving last messages
- Receiving or skipping its own messages
- Supports renaming of device
- Supports notification via OS of received messages
- Supports periodic execution via crontab
- Supports room aliases
- Provides PID files
- Logging
- In-source documentation
- Can be run as a service

# For Developers

- Don't change tabbing, spacing, or formating as file is automatically
  sorted, linted and formated.
- `pylama:format=pep8:linters=pep8`
- first `isort` import sorter
- then `flake` linter/formater
- then `black` linter/formater
- linelength: 79

# Things to do, Things missing

- help me add config file handling

# Final Remarks

- Enjoy!
- Pull requests are welcome

