#!/usr/bin/env python3

r"""matrix_commander.py.

For help and documentation, please read the README.md file.
Online available at:
https://github.com/8go/matrix-commander/blob/master/README.md

"""

# 234567890123456789012345678901234567890123456789012345678901234567890123456789
# 000000001111111111222222222233333333334444444444555555555566666666667777777777

# automatically sorted by isort,
# then formatted by black --line-length 79


import argparse
import ast
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
from typing import Literal, Optional, Union
from urllib.parse import quote, urlparse

import aiofiles
import aiofiles.os
import emoji
import magic
import pkg_resources
from aiohttp import ClientConnectorError, ClientSession, TCPConnector, web
from markdown import markdown
from nio import (AsyncClient, AsyncClientConfig, ContentRepositoryConfigError,
                 DeleteDevicesAuthResponse, DeleteDevicesError, DevicesError,
                 DiscoveryInfoError, DownloadError, EnableEncryptionBuilder,
                 EncryptionError, ErrorResponse, InviteMemberEvent,
                 JoinedMembersError, JoinedRoomsError, JoinError,
                 KeyVerificationCancel, KeyVerificationEvent,
                 KeyVerificationKey, KeyVerificationMac, KeyVerificationStart,
                 LocalProtocolError, LoginInfoError, LoginResponse,
                 LogoutError, MatrixRoom, MessageDirection, PresenceGetError,
                 PresenceSetError, ProfileGetAvatarResponse,
                 ProfileGetDisplayNameError, ProfileGetError,
                 ProfileSetAvatarResponse, ProfileSetDisplayNameError,
                 RedactedEvent, RedactionEvent, RoomAliasEvent, RoomBanError,
                 RoomCreateError, RoomDeleteAliasResponse, RoomEncryptedAudio,
                 RoomEncryptedFile, RoomEncryptedImage, RoomEncryptedMedia,
                 RoomEncryptedVideo, RoomEncryptionEvent, RoomForgetError,
                 RoomGetStateResponse, RoomGetVisibilityResponse,
                 RoomInviteError, RoomKickError, RoomLeaveError,
                 RoomMemberEvent, RoomMessage, RoomMessageAudio,
                 RoomMessageEmote, RoomMessageFile, RoomMessageFormatted,
                 RoomMessageImage, RoomMessageMedia, RoomMessageNotice,
                 RoomMessagesError, RoomMessageText, RoomMessageUnknown,
                 RoomMessageVideo, RoomNameEvent, RoomPreset,
                 RoomPutAliasResponse, RoomReadMarkersError, RoomRedactError,
                 RoomResolveAliasError, RoomResolveAliasResponse,
                 RoomSendError, RoomUnbanError, RoomVisibility, SyncError,
                 SyncResponse, ToDeviceError, UnknownEvent, UpdateDeviceError,
                 UploadError, UploadResponse, crypto, responses)
from PIL import Image
from xdg import BaseDirectory

try:
    import notify2

    HAVE_NOTIFY = True
except ImportError:
    HAVE_NOTIFY = False

try:
    from nio import GetOpenIDTokenError

    HAVE_OPENID = True
except ImportError:
    HAVE_OPENID = False

# version number
VERSION = "2023-10-12"
VERSIONNR = "7.4.0"
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
    BaseDirectory.xdg_config_home + "/"  # "~/.config/"
) + os.path.splitext(os.path.basename(__file__))[0].replace("_", "-")
# directory to be used by end-to-end encrypted protocol for persistent storage
STORE_DIR_DEFAULT = "./store/"
# e.g. ~/.local/share/matrix-commander/
# the STORE_PATH_LASTRESORT will be concatenated with a directory name
# like store to result in a final path of
# e.g. ~/.local/share/matrix-commander/store/ as actual persistent store dir
STORE_PATH_LASTRESORT = os.path.normpath(
    (
        os.path.expanduser(
            BaseDirectory.xdg_data_home + "/"
        )  # ~/.local/share/
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
PRINT = "print"  # version type
CHECK = "check"  # version type
ONCE = "once"  # listening type
NEVER = "never"  # listening type
FOREVER = "forever"  # listening type
ALL = "all"  # listening type
TAIL = "tail"  # listening type
DEFAULT_SEPARATOR = "    "  # used for sperating columns in print outputs
SEP = DEFAULT_SEPARATOR
LISTEN_DEFAULT = NEVER
TAIL_UNUSED_DEFAULT = 0  # get 0 if --tail is not specified
TAIL_USED_DEFAULT = 10  # get the last 10 msgs by default with --tail
VERIFY_UNUSED_DEFAULT = None  # use None if --verify is not specified
VERIFY_USED_DEFAULT = EMOJI  # use 'emoji' by default with --verify
VERSION_UNUSED_DEFAULT = None  # use None if --version is not specified
VERSION_USED_DEFAULT = PRINT  # use 'print' by default with --version
SET_DEVICE_NAME_UNUSED_DEFAULT = None  # use None if option is not specified
SET_DISPLAY_NAME_UNUSED_DEFAULT = None  # use None option not used
NO_SSL_UNUSED_DEFAULT = None  # use None if --no-ssl is not given
SSL_CERTIFICATE_DEFAULT = None  # use None if --ssl-certificate is not given
MXC_ID_PLACEHOLDER = "__mxc_id__"
HOMESERVER_PLACEHOLDER = "__homeserver__"  # like https://matrix.example.org
HOSTNAME_PLACEHOLDER = "__hostname__"  # like matrix.example.org
ACCESS_TOKEN_PLACEHOLDER = "__access_token__"
USER_ID_PLACEHOLDER = "__user_id__"  # like @ mc: matrix.example.com
DEVICE_ID_PLACEHOLDER = "__device_id__"
ROOM_ID_PLACEHOLDER = "__room_id__"
SYNC_FULL = "full"  # sync with full_state=True for send actions
# SYNC_PARTIAL = "full" # sync with full_state=False for send actions
SYNC_OFF = "off"  # no sync is done for send actions
SYNC_DEFAULT = SYNC_FULL
# text, intended for human consumption
OUTPUT_TEXT = "text"
# json, as close to as what NIO API provides, a few convenient fields added
# transport_response removed
OUTPUT_JSON = "json"
# json-max, json format, like "json" but with transport_response object added
OUTPUT_JSON_MAX = "json-max"
# json-spec, json format, if and only if output adheres 100% to Matrix
# Specification will the data be printed. Currently, only --listen (--tail)
# adhere to Spec and hence print a JSON object. All other print nothing.
OUTPUT_JSON_SPEC = "json-spec"
OUTPUT_DEFAULT = OUTPUT_TEXT

# source, use media file name as provided by sender
MEDIA_NAME_SOURCE = "source"
# clean up source name. Use source name but with unusual chars replaced with _
MEDIA_NAME_CLEAN = "clean"
# ignore source provided name, use event-id as media file name
# Looks like this $rsad57dafs57asfag45gsFjdTXW1dsfroBiO2IsidKk'
MEDIA_NAME_EVENTID = "eventid"
# ignore source provided name, use current time at receiver as media file name
# Looks like this '20231012_152234_266600', date_time_microseconds
MEDIA_NAME_TIME = "time"
# defaults to "clean"
MEDIA_NAME_DEFAULT = MEDIA_NAME_CLEAN
# chars allowed in a clean name: alphanumerical and these
MEDIA_NAME_CLEAN_CHARS = "._- ~$"

# location of README.md file if it is not found on local harddisk
# used for --manual
README_FILE_RAW_URL = (
    "https://raw.githubusercontent.com/8go/matrix-commander/master/README.md"
)
INVITES_LIST = "list"
INVITES_JOIN = "join"
INVITES_LIST_JOIN = "list+join"
INVITES_UNUSED_DEFAULT = None  # use None if --room-invites is not specified
INVITES_USED_DEFAULT = (
    INVITES_LIST  # use 'list' by default with --room-invites
)

# increment this number and use new incremented number for next warning
# last unique Wxxx warning number used: W112:
# increment this number and use new incremented number for next error
# last unique Exxx error number used: E249:


class LooseVersion:
    """Version numbering and comparison.
    See https://github.com/effigies/looseversion/blob/main/looseversion.py.
    Argument 'other' must be of type LooseVersion.
    """

    component_re = re.compile(r"(\d+ | [a-z]+ | \.)", re.VERBOSE)

    def __init__(self, vstring=None):
        if vstring:
            self.parse(vstring)

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __ge__(self, other):
        return self._cmp(other) >= 0

    def parse(self, vstring):
        self.vstring = vstring
        components = [
            x for x in self.component_re.split(vstring) if x and x != "."
        ]
        for i, obj in enumerate(components):
            try:
                components[i] = int(obj)
            except ValueError:
                pass
        self.version = components

    def __str__(self):
        return self.vstring

    def __repr__(self):
        return "LooseVersion ('%s')" % str(self)

    def _cmp(self, other):
        if self.version == other.version:
            return 0
        if self.version < other.version:
            return -1
        if self.version > other.version:
            return 1


class MatrixCommanderError(Exception):
    pass


class MatrixCommanderWarning(Warning):
    pass


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
        self.client: Union[None, AsyncClient] = None
        self.credentials: Union[None, dict] = None
        self.send_action = False  # argv contains send action
        self.listen_action = False  # argv contains listen action
        self.room_action = False  # argv contains room action
        self.set_action = False  # argv contains set action
        self.get_action = False  # argv contains get action
        self.setget_action = False  # argv contains set or get action
        self.err_count = 0  # how many errors have occurred so far
        self.warn_count = 0  # how many warnings have occurred so far


# Convert None to "", useful when reporting values to stdout
# Should only be called with a) None or b) a string.
# We want to avoid situation where we would print: name = None
def zn(str):
    return str or ""


def get_qualifiedclassname(obj):
    klass = obj.__class__
    module = klass.__module__
    if module == "builtins":
        return klass.__qualname__  # avoid outputs like 'builtins.str'
    return module + "." + klass.__qualname__


def privacy_filter(dirty: str) -> str:
    """Remove private info from string"""
    # homeserver = urlparse(gs.credentials["homeserver"])
    # server_name = homeserver.netloc
    # clean = dirty.replace(server_name, "your.homeserver.org")
    return dirty.replace(gs.credentials["access_token"], "***")


def print_output(
    option: Literal["text", "json", "json-max", "json-spec"],
    *,
    text: str,
    json_: dict = None,
    json_max: dict = None,
    json_spec: dict = None,
) -> None:
    """Print output according to which option is specified with --output"""
    # json_ has the underscore to avoid a name clash with the module json
    results = {
        OUTPUT_TEXT: text,
        OUTPUT_JSON: json_,
        OUTPUT_JSON_MAX: json_max,
        OUTPUT_JSON_SPEC: json_spec,
    }
    if results[option] is None:
        if option == OUTPUT_JSON_SPEC:
            gs.log.debug(
                "Are you sure you wanted to use --output json-spec? "
                "Most outputs will be empty."
            )
        return
    if option == OUTPUT_TEXT:
        print(results[option], flush=True)
    elif option == OUTPUT_JSON_SPEC:
        print(json.dumps(results[option]), flush=True)
    else:  # OUTPUT_JSON or OUTPUT_JSON_MAX
        print(json.dumps(results[option], default=obj_to_dict), flush=True)


def obj_to_dict(obj):
    """Return dict of object

    Useful for json.dump() dict-to-json conversion.
    """
    if gs.pa.verbose > 1:  # 2+
        gs.log.debug(f"obj_to_dict: {obj.__class__}")
        gs.log.debug(f"obj_to_dict: {obj.__class__.__name__}")
        gs.log.debug(f"obj_to_dict: {get_qualifiedclassname(obj)}")
    # summary: shortcut: just these 2: RequestInfo and ClientResponse
    # if get_qualifiedclassname(obj) == "aiohttp.client_reqrep.RequestInfo":
    #     return {obj.__class__.__name__: str(obj)}
    # if get_qualifiedclassname(obj) == "aiohttp.client_reqrep.ClientResponse":
    #    return {obj.__class__.__name__: str(obj)}
    # details, one by one:
    # if get_qualifiedclassname(obj) == "collections.deque":
    #     return {obj.__class__.__name__: str(obj)}
    # if get_qualifiedclassname(obj) == "aiohttp.helpers.TimerContext":
    #     return {obj.__class__.__name__: str(obj)}
    # if get_qualifiedclassname(obj) == "asyncio.events.TimerHandle":
    #     return {obj.__class__.__name__: str(obj)}
    # if get_qualifiedclassname(obj) =="multidict._multidict.CIMultiDictProxy":
    #     return {obj.__class__.__name__: str(obj)}
    # if get_qualifiedclassname(obj) == "aiosignal.Signal":
    #     return {obj.__class__.__name__: str(obj)}
    # this one is crucial, it make the serialization circular reference.
    if get_qualifiedclassname(obj) == "aiohttp.streams.StreamReader":
        return {obj.__class__.__name__: str(obj)}
    # these four are crucial, they make the serialization circular reference.
    if (
        get_qualifiedclassname(obj)
        == "asyncio.unix_events._UnixSelectorEventLoop"
    ):
        return {obj.__class__.__name__: str(obj)}
    if get_qualifiedclassname(obj) == "aiohttp.tracing.Trace":
        return {obj.__class__.__name__: str(obj)}
    if get_qualifiedclassname(obj) == "aiohttp.tracing.TraceConfig":
        return {obj.__class__.__name__: str(obj)}
    # avoid "keys must be str, int, float, bool or None" errors
    if get_qualifiedclassname(obj) == "aiohttp.connector.TCPConnector":
        return {obj.__class__.__name__: str(obj)}

    if hasattr(obj, "__dict__"):
        if (
            "inbound_group_store" in obj.__dict__
            and "session_store" in obj.__dict__
            and "outbound_group_sessions" in obj.__dict__
        ):
            # "olm" is hige, 1MB+, 20K lines of JSON
            # grab only some items
            # "olm": {
            #   "user_id": "@xxx:xxx.xxx.xxx",
            #   "device_id": "xxx",
            #   "uploaded_key_count": 50,
            #   "users_for_key_query": {
            #     "set": "..."
            #   },
            #   "device_store": {
            #       ... want
            #   },
            #   "session_store": {
            #       ... dont want, too long
            #   },
            #   "inbound_group_store": {
            #       ... dont want, 20K lines, too long
            #   },
            #   "outbound_group_sessions": {},
            #   "tracked_users": {
            #     "set": "set()"
            #   },
            dictcopy = {}
            for key in [
                "user_id",
                "device_id",
                "uploaded_key_count",
                "users_for_key_query",
                "device_store",
                "outbound_group_sessions",
                "tracked_users",
                "outgoing_key_requests",
                "received_key_requests",
                "key_requests_waiting_for_session",
                "key_request_devices_no_session",
                "key_request_from_untrusted",
                "wedged_devices",
                "key_re_requests_events",
                "key_verifications",
                "outgoing_to_device_messages",
                "message_index_store",
                "store",
            ]:
                dictcopy.update({key: obj.__dict__[key]})
            if gs.pa.verbose > 1:  # 2+
                gs.log.debug(
                    f"{obj} is not serializable, simplifying to {dictcopy}."
                )
            return dictcopy
        if gs.pa.verbose > 1:  # 2+
            gs.log.debug(
                f"{obj} is not serializable, using its available dictionary "
                f"{obj.__dict__}."
            )
        return obj.__dict__
    else:
        # gs.log.debug(
        #     f"Object {obj} ({type(obj)}) has no class dictionary. "
        #     "Cannot be converted to JSON object. "
        #     "Will be converted to JSON string."
        # )
        # simple types like yarl.URL do not have a __dict__
        # get the class name as string, create a dict with classname and value
        if gs.pa.verbose > 1:  # 2+
            gs.log.debug(
                f"{obj} is not serializable, simplifying to key value pair "
                f"key '{obj.__class__.__name__}' and value '{str(obj)}'."
            )
        return {obj.__class__.__name__: str(obj)}


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


def derive_media_filename_with_path(event):
    """Derive file name under which to store a given media file.

    Depending on --download-media-name derive the corresponding file
    name under which to store the downloaded media file. Note that
    the file name giveb be the source, i.e. the sender, cannot be trusted.
    The source can specify and provide any string, even invalid file
    names or names containing backslash or slash and similar.

    Adds path as given in --download-media to file name.

    As last step function adds a sequential number, iff necessary, to assure
    that the file does not yet exist and that no file is overwritten
    (if multiple media files have the same name).
    """
    method = gs.pa.download_media_name
    if method == MEDIA_NAME_SOURCE:
        newfn = event.body
    elif method == MEDIA_NAME_EVENTID:
        newfn = event.event_id
    elif method == MEDIA_NAME_TIME:
        # e.g. '20231012_152234_266600' (YYYYMMDD_HHMMSS_MICROSECONDS)
        newfn = "{date:%Y%m%d_%H%M%S_%f}".format(date=datetime.datetime.now())
    else:
        # event.body is not trustworthy
        # and can contain garbage characters
        # such as / or \ which will cause file open
        # to fail. Replace those.
        newfn = "".join(
            [
                x if (x.isalnum() or x in MEDIA_NAME_CLEAN_CHARS) else "_"
                for x in event.body
            ]
        )
    gs.log.debug(f"Media file name method is: {method}")
    gs.log.debug(f"New file name for media is: {newfn}")
    filename_with_path = choose_available_filename(
        os.path.join(gs.pa.download_media, newfn)
    )
    gs.log.debug(
        f"Unique file name for media with path is: {filename_with_path}"
    )
    return filename_with_path


async def synchronize(client: AsyncClient) -> SyncResponse:
    """Synchronize with server, e.g. in order to get rooms.

    Arguments:
    ---------
    client : Client

    Returns: None

    Raises exception on error.
    """
    try:
        resp = await client.sync(timeout=10000, full_state=True)
    except ClientConnectorError as e:
        err = (
            "E100: "
            "sync() failed. Do you have connectivity to internet? "
            f"ClientConnectorError {e}"
        )
        raise MatrixCommanderError(err) from e
    except Exception as e:
        err = "E101: " f"sync() failed. Exception {e}"
        raise MatrixCommanderError(err) from e
    if isinstance(resp, SyncError):
        err = "E102: " f"sync failed with resp = {privacy_filter(str(resp))}"
        raise MatrixCommanderError(err) from None
    return resp


async def download_mxc(
    client: AsyncClient, mxc: str, filename: Optional[str] = None
):
    """Download MXC resource.

    Arguments:
    ---------
    client : Client
    mxc : str
        string representing URL like mxc://matrix.org/someRandomKey
    filename : str
        optional name of file for storing download
    """
    nio_version = pkg_resources.get_distribution("matrix-nio").version
    # version incompatibility between matrix-nio 0.19.0 and 0.20+
    # https://matrix.example.com/Abc123
    # server_name = "matrix.example.com"
    # media_id = "Abc123"
    # matrix-nio v0.19.0 has: download(server_name: str, media_id: str, ..)
    # convert mxc to server_name and media_id
    # v0.20+ : resp = await client.download(mxc=mxc, filename=filename)
    # v0.19- : resp = await client.download(
    #                     server_name=server_name, media_id=media_id,
    #                     filename=filename)
    gs.log.debug(f"download_mxc input mxc is {mxc}.")
    if nio_version.startswith("0.1"):  # like 0.19
        gs.log.info(
            f"You are running matrix-nio version {nio_version}. "
            "You should be running version 0.20+. Update if necessary. "
        )
        url = urlparse(mxc)
        gs.log.debug(f"download_mxc input url is {url}.")
        response = await client.download(
            server_name=url.netloc,
            media_id=url.path.strip("/"),
            filename=filename,
        )
    else:
        gs.log.debug(
            f"You are running matrix-nio version {nio_version}. Great!"
        )
        response = await client.download(mxc=mxc, filename=filename)
    gs.log.debug(f"download_mxc response is {response}.")
    return response


class Callbacks(object):
    """Class to pass client to callback methods."""

    def __init__(self, client):
        """Store AsyncClient."""
        self.client = client

    async def invite_callback(self, room, event):
        """Handle an incoming invite event.

        If an invite is received, then list or join the room specified
        in the invite.
        """
        try:
            gs.log.debug(
                f"message_callback(): for room {room} received this "
                f"event: type: {type(event)}, "
                f"event: {event}"
            )
            # There are MULTIPLE events received!
            # event 1:
            # InviteMemberEvent(source={'type': 'm.room.member',
            #   'state_key': '@jane:matrix.example.com',
            #   'sender': '@jane:matrix.example.com'},
            # sender='@jane:matrix.example.com',
            # state_key='@jane:matrix.example.com',
            # membership='join',
            # prev_membership=None,
            # content={'membership': 'join', 'displayname': 'M',
            #   'avatar_url': '...'}, prev_content=None)
            # event 2:
            # InviteMemberEvent(source={'type': 'm.room.member',
            #   'sender': '@jane:matrix.example.com',
            #   'state_key': '@john:matrix.example.com',
            #   'origin_server_ts': 1681986390778,
            #   'unsigned': {'replaces_state': '$xxx',
            #       'prev_content': {'membership': 'leave'},
            #       'prev_sender': '@john:matrix.example.com', 'age': 13037},
            #   'event_id': 'xxx'},
            # sender='@jane:matrix.example.com',
            # state_key='@john:matrix.example.com',
            # membership='invite',
            # prev_membership='leave',
            # content={'membership': 'invite', 'displayname': 'bot',
            #   'avatar_url': 'xxx'}, prev_content={'membership': 'leave'})

            gs.log.debug(
                f"Got invite event for room {room.room_id} from "
                f"{event.sender}. "
                f"Event shows membership as '{event.membership}'."
            )

            if event.membership == "invite":
                gs.log.debug(
                    "Event will be processed because it shows "
                    f"membership as '{event.membership}'."
                )
                # list
                if (
                    gs.pa.room_invites == INVITES_LIST
                    or gs.pa.room_invites == INVITES_LIST_JOIN
                ):
                    # output format controlled via --output flag
                    text = (
                        f"{room.room_id}{SEP}m.room.member"
                        f"{SEP}{event.membership}"
                    )
                    # we use the dictionary.
                    json_max = {"room_id": room.room_id}
                    json_max.update({"event": "m.room.member"})
                    json_max.update({"membership": event.membership})
                    json_ = json_max.copy()
                    json_spec = None
                    print_output(
                        gs.pa.output,
                        text=text,
                        json_=json_,
                        json_max=json_max,
                        json_spec=json_spec,
                    )

                # join
                if (
                    gs.pa.room_invites == INVITES_JOIN
                    or gs.pa.room_invites == INVITES_LIST_JOIN
                ):
                    result = await self.client.join(room.room_id)
                    if type(result) == JoinError:
                        gs.log.error(
                            f"E249: Error joining room {room.room_id}: "
                            f"{result.message}",
                        )
                        gs.err_count += 1
                    else:
                        # Successfully joined room
                        gs.log.info(
                            f"Joined room {room.room_id} successfully."
                        )
            else:
                gs.log.debug(
                    "Event will be skipped because it shows "
                    f"membership as '{event.membership}'."
                )

        except BaseException:
            gs.log.debug("Here is the traceback.\n" + traceback.format_exc())

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
                mxc = event.url  # media mxc
                url = await self.client.mxc_to_http(mxc)  # media url
                gs.log.debug(f"HTTP URL of media is : {url}")
                msg_url = " [" + url + "]"
                if gs.pa.download_media != "":
                    # download unencrypted/plain media file
                    resp = await download_mxc(self.client, mxc)
                    if isinstance(resp, DownloadError):
                        gs.log.error(
                            "E105: "
                            f"download of URI '{mxc}' to local file "
                            f"failed with response {privacy_filter(str(resp))}"
                        )
                        gs.err_count += 1
                        msg_url += " [Download of media file failed]"
                    else:
                        media_data = resp.body
                        filename = derive_media_filename_with_path(event)
                        async with aiofiles.open(filename, "wb") as f:
                            await f.write(media_data)
                            # Set atime and mtime of file to event timestamp
                            os.utime(
                                filename,
                                ns=((event.server_timestamp * 1000000,) * 2),
                            )
                        msg_url += f" [Downloaded media file to {filename}]"

            if isinstance(event, RoomEncryptedMedia):  # for all e2e media
                mxc = event.url  # media mxc
                url = await self.client.mxc_to_http(mxc)  # media url
                gs.log.debug(f"HTTP URL of media is : {url}")
                msg_url = " [" + url + "]"
                if gs.pa.download_media != "":
                    # download encrypted media file
                    resp = await download_mxc(self.client, mxc)
                    if isinstance(resp, DownloadError):
                        gs.log.error(
                            "E106: "
                            f"download of URI '{mxc}' to local file "
                            f"failed with response {privacy_filter(str(resp))}"
                        )
                        gs.err_count += 1
                        msg_url += " [Download of media file failed]"
                    else:
                        media_data = resp.body
                        filename = derive_media_filename_with_path(event)
                        async with aiofiles.open(filename, "wb") as f:
                            await f.write(
                                crypto.attachments.decrypt_attachment(
                                    media_data,
                                    event.source["content"]["file"]["key"][
                                        "k"
                                    ],
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
                            " [Downloaded and decrypted media "
                            f"file to {filename}]"
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
                sender_nick = user_id_to_short_user_name(event.sender)
            room_nick = room.display_name
            if room_nick in (None, "", "Empty Room"):
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
            # output format controlled via --output flag
            text = complete_msg  # print the received message
            json_ = {"source": event.source}
            json_.update({"room": room})
            json_.update({"room_display_name": room.display_name})
            json_.update({"sender_nick": sender_nick})
            json_.update({"event_datetime": event_datetime})
            json_max = event.__dict__
            json_max.update({"room": room})
            json_max.update({"room_display_name": room.display_name})
            json_max.update({"sender_nick": sender_nick})
            json_max.update({"event_datetime": event_datetime})
            json_spec = event.source
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )

            if gs.pa.os_notify:
                avatar_url = await get_avatar_url(self.client, event.sender)
                notify(
                    f"From {room.user_name(event.sender)}",
                    msg[:160],
                    avatar_url,
                )

        except BaseException:
            gs.log.debug("Here is the traceback.\n" + traceback.format_exc())

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
                    gs.log.error(
                        "E107: "
                        "Other device does not support emoji verification. "
                        f"{event.short_authentication_string}."
                    )
                    return
                resp = await client.accept_key_verification(
                    event.transaction_id
                )
                if isinstance(resp, ToDeviceError):
                    gs.log.error(
                        "E108: "
                        "accept_key_verification failed with error "
                        f"'{privacy_filter(str(resp))}'."
                    )

                sas = client.key_verifications[event.transaction_id]

                todevice_msg = sas.share_key()
                resp = await client.to_device(todevice_msg)
                if isinstance(resp, ToDeviceError):
                    gs.log.error(
                        "E109: "
                        "to_device failed with error "
                        f"'{privacy_filter(str(resp))}'."
                    )

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
                gs.log.error(
                    "E110: "
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

                print(
                    f"{sas.get_emoji()}",
                    file=sys.stdout,
                    flush=True,
                )

                yn = input("Do the emojis match? (Y/N) (C for Cancel) ")
                if yn.lower() == "y":
                    print(
                        "Match! The verification for this "
                        "device will be accepted.",
                        file=sys.stdout,
                        flush=True,
                    )
                    resp = await client.confirm_short_auth_string(
                        event.transaction_id
                    )
                    if isinstance(resp, ToDeviceError):
                        gs.log.error(
                            "E111: "
                            "confirm_short_auth_string failed with "
                            f"error '{privacy_filter(str(resp))}'."
                        )
                elif yn.lower() == "n":  # no, don't match, reject
                    print(
                        "No match! Device will NOT be verified. "
                        "Verification will be rejected.",
                        file=sys.stderr,
                        flush=True,
                    )
                    resp = await client.cancel_key_verification(
                        event.transaction_id, reject=True
                    )
                    if isinstance(resp, ToDeviceError):
                        gs.log.error(
                            "E112: "
                            "cancel_key_verification failed with "
                            f"'{privacy_filter(str(resp))}'."
                        )
                else:  # C or anything for cancel
                    print(
                        "Cancelled by user! Verification will be cancelled.",
                        file=sys.stderr,
                        flush=True,
                    )
                    resp = await client.cancel_key_verification(
                        event.transaction_id, reject=False
                    )
                    if isinstance(resp, ToDeviceError):
                        gs.log.error(
                            "E113: "
                            "cancel_key_verification failed with "
                            f"'{privacy_filter(str(resp))}'."
                        )

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
                    gs.log.error(
                        "E114: "
                        f"Cancelled or protocol error: Reason: {e}.\n"
                        f"Verification with {event.sender} not concluded. "
                        "Try again?"
                    )
                else:
                    resp = await client.to_device(todevice_msg)
                    if isinstance(resp, ToDeviceError):
                        gs.log.error(
                            "E115: "
                            "to_device failed with error "
                            f"'{privacy_filter(str(resp))}'."
                        )
                    gs.log.info(
                        f"sas.we_started_it = {sas.we_started_it}\n"
                        f"sas.sas_accepted = {sas.sas_accepted}\n"
                        f"sas.canceled = {sas.canceled}\n"
                        f"sas.timed_out = {sas.timed_out}\n"
                        f"sas.verified = {sas.verified}\n"
                        f"sas.verified_devices = {sas.verified_devices}\n"
                    )
                    print(
                        "Emoji verification was successful!\n"
                        "Verify with other devices or hit Control-C to "
                        "continue.",
                        file=sys.stdout,
                        flush=True,
                    )
            else:
                gs.log.error(
                    "E116: "
                    f"Received unexpected event type {type(event)}. "
                    f"Event is {event}. Event will be ignored."
                )
        except BaseException:
            gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


def notify(title: str, content: str, image_url: str):
    """Notify OS of message receipt.

    If the system is running headless or any problem happens with
    operating system notifications, ignore it.
    """
    if not HAVE_NOTIFY:
        gs.log.warning(
            "W100: "
            "notify2 or dbus is not installed. Notifications will not be "
            "displayed. "
            "Make sure that notify2 and dbus are installed or remove the "
            "--os-notify option."
        )
        gs.warn_count += 1
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
    except Exception as e:
        gs.log.debug(
            f"Showing notification for {title} failed. Exception: {e}"
            f"\nHere is the traceback:\n{traceback.format_exc()}"
        )
        pass


async def get_avatar_url(client: AsyncClient, user_id: str) -> str:
    """Get https avatar URL for user user_id.

    Returns URL or None if user has no avatar
    """
    avatar_url = None  # default
    resp = await client.get_avatar(user_id)
    if isinstance(resp, ProfileGetAvatarResponse):
        gs.log.debug(
            "ProfileGetAvatarResponse. Response is: "
            f"{privacy_filter(str(resp))}"
        )
        avatar_mxc = resp.avatar_url
        gs.log.debug(f"avatar_mxc is {avatar_mxc}")
        if avatar_mxc:  # could be None if no avatar
            avatar_url = await client.mxc_to_http(avatar_mxc)
    else:
        gs.log.info(
            f"Failed getting avatar from server. {privacy_filter(str(resp))}"
        )
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


def credentials_exist(credentials_file_path: Optional[str] = None) -> bool:
    """Determine if credentials file already exists."""
    if not credentials_file_path:
        credentials_file_path = determine_credentials_file()
    return os.path.exists(credentials_file_path)


def store_exists(store_dir_path: Optional[str] = None) -> bool:
    """Determine if store dir already exists."""
    if not store_dir_path:
        store_dir_path = determine_store_dir()
    return os.path.isdir(store_dir_path)


def store_create(store_dir_path: Optional[str] = None) -> None:
    """Create store dir."""
    if not store_dir_path:
        store_dir_path = determine_store_dir()
    os.makedirs(store_dir_path)
    gs.log.info(
        f"The persistent storage directory {store_dir_path} "
        "was created for you."
    )


def store_delete(store_dir_path: Optional[str] = None) -> None:
    """Delete store dir."""
    if not store_dir_path:
        store_dir_path = determine_store_dir()
    os.rmdir(store_dir_path)
    gs.log.info(
        f"The persistent storage directory {store_dir_path} "
        "was deleted for you."
    )


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
    gs.log.debug("Starting to read credentials file.")
    with open(credentials_file, "r") as f:
        cdict = json.load(f)
    gs.log.debug("Finished reading credentials file.")
    return cdict


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
    if gs.pa.store != STORE_DIR_DEFAULT and gs.pa.store != os.path.basename(
        gs.pa.store
    ):
        gs.log.debug(
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

    gs.log.debug(
        "Store directory was not found anywhere. Hence, we will suggest "
        f'"{pargs_store_norm}" (local directory) as store directory.'
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
    gs.log.debug(f"Trying to get members for all rooms of sender: {sender}")
    resp = await client.joined_rooms()
    if isinstance(resp, JoinedRoomsError):
        gs.log.error(
            "E117: "
            f"joined_rooms failed with {privacy_filter(str(resp))}. "
            "Not able to "
            "get all rooms. "
            f"Not able to find DM rooms for sender {sender}. "
            f"Not able to send to receivers {users}."
        )
        gs.err_count += 1
        senderrooms = []
    else:
        gs.log.debug(
            f"joined_rooms successful with {privacy_filter(str(resp))}"
        )
        senderrooms = resp.rooms
    room_found_for_users = []
    for room in senderrooms:
        resp = await client.joined_members(room)
        if isinstance(resp, JoinedMembersError):
            gs.log.error(
                "E118: "
                f"joined_members failed with {privacy_filter(str(resp))}. "
                "Not able to "
                f"get room members for room {room}. "
                f"Not able to find DM rooms for sender {sender}. "
                f"Not able to send to some of these receivers {users}."
            )
            gs.err_count += 1
        else:
            # resp.room_id
            # resp.members = List[RoomMember] ; RoomMember
            # member.user_id
            # member.display_name
            # member.avatar_url
            gs.log.debug(
                f"joined_members successful with {privacy_filter(str(resp))}"
            )
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
                    gs.log.error(
                        "E119: "
                        f"Sender does not match {privacy_filter(str(resp))}"
                    )
                    gs.err_count += 1
                for user in users:
                    if (
                        rcvr
                        and user == rcvr.user_id
                        or short_user_name_to_user_id(user, credentials)
                        == rcvr.user_id
                        or user == rcvr.display_name
                    ):
                        room_found_for_users.append(user)
                        rooms.append(resp.room_id)
    for user in users:
        if user not in room_found_for_users:
            gs.log.error(
                "E120: "
                "Room(s) were specified for a DM (direct messaging) "
                "send operation via --room. But no DM room was "
                f"found for user '{user}'. "
                "Try setting up a room first via --room-create and "
                "--room-invite option or --room-dm-create."
            )
            gs.err_count += 1
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


async def map_roominfo_to_roomid(client: AsyncClient, info: str) -> str:
    """Attempt to convert room info to room_id.

    Arguments:
    ---------
    client : nio client
    info : str
        can be a canonical alias in the form of '#someRoomAlias:example.com'
        can be a canonical room_id in the form of '!someRoomId:example.com'
        can be a short alias in the form of 'someRoomAlias'
        can be a short alias in the form of '#someRoomAlias'
        can be a short room id in the form of '!someRoomId'

    Return corresponding full room_id (!id:sample.com) or or raises exception.

    """
    ri = info.strip()
    ri = ri.replace(r"\!", "!")  # remove possible escape
    if (
        ri in (None, "", "!", "#")
        or ri.startswith(":")
        or ri.count(":") > 1
        or ri.startswith("@")
        or "#" in ri[1:]
        or any(elem in ri for elem in "[]{} ")  # does it contain bad chars?
        or (
            not ri.startswith("!") and not ri.startswith("#") and ":" in ri
        )  # alias:sample.com
    ):
        err = (
            "E121: "
            f"Invalid room specification. '{info}' ({ri}) is neither "
            "a valid room id nor a valid room alias."
        )
        raise MatrixCommanderError(err) from None
    if not ri.startswith("!"):
        # 'someRoomAlias' or '#someRoomAlias' or '#someRoomAlias:sample.com'
        if ":" not in ri:  # 'someRoomAlias' or '#someRoomAlias'
            ri = short_room_alias_to_room_alias(ri, gs.credentials)
        ri = await map_roomalias_to_roomid(client, ri)
        return ri
    if ":" not in ri:
        # '!someRoomId'
        ri = ri + ":" + default_homeserver(gs.credentials)
    return ri


async def map_roomalias_to_roomid(client, alias) -> str:
    """Attempt to convert room alias to room_id.

    Arguments:
    ---------
    client : nio client
    alias : can be an alias in the form of '#someRoomAlias:example.com'
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
                "E122: "
                f"room_resolve_alias for alias {alias} failed with "
                f"{privacy_filter(str(resp))}. "
                f"Trying operation with input {alias} anyway. Might fail."
            )
            gs.err_count += 1
        else:
            ret = resp.room_id
            gs.log.debug(
                f'Mapped room alias "{alias}" to room id "{ret}". '
                f"({resp.room_alias}, {resp.room_id})."
            )
    return ret


def default_homeserver(credentials: dict):
    """Get the default homeserver (domain) from the credentials file.
    Use the user_id, not the room_id. The room_id could be on a
    different server owned by someone else. user_id makes more sense.
    """
    user = credentials["user_id"]  # who am i
    homeserver = user.partition(":")[2]
    return homeserver  # matrix.example.com


def short_room_alias_to_room_alias(short_room_alias: str, credentials: dict):
    """Convert 'SomeRoomAlias' to ''#SomeToomAlias:matrix.example.com'.
    Converts short canonical local room alias to full room alias.
    """
    if short_room_alias in (None, ""):
        err = "E124: " "Invalid room alias. Alias is none or empty."
        raise MatrixCommanderError(err) from None
    if short_room_alias[0] == "#":
        ret = short_room_alias + ":" + default_homeserver(credentials)
    else:
        ret = "#" + short_room_alias + ":" + default_homeserver(credentials)
    return ret


def room_alias_to_short_room_alias(room_alias: str, credentials: dict):
    """Convert '#SomeToomAlias:matrix.example.com' to 'SomeRoomAlias'.
    Converts full room alias to short canonical local room alias.
    """
    return room_alias.split(":")[0][1:]


def user_id_to_short_user_name(user_id: str):
    """Convert '@someuser:matrix.example.com' to 'someuser'.
    Convert full user_id to user nick name.
    """
    return user_id.split(":")[0][1:]


def short_user_name_to_user_id(short_user: str, credentials: dict):
    """Convert 'someuser' to '@someuser:matrix.example.com'.
    Convert user nick name to full user_id.
    """
    return "@" + short_user + ":" + default_homeserver(credentials)


def is_room_alias(room_id: str) -> bool:
    """Determine if room identifier is a room alias.

    Room aliases are of syntax: #somealias:someserver
    This is not an exhaustive check!

    """
    if (
        room_id
        and len(room_id) > 3
        and (room_id[0] == "#")
        and ("#" not in room_id[1:])
        and (":" in room_id)
        and room_id.count(":") == 1
        and (" " not in room_id)
        and not any(elem in room_id for elem in "[]{} ")  # contains bad chars?
    ):
        return True
    else:
        return False


def is_room_id(room_id: str) -> bool:
    """Determine if room identifier is a valid room id.

    Room ids are of syntax: !somealias:someserver
    This is not an exhaustive check!

    """
    if (
        room_id
        and len(room_id) > 3
        and (room_id[0] == "!")
        and ("#" not in room_id)
        and (":" in room_id)
        and room_id.count(":") == 1
        and (" " not in room_id)
    ):
        return True
    else:
        return False


def is_room(room_id: str) -> bool:
    """Determine if room id is a valid room id or a valid room alias.

    This is not an exhaustive check!

    """
    return is_room_id(room_id) or is_room_alias(room_id)


def is_short_room_alias(room_id: str) -> bool:
    """Determine if room identifier is a local part of canonical room alias.

    Local parts of canonical room aliases are of syntax: somealias

    Now also allowing #somealias

    """
    if (
        room_id
        and len(room_id) > 0
        and room_id != "#"
        and (":" not in room_id)
        and ("#" not in room_id[1:])
        and (not room_id.startswith("!"))
        and (not room_id.startswith("@"))
        and (" " not in room_id)
    ):
        return True
    else:
        return False


def is_user_id(user_id: str) -> bool:
    """Determine if user identifier is a valid user id.

    User ids are of syntax: @someuser:someserver
    This is not an exhaustive check!

    """
    if (
        user_id
        and len(user_id) > 3
        and (user_id[0] == "@")
        and (":" in user_id)
        and (" " not in user_id)
    ):
        return True
    else:
        return False


def is_short_user_id(user_id: str) -> bool:
    """Determine if user identifier is a valid short user id.

    Short user ids are of syntax: someuser
    This is not an exhaustive check!

    """
    if (
        user_id
        and len(user_id) > 0
        and (":" not in user_id)
        and ("@" not in user_id)
        and (" " not in user_id)
    ):
        return True
    else:
        return False


def is_partial_user_id(user_id: str) -> bool:
    """Determine if user identifier is a valid abbreviated user id.

    Abbrev. user ids are of syntax: @someuser
    This is not an exhaustive check!

    """
    if (
        user_id
        and len(user_id) > 1
        and (user_id[0] == "@")
        and (":" not in user_id)
        and (" " not in user_id)
    ):
        return True
    else:
        return False


def is_user(user_id: str) -> bool:
    """Determine if user id is a valid user id or a valid short user id.

    This is not an exhaustive check!

    """
    return (
        is_user_id(user_id)
        or is_partial_user_id(user_id)
        or is_short_user_id(user_id)
    )


async def action_room_dm_create(client: AsyncClient, credentials: dict):
    """Create a direct message (DM) room while already being logged in.

    After creating the private DM room it invites the other user to it.

    Arguments:
    ---------
    client: AsyncClient: nio client, allows as to query the server
    credentials: dict: allows to get the user_id of sender, etc
    """
    # users : list of users to create DM rooms with
    # room_aliases : list of room aliases in the form of "sampleAlias"
    #         These aliases will then be used by the server and
    #         the server creates the definite alias in the form
    #         of "#sampleAlias:example.com" from it.
    #         We permit "#sampleAlias:example.com" and downscale it to
    #         "sampleAlias".
    # names : list of names for rooms
    # topic : room topics

    users = gs.pa.room_dm_create
    room_aliases = gs.pa.alias
    names = gs.pa.name
    topics = gs.pa.topic
    try:
        index = 0
        gs.log.debug(
            f'Trying to create DM rooms with users "{users}", '
            f'room aliases "{room_aliases}", '
            f'names "{names}", and topics "{topics}".'
        )
        for user in users:
            try:
                alias = room_aliases[index]
                alias = alias.replace(r"\!", "!")  # remove possible escape
                # alias is a true alias, not a room id
                # if by mistake user has given full room alias, shorten it
                if is_room_alias(alias):
                    alias = room_alias_to_short_room_alias(alias, credentials)
            except (IndexError, TypeError):
                alias = ""
            try:
                name = names[index]
            except (IndexError, TypeError):
                name = ""
            try:
                topic = topics[index]
            except (IndexError, TypeError):
                topic = ""
            alias = alias.strip()
            alias = None if alias == "" else alias
            name = name.strip()
            name = None if name == "" else name
            topic = topic.strip()
            topic = None if topic == "" else topic
            if gs.pa.plain:
                encrypt = False
                initial_state = ()
            else:
                encrypt = True
                initial_state = [EnableEncryptionBuilder().as_dict()]
            gs.log.debug(
                f'Creating DM room with user "{user}", '
                f'room alias "{alias}", '
                f'name "{name}", topic "{topic}" and '
                f'encrypted "{encrypt}".'
            )
            # nio's room_create does NOT accept "#foo:example.com"
            resp = await client.room_create(
                alias=alias,  # desired canonical alias local part, e.g. foo
                visibility=RoomVisibility.private,
                is_direct=True,
                preset=RoomPreset.private_chat,
                invite={user},  # invite the user to the DM
                name=name,  # room name
                topic=topic,  # room topic
                initial_state=initial_state,
            )
            # "alias1" will create a "#alias1:example.com"
            if isinstance(resp, RoomCreateError):
                gs.log.error(
                    "E125: "
                    "Room_create failed with response: "
                    f"{privacy_filter(str(resp))}"
                )
                gs.err_count += 1
            else:
                if alias:
                    full_alias = short_room_alias_to_room_alias(
                        alias, credentials
                    )
                else:
                    full_alias = None
                gs.log.info(
                    f'Created DM room with room id "{resp.room_id}", '
                    f'short alias "{zn(alias)}", '
                    f'full alias "{zn(full_alias)}" and '
                    f'encrypted "{encrypt}".'
                )
                # output format controlled via --output flag
                text = (
                    f"{resp.room_id}{SEP}{zn(alias)}{SEP}{zn(full_alias)}"
                    f"{SEP}{zn(name)}{SEP}{zn(topic)}{SEP}{encrypt}"
                )
                # Object of type RoomCreateResponse is not JSON
                # serializable, hence we use the dictionary.
                json_max = resp.__dict__
                # resp has only 1 useful useful member: room_id
                json_max.update({"alias": alias})  # add dict items
                json_max.update({"alias_full": full_alias})
                json_max.update({"name": name})
                json_max.update({"topic": topic})
                json_max.update({"encrypted": encrypt})
                json_ = json_max.copy()
                json_.pop("transport_response")
                json_spec = None
                print_output(
                    gs.pa.output,
                    text=text,
                    json_=json_,
                    json_max=json_max,
                    json_spec=json_spec,
                )
            index = index + 1
    except Exception:
        gs.log.error("E126: " "DM room creation failed. Sorry.")
        gs.err_count += 1
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def action_room_create(client: AsyncClient, credentials: dict):
    """Create one or multiple rooms while already being logged in.

    Arguments:
    ---------
    client: AsyncClient: nio client, allows as to query the server
    credentials: dict: allows to get the user_id of sender, etc
    """
    # room_aliases : list of room aliases in the form of "sampleAlias"
    #         These aliases will then be used by the server and
    #         the server creates the definite alias in the form
    #         of "#sampleAlias:example.com" from it.
    #         We permit "#sampleAlias:example.com" and downscale it to
    #         "sampleAlias".
    # names : list of names for rooms
    # topics : list of room topics

    room_aliases = gs.pa.room_create
    names = gs.pa.name
    topics = gs.pa.topic
    try:
        index = 0
        gs.log.debug(
            f'Trying to create rooms with room aliases "{room_aliases}", '
            f'names "{names}", and topics "{topics}".'
        )
        for alias in room_aliases:
            alias = alias.replace(r"\!", "!")  # remove possible escape
            # alias is a true alias, not a room id
            # if by mistake user has given full room alias, shorten it
            if is_room_alias(alias):
                alias = room_alias_to_short_room_alias(alias, credentials)
            try:
                name = names[index]
            except (IndexError, TypeError):
                name = ""
            try:
                topic = topics[index]
            except (IndexError, TypeError):
                topic = ""
            alias = alias.strip()
            alias = None if alias == "" else alias
            name = name.strip()
            name = None if name == "" else name
            topic = topic.strip()
            topic = None if topic == "" else topic
            if gs.pa.plain:
                encrypt = False
                initial_state = ()
            else:
                encrypt = True
                initial_state = [EnableEncryptionBuilder().as_dict()]
            gs.log.debug(
                f'Creating room with room alias "{alias}", '
                f'name "{name}", topic "{topic}" and '
                f'encrypted "{encrypt}".'
            )
            # nio's room_create does NOT accept "#foo:example.com"
            resp = await client.room_create(
                alias=alias,  # desired canonical alias local part, e.g. foo
                name=name,  # room name
                topic=topic,  # room topic
                initial_state=initial_state,
            )
            # "alias1" will create a "#alias1:example.com"
            if isinstance(resp, RoomCreateError):
                gs.log.error(
                    "E127: "
                    "Room_create failed with response: "
                    f"{privacy_filter(str(resp))}"
                )
                gs.err_count += 1
            else:
                if alias:
                    full_alias = short_room_alias_to_room_alias(
                        alias, credentials
                    )
                else:
                    full_alias = None
                gs.log.info(
                    f'Created room with room id "{resp.room_id}", '
                    f'short alias "{zn(alias)}", '
                    f'full alias "{zn(full_alias)}" and '
                    f'encrypted "{encrypt}".'
                )
                # output format controlled via --output flag
                text = (
                    f"{resp.room_id}{SEP}{zn(alias)}{SEP}{zn(full_alias)}"
                    f"{SEP}{zn(name)}{SEP}{zn(topic)}{SEP}{encrypt}"
                )
                # Object of type RoomCreateResponse is not JSON
                # serializable, hence we use the dictionary.
                json_max = resp.__dict__
                # resp has only 1 useful useful member: room_id
                json_max.update({"alias": alias})  # add dict items
                json_max.update({"alias_full": full_alias})
                json_max.update({"name": name})
                json_max.update({"topic": topic})
                json_max.update({"encrypted": encrypt})
                json_ = json_max.copy()
                json_.pop("transport_response")
                json_spec = None
                print_output(
                    gs.pa.output,
                    text=text,
                    json_=json_,
                    json_max=json_max,
                    json_spec=json_spec,
                )
            index = index + 1
    except Exception:
        gs.log.error("E128: " "Room creation failed. Sorry.")
        gs.err_count += 1
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def action_room_join(client, credentials):
    """Join one or multiple rooms."""
    rooms = gs.pa.room_join
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            gs.log.debug(f'Preparing to join room "{room_id}".')
            room_id = await map_roominfo_to_roomid(client, room_id)
            gs.log.debug(f'Joining room "{room_id}".')
            resp = await client.join(room_id)
            if isinstance(resp, JoinError):
                gs.log.error(
                    "E129: " f"join failed with {privacy_filter(str(resp))}"
                )
                gs.err_count += 1
            else:
                gs.log.info(f'Joined room "{room_id}" successfully.')
    except Exception:
        gs.log.error("E130: " "Joining rooms failed. Sorry.")
        gs.err_count += 1
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def action_room_leave(client, credentials):
    """Leave one or multiple rooms."""
    rooms = gs.pa.room_leave
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            gs.log.debug(f'Preparing to leave room "{room_id}".')
            room_id = await map_roominfo_to_roomid(client, room_id)
            gs.log.debug(f'Leaving room "{room_id}".')
            resp = await client.room_leave(room_id)
            if isinstance(resp, RoomLeaveError):
                gs.log.error(
                    "E131: " f"Leave failed with {privacy_filter(str(resp))}"
                )
                gs.err_count += 1
            else:
                gs.log.info(f'Left room "{room_id}".')
    except Exception:
        gs.log.error("E132: " "Room leave failed. Sorry.")
        gs.err_count += 1
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def action_room_forget(client, credentials):
    """Forget one or multiple rooms."""
    rooms = gs.pa.room_forget
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            gs.log.debug(f'Preparing to forget room "{room_id}".')
            room_id = await map_roominfo_to_roomid(client, room_id)
            gs.log.debug(f'Forgetting room "{room_id}".')
            resp = await client.room_forget(room_id)
            if isinstance(resp, RoomForgetError):
                gs.log.error(
                    "E133: " f"Forget failed with {privacy_filter(str(resp))}"
                )
                gs.err_count += 1
            else:
                gs.log.info(f'Forgot room "{room_id}".')
    except Exception:
        gs.log.error("E134: " "Room forget failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def action_room_invite(client, credentials):
    """Invite one or multiple users to one or multiple rooms."""
    rooms = gs.pa.room_invite
    users = gs.pa.user
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            gs.log.debug(f'Preparing to invite to room "{room_id}".')
            room_id = await map_roominfo_to_roomid(client, room_id)
            gs.log.debug(f'Inviting to room "{room_id}".')
            for user in users:
                gs.log.debug(
                    f'Inviting user "{user}" to room with '
                    f'room alias "{room_id}".'
                )
                resp = await client.room_invite(room_id, user)
                if isinstance(resp, RoomInviteError):
                    gs.log.error(
                        "E135: "
                        f"room_invite failed with {privacy_filter(str(resp))}"
                    )
                    gs.err_count += 1
                else:
                    gs.log.info(
                        f'User "{user}" was successfully invited '
                        f'to room "{room_id}".'
                    )
    except Exception:
        gs.log.error("E136: " "User invite failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def action_room_ban(client, credentials):
    """Ban one or multiple users from one or multiple rooms."""
    rooms = gs.pa.room_ban
    users = gs.pa.user
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            gs.log.debug(f'Preparing to ban in room "{room_id}".')
            room_id = await map_roominfo_to_roomid(client, room_id)
            gs.log.debug(f'Banning to room "{room_id}".')
            for user in users:
                gs.log.debug(
                    f'Banning user "{user}" from room with '
                    f'room alias "{room_id}".'
                )
                resp = await client.room_ban(room_id, user)
                if isinstance(resp, RoomBanError):
                    gs.log.error(
                        "E137: "
                        f"room_ban failed with {privacy_filter(str(resp))}"
                    )
                    gs.err_count += 1
                else:
                    gs.log.info(
                        f'User "{user}" was successfully banned '
                        f'from room "{room_id}".'
                    )
    except Exception:
        gs.log.error("E138: " "User ban failed. Sorry.")
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def action_room_unban(client, credentials):
    """Unban one or multiple users from one or multiple rooms."""
    rooms = gs.pa.room_unban
    users = gs.pa.user
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            gs.log.debug(f'Preparing to unban in room "{room_id}".')
            room_id = await map_roominfo_to_roomid(client, room_id)
            gs.log.debug(f'Unbanning to room "{room_id}".')
            for user in users:
                gs.log.debug(
                    f'Unbanning user "{user}" from room with '
                    f'room alias "{room_id}".'
                )
                resp = await client.room_unban(room_id, user)
                if isinstance(resp, RoomUnbanError):
                    gs.log.error(
                        "E139: "
                        f"room_unban failed with {privacy_filter(str(resp))}"
                    )
                    gs.err_count += 1
                else:
                    gs.log.info(
                        f'User "{user}" was successfully unbanned '
                        f'from room "{room_id}".'
                    )
    except Exception:
        gs.log.error("E140: " "User unban failed. Sorry.")
        gs.err_count += 1
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def action_room_kick(client, credentials):
    """Kick one or multiple users from one or multiple rooms."""
    rooms = gs.pa.room_kick
    users = gs.pa.user
    try:
        for room_id in rooms:
            # room_id can be #roomAlias or !roomId
            gs.log.debug(f'Preparing to kicking off room "{room_id}".')
            room_id = await map_roominfo_to_roomid(client, room_id)
            gs.log.debug(f'Kicking off room "{room_id}".')
            for user in users:
                gs.log.debug(
                    f'Kicking user "{user}" from room with '
                    f'room alias "{room_id}".'
                )
                resp = await client.room_kick(room_id, user)
                if isinstance(resp, RoomKickError):
                    gs.log.error(
                        "E141: "
                        f"room_kick failed with {privacy_filter(str(resp))}"
                    )
                    gs.err_count += 1
                else:
                    gs.log.info(
                        f'User "{user}" was successfully kicked '
                        f'from room "{room_id}".'
                    )
    except Exception:
        gs.log.error("E142: " "User kick failed. Sorry.")
        gs.err_count += 1
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
            "This file is being dropped and NOT sent."
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
            "Event is empty. This event is being dropped and NOT sent."
        )
        return

    try:
        content_json = json.loads(jsondata)
        message_type = content_json["type"]
        content = content_json["content"]
    except Exception:
        gs.log.error(
            "E143: "
            "Event is not a valid JSON object or not of Matrix JSON format. "
            "This event is being dropped and NOT sent."
        )
        gs.err_count += 1
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())
        return

    try:
        for room_id in rooms:
            room_id = await map_roominfo_to_roomid(client, room_id)
            resp = await client.room_send(
                room_id, message_type=message_type, content=content
            )
            if isinstance(resp, RoomSendError):
                gs.log.error(
                    "E144: "
                    "room_send failed with error "
                    f"'{privacy_filter(str(resp))}'."
                )
                # gs.err_count += 1 # not needed, will raise exception
                # in following line of code
            gs.log.info(
                f'This event was sent: "{event}" to room "{resp.room_id}" '
                f'as event "{resp.event_id}".'
            )
            if gs.pa.print_event_id:
                # output format controlled via --output flag
                text = f"{resp.event_id}{SEP}{resp.room_id}{SEP}{event}"
                # Object of type RoomCreateResponse is not JSON
                # serializable, hence we use the dictionary.
                json_max = resp.__dict__
                json_max.update({"event": event})  # add dict items
                json_ = json_max.copy()
                json_.pop("transport_response")
                json_spec = None
                print_output(
                    gs.pa.output,
                    text=text,
                    json_=json_,
                    json_max=json_max,
                    json_spec=json_spec,
                )
            gs.log.debug(
                f'This event was sent: "{event}" ({content}) '
                f'to room "{room_id}". '
                f"Response: event_id={resp.event_id}, room_id={resp.room_id}, "
                f"full response: {privacy_filter(str(resp))}. "
            )
    except Exception:
        gs.log.error("E145: " f"Event send of file {event} failed. Sorry.")
        gs.err_count += 1
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
            "This file is being dropped and NOT sent."
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
            "This file is being dropped and NOT sent."
        )
        return

    # # restrict to "txt", "pdf", "mp3", "ogg", "wav", ...
    # if not re.match("^.pdf$|^.txt$|^.doc$|^.xls$|^.mobi$|^.mp3$",
    #                os.path.splitext(file)[1].lower()):
    #    gs.log.debug(f"File {file} is not a permitted file type. Should be "
    #                 ".pdf, .txt, .doc, .xls, .mobi or .mp3 ... "
    #                 f"[{os.path.splitext(file)[1].lower()}]"
    #                 "This file is being dropped and NOT sent.")
    #    return

    # 'application/pdf' "plain/text" "audio/ogg"
    mime_type = magic.from_file(file, mime=True)
    # if ((not mime_type.startswith("application/")) and
    #        (not mime_type.startswith("plain/")) and
    #        (not mime_type.startswith("audio/"))):
    #    gs.log.debug(f"File {file} does not have an accepted mime type. "
    #                 "Should be something like application/pdf. "
    #                 f"Found mime type {mime_type}. "
    #                 "This file is being dropped and NOT sent.")
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
            "File was uploaded successfully to server. Response is: "
            f"{privacy_filter(str(resp))}"
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
            f"Failed to upload: {privacy_filter(str(resp))}"
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
            room_id = await map_roominfo_to_roomid(client, room_id)
            resp = await client.room_send(
                room_id, message_type="m.room.message", content=content
            )
            if isinstance(resp, RoomSendError):
                gs.log.error(
                    "E146: "
                    "room_send failed with error "
                    f"'{privacy_filter(str(resp))}'."
                )
                # gs.err_count += 1 # not needed, will raise exception
                # in following line of code
            gs.log.info(
                f'This file was sent: "{file}" to room "{resp.room_id}" '
                f'as event "{resp.event_id}".'
            )
            if gs.pa.print_event_id:
                # output format controlled via --output flag
                text = f"{resp.event_id}{SEP}{resp.room_id}{SEP}{file}"
                # Object of type RoomCreateResponse is not JSON
                # serializable, hence we use the dictionary.
                json_max = resp.__dict__
                json_max.update({"file": file})  # add dict items
                json_ = json_max.copy()
                json_.pop("transport_response")
                json_spec = None
                print_output(
                    gs.pa.output,
                    text=text,
                    json_=json_,
                    json_max=json_max,
                    json_spec=json_spec,
                )
            gs.log.debug(
                f'This file was sent: "{file}" to room "{room_id}". '
                f"Response: event_id={resp.event_id}, room_id={resp.room_id}, "
                f"full response: {privacy_filter(str(resp))}. "
            )
    except Exception:
        gs.log.error("E147: " f"File send of file {file} failed. Sorry.")
        gs.err_count += 1
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
            "W101: "
            "No rooms are given. This should not happen. "
            "Maybe your DM rooms specified via --user were not found. "
            "This image is being dropped and NOT sent."
        )
        gs.warn_count += 1
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
            "W102: "
            f"Image file {image} is not a file. Doesn't exist or "
            "is a directory. "
            "This image is being dropped and NOT sent."
        )
        gs.warn_count += 1
        return

    # "bmp", "gif", "jpg", "jpeg", "png", "pbm", "pgm", "ppm", "xbm", "xpm",
    # "tiff", "webp", "svg",

    # svg files are not shown in Element, hence send SVG files as files with -f
    if not isPipe and not re.match(
        "^.jpg$|^.jpeg$|^.gif$|^.png$|^.svg$",
        os.path.splitext(image)[1].lower(),
    ):
        gs.log.warning(
            "W103: "
            f"Image file {image} is not an image file. Should be "
            ".jpg, .jpeg, .gif, or .png. "
            f"Found [{os.path.splitext(image)[1].lower()}]. "
            "This image is being dropped and NOT sent."
        )
        gs.warn_count += 1
        return

    # 'application/pdf' "image/jpeg"
    # svg mime-type is "image/svg+xml"
    mime_type = magic.from_file(image, mime=True)
    gs.log.debug(f"Image file mime-type is {mime_type}")
    if not mime_type.startswith("image/"):
        gs.log.warning(
            "W104: "
            f"Image file {image} does not have an image mime type. "
            "Should be something like image/jpeg. "
            f"Found mime type {mime_type}. "
            "This image is being dropped and NOT sent."
        )
        gs.warn_count += 1
        return

    if mime_type.startswith("image/svg"):
        gs.log.warning(
            "W105: "
            "There is a bug in Element preventing previews of SVG images. "
            "Alternatively you may send SVG files as files via -f."
        )
        width = 100  # in pixel
        height = 100
        # Python blurhash package does not work on SVG
        # blurhash: some random colorful image
        blurhash = "ULH_C:0HGF}B.$k:PLVG8z}$4;o?~IQ:9$yB"
        blurhash = None  # shows turning circle forever in Element due to bug
    else:
        im = Image.open(image)  # this will fail for SVG files
        (width, height) = im.size  # im.size returns (width,height) tuple
        blurhash = None

    # first do an upload of image, see upload() documentation
    # http://matrix-nio.readthedocs.io/en/latest/nio.html#nio.AsyncClient.upload
    # then send URI of upload to room
    # Note that encrypted upload works even with unencrypted/plain rooms; the
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
            f"Response is: {privacy_filter(str(resp))}"
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
            f"Failed to upload: {privacy_filter(str(resp))}"
        )

    # TODO compute thumbnail, upload thumbnail to Server
    # TODO add thumbnail info to `content`

    content = {
        "body": os.path.basename(image),  # descriptive title
        "info": {
            "size": file_stat.st_size,
            "mimetype": mime_type,
            # "thumbnail_info": None,  # TODO
            "w": width,  # width in pixel
            "h": height,  # height in pixel
            # "thumbnail_url": None,  # TODO
            "xyz.amorgan.blurhash": blurhash
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
            room_id = await map_roominfo_to_roomid(client, room_id)
            resp = await client.room_send(
                room_id, message_type="m.room.message", content=content
            )
            if isinstance(resp, RoomSendError):
                gs.log.error(
                    "E148: "
                    "room_send failed with error "
                    f"'{privacy_filter(str(resp))}'."
                )
                # gs.err_count += 1 # not needed, will raise exception
                # in following line of code
            gs.log.info(
                f'This image file was sent: "{image}" '
                f'to room "{resp.room_id}" '
                f'as event "{resp.event_id}".'
            )
            if gs.pa.print_event_id:
                # output format controlled via --output flag
                text = f"{resp.event_id}{SEP}{resp.room_id}{SEP}{image}"
                # Object of type RoomCreateResponse is not JSON
                # serializable, hence we use the dictionary.
                json_max = resp.__dict__
                json_max.update({"image": image})  # add dict items
                json_ = json_max.copy()
                json_.pop("transport_response")
                json_spec = None
                print_output(
                    gs.pa.output,
                    text=text,
                    json_=json_,
                    json_max=json_max,
                    json_spec=json_spec,
                )
            gs.log.debug(
                f'This image file was sent: "{image}" '
                f'to room "{room_id}". '
                f"Response: event_id={resp.event_id}, room_id={resp.room_id}, "
                f"full response: {privacy_filter(str(resp))}. "
            )
    except Exception:
        gs.log.error("E149: " f"Image send of file {image} failed. Sorry.")
        gs.err_count += 1
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


# according to linter: function is too complex, C901
async def send_message(client, rooms, message):  # noqa: C901
    """Process message.

    Format message according to instructions from command line arguments.
    Then send the one message to all rooms.

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
            "This text message is being dropped and NOT sent."
        )
        return
    # remove leading AND trailing newlines to beautify
    message = message.strip("\n")

    if message.strip() == "":
        gs.log.debug(
            "The message is empty. "
            "This message is being dropped and NOT sent."
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
    elif gs.pa.emojize:
        gs.log.debug('Sending message in format "emojized".')
        formatted_message = emoji.emojize(
            message
        )  # convert emoji shortcodes if present
        content["format"] = "org.matrix.custom.html"  # add to dict
        content["formatted_body"] = formatted_message
    else:
        gs.log.debug('Sending message in format "text".')
    content["body"] = message

    try:
        for room_id in rooms:
            room_id = await map_roominfo_to_roomid(client, room_id)
            resp = await client.room_send(
                room_id,
                message_type="m.room.message",
                content=content,
                ignore_unverified_devices=True,
            )
            if isinstance(resp, RoomSendError):
                gs.log.error(
                    "E150: "
                    "room_send failed with error "
                    f"'{privacy_filter(str(resp))}'."
                )
                # gs.err_count += 1 # not needed, will raise exception
                # in following line of code
            gs.log.info(
                f'This message was sent: "{message}" to room "{resp.room_id}" '
                f'as event "{resp.event_id}".'
            )
            if gs.pa.print_event_id:
                # output format controlled via --output flag
                text = f"{resp.event_id}{SEP}{resp.room_id}{SEP}{message}"
                # Object of type RoomCreateResponse is not JSON
                # serializable, hence we use the dictionary.
                json_max = resp.__dict__
                json_max.update({"message": message})  # add dict items
                json_ = json_max.copy()
                json_.pop("transport_response")
                json_spec = None
                print_output(
                    gs.pa.output,
                    text=text,
                    json_=json_,
                    json_max=json_max,
                    json_spec=json_spec,
                )
            gs.log.debug(
                f'This message was sent: "{message}" to room "{room_id}". '
                f"Response: event_id={resp.event_id}, room_id={resp.room_id}, "
                f"full response: {privacy_filter(str(resp))}. "
            )
    except Exception:
        gs.log.error("E151: " "Message send failed. Sorry.")
        gs.err_count += 1
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())


async def stream_messages_from_pipe(client, rooms):
    """Read input from pipe if available.

    Read pipe line by line. For each line received, immediately
    send it.

    Arguments:
    ---------
    client : Client
    rooms : list of room_ids

    """
    stdin_ready = select.select([sys.stdin,], [], [], 0.0)[  # noqa
        0
    ]  # noqa
    if not stdin_ready:
        gs.log.debug(
            "stdin is not ready for streaming. "
            "A pipe could be used, but pipe could be empty, "
            "stdin could also be a keyboard."
        )
    else:
        gs.log.debug(
            "stdin is ready. Something "
            "is definitely piped into program from stdin. "
            "Reading message from stdin pipe."
        )
    if ((not stdin_ready) and (not sys.stdin.isatty())) or stdin_ready:
        if not sys.stdin.isatty():
            gs.log.debug(
                "Pipe was definitely used, but pipe might be empty. "
                "Trying to read from pipe in any case."
            )
        try:
            for line in sys.stdin:
                await send_message(client, rooms, line)
                gs.log.debug("Using data from stdin pipe stream as message.")
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
            "stdin is not ready for reading. "
            "A pipe could be used, but pipe could be empty, "
            "stdin could also be a keyboard."
        )
    else:
        gs.log.debug(
            "stdin is ready. Something "
            "is definitely piped into program from stdin. "
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
            "stdin is not ready for keyboard interaction. "
            "A pipe could be used, but pipe could be empty, "
            "stdin could also be a keyboard."
        )
    else:
        gs.log.debug(
            "stdin is ready. Something "
            "is definitely piped into program from stdin. "
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
    streaming = False
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
            elif m == "\\_":  # escaped _
                messages_from_commandline += ["_"]
            elif m == "-":
                # stdin pipe, read and process everything in pipe as 1 msg
                messages_from_commandline += get_messages_from_pipe()
            elif m == "_":
                # streaming via pipe on stdin
                # stdin pipe, read and process everything in pipe line by line
                streaming = True
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
    # now we are done with all the usual sends, now we start streaming
    if streaming:
        await stream_messages_from_pipe(client, rooms)


async def login_using_credentials_file(
    credentials_file: Optional[str] = None, store_dir: Optional[str] = None
) -> (AsyncClient, dict):
    """Log in by using available credentials file.

    Arguments:
    ---------
        credentials_file: str : location of credentials file
            compute it if not provided
        store_dir: str : location of persistent storage store directory
            compute it if not provided

    Returns
    -------
        AsyncClient : the created NIO client
        dict : the credentials dictionary from the credentials file

    """

    if not credentials_file:
        credentials_file = determine_credentials_file()
    if not store_dir:
        store_dir = determine_store_dir()

    if not credentials_exist(credentials_file):
        raise MatrixCommanderError(
            "E153: "
            "Credentials file was not found. Provide credentials file or "
            "use --login to create a credentials file."
        ) from None
    if not store_exists(store_dir):
        raise MatrixCommanderError(
            "E154: "
            "Store directory was not found. Provide store directory or "
            "use --login to create a store directory."
        ) from None

    credentials = read_credentials_from_disk(credentials_file)
    gs.credentials = credentials

    gs.log.debug("About to configure Matrix Async Client.")
    # Configuration options for the AsyncClient
    client_config = AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        store_sync_tokens=True,
        encryption_enabled=True,
    )
    gs.log.debug("About to initialize Matrix Async Client.")
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
    if gs.pa.proxy:
        gs.log.debug(f"Proxy {gs.pa.proxy} will be used for connectivity.")

    gs.log.debug("About to restore login.")
    # restore_login() always returns None, on success or failure
    # restore_login() does not go to the server, it just sets some local values
    # TODO: performance
    # restore_login() is a slow operation. 1.5s to 2s. Why?
    # Because it is reading the store file database.
    # Setting store_sync_tokens=False above will not make it go any faster.
    client.restore_login(
        user_id=credentials["user_id"],
        device_id=credentials["device_id"],
        access_token=credentials["access_token"],
    )
    gs.log.debug("Finished restoring login.")
    gs.log.debug(
        "Login will be using stored credentials from "
        f'credentials file "{credentials_file}". '
        f'room_id = {credentials["room_id"]}, '
        f'device_id = {credentials["device_id"]}, '
        f'access_token = {credentials["access_token"][0:1]}***'
        f'{credentials["access_token"][-1:]}.'
    )
    if gs.pa.debug > 0:
        gs.log.debug("About to connect to server to verify connection.")
        # gs.log.debug(f"Logged_in()={client.logged_in}") is always True.
        # Just because client.logged_in is True does not mean we are logged in.
        # That just means the data structure is filled.
        # How to know if login was successful?
        # Do an actual API call against the server. E.g. whoami.
        # We don't want to do this always for performance reasons, so we only
        # do it in debug mode.
        try:
            resp = await client.whoami()
        except Exception as e:
            await client.close()
            client = None
            credentials = None
            raise (e)
        if isinstance(resp, responses.WhoamiError):
            gs.log.error(
                "E155: "
                "restore_login failed. Did you perform --logout "
                "before? Looks like your access-token expired. Maybe "
                "delete credentials file and store and perform a "
                f"new --login. Response is: {privacy_filter(str(resp))}"
            )
            gs.err_count += 1
            await client.close()
            client = None
            credentials = None
        else:
            gs.log.debug(
                "restore_login successful. Successfully "
                f"logged in as user {resp.user_id} via restore_login. "
                f"Response is: {privacy_filter(str(resp))}"
            )
    else:
        pass
        # login might or might not fail later,
        # if it fails some exception will be raised, the exception text
        # might not explain the problem well, but this way we speed up
        # performance by issuing one API less against the server.
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
    if gs.pa.room_invites:
        gs.log.debug(
            "Registering to listen to events of type "
            "InviteMemberEvent. Listening to room invites."
        )
        client.add_event_callback(
            callbacks.invite_callback, (InviteMemberEvent,)
        )
    print(
        "This program is ready and listening for its Matrix messages. "
        "To stop program type Control-C on keyboard or send signal "
        f"to process {os.getpid()}. PID can also be found in "
        f'file "{PID_FILE_DEFAULT}".',
        file=sys.stderr,
        flush=True,
    )
    # the sync_loop will be terminated by user hitting Control-C to stop
    await client.sync_forever(timeout=30000, full_state=True)


async def listen_invites_once(client: AsyncClient) -> None:
    """Listen once exclusively for room invites, then quit.

    Get all the room invitations that are currently queued up and waiting.
    List them or join these rooms. Then leave.
    """
    # Set up event callbacks
    callbacks = Callbacks(client)
    gs.log.debug(
        "Registering to listen to events of type "
        "InviteMemberEvent. Listening to room invites."
    )
    client.add_event_callback(callbacks.invite_callback, (InviteMemberEvent,))
    # We want to get out quickly, so we reduced timeout to 10 sec.
    # We want to get messages and quit, so we call sync() instead of
    # sync_forever().
    resp = await client.sync(timeout=10000, full_state=False)
    if isinstance(resp, SyncResponse):
        gs.log.debug(
            f"Sync successful. Response is: {privacy_filter(str(resp))}"
        )
    else:
        gs.log.error(
            "E160: " f"Sync failed. Error is: {privacy_filter(str(resp))}"
        )
    # sync() forces the message_callback() to fire
    # for each new message presented in the sync().


async def listen_once(client: AsyncClient) -> None:
    """Listen once, then quit.

    Get all the messages that are currently queued up and waiting.
    Print them. Then leave.
    """
    # Set up event callbacks
    callbacks = Callbacks(client)
    client.add_event_callback(callbacks.message_callback, (RoomMessage,))
    if gs.pa.room_invites:
        gs.log.debug(
            "Registering to listen to events of type "
            "InviteMemberEvent. Listening to room invites."
        )
        client.add_event_callback(
            callbacks.invite_callback, (InviteMemberEvent,)
        )
    # We want to get out quickly, so we reduced timeout to 10 sec.
    # We want to get messages and quit, so we call sync() instead of
    # sync_forever().
    resp = await client.sync(timeout=10000, full_state=False)
    if isinstance(resp, SyncResponse):
        gs.log.debug(
            f"Sync successful. Response is: {privacy_filter(str(resp))}"
        )
    else:
        gs.log.error(
            "E160: " f"Sync failed. Error is: {privacy_filter(str(resp))}"
        )
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
                    "room_read_markers failed with response "
                    f"{privacy_filter(str(resp))}."
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
    resp_s = await synchronize(client)  # sync() to get rooms
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
    limit = gs.pa.tail
    gs.log.debug(f"Rooms are: {rooms}, limit is {limit}")
    # To loop over all rooms, one can loop through the join dictionary. i.e.
    # for room_id, room_info in resp_s.rooms.join.items():  # loop all rooms
    for room_id in rooms:  # loop only over user specified rooms
        resp = await client.room_messages(
            room_id, start=resp_s.next_batch, limit=limit
        )
        if isinstance(resp, RoomMessagesError):
            gs.log.warning(
                "W106: "
                f"room_messages failed with response "
                f"{privacy_filter(str(resp))}. "
                "Processing continues."
            )
            gs.warn_count += 1
            continue  # skip this room
        gs.log.debug(
            f"room_messages response = {type(resp)} :: "
            f"{privacy_filter(str(resp))}."
        )
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
            first_event = resp.chunk[0]
            resp = await client.room_read_markers(
                room_id=room_id,
                fully_read_event=first_event.event_id,
                read_event=first_event.event_id,
            )
            if isinstance(resp, RoomReadMarkersError):
                gs.log.debug(
                    "room_read_markers failed with response "
                    f"{privacy_filter(str(resp))}."
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
    # is capped at 1000 at server side
    # 10 seems too small, i.e. too slow
    # 100 to 500 seem good values, depends on network speed, server load, ...
    # example run: 250-->7min30s, 500-->4min30s
    max_msg_per_pull = 500
    while True:
        try:
            resp = await client.room_messages(
                room_id,
                current_start_token,
                limit=max_msg_per_pull,
                direction=direction,
            )
        except Exception as e:
            # during testing I observed that sometimes an exception is raised,
            # but e is empty. Stacktrace had asyncio.exceptions.TimeoutError.
            gs.log.error(
                "E161: "
                "Error during getting messages. "
                "But program will continue anyway, despite the error. "
                "Not all messages might have been retrieved from server. "
                f"Be warned! Got {len(all_events)} messages so far."
                f"Exception: {type(e)} {e}"
            )
            gs.err_count += 1
            gs.log.debug("Here is the traceback.\n" + traceback.format_exc())
            break
        if isinstance(resp, RoomMessagesError):
            gs.err_count += 1
            gs.log.error(
                "E162: "
                f"room_messages failed with resp = {privacy_filter(str(resp))}"
            )
            break  # skip to end of function
        gs.log.debug(f"Got {len(all_events)+len(resp.chunk)} messages so far.")
        gs.log.debug(f"Received {len(resp.chunk)} events.")
        gs.log.debug(
            f"room_messages response = {type(resp)} :: "
            f"{privacy_filter(str(resp))}."
        )
        gs.log.debug(f"room_messages room_id = {resp.room_id}.")
        gs.log.debug(f"room_messages start = (str) {resp.start}.")
        gs.log.debug(f"room_messages end = (str) :: {resp.end}.")
        gs.log.debug(f"room_messages chunk = (list) :: {resp.chunk}.")
        # resp.chunk is just a list of RoomMessage events like this example:
        # chunk=[RoomMessageText(...)]
        current_start_token = resp.end
        if len(resp.chunk) == 0:
            gs.log.debug(
                "All messages have been retrieved from server successfully. "
                f"{len(all_events)} messages were pulled from server."
            )
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
    resp_s = await synchronize(client)  # sync() to get rooms
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
                gs.log.error(
                    "E163: "
                    "room_read_markers failed with response "
                    f"{privacy_filter(str(resp))}."
                )


async def action_listen() -> None:
    """Listen while being logged in."""
    if not gs.client and not gs.credentials:
        gs.log.error(
            "E164: " "Client or credentials not set. Skipping action."
        )
        gs.err_count += 1
        return
    try:
        # Sync encryption keys with the server
        # Required for participating in encrypted rooms
        if gs.client.should_upload_keys:
            await gs.client.keys_upload()
        gs.log.debug(f"Listening type: {gs.pa.listen}")
        if gs.pa.listen == FOREVER:
            await listen_forever(gs.client)
        elif gs.pa.listen == ONCE:
            await listen_once(gs.client)
            # could use 'await listen_once_alternative(gs.client)'
            # as an alternative implementation
        elif gs.pa.listen == TAIL:
            await listen_tail(gs.client, gs.credentials)
        elif gs.pa.listen == ALL:
            await listen_all(gs.client, gs.credentials)
        else:
            gs.log.error(
                "E165: "
                f'Unrecognized listening type "{gs.pa.listen}". '
                "Skipping listening."
            )
            gs.err_count += 1
    except Exception as e:
        gs.log.error(
            "E166: "
            "Error during listening. Continuing despite error. "
            f"Exception: {e}"
        )
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())
        gs.err_count += 1


async def action_set_device_name(
    client: AsyncClient, credentials: dict
) -> None:
    """Set, rename the device name of itself while already being logged in."""
    content = {"device_name": gs.pa.set_device_name}
    resp = await client.update_device(credentials["device_id"], content)
    if isinstance(resp, UpdateDeviceError):
        gs.log.error(
            "E167: " f"update_device failed with {privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(
            f"update_device successful with {privacy_filter(str(resp))}"
        )


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
        gs.log.error(
            "E168: " f"set_displayname failed with {privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(
            f"set_displayname successful with {privacy_filter(str(resp))}"
        )


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
            gs.log.error(
                "E169: "
                f"get_displayname failed with {privacy_filter(str(resp))}"
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                f"get_displayname successful with {privacy_filter(str(resp))}"
            )
            # resp.displayname is str or None (has no display name)
            if not resp.displayname:
                displayname = ""  # means no display name is set
            else:
                displayname = resp.displayname
            # output format controlled via --output flag
            text = f"{user}{SEP}{displayname}"
            # Object of type RoomCreateResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            json_max.update({"user": user})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )


async def action_set_presence(client: AsyncClient, credentials: dict) -> None:
    """Set the logged in user's presence. Change my own presence.
    Assumes that user is already logged in.
    """
    state = gs.pa.set_presence.strip().lower()
    gs.log.debug(f"Setting presence to {state} [{gs.pa.set_presence}].")
    resp = await client.set_presence(state)
    if isinstance(resp, PresenceSetError):
        gs.log.error(
            "E170: " f"set_presence failed with {privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(
            f"set_presence successful with {privacy_filter(str(resp))}"
        )


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
            gs.log.error(
                "E171: "
                f"get_presence failed with {privacy_filter(str(resp))}"
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                f"get_presence successful with {privacy_filter(str(resp))}"
            )
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
            # output format controlled via --output flag
            text = (
                f"{resp.user_id}{SEP}{resp.presence}{SEP}{last_active_ago}"
                f"{SEP}{currently_active}{SEP}{status_msg}"
            )
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            # json_max.update({"key": value})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )


async def action_upload(client: AsyncClient, credentials: dict) -> None:
    """Upload one or more files to content repository of Matrix server.
    Assumes that user is already logged in.
    """
    for filename in gs.pa.upload:
        filename = filename.strip()
        encrypt = False if gs.pa.plain else True
        mime_type = magic.from_file(filename, mime=True)
        file_stat = await aiofiles.os.stat(filename)
        async with aiofiles.open(filename, "r+b") as f:
            resp, decryption_dict = await client.upload(
                f,
                content_type=mime_type,  # e.g. application/pdf
                filename=os.path.basename(filename),
                encrypt=encrypt,
                filesize=file_stat.st_size,
            )
        if isinstance(resp, UploadError):
            gs.log.error(
                "E172: "
                "Failed to upload. "
                f'file="{filename}"; mime_type="{mime_type}"; '
                f"filessize={file_stat.st_size}; encrypt={encrypt}"
                f"Server response: {privacy_filter(str(resp))}"
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                f"File {filename}, mime={mime_type}, "
                f"{file_stat.st_size} bytes, encrypt={encrypt} "
                "was successfully uploaded to server. Response is: "
                f"{privacy_filter(str(resp))}."
            )
            gs.log.debug(
                f"URI of uploaded file {filename} is: {resp.content_uri}"
            )
            gs.log.debug(
                f"Decryption key (dictionary) of uploaded file {filename} is: "
                "'*** hidden to prevent leaks'"  # f"{decryption_dict}"
            )
            # decryption_dict will be None in case of plain-text
            # the URI and keys will be needed later. So this print is a must
            # output format controlled via --output flag
            text = f"{resp.content_uri}{SEP}{decryption_dict}"
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            json_max.update(
                {"decryption_dict": decryption_dict}
            )  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )


async def action_delete_mxc(client: AsyncClient, credentials: dict) -> None:
    """Delete one or more files from content repository of Matrix server.
    Assumes that user is already logged in.
    """
    # see: https://docs.aiohttp.org/en/stable/client_quickstart.html
    # we must emulate a curl like this:
    # curl -XDELETE  "https://SERVERHERE/_synapse/admin/v1/media/SERVERHERE/
    #      MXCIDHERE?access_token=ACCESS_TOKEN_HERE"
    for mxc in gs.pa.delete_mxc:
        mxc = mxc.strip()
        gs.log.debug(f"Preparing to delete MXC {mxc}.")
        # we allow mxc to be a) mxc://server/mxc-id or just mxc-id
        if urlparse(mxc).scheme == "mxc":
            mxc = urlparse(mxc).path.replace("/", "")
        gs.log.debug(f"Preparing to delete MXC ID {mxc}.")
        if gs.pa.access_token:
            at = gs.pa.access_token
            gs.log.debug("Using access token from --access-token argument.")
        else:
            at = credentials["access_token"]
            gs.log.debug("Using access token from credentials file.")
        srv_full = credentials["homeserver"]  # https://example.matrix.org
        srv_host = urlparse(srv_full).hostname  # example.matrix.org
        rest = (
            srv_full
            + "/_synapse/admin/v1/media/"
            + srv_host
            + "/"
            + mxc
            + "?access_token="
            + at
        )
        gs.log.debug(f"Issuing REST Matrix API call: DELETE {rest}")
        connector = TCPConnector(ssl=gs.ssl)  # setting sslcontext
        async with ClientSession(connector=connector) as session:  # aiohttp
            async with session.delete(rest) as resp:
                status = resp.status  # int, 200 success
                txt = await resp.text()  # str in dict format
        if status != 200:
            # txt is str like this:
            # {"errcode":"M_FORBIDDEN","error":"You are not a server admin"}
            gs.log.error(
                "E173: "
                f"Failed to delete object (mxc) '{mxc}' from server "
                f"'{srv_full}'. Failed with error code {status} and "
                f"error text {txt}."
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                f"MXC object {mxc} was successfully deleted from server "
                f"{srv_full}. Response is: {txt}."
            )


async def action_delete_mxc_before(
    client: AsyncClient, credentials: dict
) -> None:
    """Delete files older and larger from content repository of Matrix server.
    Assumes that user is already logged in.
    """
    # https://matrix-org.github.io/synapse/latest/admin_api/
    #   media_admin_api.html#delete-local-media-by-date-or-size
    # POST /_synapse/admin/v1/media/<server_name>/delete?before_ts=<before_ts>
    # &size_gt=<size>
    if len(gs.pa.delete_mxc_before) > 2:
        gs.log.error(
            "E174: "
            "Incorrect number of arguments for --delete_mxc_before. "
            "There must be 1 or 2 arguments , but found "
            f"{len(gs.pa.delete_mxc_before)} arguments."
        )
        gs.err_count += 1
        return
    size = 0
    if len(gs.pa.delete_mxc_before) == 2:
        size = gs.pa.delete_mxc_before[1]
    before_str = gs.pa.delete_mxc_before[0]
    millisec = int(
        datetime.datetime.strptime(before_str, "%d.%m.%Y %H:%M:%S").timestamp()
        * 1000
    )

    gs.log.debug(
        f"Preparing to delete objects older than {before_str} "
        f"(Unix time {millisec}) and larger than {size}."
    )
    if gs.pa.access_token:
        at = gs.pa.access_token
        gs.log.debug("Using access token from --access-token argument.")
    else:
        at = credentials["access_token"]
        gs.log.debug("Using access token from credentials file.")
    srv_full = credentials["homeserver"]  # https://example.matrix.org
    srv_host = urlparse(srv_full).hostname  # example.matrix.org
    rest = (
        srv_full
        + "/_synapse/admin/v1/media/"
        + srv_host
        + "/delete?before_ts="
        + str(millisec)
        + "&size_gt="
        + str(size)
        + "&access_token="
        + at
    )
    gs.log.debug(f"Issuing REST Matrix API call: POST {rest}")
    connector = TCPConnector(ssl=gs.ssl)  # setting sslcontext
    async with ClientSession(connector=connector) as session:  # aiohttp
        async with session.post(rest) as resp:
            status = resp.status  # int, 200 success
            txt = await resp.text()  # str in dict format
    if status != 200:
        # txt is str like this:
        # {"errcode":"M_FORBIDDEN","error":"You are not a server admin"}
        gs.log.error(
            "E175: "
            f"Failed to delete objects before '{before_str}' from server "
            f"'{srv_full}'. Failed with error code {status} and "
            f"error text {txt}."
        )
        gs.err_count += 1
    else:
        gs.log.debug(
            f"Objects older than {before_str} and larger than {size} "
            "were successfully deleted from server "
            f"{srv_full}. Response is: \n{txt}."
        )


async def action_download(client: AsyncClient, credentials: dict) -> None:
    """Download a file from content repository of Matrix server.
    Assumes that user is already logged in.
    """
    if not gs.pa.download:
        gs.log.debug("Download list is empty. Nothing to download. Skipping.")
        return
    filenames = gs.pa.file_name
    if filenames:
        while len(filenames) < len(gs.pa.download):
            filenames.append(None)
    decryption_strings = gs.pa.key_dict
    if decryption_strings:
        while len(decryption_strings) < len(gs.pa.key_dict):
            decryption_strings.append(None)
    # filenames is now None or list at least as long as downloads
    # decryption_strings is now None or list at least as long as downloads
    gs.log.debug(f"File names provided in arguments: {filenames}")
    gs.log.debug(
        "Decryption strings provided in arguments: "
        "'*** hidden to prevent leaks'"
        # f"{decryption_strings}"
    )
    ii = 0
    for download in gs.pa.download:
        if gs.pa.file_name:
            filename = filenames[ii]  # 1st choice
        else:
            # 2nd choice; get filename from server
            # i.e. use the original filename from upload
            filename = None
        if gs.pa.key_dict:
            decryption_str = decryption_strings[ii]
        else:
            decryption_str = None
        encrypted = True if decryption_str else False
        if not encrypted:
            gs.log.debug(
                "No key dictionary specified with --key-dict. So, it is "
                "assumed that the download is not encrypted "
                "(i.e. plain-text). No decryption will be attempted."
            )
        mxc = download
        resp = await download_mxc(client, mxc=mxc, filename=filename)
        if isinstance(resp, DownloadError):
            gs.log.error(
                "E176: "
                f"download of URI '{mxc}' to local file '{filename}' "
                f"failed with response {privacy_filter(str(resp))}"
            )
            gs.err_count += 1
        else:
            url = urlparse(mxc)
            media_id = url.path.strip("/")
            if filename == "":
                filename = "mxc-" + MXC_ID_PLACEHOLDER
            if not filename:
                filename = resp.filename  # 2nd choice, from server
                gs.log.debug(f"File name on server: {filenames}")
            else:
                filename = filename.replace(MXC_ID_PLACEHOLDER, media_id)
            if not filename:
                filename = "mxc-" + media_id  # 3rd choice, mxc_id
            gs.log.debug(
                f"Download of URI '{mxc}' to local file '{filename}' "
                f"successful with {len(resp.body)} bytes of data downloaded, "
                f"content_type {resp.content_type}; "
                f"remote filename {resp.filename}; "
                f"encrypted {encrypted}; "
                "key dictionary '*** hidden to prevent leaks'. "
                # f"key dictionary {decryption_str}. "
                "Trying to save data now."
            )
            if encrypted:
                decryption_dict = ast.literal_eval(decryption_str)
                with open(filename, "wb") as file:
                    file.write(
                        crypto.attachments.decrypt_attachment(
                            resp.body,
                            decryption_dict["key"]["k"],
                            decryption_dict["hashes"]["sha256"],
                            decryption_dict["iv"],
                        )
                    )
            else:  # plain, unencrypted
                with open(filename, "wb") as file:
                    file.write(resp.body)
        ii += 1


async def action_joined_rooms(client: AsyncClient, credentials: dict) -> None:
    """Get joined rooms while already logged in."""
    resp = await client.joined_rooms()
    if isinstance(resp, JoinedRoomsError):
        gs.log.error(
            "E177: " f"joined_rooms failed with {privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(
            f"joined_rooms successful with {privacy_filter(str(resp))}"
        )
        # output format controlled via --output flag
        text = ""
        for rr in resp.rooms:
            text += rr + "\n"
        text = text.strip()
        # Object of type xxxResponse is not JSON
        # serializable, hence we use the dictionary.
        json_max = resp.__dict__
        # json_max.update({"key": value})  # add dict items
        json_ = json_max.copy()
        json_.pop("transport_response")
        json_spec = None
        print_output(
            gs.pa.output,
            text=text,
            json_=json_,
            json_max=json_max,
            json_spec=json_spec,
        )


async def action_joined_members(
    client: AsyncClient, credentials: dict
) -> None:
    """Get members of given rooms while already being logged in."""
    rooms = gs.pa.joined_members
    if not rooms:
        gs.log.warning(
            "W107: "
            "No membership action(s) were performed because no rooms "
            "were specified. Use --joined-members option and specify rooms."
        )
        gs.warn_count += 1
        return

    gs.log.debug(f"Trying to get members for these rooms: {rooms}")
    if "*" in rooms:
        resp = await client.joined_rooms()
        if isinstance(resp, JoinedRoomsError):
            gs.log.error(
                "E178: "
                "joined_rooms failed with "
                f"{privacy_filter(str(resp))}. Not able to "
                "get all rooms as specified by '*'. "
                "The member listing will be incomplete or missing."
            )
            gs.err_count += 1
            # since we can't get all rooms leave room list as is
            rooms = filter(lambda val: val != "*", rooms)  # remove all *
        else:
            gs.log.debug(
                f"joined_rooms successful with {privacy_filter(str(resp))}"
            )
            gs.log.debug(
                "Room list has been successfully overwritten with '*'"
            )
            rooms = resp.rooms  # overwrite args with full list
    for room in rooms:
        room = room.replace(r"\!", "!")  # remove possible escape
        resp = await client.joined_members(room)
        if isinstance(resp, JoinedMembersError):
            gs.log.error(
                "E179: "
                f"joined_members failed with {privacy_filter(str(resp))}"
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                f"joined_members successful with {privacy_filter(str(resp))}"
            )
            # members = List[RoomMember] ; RoomMember
            # output format controlled via --output flag
            text = resp.room_id + "\n"
            for member in resp.members:
                # convert None to ''
                text += (
                    SEP
                    + member.user_id
                    + SEP
                    + zn(member.display_name)
                    + SEP
                    + zn(member.avatar_url)
                    + "\n"
                )
            text = text.strip()
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            # json_max.update({"key": value})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )


async def action_mxc_to_http(client: AsyncClient, credentials: dict) -> None:
    """Convert MXC URI to HTTP URL while already logged in."""
    for mxc in gs.pa.mxc_to_http:
        mxc = mxc.strip()
        http = await client.mxc_to_http(mxc)  # returns None or str
        # output format controlled via --output flag
        text = f"{mxc}{SEP}{http}"
        json_max = {"mxc": mxc, "http": http}
        # json_max.update({"key": value})  # add dict items
        json_ = json_max.copy()
        # json_.pop("key")
        json_spec = None
        print_output(
            gs.pa.output,
            text=text,
            json_=json_,
            json_max=json_max,
            json_spec=json_spec,
        )


async def action_devices(client: AsyncClient, credentials: dict) -> None:
    """List devices of account while already logged in."""
    resp = await client.devices()
    if isinstance(resp, DevicesError):
        gs.log.error(
            "E180: " f"devices failed with {privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(f"devices successful with {privacy_filter(str(resp))}")
        # output format controlled via --output flag
        text = ""
        for rr in resp.devices:
            text += (
                rr.id
                + SEP
                + rr.display_name
                + SEP
                + rr.last_seen_ip
                + SEP
                + str(rr.last_seen_date)
                + "\n"
            )
        text = text.strip()
        # Object of type xxxResponse is not JSON
        # serializable, hence we use the dictionary.
        json_max = resp.__dict__
        # json_max.update({"key": value})  # add dict items
        json_ = json_max.copy()
        json_.pop("transport_response")
        json_spec = None
        print_output(
            gs.pa.output,
            text=text,
            json_=json_,
            json_max=json_max,
            json_spec=json_spec,
        )


async def action_discovery_info(
    client: AsyncClient, credentials: dict
) -> None:
    """List discovery_info of home server while already logged in."""
    resp = await client.discovery_info()
    if isinstance(resp, DiscoveryInfoError):
        gs.log.error(
            "E181: " f"discovery_info failed with {privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(
            f"discovery_info successful with {privacy_filter(str(resp))}"
        )
        # output format controlled via --output flag
        text = f"{resp.homeserver_url}{SEP}{resp.identity_server_url}"
        # Object of type xxxResponse is not JSON
        # serializable, hence we use the dictionary.
        json_max = resp.__dict__
        # json_max.update({"key": value})  # add dict items
        json_ = json_max.copy()
        json_.pop("transport_response")
        json_spec = None
        print_output(
            gs.pa.output,
            text=text,
            json_=json_,
            json_max=json_max,
            json_spec=json_spec,
        )


async def action_login_info(client: AsyncClient, credentials: dict) -> None:
    """List login methods of home server while already logged in."""
    resp = await client.login_info()
    if isinstance(resp, LoginInfoError):
        gs.log.error(
            "E182: " f"login_info failed with {privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(f"login_info successful with {privacy_filter(str(resp))}")
        # output format controlled via --output flag
        text = ""
        for rr in resp.flows:
            text += str(rr) + "\n"
        text = text.strip()
        # Object of type xxxResponse is not JSON
        # serializable, hence we use the dictionary.
        json_max = resp.__dict__
        # json_max.update({"key": value})  # add dict items
        json_ = json_max.copy()
        json_.pop("transport_response")
        json_spec = None
        print_output(
            gs.pa.output,
            text=text,
            json_=json_,
            json_max=json_max,
            json_spec=json_spec,
        )


async def action_content_repository_config(
    client: AsyncClient, credentials: dict
) -> None:
    """List config of content repo of home server while already logged in."""
    resp = await client.content_repository_config()
    if isinstance(resp, ContentRepositoryConfigError):
        gs.log.error(
            "E183: "
            "content_repository_config failed with "
            f"{privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(
            "content_repository_config successful with "
            f"{privacy_filter(str(resp))}"
        )
        # output format controlled via --output flag
        text = resp.upload_size  # returns only 1 value
        # Object of type xxxResponse is not JSON
        # serializable, hence we use the dictionary.
        json_max = resp.__dict__
        # json_max.update({"key": value})  # add dict items
        json_ = json_max.copy()
        json_.pop("transport_response")
        json_spec = None
        print_output(
            gs.pa.output,
            text=text,
            json_=json_,
            json_max=json_max,
            json_spec=json_spec,
        )


async def action_rest(client: AsyncClient, credentials: dict) -> None:
    """Invoke REST API on Matrix server.
    Assumes that user is already logged in.
    """
    # see: https://docs.aiohttp.org/en/stable/client_quickstart.html
    # we must emulate a curl like this:
    # curl -XDELETE  "https://SERVERHERE/_synapse/admin/v1/media/SERVERHERE/
    #      MXCIDHERE?access_token=ACCESS_TOKEN_HERE"
    # curl -XPOST -d '{"msgtype":"m.text", "body":"hello"}' \
    #   "__homeserver__/_matrix/client/r0/rooms/__encoded_full_room_id__/\
    #   send/m.room.message?access_token=YOURTOKENHERE"
    # curl -XGET -d "" '__homeserver__/_matrix/client/versions'
    if not len(gs.pa.rest) % 3 == 0:
        gs.log.error(
            "E184: "
            "Incorrect number of arguments for --rest. Arguments must be "
            f"triples, i.e. multiples of 3, but found {len(gs.pa.rest)} "
            "arguments."
        )
        gs.err_count += 1
        return
    for ii in range(len(gs.pa.rest) // 3):
        method = gs.pa.rest[ii * 3 + 0]
        data = gs.pa.rest[ii * 3 + 1]
        url = gs.pa.rest[ii * 3 + 2]
        if not method or method.upper().strip() not in [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",
        ]:
            gs.log.error(
                "E185: "
                f"Incorrect REST method {method}. "
                'Must be one of: "GET", "POST", "PUT", "DELETE", "OPTIONS".'
            )
            gs.err_count += 1
            continue
        method = method.upper().strip()
        if not data:
            data = ""
        if not url or url.strip() == "":
            gs.log.error(
                "E186: " f"Incorrect REST URL {url}. Must not be empty."
            )
            gs.err_count += 1
            continue
        if gs.pa.access_token:
            at = gs.pa.access_token
            gs.log.debug("Using access token from --access-token argument.")
        else:
            at = credentials["access_token"]
            gs.log.debug("Using access token from credentials file.")
        for ph in [
            HOMESERVER_PLACEHOLDER,
            HOSTNAME_PLACEHOLDER,
            ACCESS_TOKEN_PLACEHOLDER,
            USER_ID_PLACEHOLDER,
            DEVICE_ID_PLACEHOLDER,
            ROOM_ID_PLACEHOLDER,
        ]:
            if ph == HOMESERVER_PLACEHOLDER:
                data = data.replace(ph, credentials["homeserver"])
                url = url.replace(ph, credentials["homeserver"])
            elif ph == HOSTNAME_PLACEHOLDER:
                hostname = urlparse(credentials["homeserver"]).hostname
                data = data.replace(ph, hostname)
                url = url.replace(ph, hostname)
            elif ph == ACCESS_TOKEN_PLACEHOLDER:
                data = data.replace(ph, at)
                url = url.replace(ph, at)
            elif ph == USER_ID_PLACEHOLDER:
                data = data.replace(ph, credentials["user_id"])
                url = url.replace(ph, credentials["user_id"])
            elif ph == DEVICE_ID_PLACEHOLDER:
                data = data.replace(ph, credentials["device_id"])
                url = url.replace(ph, credentials["device_id"])
            elif ph == ROOM_ID_PLACEHOLDER:
                room_id = credentials["room_id"]
                room_id = await map_roominfo_to_roomid(client, room_id)
                room_id = quote(room_id)
                data = data.replace(ph, room_id)
                url = url.replace(ph, room_id)
        url = url.strip()
        if data != "" and (method in ("GET", "DELETE", "OPTIONS")):
            gs.log.warning(
                "W108: "
                f'Found REST data "{data}" for method {method}. '
                'There is usually no data for: "GET", "DELETE", "OPTIONS". '
                "Most likely this is not what you want. "
            )
            gs.warn_count += 1
            continue
        gs.log.debug(
            f"Preparing to invoke REST API call: method={method} "
            f"data={data}, url={privacy_filter(str(url))}."
        )
        connector = TCPConnector(ssl=gs.ssl)  # setting sslcontext
        async with ClientSession(connector=connector) as session:  # aiohttp
            if method == "GET":
                async with session.get(url, data=data) as resp:
                    status = resp.status  # int, 200 success
                    txt = await resp.text()  # str in dict format
            elif method == "POST":
                async with session.post(url, data=data) as resp:
                    status = resp.status  # int, 200 success
                    txt = await resp.text()  # str in dict format
            elif method == "PUT":
                async with session.put(url, data=data) as resp:
                    status = resp.status  # int, 200 success
                    txt = await resp.text()  # str in dict format
            elif method == "DELETE":
                async with session.delete(url, data=data) as resp:
                    status = resp.status  # int, 200 success
                    txt = await resp.text()  # str in dict format
            elif method == "OPTIONS":
                async with session.options(url, data=data) as resp:
                    status = resp.status  # int, 200 success
                    txt = await resp.text()  # str in dict format
        if status != 200:
            # txt is str like this:
            # {"errcode":"M_FORBIDDEN","error":"You are not a server admin"}
            gs.log.error(
                "E187: "
                f"REST API call failed. Failed with error code {status} and "
                f"error text {txt}. Input was: method={method} "
                f"data={data}, url={privacy_filter(str(url))}."
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                f"REST API call was successful. "
                f"Response is: {txt}. Input was: method={method} "
                f"data={data}, url={privacy_filter(str(url))}."
            )
            # output format controlled via --output flag
            text = f"{txt}"  # returns only 1 value
            json_max = resp.__dict__
            json_max.update({"response": txt})  # add dict items
            json_ = json_max.copy()
            # json_.pop("key")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )


async def action_get_avatar(client: AsyncClient, credentials: dict) -> None:
    """Get avatar(s) of itself or users while already logged in."""
    if gs.pa.get_avatar == []:
        gs.pa.get_avatar.append(credentials["user_id"])  # whoami
    gs.log.debug(f"Getting avatars for these users: {gs.pa.get_avatar}")
    for user_id in gs.pa.get_avatar:
        user_id = user_id.strip()
        resp = await client.get_avatar(user_id)
        if isinstance(resp, ProfileGetAvatarResponse):
            gs.log.debug(
                "ProfileGetAvatarResponse. Response is: "
                f"{privacy_filter(str(resp))}"
            )
            avatar_mxc = resp.avatar_url
            avatar_url = None
            if avatar_mxc:  # could be None if no avatar
                avatar_url = await client.mxc_to_http(avatar_mxc)
            gs.log.debug(
                f"avatar_mxc is {avatar_mxc}. avatar_url is {avatar_url}"
            )
            # output format controlled via --output flag
            text = f"{avatar_mxc}{SEP}{avatar_url}"
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            json_max.update({"avatar_http": avatar_url})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )
        else:
            gs.log.error(
                "E188: "
                f"Failed getting avatar for user {user_id} "
                f"from server. {privacy_filter(str(resp))}"
            )
            gs.err_count += 1


async def action_get_profile(client: AsyncClient, credentials: dict) -> None:
    """Get user profile(s) of itself or users while already logged in."""
    if gs.pa.get_profile == []:
        gs.pa.get_profile.append(credentials["user_id"])  # whoami
    gs.log.debug(f"Getting user profiles for these users: {gs.pa.get_profile}")
    for user_id in gs.pa.get_profile:
        user_id = user_id.strip()
        resp = await client.get_profile(user_id)
        if isinstance(resp, ProfileGetError):
            gs.log.error(
                "E189: "
                f"Failed getting profile for user {user_id} "
                f"from server. {privacy_filter(str(resp))}"
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                f"ProfileGetResponse. Response is: {privacy_filter(str(resp))}"
            )
            displayname = resp.displayname
            avatar_mxc = resp.avatar_url
            avatar_url = None
            if avatar_mxc:  # could be None if no avatar
                avatar_url = await client.mxc_to_http(avatar_mxc)
            other_info = resp.other_info
            if not other_info:  # empty dict
                other_info = ""
            gs.log.debug(
                f"displayname is {displayname}. avatar_mxc is {avatar_mxc}. "
                f"avatar_url is {avatar_url}. other_info is {resp.other_info}."
            )
            # output format controlled via --output flag
            text = (
                f"{displayname}{SEP}{avatar_mxc}{SEP}{avatar_url}"
                f"{SEP}{other_info}"
            )
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            json_max.update({"avatar_http": avatar_url})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )


async def action_get_client_info(
    client: AsyncClient, credentials: dict
) -> None:
    """Get client info while already logged in."""
    gs.log.debug("Getting client info.")
    await synchronize(client)  # sync() to get rooms
    print(json.dumps(client.__dict__, default=obj_to_dict))


async def action_get_room_info(client: AsyncClient, credentials: dict) -> None:
    """Get room display name(s) of itself or rooms while already logged in."""
    if gs.pa.get_room_info == []:
        gs.pa.get_room_info.append(credentials["room_id"])
    gs.log.debug(
        "Getting room display names for these rooms: " f"{gs.pa.get_room_info}"
    )
    await synchronize(client)  # sync() to get rooms
    # user_id = credentials["user_id"]
    for room_id in gs.pa.get_room_info:
        room_id = await map_roominfo_to_roomid(client, room_id)
        try:
            room = client.rooms[room_id]
            room_displayname = room.display_name
        except Exception as e:
            gs.log.error(
                "E190: "
                f"Failed getting room display name for room {room_id} "
                f"from server. "
                f"Exception is {e}. "
                f"Room is {room}. Room dict is {room.__dict__}. "
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                f"room id is {room_id}, "
                f"room display name is {room_displayname}, "
                f"room is {room}. "
            )
            resp = room
            # output format controlled via --output flag
            text = (
                f"{room_id}{SEP}{room_displayname}{SEP}"
                f"{room.canonical_alias}{SEP}{room.topic}{SEP}"
                f"{room.creator}{SEP}{room.encrypted}"
                # f"{SEP}{user_id}"
            )
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            json_max.update(
                {"display_name": room_displayname}
            )  # add dict items
            json_ = json_max.copy()
            # json_.pop("key")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )


async def action_has_permission(
    client: AsyncClient, credentials: dict
) -> None:
    """Inquire about permissions in rooms while already logged in."""
    if not len(gs.pa.has_permission) % 2 == 0:
        gs.log.error(
            "E191: "
            "Incorrect number of arguments for --has-permission. Arguments "
            "must be pairs, i.e. multiples of 2, but found "
            f"{len(gs.pa.has_permission)} arguments."
        )
        gs.err_count += 1
        return
    user_id = credentials["user_id"]  # whoami
    for ii in range(len(gs.pa.has_permission) // 2):
        room_id = gs.pa.has_permission[ii * 2 + 0]
        room_id = room_id.replace(r"\!", "!")  # remove possible escape
        room_id = await map_roominfo_to_roomid(client, room_id)
        permission_type = gs.pa.has_permission[ii * 2 + 1].strip()
        gs.log.debug(
            "Preparing to ask about permission for permission type "
            f"'{permission_type}' in room {room_id}."
        )
        try:
            resp = await client.has_permission(room_id, permission_type)
        except Exception as e:
            resp = ErrorResponse(
                "E192: "
                f"has_permission() failed with '{e}'. "
                f"Is the room id {room_id} correct?"
            )
        if isinstance(resp, ErrorResponse):
            gs.log.error(
                "E193: "
                "Failed to ask about permission for permission type "
                f"'{permission_type}' in room {room_id}. "
                f"Response is {privacy_filter(str(resp))}"
            )
            gs.err_count += 1
            # output format controlled via --output flag
            # for JSON the user can determine which one from the list
            # was successful and which one failed. For 4 inputs there
            # might only be 3 output JSON objects if there was 1 error.
            # In text mode we print this error line, so that for 4 inputs
            # there will be 4 output lines.
            print_output(
                gs.pa.output,
                text=(
                    f"Error{SEP}{user_id}{SEP}{room_id}"
                    f"{SEP}{permission_type}"
                ),
                json_=None,
                json_max=None,
                json_spec=None,
            )
        else:
            gs.log.debug(
                f"has_permission {user_id} for permission type "
                f"'{permission_type}' in room {room_id}: "
                f"{privacy_filter(str(resp))}"
            )
            # output format controlled via --output flag
            text = (
                f"{privacy_filter(str(resp))}{SEP}{user_id}{SEP}{room_id}{SEP}"
                f"{permission_type}"
            )
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            # json_max.update({"key": value})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )


async def action_set_avatar(client: AsyncClient, credentials: dict) -> None:
    """Set avatar of itself while already logged in."""
    user_id = credentials["user_id"]  # whoami
    avatar_mxc = gs.pa.set_avatar
    gs.log.debug(f"Setting avatar for user {user_id} to URI {avatar_mxc}.")
    resp = await client.set_avatar(avatar_mxc)
    if isinstance(resp, ProfileSetAvatarResponse):
        gs.log.debug(
            "ProfileSetAvatarResponse. Response is: "
            f"{privacy_filter(str(resp))}"
        )
        gs.log.info(
            f"Successfully set avatar for user {user_id} "
            f"to URI {avatar_mxc}."
        )
    else:
        gs.log.error(
            "E195: "
            f"Failed setting avatar for user {user_id} on server. "
            f"{privacy_filter(str(resp))}"
        )
        gs.err_count += 1


async def action_import_keys(client: AsyncClient, credentials: dict) -> None:
    """Import Megolm keys from file while already logged in."""
    file = gs.pa.import_keys[0]
    passphrase = gs.pa.import_keys[1]
    gs.log.debug(f"Importing keys from file {file} using a passphrase.")
    resp = await client.import_keys(file, passphrase)
    if isinstance(resp, EncryptionError):
        gs.log.error(
            "E196: "
            f"Failed to decrypt keys file. File {file} is invalid or "
            f"couldn’t be decrypted. {privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(
            f"import_keys successful. Response is: {privacy_filter(str(resp))}"
        )
        gs.log.info(f"Successfully imported keys from file {file}.")


async def action_export_keys(client: AsyncClient, credentials: dict) -> None:
    """Export Megolm keys from file while already logged in."""
    file = gs.pa.export_keys[0]
    passphrase = gs.pa.export_keys[1]
    gs.log.debug(f"Exporting keys to file {file} using a passphrase.")
    try:
        resp = await client.export_keys(file, passphrase)
    except Exception:
        gs.log.error("E197: " f"Failed to export keys to file {file}.")
        raise
    gs.log.debug(
        f"export_keys successful. Response is: {privacy_filter(str(resp))}"
    )
    gs.log.info(f"Successfully exported keys to file {file}.")


async def action_room_set_alias(
    client: AsyncClient, credentials: dict
) -> None:
    """Add alias(es) to room(s) while already logged in."""
    if len(gs.pa.room_set_alias) == 1:  # special case
        gs.pa.room_set_alias.append(credentials["room_id"])
    if not len(gs.pa.room_set_alias) % 2 == 0:
        gs.log.error(
            "E198: "
            "Incorrect number of arguments for --room-set-alias. Arguments "
            "must be pairs, i.e. multiples of 2, but found "
            f"{len(gs.pa.room_set_alias)} arguments. 1 is allowed too."
        )
        gs.err_count += 1
        return
    for ii in range(len(gs.pa.room_set_alias) // 2):
        alias = gs.pa.room_set_alias[ii * 2 + 0].strip()
        room_id = gs.pa.room_set_alias[ii * 2 + 1]
        room_id = await map_roominfo_to_roomid(client, room_id)
        gs.log.debug(f"Adding alias '{alias}' to room '{room_id}'.")
        if not is_room_alias(alias) and not is_short_room_alias(alias):
            # not an exhaustive check
            gs.log.error(
                "E199: "
                f"Invalid alias '{alias}'. This is neither a full room alias "
                "nor a short room alias. It should either be "
                "'#SomeRoomAlias:matrix.example.com' or "
                "'#SomeRoomAlias' or 'SomeRoomAlias'."
            )
            gs.err_count += 1
            continue
        if ":" not in alias:
            # Do NOT use short_room_alias_to_room_alias().
            # We want this to be based on provided room_id not the default
            # homeserver!
            if alias[0] != "#":
                alias = "#" + alias
            alias = alias + ":" + room_id.split(":")[1]
        resp = await client.room_put_alias(alias, room_id)
        if isinstance(resp, RoomPutAliasResponse):
            gs.log.debug(
                "room_put_alias successful. Response is: "
                f"{privacy_filter(str(resp))}"
            )
            gs.log.info(
                f"Successfully added alias '{alias}' to room '{room_id}'."
            )
        else:
            gs.log.error(
                "E200: "
                f"Failed to add alias '{alias}' to room '{room_id}': "
                f"{privacy_filter(str(resp))}"
            )
            gs.err_count += 1


async def action_room_resolve_alias(
    client: AsyncClient, credentials: dict
) -> None:
    """Resolve room alias(es) while already logged in."""
    for alias in gs.pa.room_resolve_alias:
        alias = alias.strip()
        gs.log.debug(f"Resolving room alias '{alias}'.")
        if not is_room_alias(alias) and not is_short_room_alias(alias):
            # not an exhaustive check
            gs.log.error(
                "E201: "
                f"Invalid alias '{alias}'. This is neither a full room alias "
                "nor a short room alias. It should either be "
                "'#SomeRoomAlias:matrix.example.com' or "
                "'#SomeRoomAlias' or 'SomeRoomAlias'."
            )
            gs.err_count += 1
            continue
        if ":" not in alias:  # short alias, without homeserver
            alias = short_room_alias_to_room_alias(alias, credentials)
        resp = await client.room_resolve_alias(alias)
        if isinstance(resp, RoomResolveAliasResponse):
            gs.log.debug(
                "room_resolve_alias successful. Response is: "
                f"{privacy_filter(str(resp))}"
            )
            gs.log.info(
                f"Successfully resolved room alias '{alias}' to "
                f"{resp.room_id}."
            )
            # output format controlled via --output flag
            text = (
                f"{resp.room_alias}{SEP}{resp.room_id}{SEP}" f"{resp.servers}"
            )
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            # json_max.update({"key": value})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )
        else:
            gs.log.error(
                "E202: "
                f"Failed to resolve room alias '{alias}': "
                f"{privacy_filter(str(resp))}"
            )
            gs.err_count += 1
            # output format controlled via --output flag
            # for JSON the user can determine which one from the list
            # was successful and which one failed. For 4 inputs there
            # might only be 3 output JSON objects if there was 1 error.
            # In text mode we print this error line, so that for 4 inputs
            # there will be 4 output lines.
            print_output(
                gs.pa.output,
                text=(f"{alias}{SEP}Error{SEP}[]"),
                json_=None,
                json_max=None,
                json_spec=None,
            )


async def action_room_delete_alias(
    client: AsyncClient, credentials: dict
) -> None:
    """Delete room alias(es) while already logged in."""
    for alias in gs.pa.room_delete_alias:
        alias = alias.strip()
        gs.log.debug(f"Deleting room alias '{alias}'.")
        if not is_room_alias(alias) and not is_short_room_alias(alias):
            # not an exhaustive check
            gs.log.error(
                "E203: "
                f"Invalid alias '{alias}'. This is neither a full room alias "
                "nor a short room alias. It should either be "
                "'#SomeRoomAlias:matrix.example.com' or 'SomeRoomAlias'."
            )
            gs.err_count += 1
            continue
        if ":" not in alias:  # short alias, without homeserver
            alias = short_room_alias_to_room_alias(alias, credentials)
        resp = await client.room_delete_alias(alias)
        if isinstance(resp, RoomDeleteAliasResponse):
            gs.log.debug(
                "room_delete_alias successful. Response is: "
                f"{privacy_filter(str(resp))}"
            )
            gs.log.info(f"Successfully deleted room alias '{alias}'.")
        else:
            gs.log.error(
                "E204: "
                f"Failed to delete room alias '{alias}': "
                f"{privacy_filter(str(resp))}"
            )
            gs.err_count += 1


async def action_get_openid_token(
    client: AsyncClient, credentials: dict
) -> None:
    """Get OpenId token(s) for itself or users while already logged in."""
    if not HAVE_OPENID:
        nio_version = pkg_resources.get_distribution("matrix-nio").version
        gs.log.error(
            "E205: "
            f"You are running matrix-nio version {nio_version}. "
            f"This feature is only available on versions larger than 0.19.0. "
            "Update if necessary. "
            "Wait for version 0.19.1 or 0.20 to be released. "
            "Or use unreleased code from master branch on Github."
        )
        gs.err_count += 1
        return
    if gs.pa.get_openid_token == []:
        gs.pa.get_openid_token.append(credentials["user_id"])  # whoami
    gs.log.debug(f"Getting OpenIDs for these users: {gs.pa.get_openid_token}")
    for user_id in gs.pa.get_openid_token:
        user_id = user_id.strip()
        resp = await client.get_openid_token(user_id)
        if isinstance(resp, GetOpenIDTokenError):
            gs.log.error(
                "E206: "
                f"Failed to get OpenId for user {user_id}. Response: "
                f"{privacy_filter(str(resp))}"
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                "get_openid_token successful. Response is: "
                f"{privacy_filter(str(resp))}"
            )
            gs.log.info(
                f"Successfully obtained OpenId token "
                f"{resp.access_token} for user {user_id}."
            )
            # output format controlled via --output flag
            text = (
                f"{user_id}{SEP}{resp.access_token}{SEP}{resp.expires_in}"
                f"{SEP}{resp.matrix_server_name}{SEP}{resp.token_type}"
            )
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            json_max.update({"user_id": user_id})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )


async def action_room_get_visibility(
    client: AsyncClient, credentials: dict
) -> None:
    """Get visibility of room(s) while already logged in."""
    if gs.pa.room_get_visibility == []:
        gs.pa.room_get_visibility.append(credentials["room_id"])  # def. room
    for room_id in gs.pa.room_get_visibility:
        room_id = await map_roominfo_to_roomid(client, room_id)
        gs.log.debug(f"Getting visibility for room {room_id}.")
        resp = await client.room_get_visibility(room_id)
        if isinstance(resp, RoomGetVisibilityResponse):
            gs.log.info(
                f"Successfully got visibility for room {resp.room_id}: "
                f"{resp.visibility}."
            )
            # output format controlled via --output flag
            text = f"{resp.visibility}{SEP}{room_id}"
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            # json_max.update({"key": value})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )
        else:
            gs.log.error(
                "E207: "
                f"Failed getting visibility for room {room_id}. "
                f"{privacy_filter(str(resp))}"
            )
            gs.err_count += 1
            errmsg = "Error: " + str(resp.status_code) + " " + resp.message
            # output format controlled via --output flag
            # for JSON the user can determine which one from the list
            # was successful and which one failed. For 4 inputs there
            # might only be 3 output JSON objects if there was 1 error.
            # In text mode we print this error line, so that for 4 inputs
            # there will be 4 output lines.
            print_output(
                gs.pa.output,
                text=(f"{errmsg}{SEP}{room_id}"),
                json_=None,
                json_max=None,
                json_spec=None,
            )


async def action_room_get_state(
    client: AsyncClient, credentials: dict
) -> None:
    """Get state of room(s) while already logged in."""
    if gs.pa.room_get_state == []:
        gs.pa.room_get_state.append(credentials["room_id"])  # default room
    for room_id in gs.pa.room_get_state:
        room_id = await map_roominfo_to_roomid(client, room_id)
        gs.log.debug(f"Getting visibility for room {room_id}.")
        resp = await client.room_get_state(room_id)
        if isinstance(resp, RoomGetStateResponse):
            gs.log.info(
                f"Successfully got state for room {resp.room_id}: "
                f"{resp.events}."
            )
            # output format controlled via --output flag
            text = f"{resp.events}{SEP}{room_id}"
            # Object of type xxxResponse is not JSON
            # serializable, hence we use the dictionary.
            json_max = resp.__dict__
            # json_max.update({"key": value})  # add dict items
            json_ = json_max.copy()
            json_.pop("transport_response")
            json_spec = None
            print_output(
                gs.pa.output,
                text=text,
                json_=json_,
                json_max=json_max,
                json_spec=json_spec,
            )
        else:
            gs.log.error(
                "E208: "
                f"Failed getting state for room {room_id}. "
                f"{privacy_filter(str(resp))}"
            )
            gs.err_count += 1
            errmsg = "Error: " + str(resp.status_code) + " " + resp.message
            # output format controlled via --output flag
            # for JSON the user can determine which one from the list
            # was successful and which one failed. For 4 inputs there
            # might only be 3 output JSON objects if there was 1 error.
            # In text mode we print this error line, so that for 4 inputs
            # there will be 4 output lines.
            print_output(
                gs.pa.output,
                text=(f"{errmsg}{SEP}{room_id}"),
                json_=None,
                json_max=None,
                json_spec=None,
            )


async def action_delete_device(client: AsyncClient, credentials: dict) -> None:
    """Delete device(s) for itself or other user while already logged in.

    For documentation read:
    https://matrix-nio.readthedocs.io/en/latest/nio.html#asyncclient
    https://matrix.org/docs/spec/client_server/r0.6.0#authentication-types

    There are several ways to authenticate, some of these ways may or may not
    be supported by the server. So, this is server specific.
    The "m.login.token" option seems useful at first glance, but note that
    this is NOT an access token, but a login token received from somewhere
    else. So, in reality the "m.login.token" option is not useful.
    {
      "type": "m.login.token",
      "token": "<token>",  <== this is a login token, NOT an access token!
      "txn_id": "<client generated nonce>",
      "session": "<session ID>"
    }

    The "m.login.sso" option would be useful, but I haven't implemented it
    yet. It would be a bit similar as to the code in action_login().

    The most common option is "m.login.password". This option is implemented.
    """
    if not gs.pa.password:
        gs.log.error(
            "E209: "
            f"Failed to delete devices because --password was not set. "
            f"({gs.pa.password})"
        )
        gs.err_count += 1
        return
    else:
        password = gs.pa.password
    if not gs.pa.user:
        # get presence name of myself
        user_id = credentials["user_id"]
    else:
        user_id = gs.pa.user[0]
        if len(gs.pa.user) > 1:
            gs.log.warning(
                "W109: "
                "Warning. "
                "--user specifies more then one user. If --user is used at "
                "all, then exactly one user should be given."
            )
            gs.warn_count += 1
    devices = gs.pa.delete_device
    # this automatically escapes the " letters in the password,
    # and takes care of spaces, etc.
    auth = {
        "type": "m.login.password",
        "identifier": {"type": "m.id.user", "user": user_id},
        "password": password,
    }
    passwordfake = "***"
    authfake = {
        "type": "m.login.password",
        "identifier": {"type": "m.id.user", "user": user_id},
        "password": passwordfake,
    }
    gs.log.debug(
        f"About to delete devices {devices} for user {user_id} "
        f"with password {passwordfake} and auth {authfake}."
    )
    resp = await client.delete_devices(devices, auth)
    if isinstance(resp, DeleteDevicesError):
        gs.log.error(
            "E210: "
            f"Failed to delete devices {devices} for user {user_id} "
            f"with password {passwordfake} and auth {authfake}. "
            f"Response: {privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    elif isinstance(resp, DeleteDevicesAuthResponse):
        gs.log.error(
            "E211: "
            f"Failed to delete devices {devices} for user {user_id} due to "
            "authentication failure. Are you authorized? "
            f"Authentication: {authfake}, Response: "
            f"{privacy_filter(str(resp))}"
        )
        gs.err_count += 1
    else:
        gs.log.debug(
            "delete_devices successful. Response is: "
            f"{privacy_filter(str(resp))}"
        )
        gs.log.info(
            f"Successfully deleted devices {devices} for user {user_id}."
        )


async def action_room_redact(client: AsyncClient, credentials: dict) -> None:
    """Redact event(s) of room(s) while already logged in."""
    if len(gs.pa.room_redact) == 2:
        gs.pa.room_redact.append("")
    if not len(gs.pa.room_redact) % 3 == 0:
        gs.log.error(
            "E212: "
            "Incorrect number of arguments for --room-redact. Arguments must "
            f"be triples, i.e. multiples of 3, but found "
            f"{len(gs.pa.room_redact)} arguments. 2 is also allowed."
        )
        gs.err_count += 1
        return
    for ii in range(len(gs.pa.room_redact) // 3):
        room_id = gs.pa.room_redact[ii * 3 + 0]
        room_id = await map_roominfo_to_roomid(client, room_id)
        event_id = gs.pa.room_redact[ii * 3 + 1]
        reason = gs.pa.room_redact[ii * 3 + 2].strip()
        if reason == "":
            reason = None
        gs.log.debug(
            f"Preparing to redact event {event_id} in room {room_id} "
            f"providing reason '{reason}'."
        )
        resp = await client.room_redact(room_id, event_id, reason=reason)
        if isinstance(resp, RoomRedactError):
            gs.log.error(
                "E213: "
                f"Failed to redact event {event_id} in room {room_id} "
                f"with reason '{reason}'. "
                f"Response: {privacy_filter(str(resp))}"
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                "room_redact successful. Response is: "
                f"{privacy_filter(str(resp))}"
            )
            gs.log.info(
                f"Successfully redacted event {event_id} in room {room_id} "
                f"providing reason '{'' if reason is None else reason}'."
            )


async def action_whoami(client: AsyncClient, credentials: dict) -> None:
    """Get user id while already logged in."""
    whoami = credentials["user_id"]
    gs.log.debug(f"whoami: user id: {whoami}")
    # output format controlled via --output flag
    text = whoami
    json_max = {"user_id": whoami}
    # json_max.update({"key": value})  # add dict items
    json_ = json_max.copy()
    # json_.pop("key")
    json_spec = None
    print_output(
        gs.pa.output,
        text=text,
        json_=json_,
        json_max=json_max,
        json_spec=json_spec,
    )


async def action_roomsetget() -> None:
    """Perform room, get, set actions while being logged in."""
    if not gs.client and not gs.credentials:
        gs.log.error(
            "E214: " "Client or credentials not set. Skipping action."
        )
        gs.err_count += 1
        return
    try:
        # room_action
        # we already checked args at the beginning, no need to check
        # room and user argument combinations again.
        # room set actions
        if gs.pa.room_create:
            await action_room_create(gs.client, gs.credentials)
        if gs.pa.room_dm_create:
            await action_room_dm_create(gs.client, gs.credentials)
        if gs.pa.room_join:
            await action_room_join(gs.client, gs.credentials)
        if gs.pa.room_leave:
            await action_room_leave(gs.client, gs.credentials)
        if gs.pa.room_forget:
            await action_room_forget(gs.client, gs.credentials)
        if gs.pa.room_invite and gs.pa.user:
            await action_room_invite(gs.client, gs.credentials)
        if gs.pa.room_ban and gs.pa.user:
            await action_room_ban(gs.client, gs.credentials)
        if gs.pa.room_unban and gs.pa.user:
            await action_room_unban(gs.client, gs.credentials)
        if gs.pa.room_kick and gs.pa.user:
            await action_room_kick(gs.client, gs.credentials)
        if gs.pa.room_redact:
            await action_room_redact(gs.client, gs.credentials)
        if gs.pa.room_set_alias:
            await action_room_set_alias(gs.client, gs.credentials)
        if gs.pa.room_delete_alias:
            await action_room_delete_alias(gs.client, gs.credentials)
        # room get actions
        if gs.pa.room_get_visibility is not None:  # empty [] must invoke func
            await action_room_get_visibility(gs.client, gs.credentials)
        if gs.pa.room_get_state is not None:  # empty list must invoke func
            await action_room_get_state(gs.client, gs.credentials)
        if gs.pa.room_resolve_alias:
            await action_room_resolve_alias(gs.client, gs.credentials)
        if gs.room_action:
            gs.log.debug("Room action(s) were performed or attempted.")

        # set_action
        if gs.pa.set_display_name:
            await action_set_display_name(gs.client, gs.credentials)
        if gs.pa.set_device_name:
            await action_set_device_name(gs.client, gs.credentials)
        if gs.pa.set_presence:
            await action_set_presence(gs.client, gs.credentials)
        if gs.pa.upload:
            await action_upload(gs.client, gs.credentials)
        if gs.pa.delete_mxc:
            await action_delete_mxc(gs.client, gs.credentials)
        if gs.pa.delete_mxc_before:
            await action_delete_mxc_before(gs.client, gs.credentials)
        if gs.pa.rest:
            await action_rest(gs.client, gs.credentials)
        if gs.pa.set_avatar:
            await action_set_avatar(gs.client, gs.credentials)
        if gs.pa.import_keys:
            await action_import_keys(gs.client, gs.credentials)
        if gs.pa.delete_device:
            await action_delete_device(gs.client, gs.credentials)

        # get_action
        if gs.pa.get_display_name:
            await action_get_display_name(gs.client, gs.credentials)
        if gs.pa.get_presence:
            await action_get_presence(gs.client, gs.credentials)
        if gs.pa.download:
            await action_download(gs.client, gs.credentials)
        if gs.pa.joined_rooms:
            await action_joined_rooms(gs.client, gs.credentials)
        if gs.pa.joined_members:
            await action_joined_members(gs.client, gs.credentials)
        if gs.pa.mxc_to_http:
            await action_mxc_to_http(gs.client, gs.credentials)
        if gs.pa.devices:
            await action_devices(gs.client, gs.credentials)
        if gs.pa.discovery_info:
            await action_discovery_info(gs.client, gs.credentials)
        if gs.pa.login_info:
            await action_login_info(gs.client, gs.credentials)
        if gs.pa.content_repository_config:
            await action_content_repository_config(gs.client, gs.credentials)
        if gs.pa.get_avatar is not None:  # empty list must invoke function
            await action_get_avatar(gs.client, gs.credentials)
        if gs.pa.get_profile is not None:  # empty list must invoke function
            await action_get_profile(gs.client, gs.credentials)
        if gs.pa.get_room_info is not None:  # empty list must invoke function
            await action_get_room_info(gs.client, gs.credentials)
        if gs.pa.get_client_info:
            await action_get_client_info(gs.client, gs.credentials)
        if gs.pa.has_permission:
            await action_has_permission(gs.client, gs.credentials)
        if gs.pa.export_keys:
            await action_export_keys(gs.client, gs.credentials)
        if gs.pa.get_openid_token is not None:  # empty list must invoke func
            await action_get_openid_token(gs.client, gs.credentials)
        if gs.pa.whoami:
            await action_whoami(gs.client, gs.credentials)
        if gs.setget_action:
            gs.log.debug("Set or get action(s) were performed or attempted.")
    except Exception as e:
        gs.log.error(
            "E215: "
            "Error during room, set, get actions. Continuing despite error. "
            f"Exception: {e}"
        )
        gs.log.debug("Here is the traceback.\n" + traceback.format_exc())
        gs.err_count += 1


async def action_verify() -> None:
    """Verify while already logged in."""
    if not gs.client and not gs.credentials:
        gs.log.error(
            "E216: " "Client or credentials not set. Skipping action."
        )
        gs.err_count += 1
        return
    try:
        # Set up event callbacks
        callbacks = Callbacks(gs.client)
        gs.client.add_to_device_callback(
            callbacks.to_device_callback, (KeyVerificationEvent,)
        )
        # Sync encryption keys with the server
        # Required for participating in encrypted rooms
        if gs.client.should_upload_keys:
            await gs.client.keys_upload()
        print(
            f"{PROG_WITHOUT_EXT} is ready and waiting for the other party to "
            "initiate an emoji verification with us by selecting "
            "'Verify by Emoji' "
            "in their Matrix client. Read --verify instructions in --manual "
            "carefully to assist you in how to do this quickly.",
            file=sys.stdout,
            flush=True,
        )
        # the sync_loop will be terminated by user hitting Control-C
        await gs.client.sync_forever(timeout=30000, full_state=True)
    except KeyboardInterrupt:
        # This will never be caught. I do not know why.
        gs.log.debug("Keyboard interrupt after Emoji verification.")
    except Exception as e:
        gs.log.error(
            "E217: "
            "Error during verify. Continuing despite error. "
            f"Exception: {e}"
        )
        gs.err_count += 1


async def action_send() -> None:
    """Send messages while already logged in."""
    if not gs.client and not gs.credentials:
        gs.log.error(
            "E218: " "Client or credentials not set. Skipping action."
        )
        gs.err_count += 1
        return
    try:
        # a few more steps to prepare for sending messages
        rooms = await determine_rooms(
            gs.credentials["room_id"], gs.client, gs.credentials
        )
        gs.log.debug(f"Rooms are: {rooms}")
        gs.log.debug(f"gs.client.rooms are: {gs.client.rooms}")
        # Sync encryption keys with the server
        # Required for participating in encrypted rooms
        if gs.client.should_upload_keys:
            gs.log.debug("Starting keys_upload")
            await gs.client.keys_upload()
            gs.log.debug("Finished keys_upload")
        if gs.pa.sync == SYNC_OFF:
            gs.log.debug(
                f"Due to '--sync {SYNC_OFF}' option, sync() will be skipped."
            )
            # Prefill rooms as outlined in Issue #91
            # Since sync() is not called we MUST fill in the rooms manually.
            # This line was suggested as workaround:
            # async_client.rooms[room_id] = nio.rooms.MatrixRoom(
            #          room_id=room_id, own_user_id=user_id, encrypted=True)
            # We must also map room aliases to room ids.
            for room_id in rooms:
                room_id = await map_roominfo_to_roomid(gs.client, room_id)
                gs.client.rooms[room_id] = MatrixRoom(
                    room_id=room_id,
                    own_user_id=gs.credentials["user_id"],
                    encrypted=True,
                )
        else:  # SYNC_FULL
            # Default case, standard:
            # One must sync first to get room ids for encrypted rooms
            # since we only send a msg and then stop,
            # we can use sync() instead of sync_forever().
            full_state = True
            gs.log.debug(
                f"Starting sync(full_state={full_state}) "
                "to synchronize events with server."
            )
            await gs.client.sync(timeout=30000, full_state=full_state)
            gs.log.debug("Finished sync() with server.")
        # Now we can send messages as the user
        await process_arguments_and_input(gs.client, rooms)
        # gs.log.debug(f"gs.client.rooms are: {gs.client.rooms}")
        gs.log.debug("Message send action finished.")
    except Exception as e:
        gs.log.error(
            "E219: "
            "Error during sending. Continuing despite error. "
            f"Exception: {e}"
        )
        gs.err_count += 1


async def action_logout() -> None:
    """Log out one or all devices from Matrix server."""
    if not gs.client and not gs.credentials:
        gs.log.error(
            "E220: " "Client or credentials not set. Skipping action."
        )
        gs.err_count += 1
        return
    try:
        device = gs.pa.logout.lower()
        if device == "me":
            gs.log.debug(f"--logout has chosen to log out device {device}")
            all_devices = False
        elif device == "all":
            gs.log.debug(f"--logout has chosen to log out devices {device}")
            all_devices = True
        else:
            gs.log.error(
                "E221: "
                "Error during logout. Only 'me' and 'all' are supported. "
                f"But found --logout '{device}'. Continuing despite error. "
            )
            gs.err_count += 1
            return
        resp = await gs.client.logout(all_devices)
        if isinstance(resp, LogoutError):
            gs.log.error(
                "E222: "
                f"Failed to logout {device}. Response: "
                f"{privacy_filter(str(resp))}"
            )
            gs.err_count += 1
        else:
            gs.log.debug(
                f"logout successful. Response is: {privacy_filter(str(resp))}"
            )
            gs.log.info(f"Successfully logged out {device}.")

    except Exception as e:
        gs.log.error(
            "E223: "
            "Error during logout. Continuing despite error. "
            f"Exception: {e}"
        )
        gs.err_count += 1


async def action_login() -> None:
    """Log in using SSO or password, create credentials file, create store,
    and remain logged in.
    """
    credentials_file = determine_credentials_file()
    if credentials_exist(credentials_file):
        raise MatrixCommanderError(
            "E224: "
            "--login was used but credentials already exist "
            f"in '{credentials_file}'."
        ) from None
    store_dir = determine_store_dir()
    if store_exists(store_dir):
        raise MatrixCommanderError(
            "E225: "
            f"--login was used but store already exists in '{store_dir}'."
        ) from None
    method = gs.pa.login.lower()
    interactive = False
    if method == "password":
        gs.log.debug("--login has chosen password method for authentication")
    elif method == "sso":
        gs.log.debug("--login has chosen SSO method for authentication")
    else:
        raise MatrixCommanderError(
            "E226: "
            "--login specifies invalid authenticatin method "
            f"'{method}'. Only 'password' and 'sso' allowed."
        ) from None
    if gs.pa.homeserver:
        homeserver = gs.pa.homeserver
    else:
        interactive = True
        homeserver = "https://matrix.example.org"
        homeserver = input(f"Enter URL of your homeserver: [{homeserver}] ")
        if not homeserver:
            homeserver = "https://matrix.org"  # better error msg later
    if not (
        homeserver.startswith("https://") or homeserver.startswith("http://")
    ):
        homeserver = "https://" + homeserver
    homeserver_short = urlparse(homeserver).hostname  # matrix.example.org

    # For SSO login, user_id is not needed. But matrix-commander needs
    # user_id for credentials for arguments like --whoami.
    # For SSO, we get the user_id from login() API call, i.e. from server.
    if gs.pa.user_login:
        user_id = gs.pa.user_login
    else:
        user_id = None
    if method == "password" and not user_id:
        interactive = True
        user_id = "@john:example.org"
        user_id2 = "@john:" + homeserver_short
        user_id = input(
            f"Enter your user ID:  [{user_id}]  or  [john] for {user_id2} : "
        ).strip()
    if method == "password":
        if gs.pa.password:
            password = gs.pa.password
        else:
            interactive = True
            print("Please provide your Matrix account password.")
            password = getpass.getpass()
    elif method == "sso":
        password = None
    if gs.pa.device is not None:  # something was specified
        device_name = gs.pa.device.strip()
        if device_name == "":
            device_name = PROG_WITHOUT_EXT  # default
    else:
        interactive = True
        device_name = PROG_WITHOUT_EXT
        device_name = input(
            f"Choose a name for this device: [{device_name}] "
        ).strip()
        if device_name == "":
            device_name = PROG_WITHOUT_EXT  # default
    if gs.pa.room_default is not None:  # something was specified
        room_id = gs.pa.room_default.strip()
        room_id = room_id.replace(r"\!", "!")  # remove possible escape
    else:
        interactive = True
        room_id = "!SomeRoomIdString:example.org"
        room_id2 = "#alias:" + homeserver_short
        room_id = input(
            f"Enter room ID for default room:  [{room_id}]  "
            f"or  [alias] for {room_id2} : "
        ).strip()
    if user_id is not None:
        if is_partial_user_id(user_id):
            user_id = user_id + ":" + homeserver_short  # dont use fn
        if is_short_user_id(user_id):
            user_id = "@" + user_id + ":" + homeserver_short  # dont use fn
        if not is_user_id(user_id):
            raise MatrixCommanderError(
                "E227: "
                f"User id '{user_id}' for --login is invalid. "
                "Specify correct user id."
            ) from None
    if is_short_room_alias(room_id):
        if room_id[0] != "#":
            room_id = "#" + room_id
        room_id = room_id + ":" + homeserver_short  # dont use fn
    if not is_room(room_id):
        raise MatrixCommanderError(
            "E228: "
            f"Room id '{room_id}' for --login is invalid. "
            "Specify correct room id."
        ) from None

    gs.log.info(f"The provided login data is: homeserver='{homeserver}'")
    gs.log.info(f"                            user id='{user_id}'")
    # gs.log.info(f"                            password='{password}'")
    gs.log.info(f"                            device name='{device_name}'")
    gs.log.info(f"                            room id='{room_id}'")
    if interactive:
        print(f"The provided login data is: homeserver='{homeserver}'")
        print(f"                            user id='{user_id}'")
        # print(f"                            password='{password}'")
        print("                            password='***'")
        print(f"                            device name='{device_name}'")
        print(
            f"                            room id='{room_id}'",
            flush=True,
        )
        confirm = input("Correct? (Yes or Ctrl-C to abort) ")
        if confirm.lower() != "yes" and confirm.lower() != "y":
            print(
                "",
                flush=True,
            )  # add newline to stdout to separate any log info
            gs.log.info("Aborting due to user request.")
            return

    # all the input required for login is collected,
    # later we get user_id for SSO (returned at login API call)

    if gs.pa.proxy:
        gs.log.info(f"Proxy {gs.pa.proxy} will be used.")

    # check for password/SSO
    connector = TCPConnector(ssl=gs.ssl)  # setting sslcontext
    async with ClientSession(connector=connector) as session:  # aiohttp
        async with session.get(
            f"{homeserver}/_matrix/client/r0/login",
            raise_for_status=True,
            proxy=gs.pa.proxy,
        ) as response:
            flow_types = {
                x["type"] for x in (await response.json()).get("flows", [])
            }
            gs.log.debug("Supported login flows: %r", flow_types)

            # token_available = "m.login.token" in flow_types
            # m.login.token does not refer to std access-token login
            password_available = "m.login.password" in flow_types
            sso_available = (
                "m.login.sso" in flow_types and "m.login.token" in flow_types
            )

    if method == "sso" and not sso_available:
        raise MatrixCommanderError(
            "E229: "
            "Method 'sso' was selected for --login but Matrix server does "
            "not support Single Sign-On. Try --login with method 'password'."
        ) from None
    if method == "password" and not password_available:
        raise MatrixCommanderError(
            "E230: "
            "Method 'password' was selected for --login but Matrix server "
            "does not support password login. Try --login with method 'sso'."
        ) from None

    # SSO: Single Sign-On:
    # see https://matrix.org/docs/guides/sso-for-client-developers
    if sso_available:
        gs.log.debug("Server supports SSO for login.")
    else:
        gs.log.debug("Server does not support SSO for login.")

    if method == "sso":
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
            gs.log.info("Launching browser to complete SSO login.")
            if gs.pa.proxy:
                gs.log.warning(
                    "W110: "
                    f"Specified proxy {gs.pa.proxy} cannot "
                    "be configured for browser."
                )
                gs.warn_count += 1

            # launch web-browser
            if sys.platform.startswith("darwin"):
                cmd = [shutil.which("open")]
            elif sys.platform.startswith("win"):
                cmd = ["start"]
            else:
                cmd = [shutil.which("xdg-open")]
                if cmd == [None]:
                    cmd = [shutil.which("x-www-browser")]
            cmd.append(
                f"{homeserver}/_matrix/client/r0/login/sso/redirect"
                "?redirectUrl=http://localhost:38080/"
            )
            try:
                subprocess.check_output(cmd)
            except Exception:
                gs.log.error(
                    "E231: "
                    "Browser could not be launched. "
                    "Hence SSO (Single Sign-On) login could not be "
                    "completed. Sorry. If you think the browser and "
                    "SSO should work then try again. If you do not have "
                    "a browser or don't want SSO or want to login with a "
                    "password instead, then use '--login password' in "
                    "the command line."
                )
                raise

            # wait and shutdown server
            try:
                await asyncio.wait_for(stop_server_evt.wait(), 5 * 60)
            except asyncio.TimeoutError:
                gs.log.error(
                    "E232: "
                    f"The program {PROG_WITH_EXT} failed. "
                    "No response was received from SSO provider. "
                    "There was a timeout. Sorry."
                )
                raise
        finally:
            await runner.cleanup()

    # Configuration options for the AsyncClient
    client_config = AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        store_sync_tokens=True,
        encryption_enabled=True,
    )

    store_create(store_dir)

    # Initialize the matrix client
    client = AsyncClient(
        homeserver,
        "" if not user_id else user_id,
        store_path=store_dir,
        config=client_config,
        ssl=gs.ssl,
        proxy=gs.pa.proxy,
    )
    try:
        if method == "sso":
            resp = await client.login(
                token=login_token, device_name=device_name
            )
        elif method == "password":
            resp = await client.login(password, device_name=device_name)

        # check that we logged in succesfully
        if isinstance(resp, LoginResponse):
            # when writing, always write to primary location (e.g. .)
            write_credentials_to_disk(
                homeserver,
                resp.user_id,
                resp.device_id,  # note this is an id, not a name!
                resp.access_token,
                room_id,
                gs.pa.credentials,
            )
            gs.client = client
            gs.credentials = read_credentials_from_disk(credentials_file)
            txt = (
                "E233: "
                f"Log in using method '{method}' was successful. "
                f"Credentials were stored in file '{gs.pa.credentials}'. "
                f"From now on you can run program '{PROG_WITH_EXT}' "
                "without log in, as an access token is stored in your "
                "credentials file. "
                "If you plan on having many credential files, consider "
                f"moving them to directory '{CREDENTIALS_DIR_LASTRESORT}'."
            )
            gs.log.info(txt)
        else:
            # isinstance(resp, LoginError) == true
            # cleanup
            await client.close()  # not yet in gs.
            store_delete(store_dir)  # empty, just created
            # resp does not contain secrets
            # resp is: message="Invalid username or password", code=M_FORBIDDEN
            txt = (
                "E234: "
                "Log in failed. "
                "Most likely wrong credentials were entered. "
                f"homeserver='{homeserver}'; device name='{device_name}'; "
                f"user='{user_id}'; room_id='{room_id}'. "
                f"Failed to log in: {resp.message}, {str(resp.status_code)}"
            )
            gs.err_count += 1
            raise MatrixCommanderError(txt)
    except Exception as e:
        txt = (
            "E235: "
            "Log in failed. Sorry."
            f"homeserver='{homeserver}'; device name='{device_name}'; "
            f"user='{user_id}'; room_id='{room_id}'. "
            f"Failed to log in: {e}"
        )
        # gs.err_count += 1  # don't increment since not MatrixCommanderError
        raise
    # we are now authenticated, we are now logged in
    # gs now has client and credentials, needed by further actions


async def implicit_login() -> None:
    """Log in using credentials file and remain logged in."""
    client, credentials = await login_using_credentials_file()
    gs.client = client
    gs.credentials = credentials


def rooms_to_long_room_names() -> None:
    """Convert foo to #foo:example.com in gs.pa.room where necessary."""
    if gs.pa.room:
        long_rooms = []
        for room in gs.pa.room:
            if is_short_room_alias(room):
                long_rooms.append(
                    short_room_alias_to_room_alias(room, gs.credentials)
                )
            else:
                long_rooms.append(room)
        gs.pa.room = long_rooms


async def async_main() -> None:
    """Run main functions being inside the event loop."""
    # login explicitly
    # login implicitly
    # verify
    # set, get, room,
    # send
    # listen
    # logout
    # close client
    # sys.argv ordering? # todo
    try:
        if gs.pa.login:
            await action_login()  # explicit login
        else:
            await implicit_login()
        if gs.pa.verify:
            await action_verify()
            gs.log.debug(
                "Keyboard interrupt received after Emoji verification."
            )
        rooms_to_long_room_names()  # complete room names
        if gs.room_action or gs.setget_action:
            await action_roomsetget()
        if gs.send_action:
            await action_send()
        if gs.pa.room_invites and gs.pa.listen not in (FOREVER, ONCE):
            await listen_invites_once(gs.client)
        if gs.listen_action:
            await action_listen()
        if gs.pa.logout:
            await action_logout()
    except Exception:
        raise
    finally:
        if gs.client:
            await gs.client.close()


def check_arg_files_readable() -> None:
    """Check if files from command line are readable."""
    arg_files = gs.pa.image if gs.pa.image else []
    arg_files += gs.pa.audio if gs.pa.audio else []
    arg_files += gs.pa.file if gs.pa.file else []
    arg_files += gs.pa.event if gs.pa.event else []
    r = True
    errtxt = (
        "E236: "
        "These files specified in the command line were not found "
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
            "E237: "
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
                "E238: "
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
                "E239: "
                "Could not create media download directory "
                f"{dl} for you. ({e})",
                dl,
            )
        gs.log.debug(f'Created media download directory "{dl}" for you.')


def check_version() -> None:
    """Check if latest version."""
    pkg = PROG_WITHOUT_EXT
    ver = VERSIONNR  # default, fallback
    try:
        ver = pkg_resources.get_distribution(pkg).version
    except Exception:
        pass  # if installed via git clone, package will not exists

    installed_version = LooseVersion(ver)
    # fetch package metadata from PyPI
    pypi_url = f"https://pypi.org/pypi/{pkg}/json"
    response = urllib.request.urlopen(pypi_url).read().decode()
    latest_version = max(
        LooseVersion(s) for s in json.loads(response)["releases"].keys()
    )
    if installed_version >= latest_version:
        utd = "You are up-to-date!"
    else:
        utd = "Consider updating!"
    version_info = (
        f"package: {pkg}, installed: {installed_version}, "
        f"latest: {latest_version} ==> {utd}"
    )
    gs.log.debug(version_info)
    # output format controlled via --output flag
    text = version_info
    json_max = {
        "package": f"{pkg}",
        "version_installed": f"{installed_version}",
        "version_latest": f"{latest_version}",
        "comment": f"{utd}",
    }
    # json_max.update({"key": value})  # add dict items
    json_ = json_max.copy()
    # json_.pop("key")
    json_spec = None
    print_output(
        gs.pa.output,
        text=text,
        json_=json_,
        json_max=json_max,
        json_spec=json_spec,
    )


def version() -> None:
    """Print version info."""
    nio_version = pkg_resources.get_distribution("matrix-nio").version
    python_version = sys.version
    python_version_nr = (
        str(sys.version_info.major)
        + "."
        + str(sys.version_info.minor)
        + "."
        + str(sys.version_info.micro)
    )
    version_info = (
        "\n"
        f"  _|      _|      _|_|_|    _|       {PROG_WITHOUT_EXT}: "
        f"{VERSIONNR} {VERSION}\n"
        "  _|_|  _|_|    _|            _|     a Matrix CLI client\n"
        "  _|  _|  _|    _|              _|   enjoy and submit PRs\n"
        f"  _|      _|    _|            _|     matrix-nio: {nio_version}\n"
        f"  _|      _|      _|_|_|    _|       Python: {python_version_nr}\n"
        "\n"
    )
    gs.log.debug(version_info)
    # output format controlled via --output flag
    text = version_info
    json_max = {
        f"{PROG_WITHOUT_EXT}": {
            "version": f"{VERSIONNR}",
            "date": f"{VERSION}",
        },
        "matrix-nio": {
            "version": f"{nio_version}",
        },
        "python": {
            "version": f"{python_version_nr}",
            "info": f"{python_version}",
        },
    }
    # json_max.update({"key": value})  # add dict items
    json_ = json_max.copy()
    # json_.pop("key")
    json_spec = None
    print_output(
        gs.pa.output,
        text=text,
        json_=json_,
        json_max=json_max,
        json_spec=json_spec,
    )


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
    for i in range(len(gs.pa.log_level)):
        up = gs.pa.log_level[i].upper()
        gs.pa.log_level[i] = up
        if up not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            # gs.err_count += 1  # wrong
            raise MatrixCommanderError(
                "E241: "
                '--log-level only allows values "DEBUG", "INFO", "WARNING", '
                '"ERROR", or "CRITICAL". --log-level argument incorrect. '
                f"({up})"
            ) from None


# according to pylama: function too complex: C901 # noqa: C901
def initial_check_of_args() -> None:  # noqa: C901
    """Check arguments."""
    # First, the adjustments
    if not gs.pa.encrypted:
        gs.pa.encrypted = True  # force it on
        gs.log.debug(
            "Encryption is always enabled. It cannot be turned off. "
            "Use --tail to disable it for specific use cases."
        )
    if not gs.pa.encrypted:  # just in case we ever go back disabling e2e
        gs.pa.store = None
    if gs.pa.listen:
        gs.pa.listen = gs.pa.listen.lower()
    if gs.pa.listen == NEVER and gs.pa.tail != 0:
        gs.pa.listen = TAIL  # --tail turns on --listen TAIL
        gs.log.debug('--listen set to "tail" because "--tail" is used.')
    if gs.pa.sync is not None:
        gs.pa.sync = gs.pa.sync.lower()
    if gs.pa.output is not None:
        gs.pa.output = gs.pa.output.lower()
    if gs.pa.download_media_name is not None:
        gs.pa.download_media_name = gs.pa.download_media_name.lower()
    if gs.pa.room_invites:
        gs.pa.room_invites = gs.pa.room_invites.lower()

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

    if gs.pa.listen in (FOREVER, ONCE, TAIL, ALL):
        gs.listen_action = True
    else:
        gs.listen_action = False

    if (
        # room set
        gs.pa.room_create
        or gs.pa.room_dm_create
        or gs.pa.room_join
        or gs.pa.room_leave
        or gs.pa.room_forget
        or gs.pa.room_invite
        or gs.pa.room_ban
        or gs.pa.room_unban
        or gs.pa.room_kick
        or gs.pa.room_redact
        or gs.pa.room_set_alias
        or gs.pa.room_delete_alias
        # room get
        or gs.pa.room_get_visibility is not None  # empty list must invoke func
        or gs.pa.room_get_state is not None  # empty list must invoke func
        or gs.pa.room_resolve_alias
    ):
        gs.room_action = True
    else:
        gs.room_action = False

    if (
        gs.pa.set_device_name  # set
        or gs.pa.set_display_name
        or gs.pa.set_presence
        or gs.pa.upload
        or gs.pa.delete_mxc
        or gs.pa.delete_mxc_before
        or gs.pa.rest
        or gs.pa.set_avatar
        or gs.pa.import_keys
        or gs.pa.delete_device
    ):
        gs.set_action = True
    else:
        gs.set_action = False

    if (
        gs.pa.get_display_name  # get
        or gs.pa.get_presence
        or gs.pa.download
        or gs.pa.joined_rooms
        or gs.pa.joined_members
        or gs.pa.mxc_to_http
        or gs.pa.devices
        or gs.pa.discovery_info
        or gs.pa.login_info
        or gs.pa.content_repository_config
        or gs.pa.get_avatar is not None  # empty list must invoke function
        or gs.pa.get_profile is not None  # empty list must invoke function
        or gs.pa.get_room_info is not None  # empty list must invoke function
        or gs.pa.get_client_info
        or gs.pa.has_permission
        or gs.pa.export_keys
        or gs.pa.get_openid_token is not None  # empty list must invoke func
        or gs.pa.whoami
    ):
        gs.get_action = True
    else:
        gs.get_action = False

    if gs.set_action or gs.get_action:
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
            if message == "-" or message == "_":
                STDIN_MESSAGE += 1
                gs.stdin_use = "message"
    STDIN_TOTAL = (
        STDIN_MESSAGE + STDIN_IMAGE + STDIN_AUDIO + STDIN_FILE + STDIN_EVENT
    )

    if gs.pa.download_media_name == "" and gs.pa.download_media:
        gs.pa.download_media_name = MEDIA_NAME_DEFAULT

    # Secondly, the checks
    if gs.pa.config:
        t = (
            "This feature is not implemented yet and will most likely "
            "not be implemented. See Issue #34 on Github."
        )
    elif gs.pa.listen in (FOREVER, ONCE, ALL) and gs.pa.tail != 0:
        t = (
            "Don't use --listen forever, --listen once or --listen all "
            "together with --tail. It's one or the other."
        )
    # this is set by default anyway, just defensive programming
    elif gs.pa.encrypted and gs.pa.store in (None, ""):
        t = (
            "If --encrypted is used --store must be set too. "
            "Specify --store and run program again."
        )
    elif gs.pa.verify and (gs.pa.verify.lower() != EMOJI):
        t = f'For --verify currently only "{EMOJI}" is allowed as keyword.'
    elif gs.pa.version and (
        gs.pa.version.lower() != PRINT and gs.pa.version.lower() != CHECK
    ):
        t = (
            f'For --version currently only "{PRINT}" '
            f'or "{CHECK}" is allowed as keyword.'
        )
    elif gs.pa.room_invites and (
        gs.pa.room_invites != INVITES_LIST
        and gs.pa.room_invites != INVITES_JOIN
        and gs.pa.room_invites != INVITES_LIST_JOIN
    ):
        t = (
            f'For --room-invites currently only "{INVITES_LIST}", '
            f'"{INVITES_JOIN}" or "{INVITES_LIST_JOIN}" are allowed as '
            "keywords."
        )
    # elif gs.pa.room_invites and gs.pa.listen not in (FOREVER, ONCE):
    #     t = (
    #         "For --room-invites to work you must also be listening. "
    #         'Use "--listen once" or "--listen forever".'
    #     )
    # allow verify with everything
    # allow send with everything
    # allow listen with everything
    elif gs.pa.set_device_name and (gs.pa.set_device_name.strip() == ""):
        t = "Don't use an empty name for --set-device-name."
    elif gs.pa.set_display_name and (gs.pa.set_display_name.strip() == ""):
        t = "Don't use an empty name for --set-display-name."
    elif (gs.pa.user) and not (
        gs.send_action
        or gs.room_action
        or gs.pa.get_display_name
        or gs.pa.get_presence
        or gs.pa.delete_device
    ):
        t = (
            "If --user is specified, only a send action, a room action, "
            "--get-display-name, --get-presence, or --delete-device can be "
            "done. Adjust your arguments accordingly."
        )
    elif (gs.pa.sync is not None) and not (gs.send_action):
        t = (
            "Only if a send action is provided it is meaningful to specify "
            "--sync. Remove --sync or add a send action. "
            "Adjust your arguments accordingly."
        )
    elif (gs.pa.sync is not None) and gs.pa.sync not in (SYNC_FULL, SYNC_OFF):
        t = (
            "Incorrect value given for --sync. "
            f"Only '{SYNC_FULL}' and '{SYNC_OFF}' are allowed."
        )
    elif gs.pa.output not in (
        OUTPUT_TEXT,
        OUTPUT_JSON,
        OUTPUT_JSON_SPEC,
        OUTPUT_JSON_MAX,
    ):
        t = (
            "Incorrect value given for --output. "
            f"Only '{OUTPUT_TEXT}', '{OUTPUT_JSON}', "
            f"'{OUTPUT_JSON_SPEC}' and '{OUTPUT_JSON_MAX}' are allowed."
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
    elif gs.pa.listen in (ONCE, FOREVER) and gs.pa.room:
        t = (
            "If --listen once or --listen forever are specified, "
            "--room must not be specified because "
            "these options listen in ALL rooms."
        )
    elif gs.pa.listen not in (NEVER, FOREVER, ONCE, TAIL, ALL):
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
    elif gs.pa.download_media_name != "" and (not gs.pa.download_media):
        t = (
            "If --download-media is not used, "
            "then --download-media-name must not be used "
            "either. Specify --download-media "
            f"and run program again. ({gs.pa.download_media_name})"
        )
    elif gs.pa.download_media and gs.pa.download_media_name not in (
        MEDIA_NAME_SOURCE,
        MEDIA_NAME_CLEAN,
        MEDIA_NAME_EVENTID,
        MEDIA_NAME_TIME,
    ):
        t = (
            "Incorrect value given for --download-media-name. "
            f"Only '{MEDIA_NAME_SOURCE}', '{MEDIA_NAME_CLEAN}', "
            f"'{MEDIA_NAME_EVENTID}', '{MEDIA_NAME_TIME}' are allowed."
        )
    elif gs.pa.listen == TAIL and (gs.pa.tail <= 0):
        t = (
            "An integer 1 or larger must be specified with --tail "
            f"({gs.pa.tail})."
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
        if gs.pa.sync is None:
            gs.pa.sync = SYNC_DEFAULT
        gs.log.debug(f"Option --sync is set to {gs.pa.sync}.")
        gs.log.debug("All arguments are valid. All checks passed.")
        return  # all OK
    # gs.err_count += 1 # do not increment for MatrixCommanderError
    raise MatrixCommanderError("E240: " + t) from None


class colors:
    """Colors class.

    reset all colors with colors.reset.
    2 sub classes: fg for foreground and bg for background;
    use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    also, the generic bold, disable, underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold

    use like this:
    print(colors.bg.green, "SKk", colors.fg.red, "Amartya")
    print(colors.bg.lightgrey, "SKk", colors.fg.red, "Amartya")
    """

    reset = "\033[0m"
    bold = "\033[01m"
    disable = "\033[02m"
    inverse = "\033[03m"
    underline = "\033[04m"
    blink = "\033[05m"
    blink2 = "\033[06m"
    reverse = "\033[07m"
    invisible = "\033[08m"
    strikethrough = "\033[09m"

    class fg:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    class bg:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        orange = "\033[43m"
        blue = "\033[44m"
        purple = "\033[45m"
        cyan = "\033[46m"
        lightgrey = "\033[47m"


# according to linter: function is too complex, C901
def main_inner(
    argv: Union[None, list] = None
) -> None:  # noqa: C901 # ignore mccabe if-too-complex
    """Run the program.

    Function signature identical to main().
    Please see main().

    Returns None. Returns nothing.

    Raises exception if an error is detected. Many exceptions are
        possible. One of them is: MatrixCommanderError.
        Sets global state to communicate errors.

    """
    if argv:
        sys.argv = argv
    # prepare the global state
    global gs
    gs = GlobalState()
    global SEP
    # Construct the argument parser
    ap = argparse.ArgumentParser(
        add_help=False,
        description=(f"Welcome to {PROG_WITHOUT_EXT}, a Matrix CLI client. "),
        epilog="You are running "
        f"version {VERSIONNR} {VERSION}. Enjoy, star on Github and "
        "contribute by submitting a Pull Request. "
        f"Also have a look at {PROG_WITHOUT_EXT}-tui. ",
    )
    # -h, see add_help=False
    ap.add_argument(
        # see script create help.help.txt
        # help string up to but excluding "Details::" is used for
        # (short) `--help`. The full text will be used for long `--manual`.
        "--usage",
        required=False,
        action="store_true",
        help="Print usage. "
        "Details:: See also --help for printing a bit more and --manual "
        "for printing a lot more detailed information.",
    )
    # -h, see add_help=False
    ap.add_argument(
        "-h",
        "--help",
        required=False,
        action="store_true",
        help="Print help. "
        "Details:: See also --usage for printing even less information, "
        "and --manual for printing more detailed information.",
    )
    # see -h, see add_help=False
    ap.add_argument(
        "--manual",
        required=False,
        action="store_true",
        help="Print manual. "
        "Details:: See also --usage for printing the absolute minimum, "
        "and --help for printing less.",
    )
    # see -h, see add_help=False
    ap.add_argument(
        "--readme",
        required=False,
        action="store_true",
        help="Print README.md file. "
        "Details:: Tries to print the local README.md file from installation. "
        "If not found it will get the README.md file from github.com and "
        "print it. See also --usage, --help, and --manual.",
    )
    # Add the arguments to the parser
    ap.add_argument(
        "-d",
        "--debug",
        action="count",
        default=0,
        help="Print debug information. "
        "Details:: If used once, only the log level of "
        f"{PROG_WITHOUT_EXT} is set to DEBUG. "
        'If used twice ("-d -d" or "-dd") then '
        f"log levels of both {PROG_WITHOUT_EXT} and underlying modules are "
        'set to DEBUG. "-d" is a shortcut for "--log-level DEBUG". '
        'See also --log-level. "-d" takes precedence over "--log-level". '
        'Additionally, have a look also at the option "--verbose". ',
    )
    ap.add_argument(
        "--log-level",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar=("DEBUG|INFO|WARNING|ERROR|CRITICAL"),
        help="Set the log level(s). "
        "Details:: Possible values are "
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
        "--verbose",
        action="count",
        default=0,
        help="Set the verbosity level. "
        "Details:: If not used, then verbosity will be "
        "set to low. If used once, verbosity will be high. "
        "If used more than once, verbosity will be very high. "
        "Verbosity only affects the debug information. "
        "So, if '--debug' is not used then '--verbose' will be ignored.",
    )
    ap.add_argument(
        "--login",
        required=False,
        type=str,  # login method: password, sso, (access-token)
        metavar="PASSWORD|SSO",
        help="Login to and authenticate with the Matrix homeserver. "
        "Details:: This requires exactly one argument, the login method. "
        "Currently two choices are offered: 'password' and 'sso'. "
        "Provide one of these methods. "
        "If you have chosen 'password', "
        "you will authenticate through your account password. You can "
        "optionally provide these additional arguments: "
        "--homeserver to specify the Matrix homeserver, "
        "--user-login to specify the log in user id, "
        "--password to specify the password, "
        "--device to specify a device name, "
        "--room-default to specify a default room for sending/listening. "
        "If you have chosen 'sso', "
        "you will authenticate through Single Sign-On. A web-browser will "
        "be started and you authenticate on the webpage. You can "
        "optionally provide these additional arguments: "
        "--homeserver to specify the Matrix homeserver, "
        "--user-login to specify the log in user id, "
        "--device to specify a device name, "
        "--room-default to specify a default room for sending/listening. "
        "See all the extra arguments for further explanations. ----- "
        "SSO (Single Sign-On) starts a web "
        "browser and connects the user to a web page on the "
        "server for login. SSO will only work if the server "
        "supports it and if there is access to a browser. So, don't use SSO "
        "on headless homeservers where there is no "
        "browser installed or accessible.",
    )
    ap.add_argument(
        # "-v", ## incompatible change, -v moved to --version
        "--verify",
        required=False,
        type=str,
        default=VERIFY_UNUSED_DEFAULT,  # when -t is not used
        nargs="?",  # makes the word optional
        # when -v is used, but text is not added
        const=VERIFY_USED_DEFAULT,
        metavar="EMOJI",
        help="Perform verification. "
        "Details:: By default, no "
        "verification is performed. "
        f'Possible values are: "{EMOJI}". '
        "If verification is desired, run this program in the "
        "foreground (not as a service) and without a pipe. "
        "While verification is optional it is highly recommended, and it "
        "is recommended to be done right after (or together with) the "
        "--login action. Verification is always interactive, i.e. it "
        "required keyboard input. "
        "Verification questions "
        "will be printed on stdout and the user has to respond "
        "via the keyboard to accept or reject verification. "
        "Once verification is complete, the program may be "
        "run as a service. Verification is best done as follows: "
        "Perform a cross-device verification, that means, perform a "
        "verification between two devices of the *same* user. For that, "
        "open (e.g.) Element in a browser, make sure Element is using the "
        f"same user account as the {PROG_WITHOUT_EXT} user (specified with "
        "--user-login at --login). Now in the Element webpage go to the room "
        f"that is the {PROG_WITHOUT_EXT} default room (specified with "
        "--room-default at --login). OK, in the web-browser you are now the "
        f"same user and in the same room as {PROG_WITHOUT_EXT}. "
        "Now click the round 'i' 'Room Info' icon, then click 'People', "
        f"click the appropriate user (the {PROG_WITHOUT_EXT} user), "
        "click red 'Not Trusted' text "
        "which indicated an untrusted device, then click the square "
        "'Interactively verify by Emoji' button (one of 3 button choices). "
        f"At this point both web-page and {PROG_WITHOUT_EXT} in terminal "
        "show a set of emoji icons and names. Compare them visually. "
        "Confirm on both sides (Yes, They Match, Got it), finally click OK. "
        "You should see a green shield and also see that the "
        f"{PROG_WITHOUT_EXT} device is now green and verified in the webpage. "
        "In the terminal you should see a text message indicating success. "
        "You should now be verified across all devices and across all users.",
    )
    ap.add_argument(
        "--logout",
        required=False,
        type=str,  # logout options: me and all
        metavar="ME|ALL",
        help="Logout. "
        "Details:: Logout this or all devices from the Matrix homeserver. "
        "This requires exactly one argument. "
        "Two choices are offered: 'me' and 'all'. "
        "Provide one of these choices. "
        f"If you choose 'me', only the one device {PROG_WITHOUT_EXT} "
        "is currently using will be logged out. "
        "If you choose 'all', all devices of the user used by "
        f"{PROG_WITHOUT_EXT} will be logged out. "
        "While --logout neither removes the credentials nor the store, the "
        "logout action removes the device and makes the access-token stored "
        "in the credentials invalid. Hence, after a --logout, one must "
        "manually remove credentials and store, and then perform a new "
        f"--login to use {PROG_WITHOUT_EXT} again. "
        "You can perfectly use "
        f"{PROG_WITHOUT_EXT} without ever logging out. --logout is a cleanup "
        "if you have decided not to use this (or all) device(s) ever again.",
    )
    ap.add_argument(
        "-c",
        "--credentials",
        required=False,
        type=str,
        default=CREDENTIALS_FILE_DEFAULT,
        metavar="CREDENTIALS_FILE",
        help="Specify location of credentials file. "
        "Details:: On first run, information about homeserver, "
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
        "-s",
        "--store",
        required=False,
        type=str,
        default=STORE_DIR_DEFAULT,
        metavar="STORE_DIRECTORY",
        help="Specify location of store directory. "
        "Details:: Path to directory to be "
        'used as "store" for encrypted messaging. '
        "By default, this directory "
        f'is "{STORE_DIR_DEFAULT}". '
        "Since encryption is always enabled, a store is "
        "always needed. "
        "The provided directory name "
        "will be used as persistent storage directory instead of "
        "the default one. Preferably, for multiple executions "
        "of this program use the same store for the same device. "
        "The store directory can be shared between multiple "
        "different devices and users.",
    )
    ap.add_argument(
        "-r",
        "--room",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM",
        help="Specify one or multiple rooms. "
        "Details:: Optionally specify one or multiple rooms via room ids or "
        "room aliases. --room is used by various send actions and "
        "various listen actions. "
        "The default room is provided "
        "in the credentials file (specified at --login with --room-default). "
        "If a room (or multiple ones) "
        "is (or are) provided in the --room arguments, then it "
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
        "and similar. Most actions also support room aliases instead of "
        "room ids. Some even short room aliases.",
    )
    ap.add_argument(
        "--room-default",
        required=False,
        type=str,
        metavar="DEFAULT_ROOM",
        help="Specify the default room at --login. "
        "Details:: Optionally specify a room as the "
        "default room for future actions. If not specified for --login, it "
        "will be queried via the keyboard. --login stores the specified room "
        "as default room in your credentials file. This option is only used "
        "in combination with --login. A default room is needed. Specify a "
        "valid room either with --room-default or provide it via keyboard.",
    )
    ap.add_argument(
        "--room-create",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM_ALIAS",
        help="Create one or multiple rooms for given alias(es). "
        "Details:: One or multiple "
        "room aliases can be specified. "
        "For each alias specified a room will be created. "
        "For each created room one line with room id and alias "
        "will be printed to stdout. "
        "If you are not interested in an "
        'alias, provide an empty string like "". '
        "The alias provided must be in canonical local form, i.e. "
        "if you want a final full alias like "
        '"#SomeRoomAlias:matrix.example.com" '
        "you must provide the string 'SomeRoomAlias'. "
        "The user must be permitted to create rooms. "
        "Combine --room-create with --name and --topic to add "
        "names and topics to the room(s) to be created. "
        "Rooms are by default created encrypted; "
        "to overwrite that and to create a room with encryption disabled "
        "use '--plain'. "
        "Room id, room alias, encryption and other fields "
        "are printed as output, one line per created room.",
    )
    ap.add_argument(
        "--room-dm-create",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="USER",
        help="Create one or multiple DM rooms with the specified users. "
        "Details:: For each user specified a DM room will be created and the "
        "user invited to it. For each created room one line with "
        "room id and alias will be printed to stdout. The user "
        "must be permitted to create rooms. Combine --room-dm-create "
        "with --name, --topic, --alias to add names, topics and "
        "aliases to the room(s) to be created. "
        "DM rooms are by default created encrypted; "
        "to overwrite that and to create a room with encryption disabled "
        "use '--plain'. "
        "Room id, room alias, encryption and other fields "
        "are printed as output, one line per created room.",
    )
    ap.add_argument(
        "--room-join",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM",
        help="Join one room or multiple rooms. "
        "Details:: One or multiple "
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
        metavar="ROOM",
        help="Leave one room or multiple rooms. "
        "Details:: One or multiple "
        "room aliases can be specified. The room (or multiple "
        "ones) provided in the arguments will be left. ",
    )
    ap.add_argument(
        "--room-forget",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM",
        help="Forget one room or multiple rooms. "
        "Details:: After leaving a room you should (most likely) forget the "
        "room. Forgetting a room removes the users' room history. "
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
        metavar="ROOM",
        help="Invite one ore more users to join one or more rooms. "
        "Details:: Specify the user(s) as arguments to --user. "
        "Specify the rooms as arguments to this option, i.e. "
        "as arguments to --room-invite. "
        "The user must have permissions to invite users. "
        "Don't confuse this option with --room-invites.",
    )
    ap.add_argument(
        "--room-ban",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM",
        help="Ban one ore more users from one or more rooms. "
        "Details:: Specify the user(s) as arguments to --user. "
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
        metavar="ROOM",
        help="Unban one ore more users from one or more rooms. "
        "Details:: Specify the user(s) as arguments to --user. "
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
        metavar="ROOM",
        help="Kick one ore more users from one or more rooms. "
        "Details:: Specify the user(s) as arguments to --user. "
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
        metavar="USER",
        help="Specify one or multiple users. "
        "Details:: This option is meaningful "
        "in combination with a) room actions like --room-invite, --room-ban, "
        "--room-unban, etc. and b) send actions like -m, -i, -f, etc. "
        "c) some listen actions --listen, as well as d) actions like "
        "--delete-device. "
        "In case of a) this option --user specifies the users "
        "to be used with room commands (like invite, ban, etc.). "
        "In case of b) the option --user can be used as an alternative "
        "to specifying a room as destination for text (-m), images (-i), "
        "etc. For send actions '--user' is providing the functionality of "
        "'DM (direct messaging)'. For c) this option allows an alternative "
        "to specifying a room as destination for some --listen actions. "
        "For d) this gives the option to delete the device of a different "
        "user. "
        f"----- What is a DM? {PROG_WITHOUT_EXT} tries to find a "
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
        "as in '@john:example.org', 2) partial user id as in '@john' when "
        "the user is on the same homeserver (example.org will be "
        "automatically appended), or 3) a display name as in 'john'. "
        "Be careful, when "
        "using display names as they might not be unique, and you could "
        "be sending to the wrong person. To see possible display names use "
        "the --joined-members '*' option which will show you the display "
        "names in the middle column.",
    )
    ap.add_argument(
        "--user-login",
        required=False,
        type=str,
        # @john:example.com and @john and john accepted
        metavar="USER",
        help="Specify user for --login. "
        "Details:: Optional argument to specify the user for --login. "
        "This gives the option to specify the user id for login. "
        "For '--login sso' the --user-login is not needed as user id can be "
        "obtained from server via SSO. For '--login password', if not "
        "provided it will be queried via keyboard. A full user id like "
        "'@john:example.com', a partial user name like '@john', and "
        "a short user name like 'john' can be given. "
        "--user-login is only used by --login and ignored by all other "
        "actions.",
    )
    ap.add_argument(
        "--name",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM_NAME",
        help="Specify one or multiple room names. "
        "Details:: This option is only meaningful "
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
        metavar="ROOM_TOPIC",
        help="Specify one or multiple room topics. "
        "Details:: This option is only meaningful "
        "in combination with option --room-create. "
        "This option --topic specifies the topics "
        "to be used with the command --room-create.",
    )
    ap.add_argument(
        "--alias",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM_ALIAS",
        help="Specify one or multiple room aliases. "
        "Details:: This option is only "
        "meaningful in combination with option --room-dm-create. "
        "This option --alias specifies the aliases to be used "
        "with the command --room-dm-create.",
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
        metavar="TEXT",
        help="Send one or multiple text messages. "
        "Details:: Message data must not be binary data, it "
        "must be text. If no '-m' is used and no other conflicting "
        "arguments are provided, and information is piped into the program, "
        "then the piped data will be used as message. "
        "Finally, if there are no operations at all in the arguments, then "
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
        "With '-' the whole message, all lines, will be considered "
        "a single message and sent as one message. "
        "If your message is literally '-' then use '\\-' "
        "as message in the argument. "
        "'-' may appear in any position, i.e. '-m \"start\" - \"end\"' "
        "will send 3 messages out of which the second one is read from stdin. "
        "'-' may appear only once overall in all arguments. "
        "Similar to '-', another shortcut character is '_'. The "
        "special character '_' is used for streaming data via "
        "a pipe on stdin. With '_' the stdin pipe is read line-by-line "
        "and each line is treated as a separate message and sent right "
        "away. The program waits for pipe input until the pipe is "
        "closed. E.g. Imagine a tool that generates output sporadically "
        f"24x7. It can be piped, i.e. streamed, into {PROG_WITHOUT_EXT}, and "
        f"{PROG_WITHOUT_EXT} stays active, sending all input instantly. "
        "If you want to send the literal letter '_' then escape it "
        "and send '\\_'. "
        "'_' can be used only once. And either '-' or '_' can be used. ",
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
        metavar="IMAGE_FILE",
        help="Send one or multiple image files. "
        "Details:: This option can be used multiple times to send "
        "multiple images. First images are sent, "
        "then text messages are sent. "
        f"If you want to feed an image into {PROG_WITHOUT_EXT} "
        "via a pipe, via stdin, then specify the special "
        "character '-'. If '-' is specified as image file name, "
        "then the program will read the image data from stdin. "
        "If your image file is literally named '-' then use '\\-' "
        "as file name in the argument. "
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
        metavar="AUDIO_FILE",
        help="Send one or multiple audio files. "
        "Details:: This option can be used multiple times to send "
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
        metavar="FILE",
        help="Send one or multiple files (e.g. PDF, DOC, MP4). "
        "Details:: This option can be used multiple times to send "
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
        metavar="MATRIX_JSON_OBJECT",
        help="Send a Matrix JSON event. "
        "Details:: Send an event that is formatted as a JSON object as "
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
        "character '-'. See description of '-i' to see how '-' is handled. "
        "See tests/test-event.sh for examples.",
    )
    # -h already used for --help, -w for "web"
    ap.add_argument(
        "-w",
        "--html",
        required=False,
        action="store_true",
        help='Send message as format "HTML". '
        "Details:: If not specified, message will be sent "
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
        help='Send message as format "MARKDOWN". '
        "Details:: If not specified, message will be sent "
        'as format "TEXT". E.g. that allows sending of text '
        "formatted in MarkDown language.",
    )
    #  -c is already used for --credentials, -k as it sounds like c
    ap.add_argument(
        "-k",
        "--code",
        required=False,
        action="store_true",
        help='Send message as format "CODE". '
        "Details:: If not specified, message will be sent "
        'as format "TEXT". If both --html and --code are '
        "specified then --code takes priority. This is "
        "useful for sending ASCII-art or tabbed output "
        "like tables as a fixed-sized font will be used "
        "for display.",
    )
    #  -j for emoJize
    ap.add_argument(
        "-j",
        "--emojize",
        required=False,
        action="store_true",
        help="Send message after emojizing. "
        "Details:: If not specified, message will be sent "
        'as format "TEXT". If both --code and --emojize are '
        "specified then --code takes priority. This is "
        "useful for sending emojis in shortcode form :collision:.",
    )

    # -s is already used for --store, -i for sPlit
    ap.add_argument(
        "-p",
        "--split",
        required=False,
        type=str,
        metavar="SEPARATOR",
        help="Split message text into multiple Matrix messages. "
        "Details:: If set, split the message(s) into multiple messages "
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
        "--config",
        required=False,
        type=str,
        metavar="CONFIG_FILE",
        help="Specify the location of a config file. "
        "Details:: By default, no "
        "config file is used. "
        "If this option is provided, the provided file name "
        "will be used to read configuration from. Not implemented.",
    )
    # -p is already used for --split
    ap.add_argument(
        "--proxy",
        required=False,
        type=str,
        metavar="PROXY",
        help="Specify a proxy for connectivity. "
        "Details:: By default, "
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
        "Details:: If not specified, message will be sent as text.",
    )
    ap.add_argument(
        # no single char flag
        "--encrypted",
        required=False,
        action="store_true",
        help="Send message end-to-end encrypted. "
        "Details:: Encryption is always turned on and "
        "will always be used where possible. "
        "It cannot be turned off. This flag does nothing "
        "as encryption is turned on with or without this "
        "argument. This flag exists only for historic reasons. "
        "In some specific case encryption "
        "can be disabled, please see --plain.",
    )
    ap.add_argument(
        "-l",
        "--listen",
        required=False,
        type=str,
        default=LISTEN_DEFAULT,  # when -l is not used
        nargs="?",  # makes the word optional
        const=FOREVER,  # when -l is used, but FOREVER is not added
        metavar="NEVER|ONCE|FOREVER|TAIL|ALL",
        help="Print received messages and listen to messages. "
        "Details:: The --listen option takes one argument. There "
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
        "file or the --room options. ",
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
        metavar="NUMBER",
        help="Print last messages. "
        "Details:: The --tail option reads and prints up to the last N "
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
        "Look at --listen as this option is related to --tail.",
    )
    ap.add_argument(
        "-y",
        "--listen-self",
        required=False,
        action="store_true",
        help="Print your own messages as well. "
        "Details:: If set and listening, "
        "then program will listen to and print also "
        "the messages sent by its own user. "
        "By default messages from oneself are not printed.",
    )
    ap.add_argument(
        # no single char flag
        "--print-event-id",
        required=False,
        action="store_true",
        help="Print event ids of received messages. "
        "Details:: If set and listening, "
        f"then '{PROG_WITHOUT_EXT}' will print also the event id for "
        "each received message or other received event. If set and "
        f"sending, then '{PROG_WITHOUT_EXT}' will print the event id "
        "of the sent message or the sent object (audio, file, event) to "
        "stdout. Other information like room id and reference to what was "
        "sent will be printed too. For sending this is useful, "
        "if after sending the user "
        "wishes to perform further operations on the sent object, "
        "e.g. redacting/deleting it after an expiration time, etc.",
    )
    ap.add_argument(
        # starting with version 2.19 "-u" has been moved to --user!
        "--download-media",
        type=str,
        default="",  # if --download-media is not used
        action="store",
        nargs="?",  # makes the word optional
        const=MEDIA_DIR_DEFAULT,  # when option is used, but no dir added
        metavar="DOWNLOAD_DIRECTORY",
        help="Download media files while listening. "
        "Details:: If set and listening, "
        "then program will download "
        "received media files (e.g. image, audio, video, text, PDF files). "
        "By default, media will be downloaded to this directory: "
        f'"{MEDIA_DIR_DEFAULT}". '
        "You can overwrite default with your preferred directory. "
        "If you provide a relative path, the relative path will be relative "
        "to the local directory. foo will become ./foo. "
        "foo/foo will become ./foo/foo and only works if ./foo already "
        "exists. "
        "Absolute paths will remein unchanged. /tmp will remain /tmp. "
        "/tmp/foo will be /tmp/foo. "
        "If media is encrypted it will be decrypted and stored decrypted. "
        "By default media files will not be downloaded.",
    )
    ap.add_argument(
        "--download-media-name",
        required=False,
        default="",  # if --download-media-name is not used
        type=str,  # method to derive filename
        metavar="SOURCE|CLEAN|EVENTID|TIME",
        help="Specify the method to derive the media filename. "
        "Details:: This argument is optional. "
        "Currently four choices are offered: 'source', 'clean', "
        "'eventid', and 'time'. "
        "'source' means the value specified by the source (sender) "
        "will be used. If the sender, i.e. source, specifies a value "
        "that is not a valid filename, then a failure will occur and "
        "the media file will not be saved. "
        "'clean' means that all unusual characters in the name "
        "provided by the source will be replaced "
        "by an underscore to create a valid file name. "
        "'eventid' means that the name provided by the source will be "
        "ignored and the event-id will be used instead. "
        "'time' means that the name provided by the source will be "
        "ignored and the current time at the receiver will be used instead. "
        "As an example, if the source/sender provided 'image(1)!.jpg' as "
        "name for a given media file "
        "then 'source' will store the media using filename 'image(1)!.jpg', "
        "'clean' will store it as 'image_1__.jpg', "
        "'eventid' as something like "
        "'$rsad57dafs57asfag45gsFjdTXW1dsfroBiO2IsidKk', "
        "and 'time' as something like "
        "'20231012_152234_266600' (YYYYMMDD_HHMMSS_MICROSECONDS). "
        f"If not specified this value defaults to '{MEDIA_NAME_DEFAULT}'. ",
    )
    ap.add_argument(
        # "-o", # incompatible change Dec 2022, -o moved to --output
        "--os-notify",
        required=False,
        action="store_true",
        help="Notify me of arriving messages. "
        "Details:: If set and listening, "
        "then program will attempt to visually notify of "
        "arriving messages through the operating system. "
        "By default there is no notification via OS.",
    )
    ap.add_argument(
        # removed "-x", starting v2.21 -x is no longer supported
        "--set-device-name",
        required=False,
        type=str,
        default=SET_DEVICE_NAME_UNUSED_DEFAULT,  # when option isn't used
        metavar="DEVICE_NAME",
        help="Set or rename the current device. "
        "Details:: Set or rename the current device to the "
        "device name provided. "
        "Send, listen and verify operations are allowed when "
        "renaming the device.",
    )
    ap.add_argument(
        "--set-display-name",
        required=False,
        type=str,
        default=SET_DISPLAY_NAME_UNUSED_DEFAULT,  # when option isn't used
        metavar="DISPLAY_NAME",
        help="Set or rename the display name. "
        "Details:: Set or rename the display name "
        "for the current user to the "
        "display name provided. "
        "Send, listen and verify operations are allowed when "
        "setting the display name. "
        "Do not confuse this option with the option '--get-room-info' "
        "which gets the room display name, not the user display name.",
    )
    ap.add_argument(
        "--get-display-name",
        required=False,
        action="store_true",
        help="Get the display name of yourself. "
        "Details:: Get the display name of "
        f"{PROG_WITHOUT_EXT} (itself), "
        "or of one or multiple users. Specify user(s) with the "
        "--user option. If no user is specified get the display name of "
        "itself. "
        "Send, listen and verify operations are allowed when "
        "getting display name(s). "
        "Do not confuse this option with the option '--get-room-info' "
        "which gets the room display name, not the user display name.",
    )
    ap.add_argument(
        "--set-presence",
        required=False,
        type=str,
        # defaults to None if not used, is str if used
        metavar="ONLINE|OFFLINE|UNAVAILABLE",
        help="Set your presence. "
        f"Details:: Set presence of {PROG_WITHOUT_EXT} to the given value. "
        "Must be one of these values: “online”, “offline”, “unavailable”. "
        "Otherwise an error will be produced.",
    )
    ap.add_argument(
        "--get-presence",
        required=False,
        action="store_true",
        # defaults to False if not used
        help="Get your presence. "
        f"Details:: Get presence of {PROG_WITHOUT_EXT} (itself), "
        "or of one or multiple users. Specify user(s) with the "
        "--user option. If no user is specified get the presence of "
        "itself. "
        "Send, listen and verify operations are allowed when "
        "getting presence(s).",
    )
    ap.add_argument(
        "--upload",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="FILE",
        help="Upload one or multiple files to the content repository. "
        "Details:: "
        "The files will be given a Matrix URI and "
        "stored on the server. --upload allows the optional argument "
        "--plain to skip encryption for upload. "
        "See tests/test-upload.sh for an example.",
    )
    ap.add_argument(
        "--download",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="MXC_URI",
        help="Download one or multiple files from the content repository. "
        "Details:: "
        "You must provide one or multiple Matrix URIs (MXCs) which are "
        "strings like "
        "this 'mxc://example.com/SomeStrangeUriKey'. If found they will "
        "be downloaded, decrypted, and stored in local files. "
        "If file names are specified with --file-name the downloads "
        "will be saved with these file names. If --file-name is not "
        "specified the original file name from the upload will be used. "
        "If neither specified nor available on server, then the file "
        f"name of last resort 'mxc-<mxc-id>' will be used. "
        f"If a file name in --file-name contains the placeholder "
        f"{MXC_ID_PLACEHOLDER}, it will be replaced with the mxc-id. "
        "If a file name is specified as empty string in --file-name, then "
        "also the name 'mxc-<mxc-id>' will be used. "
        "By default, the upload was encrypted so a decryption dictionary "
        "must be provided to decrypt the data. Specify one or multiple "
        "decryption keys "
        "with --key-dict. If --key-dict is not set, not decryption is "
        "attempted; and the data might be stored in encrypted fashion, "
        "or might be plain-text if the --upload skipped encryption with "
        "--plain. "
        "See tests/test-upload.sh for an example.",
    )
    ap.add_argument(
        "--delete-mxc",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="MXC_URI",
        help="Delete one or multiple objects from the content repository. "
        "Details:: You must provide one or multiple Matrix URIs (MXC) "
        "which are strings like "
        "this 'mxc://example.com/SomeStrangeUriKey'. Alternatively, you "
        "can just provide the MXC id, i.e. the part after the last slash. "
        "If found they (i.e. the files they represent) will "
        "be deleted from the server database. In order to delete objects "
        "one must have server admin permissions. Having only room admin "
        "permissions is not sufficient and it will fail. "
        "Read "
        "https://matrix-org.github.io/synapse/"
        "latest/usage/administration/admin_api/ "
        "for learning how to set server admin permissions on the "
        "server. Alternatively, and optionally, one can specify "
        "an access token which has server admin permissions with the "
        "--access-token argument. "
        "See tests/test-upload.sh for an example.",
    )
    ap.add_argument(
        "--delete-mxc-before",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="TIMESTAMP",
        help="Delete old objects from the content repository"
        "Details:: Delete files from the content repository "
        "that are older than a given timestamp. "
        "It is the timestamp of last access, not the timestamp when "
        "the file was created. "
        "Additionally you can specify a size in bytes to indicate "
        "that only files older than timestamp and larger than size "
        "will be deleted. "
        "You must provide a timestamp of the following format: "
        "'DD.MM.YYYY HH:MM:SS' like '20.01.2022 19:38:42' for January 20, "
        "2022, 7pm 38min 42sec. "
        "Files that are still used in image data (e.g user profile, "
        "room avatar) will not be deleted from the server database. "
        "In order to delete objects "
        "one must have server admin permissions. Having only room admin "
        "permissions is not sufficient and it will fail. "
        "Read "
        "https://matrix-org.github.io/synapse/"
        "latest/usage/administration/admin_api/ "
        "for learning how to set server admin permissions on the "
        "server. Alternatively, and optionally, one can specify "
        "an access token which has server admin permissions with the "
        "--access-token argument. "
        "See tests/test-upload.sh for an example.",
    )
    ap.add_argument(
        # no single char flag
        "--joined-rooms",
        required=False,
        action="store_true",
        help="Print the list of joined rooms. "
        "Details:: All rooms that you are a "
        "member of will be printed, one room per line.",
    )
    ap.add_argument(
        # no single char flag
        "--joined-members",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM",
        help="Print the list of joined members for one or multiple rooms. "
        "Details:: If you want to print the joined members of all rooms that "
        "you are member of, then use the special character '*'.",
    )
    ap.add_argument(
        "--mxc-to-http",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="MXC_URI",
        help="Convert MXC URIs to HTTP URLs. "
        "Details:: Convert one or more matrix content URIs to the "
        "corresponding HTTP URLs. The MXC URIs "
        "to provide look something like this "
        "'mxc://example.com/SomeStrangeUriKey'. "
        "See tests/test-upload.sh for an example.",
    )
    ap.add_argument(
        # no single char flag
        "--devices",
        "--get-devices",  # alias, cause --deviced is very similar to --device
        required=False,
        action="store_true",
        help="Print the list of devices. "
        "Details:: All device of this "
        "account will be printed, one device per line.",
    )
    ap.add_argument(
        # no single char flag
        "--discovery-info",
        required=False,
        action="store_true",
        help="Print discovery information about current homeserver. "
        "Details:: Note that not all homeservers support discovery and an "
        "error might be reported.",
    )
    ap.add_argument(
        # no single char flag
        "--login-info",
        required=False,
        action="store_true",
        help="Print login methods supported by the homeserver. "
        "Details:: It prints one login method per line.",
    )
    ap.add_argument(
        # no single char flag
        "--content-repository-config",
        required=False,
        action="store_true",
        help="Print the content repository configuration. "
        "Details:: This currently just prints "
        "the upload size limit in bytes.",
    )
    ap.add_argument(
        # no single char flag
        "--rest",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="REST_METHOD DATA URL",
        help="Use the Matrix Client REST API. "
        "Details:: Matrix has several extensive "
        "REST APIs. With the --rest argument you can invoke a Matrix REST "
        "API call. This allows the user to do pretty much anything, at the "
        "price of not being very convenient. The APIs are described in "
        "https://matrix.org/docs/api/, "
        "https://spec.matrix.org/latest/client-server-api/, "
        "https://matrix-org.github.io/synapse/latest/usage/administration/"
        "admin_api/, etc. "
        "Each REST call requires exactly 3 arguments. "
        "So, the total number of arguments used with --rest must be a "
        "multiple of 3. The argument triples are: "
        "(a) the method, a string of GET, POST, PUT, DELETE, or OPTIONS. "
        "(b) a string containing the data (if any) in JSON format. "
        "(c) a string containing the URL. All strings must be UTF-8. "
        "There are a few placeholders. They are: "
        "__homeserver__ (like https://matrix.example.org), "
        "__hostname__ (like matrix.example.org), "
        "__access_token__, __user_id__ (like @mc:matrix.example.com), "
        "__device_id__, and __room_id__. If a placeholder is found it is "
        "replaced with the value from the local credentials file. "
        "An example would be: "
        "--rest 'GET' '' '__homeserver__/_matrix/client/versions'. "
        "If there is no data, i.e. data (b) is empty, then use '' for it. "
        "Optionally, --access-token can be used to overwrite the "
        "access token from credentials (if needed). "
        "See tests/test-rest.sh for an example.",
    )
    ap.add_argument(
        "--set-avatar",
        required=False,
        type=str,
        metavar="AVATAR_MXC_URI",
        # defaults to None if not used, is str if used
        help="Set your avatar. "
        f"Details:: Set the avatar MXC resource used by {PROG_WITHOUT_EXT}. "
        "Provide one MXC URI that looks like this "
        "'mxc://example.com/SomeStrangeUriKey'.",
    )
    ap.add_argument(
        "--get-avatar",
        required=False,
        action="extend",
        nargs="*",  # None if not used, [] is used without extra args
        type=str,
        metavar="USER",
        help="Get an avatar. "
        f"Details:: Get the avatar MXC resource used by {PROG_WITHOUT_EXT}, "
        "or one or multiple other users. Specify zero or more user ids. "
        f"If no user id is specified, the avatar of {PROG_WITHOUT_EXT} will "
        "be fetched. If one or more user ids are given, the avatars of "
        "these users will be fetched. As response both MXC URI as well as URL "
        "will be printed.",
    )
    ap.add_argument(
        "--get-profile",
        required=False,
        action="extend",
        nargs="*",  # None if not used, [] is used without extra args
        type=str,
        metavar="USER",
        help="Get a user profile. "
        f"Details:: Get the user profile used by {PROG_WITHOUT_EXT}, or "
        "one or multiple other users. Specify zero or more user ids. "
        f"If no user id is specified, the user profile of {PROG_WITHOUT_EXT} "
        "will be fetched. If one or more user ids are given, the user "
        "profiles of these users will be fetched. As response "
        "display name and avatar MXC URI as well as possible additional "
        "profile information (if present) "
        "will be printed. One line per user will be printed.",
    )
    ap.add_argument(
        "--get-room-info",
        required=False,
        action="extend",
        nargs="*",  # None if not used, [] is used without extra args
        type=str,
        metavar="ROOM",
        help="Get the room information. "
        "Details:: Get the room information such as room display name, "
        "room alias, room creator, etc. for "
        "one or multiple specified rooms. The included room 'display name' is "
        "also referred to as 'room name' or incorrectly even as room title. "
        "If one or more room are given, the room "
        "informations of these rooms will be fetched. "
        "If no room is specified, the room information for the "
        f"default room configured for {PROG_WITHOUT_EXT} is fetched. "
        "Rooms can be given via "
        "room id (e.g. '\\!SomeRoomId:matrix.example.com'), "
        "canonical (full) room alias "
        "(e.g. '#SomeRoomAlias:matrix.example.com'), "
        "or short alias (e.g. 'SomeRoomAlias' or '#SomeRoomAlias'). "
        "As response "
        "room id, room display name, room canonical alias, room topic, "
        "room creator, and room encryption "
        "are printed. One line per room will be printed. "
        "Since either room id or room alias are accepted as input and both "
        "room id and room alias are given as output, one can hence use this "
        "option to map from room id to room alias "
        "as well as vice versa from room alias to room id. "
        "Do not confuse this option with the options '--get-display-name' "
        "and '--set-display-name', which get/set the user display name, not "
        "the room display name.",
    )
    ap.add_argument(
        "--get-client-info",
        required=False,
        action="store_true",
        help="Print client information. "
        "Details:: Print information kept in the client, i.e. "
        f"{PROG_WITHOUT_EXT}. "
        "Output is printed in JSON format.",
    )
    ap.add_argument(
        "--has-permission",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM BAN|INVITE|KICK|NOTIFICATIONS|REDACT|etc",
        help="Inquire about permissions. "
        f"Details:: Inquire if user used by {PROG_WITHOUT_EXT} has "
        "permission for one or multiple actions in one or multiple rooms. "
        "Each inquiry requires 2 parameters: the room id and the permission "
        "type. One or multiple of these parameter pairs may be specified. "
        "For each parameter pair there will be one line printed to stdout. "
        "Values for the permission type are 'ban', "
        "'invite', 'kick', 'notifications', 'redact', etc. "
        "See https://spec.matrix.org/v1.2/client-server-api/#mroompower_levels"
        ".",
        # 'events', 'events_default', 'state_default': valid permission types?
    )
    ap.add_argument(
        "--import-keys",
        required=False,
        action="extend",
        nargs=2,  # filename for import, passphrase
        type=str,
        metavar="FILE PASSPHRASE",
        help="Import Megolm decryption keys from a file. "
        "Details:: This is an optional argument. If used it must be followed "
        "by two values. (a) a file name from which the keys will be read. "
        "(b) a passphrase with which the file can be decrypted with. "
        "The keys will be added to the current instance as well as "
        "written to the database. See also --export-keys.",
    )
    ap.add_argument(
        "--export-keys",
        required=False,
        action="extend",
        nargs=2,  # filename for export, passphrase
        type=str,
        metavar="FILE PASSPHRASE",
        help="Export all the Megolm decryption keys of this device. "
        "Details:: This is an optional argument. If used it must be followed "
        "by two values. (a) a file name to which the keys will be written to. "
        "(b) a passphrase with which the file will be encrypted with. "
        "Note that this does not save other information such as the private "
        "identity keys of the device.",
    )
    ap.add_argument(
        "--room-set-alias",
        "--room-put-alias",  # name used by nio
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM_ALIAS ROOM",
        help="Add aliases to rooms. "
        "Details:: Add an alias to a room, or aliases to multiple rooms. "
        "Provide pairs of arguments. In each pair, the first argument must be "
        "the alias you want to assign to the room given via room id in the "
        "second argument of the pair. E.g. the 4 arguments 'a1 r1 a2 r2' "
        "would assign the alias 'a1' to room 'r1' and the alias 'a2' to room "
        "'r2'. If you just have one single pair then the second argument is "
        "optional. If just a single value is given (an alias) then this "
        "alias is assigned to the default room of "
        f"{PROG_WITHOUT_EXT} (as found in credentials file). In short, "
        "you can have just a single argument or an even number of arguments "
        "forming pairs. You can have multiple room aliases per room. So, "
        "you may add multiple aliases to the same room. "
        "A room alias looks like this: "
        "'#someRoomAlias:matrix.example.org'. Short aliases like "
        "'someRoomAlias' or '#someRoomAlias' are also accepted. "
        "In case of a short alias, "
        "it will be automatically prefixed with '#' and the "
        "homeserver will be automatically appended. "
        "Adding the same alias "
        "multiple times to the same room results in an error. "
        "--room-put-alias is eqivalent to --room-set-alias.",
    )
    ap.add_argument(
        "--room-resolve-alias",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM_ALIAS",
        help="Show room ids corresponding to room aliases. "
        "Details:: Resolves a room alias to the corresponding room id, "
        "or multiple room aliases to their corresponding room ids. "
        "Provide one or multiple room aliases. "
        "A room alias looks like this: "
        "'#someRoomAlias:matrix.example.org'. Short aliases like "
        "'someRoomAlias' or '#someRoomAlias' are also accepted. "
        "In case of a short alias, "
        "it will be automatically prefixed with '#' and the "
        f"homeserver from the default room of {PROG_WITHOUT_EXT} (as found "
        "in credentials file) will be automatically appended. "
        "Resolving an alias that does not exist results in an error. "
        "For each room alias one line will be printed to stdout with the "
        "result.",
    )
    ap.add_argument(
        "--room-delete-alias",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM_ALIAS",
        help="Delete one or multiple rooms aliases. "
        "Details:: Provide one or multiple room aliases. "
        "You can have multiple room aliases per room. So, "
        "you may delete multiple aliases from the same room or from different "
        "rooms. "
        "A room alias looks like this: "
        "'#someRoomAlias:matrix.example.org'. Short aliases like "
        "'someRoomAlias' or '#someRoomAlias' are also accepted. "
        "In case of a short alias, "
        "it will be automatically prefixed with '#' and the "
        f"homeserver from the default room of {PROG_WITHOUT_EXT} (as found "
        "in credentials file) will be automatically appended. "
        "Deleting an alias that does not exist results in an error.",
    )
    ap.add_argument(
        "--get-openid-token",
        required=False,
        action="extend",
        nargs="*",  # None if not used, [] is used without extra args
        type=str,
        metavar="USER",
        help="Get an OpenID token. "
        f"Details:: Get an OpenID token for {PROG_WITHOUT_EXT}, or for "
        "one or multiple other users. It prints an OpenID token object "
        "that the requester may supply to another service to verify their "
        "identity in Matrix. See http://www.openid.net/. "
        "Specify zero or more user ids. "
        f"If no user id is specified, an OpenID for {PROG_WITHOUT_EXT} will "
        "be fetched. If one or more user ids are given, the OpenID of "
        "these users will be fetched. As response the user id(s) and "
        "OpenID(s) will be printed.",
    )
    ap.add_argument(
        "--room-get-visibility",
        required=False,
        action="extend",
        nargs="*",  # None if not used, [] is used without extra args
        type=str,
        metavar="ROOM",
        help="Get the visibility of one or more rooms. "
        "Details:: Provide zero or more room ids as arguments. "
        "If no argument is given, then the default room of "
        f"{PROG_WITHOUT_EXT} (as found in credentials file) will be used. "
        "For each room the visibility will be printed. Currently, this "
        "is either the string 'private' or 'public'. "
        "As response one line per room will be printed to stdout.",
    )
    ap.add_argument(
        "--room-get-state",
        required=False,
        action="extend",
        nargs="*",  # None if not used, [] is used without extra args
        type=str,
        metavar="ROOM",
        help="Get the state of one or more rooms. "
        "Details::Provide zero or more room ids as arguments. "
        "If no argument is given, then the default room of "
        f"{PROG_WITHOUT_EXT} (as found in credentials file) will be used. "
        "For each room the state will be printed. The state is a long "
        "list of events including events like 'm.room.create', "
        "'m.room.encryption', 'm.room.guest_access', "
        "'m.room.history_visibility', 'm.room.join_rules', "
        "'m.room.member', 'm.room.power_levels', etc. "
        "As response one line per room will be printed to stdout. "
        "The line can be very long as the list of events can be very large. "
        "To get output into a human readable form pipe output through sed "
        "and jq as shown in an example in tests/test-setget.sh.",
    )
    ap.add_argument(
        "--delete-device",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="DEVICE",
        help=f"Delete one or multiple devices. "
        "Details:: By default devices belonging "
        f"to {PROG_WITHOUT_EXT} will be deleted. If the devices belong "
        "to a different user, use the --user argument to specify the user, "
        "i.e. owner. Only "
        "exactly one user can be specified with the optional --user argument. "
        "Device deletion requires the user password. It must be specified "
        "with the --password argument. If the server uses only HTTP (and "
        "not HTTPS), then the password can be visible to attackers. Hence, "
        "if the server does not support HTTPS this operation is discouraged.",
    )
    ap.add_argument(
        "--room-redact",
        "--room-delete-content",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="ROOM_ID EVENT_ID REASON",
        help="Strip information out of one or several events. "
        "Details:: "
        "Strip information from events, e.g. messages. "
        "Redact is used in the meaning of 'strip, wipe, black-out', not "
        "in the meaning of 'edit'. This action removes, deletes the content "
        "of an event while not removing the event. You can wipe text from a "
        "previous message, etc. Typical Matrix clients like Element will "
        "delete messages, images and other objects from the GUI once they "
        "have been redacted. "
        "So, --room-redact is a way to delete a message, images, etc. "
        "The content is "
        "wiped, the GUI deletes the message, but the server keeps the event "
        "history. Note, while this deletes from the client (GUI, e.g. "
        "Element), it does not delete from the database on the server. "
        "So, this call is not a way to clean up the server database. "
        "Each redact (wipe, strip, delete) operation requires exactly 3 "
        "arguments. "
        "The argument triples are: "
        "(a) the room id. "
        "(b) the id of the event to be redacted. "
        "(c) a string containing the reason for the redaction. Use '' if you "
        "do not want to give a reason. "
        "So, the total number of arguments used with --room-redact must be a "
        "multiple of 3, but we also accept 2 in which case only one "
        "redaction will be done without specifying a reason. "
        "Event ids start with the dollar sign ($). Depending on your shell, "
        "you might have to escape the '$' to '\\$'. --room-delete-content is "
        "an alias for --room-redact. They can be used interchangeably.",
    )
    ap.add_argument(
        # no single char flag
        "--whoami",
        required=False,
        action="store_true",
        help="Print your user id. "
        f"Details:: Print the user id used by {PROG_WITHOUT_EXT} (itself). "
        "One can get "
        "this information also by looking at the credentials file.",
    )
    ap.add_argument(
        # no single char flag
        "--no-ssl",
        required=False,
        action="store_true",
        default=NO_SSL_UNUSED_DEFAULT,  # when option isn't used
        help="Skip SSL verification. "
        "Details:: By default (if this option is not used) "
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
        metavar="SSL_CERTIFICATE_FILE",
        help="Use your own SSL certificate. "
        "Details:: Use this option to use "
        "your own local SSL certificate file. "
        "This is an optional parameter. This is useful for home servers that "
        "have their own "
        "SSL certificate. This allows you to use HTTPS/TLS for the connection "
        "while using your own local SSL certificate. Specify the path and "
        'file to your SSL certificate. If used together with the "--no-ssl" '
        "parameter, this option is meaningless and an error will be raised.",
    )
    ap.add_argument(
        "--file-name",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="FILE",
        help="Specify one or multiple file names for some actions. "
        "Details:: This is an optional argument. Use this option "
        "in combination with options like --download to specify one or "
        "multiple file names. "
        "Ignored if used by itself without an appropriate corresponding "
        "action.",
    )
    ap.add_argument(
        "--key-dict",
        required=False,
        action="extend",
        nargs="+",
        type=str,
        metavar="KEY_DICTIONARY",
        help="Specify one or multiple key dictionaries for decryption. "
        "Details:: One or multiple decryption "
        "dictionaries are provided by the --upload action as a result. "
        "A decryption dictionary is a string like this: "
        "\"{'v': 'v2', 'key': {'kty': 'oct', 'alg': 'A256CTR', 'ext': True, "
        "'k': 'somekey', 'key_ops': ['encrypt', 'decrypt']}, "
        "'iv': 'someiv', 'hashes': {'sha256': 'someSHA'}}\". If you have a "
        "list of key dictionaries and want to skip one, use the empty string.",
    )
    ap.add_argument(
        "--plain",
        required=False,
        action="store_true",
        help="Disable encryption for a specific action. "
        "Details:: By default, "
        "everything is always encrypted. "
        "Actions that support this option are: --upload, --room-create, "
        "and --room-dm-create. "
        "Rooms are by default created encrypted; "
        "to overwrite that and to create a room with encryption disabled "
        "use '--plain'. See the individual commands.",
    )
    ap.add_argument(
        "--separator",
        required=False,
        type=str,
        default=DEFAULT_SEPARATOR,  # defaults to SEP if not used
        # Text is scanned and repeated spaces are removes, so "    "
        # or {DEFAULT_SEPARATOR} will be truncated to " ". Hence "4 spaces"
        metavar="SEPARATOR",
        help="Set a custom separator used for certain print outs. "
        "Details:: By default, i.e. if --separator is not used, "
        "4 spaces are used as "
        "separator between columns in print statements. You could set "
        "it to '\\t' if you prefer a tab, but tabs are usually replaced "
        "with spaces by the terminal. So, that might not give you what you "
        "want. Maybe ' || ' is an alternative choice.",
    )
    ap.add_argument(
        "--access-token",
        required=False,
        type=str,
        metavar="ACCESS_TOKEN",
        help="Set a custom access token for use by certain actions. "
        "Details:: It is an optional argument. "
        "By default --access-token is ignored and not used. "
        "It is used by the --delete-mxc, --delete-mxc-before, "
        "and --rest actions.",
    )
    ap.add_argument(
        "--password",
        required=False,
        type=str,
        metavar="PASSWORD",
        help="Specify a password for use by certain actions. "
        "Details:: It is an optional argument. "
        "By default --password is ignored and not used. "
        "It is used by '--login password' and '--delete-device' "
        "actions. "
        "If not provided for --login the user will be queried via keyboard.",
    )
    ap.add_argument(
        "--homeserver",
        required=False,
        type=str,
        metavar="HOMESERVER_URL",
        help="Specify a homeserver for use by certain actions. "
        "Details:: It is an optional argument. "
        "By default --homeserver is ignored and not used. "
        "It is used by '--login' action. "
        "If not provided for --login the user will be queried via keyboard.",
    )
    ap.add_argument(
        "--device",  # do not confuse with --devices
        required=False,
        type=str,  # device id, device name
        metavar="DEVICE_NAME",
        help="Specify a device name, for use by certain actions. "
        "Details:: It is an optional argument. "
        "By default --device is ignored and not used. "
        "It is used by '--login' action. "
        "If not provided for --login the user will be queried via keyboard. "
        "If you want the default value specify ''. "
        "Multiple devices (with different device id) may have the same device "
        "name. In short, the same device name can be assigned to multiple "
        "different devices if desired.",
    )
    ap.add_argument(
        "--sync",
        required=False,
        type=str,  # sync method: off, full, (partial)
        metavar="FULL|OFF",
        help="Choose synchronization options. "
        "Details:: This option decides on whether the program "
        "synchronizes the state with the server before a 'send' action. "
        f"Currently two choices are offered: '{SYNC_FULL}' and '{SYNC_OFF}'. "
        "Provide one of these choices. "
        f"The default is '{SYNC_DEFAULT}'. If you want to use the default, "
        "then there is no need to use this option. "
        f"If you have chosen '{SYNC_FULL}', "
        "the full state, all state events will be synchronized between "
        "this program and the server before a 'send'. "
        f"If you have chosen '{SYNC_OFF}', "
        "synchronization will be skipped entirely before the 'send' "
        "which will improve performance.",
    )
    ap.add_argument(
        "-o",  # incompatible change Dec 2022, -o moved from --os-notify
        "--output",
        required=False,
        type=str,  # output method: text, json, json-max, ...
        default=OUTPUT_DEFAULT,  # when --output is not used
        metavar="TEXT|JSON|JSON-MAX|JSON-SPEC",
        help="Select an output format. "
        "Details:: This option decides on how the output is presented. "
        f"Currently offered choices are: '{OUTPUT_TEXT}', '{OUTPUT_JSON}', "
        f"'{OUTPUT_JSON_MAX}', and '{OUTPUT_JSON_SPEC}'. "
        "Provide one of these choices. "
        f"The default is '{OUTPUT_DEFAULT}'. If you want to use the default, "
        "then there is no need to use this option. "
        f"If you have chosen '{OUTPUT_TEXT}', "
        "the output will be formatted with the intention to be "
        "consumed by humans, i.e. readable text. "
        f"If you have chosen '{OUTPUT_JSON}', "
        "the output will be formatted as JSON. "
        "The content of the JSON object matches the data provided by the "
        "matrix-nio SDK. In some occasions the output is enhanced "
        "by having a few extra data items added for convenience. "
        "In most cases the output will be processed by other programs "
        "rather than read by humans. "
        f"Option '{OUTPUT_JSON_MAX}' is practically the same as "
        f"'{OUTPUT_JSON}', "
        "but yet another additional field is added. "
        "The data item 'transport_response' which gives information on "
        "how the data was obtained and transported is also being added. "
        "For '--listen' a few more fields are added. "
        "In most cases the output will be processed by other programs "
        "rather than read by humans. "
        f"Option '{OUTPUT_JSON_SPEC}' only prints information that adheres "
        "1-to-1 to the Matrix Specification. Currently only the events "
        "on '--listen' and '--tail' provide data exactly as in the "
        "Matrix Specification. If no data is available that corresponds "
        "exactly with the Matrix Specification, no data will be printed. "
        "In short, currently '--json-spec' only provides outputs for "
        "'--listen' and '--tail'. All other arguments like '--get-room-info' "
        "will print no output. ",
    )
    ap.add_argument(
        "--room-invites",
        required=False,
        type=str,
        default=INVITES_UNUSED_DEFAULT,  # when --room-invites is not used
        nargs="?",  # makes the word optional
        # when --room-invites is used, but text is not added
        const=INVITES_USED_DEFAULT,
        metavar="LIST|JOIN|LIST+JOIN",
        help="List room invitations and/or join invited rooms. "
        "Details:: This option takes zero or one argument. "
        f"If no argument is given, '{INVITES_LIST}' is assumed which will "
        "list all room invitation events as they are received. "
        "Listing will print the room id and other information to standard "
        "output. "
        f"'{INVITES_JOIN}' will join the room(s) each time a room invitation "
        "is received. "
        f"'{INVITES_LIST_JOIN}' will do both, list the invitations as well "
        "as automatically join the rooms to which an invitation was received. "
        "'--room-invites' can be combined with '--listen'. "
        "If and only if '--listen forever' is used, will the program "
        "listen continuously for room invites. "
        "In all other cases, the program only looks for room invitation "
        "events once; and it does so before any possible listening to "
        "messages. "
        "Warning: events are usually delivered once. So, if you listen "
        "for and list invites you will get them and list them the first "
        "time you run '--room-invites list'. On the second run of "
        "'--room-invites list' the events will not be replayed and "
        "not be listed. "
        "Hence, if you list the invites, you might want to store the output "
        "(room id) so that you can join the room later with '--room-join' "
        "for example. "
        "Don't confuse this option with --room-invite.",
    )
    ap.add_argument(
        "-v",  # incompatible change Dec 2022, -v moved here from --verify
        "-V",  # exception, allow also uppercase V
        "--version",
        required=False,
        type=str,
        default=VERSION_UNUSED_DEFAULT,  # when -t is not used
        nargs="?",  # makes the word optional
        # when -v is used, but text is not added
        const=VERSION_USED_DEFAULT,
        metavar="PRINT|CHECK",
        help="Print version information or check for updates. "
        "Details:: This option takes zero or one argument. "
        f"If no argument is given, '{PRINT}' is assumed which will "
        f"print the version of the currently installed 'PROG_WITHOUT_EXT' "
        f"package. '{CHECK}' is the alternative. "
        "'{CHECK}' connects to https://pypi.org and gets the version "
        "number of latest stable release. There is no 'calling home' "
        "on every run, only a 'check pypi.org' upon request. Your "
        "privacy is protected. The new release is neither downloaded, "
        "nor installed. It just informs you. "
        "After printing version information the "
        "program will continue to run. This is useful for having version "
        "number in the log files.",
    )
    gs.pa = ap.parse_args()
    # wrap and indent: https://towardsdatascience.com/6-fancy-built-in-text-
    #                  wrapping-techniques-in-python-a78cc57c2566
    # if output is not TTY, then don't add colors, e.g. when output is piped
    if sys.stdout.isatty():
        # You're running in a real terminal
        # colors
        # adapt width
        term_width = os.get_terminal_size()[0]
        # print("terminal width ", term_width)
        con = colors.fg.green
        coff = colors.reset
        eon = colors.bold + con
        eoff = colors.reset + con
    else:
        # You're being piped or redirected
        # no Colors
        # width = 80
        term_width = 80
        # print("not in terminal, using default terminal width ", term_width)
        con = ""
        coff = ""
        eon = ""
        eoff = ""
    if gs.pa.usage:
        print(textwrap.fill(ap.description, width=term_width))
        print("")
        ap.print_usage()
        print("")
        print(textwrap.fill(ap.epilog, width=term_width))
        return 0
    if gs.pa.help:
        print(textwrap.fill(ap.description, width=term_width))
        print("")
        print(
            textwrap.fill(
                f"{PROG_WITHOUT_EXT} supports these arguments:",
                width=term_width,
            )
        )
        # print("")
        help_help_pre = """
<--usage>
Print usage.
<-h>, <--help>
Print help.
<--manual>
Print manual.
<--readme>
Print README.md file.
<-d>, <--debug>
Print debug information.
<--log-level> DEBUG|INFO|WARNING|ERROR|CRITICAL [DEBUG|INFO|WARNING|ERROR|CRITICAL ...]
Set the log level(s).
<--verbose>
Set the verbosity level.
<--login> PASSWORD|SSO
Login to and authenticate with the Matrix homeserver.
<--verify> [EMOJI]
Perform verification.
<--logout> ME|ALL
Logout.
<-c> CREDENTIALS_FILE, <--credentials> CREDENTIALS_FILE
Specify location of credentials file.
<-s> STORE_DIRECTORY, <--store> STORE_DIRECTORY
Specify location of store directory.
<-r> ROOM [ROOM ...], <--room> ROOM [ROOM ...]
Specify one or multiple rooms.
<--room-default> DEFAULT_ROOM
Specify the default room at --login.
<--room-create> ROOM_ALIAS [ROOM_ALIAS ...]
Create one or multiple rooms for given alias(es).
<--room-dm-create> USER [USER ...]
Create one or multiple DM rooms with the specified users.
<--room-join> ROOM [ROOM ...]
Join one room or multiple rooms.
<--room-leave> ROOM [ROOM ...]
Leave one room or multiple rooms.
<--room-forget> ROOM [ROOM ...]
Forget one room or multiple rooms.
<--room-invite> ROOM [ROOM ...]
Invite one ore more users to join one or more rooms.
<--room-ban> ROOM [ROOM ...]
Ban one ore more users from one or more rooms.
<--room-unban> ROOM [ROOM ...]
Unban one ore more users from one or more rooms.
<--room-kick> ROOM [ROOM ...]
Kick one ore more users from one or more rooms.
<-u> USER [USER ...], <--user> USER [USER ...]
Specify one or multiple users.
<--user-login> USER
Specify user for --login.
<--name> ROOM_NAME [ROOM_NAME ...]
Specify one or multiple room names.
<--topic> ROOM_TOPIC [ROOM_TOPIC ...]
Specify one or multiple room topics.
<--alias> ROOM_ALIAS [ROOM_ALIAS ...]
Specify one or multiple room aliases.
<-m> TEXT [TEXT ...], <--message> TEXT [TEXT ...]
Send one or multiple text messages.
<-i> IMAGE_FILE [IMAGE_FILE ...], <--image> IMAGE_FILE [IMAGE_FILE ...]
Send one or multiple image files.
<-a> AUDIO_FILE [AUDIO_FILE ...], <--audio> AUDIO_FILE [AUDIO_FILE ...]
Send one or multiple audio files.
<-f> FILE [FILE ...], <--file> FILE [FILE ...]
Send one or multiple files (e.g. PDF, DOC, MP4).
<-e> MATRIX_JSON_OBJECT [MATRIX_JSON_OBJECT ...], <--event> MATRIX_JSON_OBJECT [MATRIX_JSON_OBJECT ...]
Send a Matrix JSON event.
<-w>, <--html>
Send message as format "HTML".
<-z>, <--markdown>
Send message as format "MARKDOWN".
<-k>, <--code>
Send message as format "CODE".
<-j>, <--emojize>
Send message after emojizing.
<-p> SEPARATOR, <--split> SEPARATOR
Split message text into multiple Matrix messages.
<--config> CONFIG_FILE
Specify the location of a config file.
<--proxy> PROXY
Specify a proxy for connectivity.
<-n>, <--notice>
Send message as notice.
<--encrypted>
Send message end-to-end encrypted.
<-l> [NEVER|ONCE|FOREVER|TAIL|ALL], <--listen> [NEVER|ONCE|FOREVER|TAIL|ALL]
Print received messages and listen to messages.
<-t> [NUMBER], <--tail> [NUMBER]
Print last messages.
<-y>, <--listen-self>
Print your own messages as well.
<--print-event-id>
Print event ids of received messages.
<--download-media> [DOWNLOAD_DIRECTORY]
Download media files while listening.
<--download-media-name> SOURCE|CLEAN|EVENTID|TIME
Specify the method to derive the media filename.
<--os-notify>
Notify me of arriving messages.
<--set-device-name> DEVICE_NAME
Set or rename the current device.
<--set-display-name> DISPLAY_NAME
Set or rename the display name.
<--get-display-name>
Get the display name of yourself.
<--set-presence> ONLINE|OFFLINE|UNAVAILABLE
Set your presence.
<--get-presence>
Get your presence.
<--upload> FILE [FILE ...]
Upload one or multiple files to the content repository.
<--download> MXC_URI [MXC_URI ...]
Download one or multiple files from the content repository.
<--delete-mxc> MXC_URI [MXC_URI ...]
Delete one or multiple objects from the content repository.
<--delete-mxc-before> TIMESTAMP [TIMESTAMP ...]
Delete old objects from the content repository
<--joined-rooms>
Print the list of joined rooms.
<--joined-members> ROOM [ROOM ...]
Print the list of joined members for one or multiple rooms.
<--mxc-to-http> MXC_URI [MXC_URI ...]
Convert MXC URIs to HTTP URLs.
<--devices,> <--get-devices>
Print the list of devices.
<--discovery-info>
Print discovery information about current homeserver.
<--login-info>
Print login methods supported by the homeserver.
<--content-repository-config>
Print the content repository configuration.
<--rest> REST_METHOD DATA URL [REST_METHOD DATA URL ...]
Use the Matrix Client REST API.
<--set-avatar> AVATAR_MXC_URI
Set your avatar.
<--get-avatar> [USER ...]
Get an avatar.
<--get-profile> [USER ...]
Get a user profile.
<--get-room-info> [ROOM ...]
Get the room information.
<--get-client-info>
Print client information.
<--has-permission> ROOM BAN|INVITE|KICK|NOTIFICATIONS|REDACT|etc [ROOM BAN|INVITE|KICK|NOTIFICATIONS|REDACT|etc ...]
Inquire about permissions.
<--import-keys> FILE PASSPHRASE FILE PASSPHRASE
Import Megolm decryption keys from a file.
<--export-keys> FILE PASSPHRASE FILE PASSPHRASE
Export all the Megolm decryption keys of this device.
<--room-set-alias> ROOM_ALIAS ROOM [ROOM_ALIAS ROOM ...], <--room-put-alias> ROOM_ALIAS ROOM [ROOM_ALIAS ROOM ...]
Add aliases to rooms.
<--room-resolve-alias> ROOM_ALIAS [ROOM_ALIAS ...]
Show room ids corresponding to room aliases.
<--room-delete-alias> ROOM_ALIAS [ROOM_ALIAS ...]
Delete one or multiple rooms aliases.
<--get-openid-token> [USER ...]
Get an OpenID token.
<--room-get-visibility> [ROOM ...]
Get the visibility of one or more rooms.
<--room-get-state> [ROOM ...]
Get the state of one or more rooms.
<--delete-device> DEVICE [DEVICE ...]
Delete one or multiple devices.
<--room-redact> ROOM_ID EVENT_ID REASON [ROOM_ID EVENT_ID REASON ...], <--room-delete-content> ROOM_ID EVENT_ID REASON [ROOM_ID EVENT_ID REASON ...]
Strip information out of one or several events.
<--whoami>
Print your user id.
<--no-ssl>
Skip SSL verification.
<--ssl-certificate> SSL_CERTIFICATE_FILE
Use your own SSL certificate.
<--file-name> FILE [FILE ...]
Specify one or multiple file names for some actions.
<--key-dict> KEY_DICTIONARY [KEY_DICTIONARY ...]
Specify one or multiple key dictionaries for decryption.
<--plain>
Disable encryption for a specific action.
<--separator> SEPARATOR
Set a custom separator used for certain print outs.
<--access-token> ACCESS_TOKEN
Set a custom access token for use by certain actions.
<--password> PASSWORD
Specify a password for use by certain actions.
<--homeserver> HOMESERVER_URL
Specify a homeserver for use by certain actions.
<--device> DEVICE_NAME
Specify a device name, for use by certain actions.
<--sync> FULL|OFF
Choose synchronization options.
<-o> TEXT|JSON|JSON-MAX|JSON-SPEC, <--output> TEXT|JSON|JSON-MAX|JSON-SPEC
Select an output format.
<--room-invites> [LIST|JOIN|LIST+JOIN]
List room invitations and/or join invited rooms.
<-v> [PRINT|CHECK], -V [PRINT|CHECK], <--version> [PRINT|CHECK]
Print version information or check for updates.
""".replace(
            "<", eon
        ).replace(
            ">", eoff
        )
        header = False  # first line is newline
        for line in help_help_pre.split("\n"):
            if header:
                print(
                    textwrap.fill(con + line + coff, width=term_width),
                    flush=True,
                )
            else:
                print(
                    textwrap.indent(
                        textwrap.fill(line, width=term_width - 2), "  "
                    ),
                    flush=True,
                )

            header = not header
        # print("")
        print(textwrap.fill(ap.epilog, width=term_width))
        return 0
    if gs.pa.manual:
        description = (
            f"Welcome to {PROG_WITHOUT_EXT}, a Matrix CLI client. ─── "
            "On first run use --login to log in, to authenticate. "
            "On second run we suggest to use --verify to get verified. "
            "Emoji verification is built-in which can be used "
            "to verify devices. "
            "On further runs this program implements a simple Matrix CLI "
            "client that can send messages, listen to messages, verify "
            "devices, etc. It can send one or multiple message to one or "
            "multiple Matrix rooms and/or users. The text messages can be "
            "of various "
            'formats such as "text", "html", "markdown" or "code". '
            "Images, audio, arbitrary files, or events can be sent as well. "
            "For receiving there are three main options: listen forever, "
            "listen once and quit, and get the last N messages "
            "and quit. End-to-end encryption is enabled by default "
            "and cannot be turned off, but it can be disabled for specific "
            "use cases.  ─── "
            "Bundling several actions together into a single call to "
            f"{PROG_WITHOUT_EXT} is faster than calling {PROG_WITHOUT_EXT} "
            "multiple times with only one action. If there are both 'set' "
            "and 'get' actions present in the arguments, then the 'set' "
            "actions will be performed before the 'get' actions. Then "
            "send actions and at the very end listen actions will be "
            "performed. ─── "
            "For even more explications and examples also read the "
            "documentation provided in the on-line Github README.md file "
            "or the README.md in your local installation.  ─── "
            "For less information just use --help instead of --manual."
        )
        print(textwrap.fill(description, width=term_width), flush=True)
        print("")
        ap.print_help(file=None)  # ap.print_usage() is included
        return 0
    if gs.pa.readme:
        # Todo
        exedir = os.path.dirname(os.path.realpath(__file__))
        readme = exedir + "/../" + "README.md"
        readme_primary = readme
        foundpath = None
        if os.path.exists(readme):
            foundpath = readme
            print(f"Found local README.md here: {readme}")
        else:
            readme = exedir + "/" + "README.md"
            if os.path.exists(readme):
                foundpath = readme
                print(f"Found local README.md here: {readme}")
        if foundpath is None:
            print(
                "Sorry, README.md not found locally "
                f"in installation directory {readme_primary}."
            )
            print(f"Hence downloading it from {README_FILE_RAW_URL}.")
            notused, foundpath = tempfile.mkstemp()
            urllib.request.urlretrieve(README_FILE_RAW_URL, foundpath)
        try:
            with open(foundpath, "r+") as f:
                text = f.read()
            print(f"{text}")
        except Exception:  # (BrokenPipeError, IOError):
            # print("BrokenPipeError caught", file=sys.stderr)
            pass
        return 0

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
            gs.log.warning(
                "W111: " "Debug option -d overwrote option --log-level."
            )
            gs.warn_count += 1

    SEP = bytes(gs.pa.separator, "utf-8").decode("unicode_escape")
    gs.log.debug(
        f'Separator is set to "{SEP}" of '
        f"length {len(SEP)}. E.g. Col1{SEP}Col2."
    )
    initial_check_of_args()
    check_download_media_dir()
    try:
        check_arg_files_readable()
    except Exception as e:
        gs.log.error(e)  # already has Exxx: unique error number
        raise MatrixCommanderError(
            f"{PROG_WITHOUT_EXT} forces an early abort. "
            "To avoid partial execution, no action has been performed at all. "
            "Nothing has been sent. Fix your arguments and run the command "
            "again."
        ) from None

    if gs.pa.version:
        if gs.pa.version.lower() == PRINT:
            version()  # continue execution
        else:
            check_version()  # continue execution
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

    gs.log.debug(f'Python version is "{sys.version}"')
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
            gs.err_count += 1
            raise MatrixCommanderError(
                "E243: "
                f'SSL certificate file "{gs.pa.ssl_certificate}" was '
                "not found."
            ) from None
        except PermissionError:
            gs.err_count += 1
            raise MatrixCommanderError(
                "E244: "
                f'SSL certificate file "{gs.pa.ssl_certificate}" does '
                "not have read permissions."
            ) from None
        except ssl.SSLError:
            gs.err_count += 1
            raise MatrixCommanderError(
                "E245: "
                f'SSL certificate file "{gs.pa.ssl_certificate}" has '
                "invalid content. Does not seem to be a certificate."
            ) from None
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
        asyncio.run(async_main())  # do everything in the event loop
        # the next can be reached on success or failure
        gs.log.debug(f"The program {PROG_WITH_EXT} left the event loop.")
    except TimeoutError as e:
        gs.err_count += 1
        raise MatrixCommanderError(
            "E247: "
            f"The program {PROG_WITH_EXT} ran into a timeout. "
            "Most likely connectivity to internet was lost. "
            "If this happens frequently consider running this "
            "program as a service so it will restart automatically. Sorry."
        ) from e
    except MatrixCommanderError:
        raise
    except KeyboardInterrupt:
        gs.log.debug("Keyboard interrupt received.")
    except Exception:
        gs.err_count += 1
        gs.log.error("E248: " f"The program {PROG_WITH_EXT} failed. Sorry.")
        raise
    finally:
        cleanup()


def main(argv: Union[None, list] = None) -> int:
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

    Returns int. 0 for success. Positive integer for failure.
        Returns the total number of errors encountered.

    Tries to avoid raising exceptions.

    """
    try:
        main_inner(argv)
    except (Exception, MatrixCommanderError, MatrixCommanderWarning) as e:
        if e not in (MatrixCommanderError, MatrixCommanderWarning):
            gs.err_count += 1
        tb = ""
        if gs.pa.debug > 0:
            tb = f"\nHere is the traceback.\n{traceback.format_exc()}"
        if e == MatrixCommanderWarning:
            gs.log.warning(f"{e}{tb}")
        else:
            gs.log.error(f"{e}{tb}")
    if gs.err_count > 0 or gs.warn_count > 0:
        gs.log.info(
            f"{gs.err_count} "
            f"error{'' if gs.err_count == 1 else 's'} and "
            f"{gs.warn_count} "
            f"warning{'' if gs.warn_count == 1 else 's'} occurred."
        )
    return gs.err_count  # 0 for success


if __name__ == "__main__":
    sys.exit(main())
# EOF
