"""
This file contains the mock framework for testing
"""

import builtins
import io
import sys
import tkinter
import tkinter.font
import email
import os
import weakref
from unittest import mock
from ssl import SSLCertVerificationError


def normalize_display_list(dl):
    dl = [(float(t[0]), float(t[1]), t[2].replace("\xad", ""), *t[3:]) for t in dl]
    return dl

def print_list(dl):
    for l in dl:
        print(repr(l))

class certifi:
    def where(self):
        return os.getcwd()

sys.modules["certifi"] = certifi()


def fake_badssl(hostname):
    if hostname.endswith(".badssl.com"):
        raise SSLCertVerificationError()

NO_CACHE = False
class socket:
    URLs = {}
    Requests = {}
    recent_request_path = None

    def __init__(self, *args, **kwargs):
        self.request = b""
        self.connected = False
        self.ssl_hostname = None

    def __enter__(self):
        return self
    
    def __exit__(self, type_, value, traceback):
        # TODO: does not handle exit with exceptions differently
        self.close()

    def setsockopt(self, *args):
        assert False, "In your server.py file place socket creation/bind/etc inside an if __name__ == \"__main__\""

    def bind(self, *args):
        assert False, "In your server.py file place socket creation/bind/etc inside an if __name__ == \"__main__\""

    def listen(self, *args):
        assert False, "In your server.py file place socket creation/bind/etc inside an if __name__ == \"__main__\""

    def connect(self, host_port):
        self.host, self.port = host_port
        self.connected = True
        if self.ssl_hostname is not None:
            assert self.ssl_hostname == self.host
            fake_badssl(self.host)
            self.scheme = "https"
        else:
            self.scheme = "http"

    def send(self, text):
        self.request += text
        self.method, self.path, _ = self.request.decode("latin1").split(" ", 2)
        socket.recent_request_path = self.path

        if self.method == "POST":
            req = self.request.decode("latin1")
            assert "\r\n\r\n" in req, "HTTP request does not separate headers from body with an empty line"
            beginning, self.body = req.split("\r\n\r\n")
            headers = [item.split(":", 1) for item in beginning.split("\r\n")[1:]]
            content_length = None
            for tup in headers:
                key, val = tup
                if key.lower() == "content-length":
                    content_length = val.strip()
            assert content_length is not None, "Content-Length not present in headers"
            assert len(self.body) == int(content_length), "Payload {!r} is {} bytes but Content-Length is given as {}".format(self.body, len(self.body), content_length)

    def makefile(self, mode, encoding, newline):
        """
            do not support 'w' mode; 'r' is a synonym of 'rt'
            encoding and newline ignored for 'b' mode
            implementation note:
            copied some from https://github.com/python/cpython/blob/main/Lib/socket.py
        """
        if not set(mode) <= {"r", "b"}:
            raise ValueError("invalid mode %r (only r, b allowed)" % (mode,))
        binary = "b" in mode  # 't' or 'b'

        assert self.connected and self.host and self.port, \
            "You cannot call makefile() on a socket until you call connect() and send()"
        if self.port == 80 and self.scheme == "http":
            url = self.scheme + "://" + self.host + self.path
        elif self.port == 443 and self.scheme == "https":
            url = self.scheme + "://" + self.host + self.path
        else:
            url = self.scheme + "://" + self.host + ":" + str(self.port) + self.path
        self.Requests.setdefault(url, []).append(self.request)
        if url not in self.URLs and "?" in url:
            response = ("HTTP/1.0 200 Incorrect GET form submisson\r\n"
                        "\r\n"
                        "Incorrect GET form submisson")
            return io.StringIO(response.replace(newline, "\n"), newline)
        assert url in self.URLs, f"You are requesting a url that you shouldn't: {url}"
        assert self.method == self.URLs[url][0], \
            f"Expected a {self.URLs[url][0]} request but got a {self.method} request to {url}"
        output = self.URLs[url][1]
        if self.URLs[url][2]:
            assert self.body == self.URLs[url][2], \
                "Expected request body of {!r} but got {!r}".format(
                    self.URLs[url][2], self.body)
        if binary:
            return io.BytesIO(output)
        return io.StringIO(output.decode(encoding).replace(newline, "\n"), newline)

    def close(self):
        self.connected = False

    @classmethod
    def patch(cls):
        cls.reset()
        return mock.patch("socket.socket", wraps=cls)

    @classmethod
    def respond(cls, url, response, method="GET", body=None):
        if NO_CACHE:
            response = response.replace(b"\r\n\r\n",
                                        b"\r\nCache-Control: no-store\r\n\r\n")
        cls.URLs[url] = [method, response, body]

    @classmethod
    def respond_200(cls, url, response_body, **kwargs):
        response = ("HTTP/1.0 200 OK\r\n" +
                    "\r\n" +
                    response_body).encode()
        cls.respond(url, response, **kwargs)

    @classmethod
    def respond_ok(cls, url, body):
        response = ("HTTP/1.0 200 OK\r\n" +
                    "\r\n" +
                    body).encode()
        cls.respond(url, response, "GET")

    @classmethod
    def serve(cls, html):
        html = html.encode("utf8") if isinstance(html, str) else html
        response  = b"HTTP/1.0 200 OK\r\n"
        response += b"Content-Type: text/html\r\n"
        response += b"Content-Length: " + str(len(html)).encode("ascii") + b"\r\n"
        response += b"\r\n" + html
        prefix = "http://test/"
        url = next(prefix + str(i) for i in range(1000) if prefix + str(i) not in cls.URLs)
        cls.respond(url, response)
        return url

    @classmethod
    def made_request(cls, url):
        return url in cls.Requests

    @classmethod
    def last_request(cls, url):
        return cls.Requests[url][-1]

    @classmethod
    def clear_history(cls):
        cls.Requests = {}

    @classmethod
    def count_header_last_request(cls, url, header):
        raw_request = cls.Requests[url][-1].decode()
        raw_headers, raw_body = raw_request.split("\r\n\r\n", 1)
        raw_headers = raw_headers.lower()
        header = header.lower()
        return raw_headers.count(header)

    @classmethod
    def parse_last_request(cls, url):
        raw_request = cls.Requests[url][-1].decode()
        raw_command, raw_headers = raw_request.split('\r\n', 1)
        message = email.message_from_file(io.StringIO(raw_headers))
        headers = dict(message.items())
        headers = {key.lower(): val for key, val in headers.items()}
        command, path, version = raw_command.split(" ", 2)
        return command, path, version, headers

    @classmethod
    def redirect_url(cls, from_url, to_url):
        cls.respond(url=from_url,
                    response=("HTTP/1.0 301 Moved Permanently\r\n" +
                              "Location: {}\r\n" +
                              "\r\n").format(to_url).encode(),
                    method="GET")

    @classmethod
    def last_request_path(cls):
        return cls.recent_request_path

    @classmethod
    def reset(cls):
        cls.URLs = {}
        cls.Requests = {}
        cls.recent_request_path = None

class ssl:
    def __init__(self, *args):
        pass

    def wrap_socket(self, s, server_hostname):
        s.ssl_hostname = server_hostname
        if s.connected:
            assert s.host == server_hostname
            fake_badssl(s.host)
        s.scheme = "https"
        return s

    def load_default_certs(self, *args):
        pass

    def load_verify_locations(self, **kwargs):
        pass

    # @classmethod
    # def SSLContext(cls, protocol=None):
    #     return cls.create_default_context()

    @classmethod
    def patch(cls):
        _ = mock.patch("ssl.SSLContext", wraps=cls).start()
        return mock.patch("ssl.create_default_context", wraps=cls)

class SilentTk:
    def bind(self, event, callback):
        pass

tkinter.Tk = SilentTk
    
class PhotoImage:
    DO_NOT_GC = weakref.WeakKeyDictionary()

    def __init__(self, file, *, secret_width=None, secret_height=None):
        self.filename = file
        width, height = secret_width, secret_height

        if width == None and height == None:
            assert os.path.isfile(file), "Could not find image file {}".format(file)
            with open(file, "rb") as f:
                # I can't rely on any library being available so I
                # manually parse the image formats to figure out their
                # sizes. Only GIF and PNG supported.
                header = f.read(6)
                if header == b"\211PNG\r\n":
                    # It's a PNG file
                    more_header = f.read(2)
                    length = f.read(4)
                    type = f.read(4)
                    assert more_header == b"\032\n" and \
                        length == b"\0\0\0\x0d" and \
                        type == b"IHDR", \
                        "PNG file {} appears invalid".format(file)
                    width = f.read(4)
                    height = f.read(4)
                    width = width[3] + (width[2]<<8) + (width[1]<<16) + (width[0]<<24)
                    height = height[3] + (height[2]<<8) + (height[1]<<16) + (height[0]<<24)
                elif header == b"GIF89a":
                    # It's a GIF file
                    width = f.read(2)
                    height = f.read(2)
                    width = width[0] + (width[1]<<8)
                    height = height[0] + (height[1]<<8)
                else:
                    raise ValueError("{} does not appear to be a PNG or GIF file".format(file))
        self.w = width
        self.h = height

    def zoom(self, zoom_x, zoom_y):
        ret = PhotoImage(self.filename,
                         secret_width=self.w * zoom_x, secret_height=self.h * zoom_y)
        return ret

    def subsample(self, zoom_x, zoom_y):
        ret = PhotoImage(self.filename,
                         secret_width=self.w // zoom_x, secret_height=self.h // zoom_y)
        return ret

    def __del__(self):
        if self in PhotoImage.DO_NOT_GC:
            print("{} used in create_image() was garbage collected.".format(self))
            print("This is bad and is probably a bug in your code.")
            "A PhotoImage used in create_image() has been garbage collected; this is bad"

    def __repr__(self):
        return "PhotoImage(" + repr(self.filename) + ")"

    @classmethod
    def cleanup(cls):
        cls.DO_NOT_GC = weakref.WeakKeyDictionary()

tkinter.PhotoImage = PhotoImage

TK_CANVAS_CALLS = list()
class SilentCanvas:
    def __init__(self, *args, **kwargs):
        global TK_CANVAS_CALLS
        TK_CANVAS_CALLS = list()

    def create_text(self, x, y, text, font=None, anchor=None, fill=None):
        global TK_CANVAS_CALLS
        if text.isspace():
            return
        if font or anchor:
            TK_CANVAS_CALLS.append("create_text: x={} y={} text={} font={} anchor={}".format(
                x, y, text, font, anchor))
        else:
            TK_CANVAS_CALLS.append("create_text: x={} y={} text={}".format(
                x, y, text))

    def create_rectangle(self, x1, y1, x2, y2, width=None, fill=None, outline=None):
        global TK_CANVAS_CALLS
        TK_CANVAS_CALLS.append("create_rectangle: x1={} y1={} x2={} y2={} width={} fill={}".format(
            x1, y1, x2, y2, width, repr(fill)))

    def create_line(self, x1, y1, x2, y2, fill=None, width=None):
        pass

    def create_oval(self, x1, y1, x2, y2):
        pass

    def create_polygon(self, *args, **kwargs):
        pass

    def pack(self, expand=None, fill=None):
        pass

    def delete(self, v):
        global TK_CANVAS_CALLS
        assert(v == "all")
        TK_CANVAS_CALLS = list()


def maybeint(x):
    return int(x) if (isinstance(x, float) and x == int(x)) else x

tkinter.Canvas = SilentCanvas

class MockCanvas:
    HIDE_COMMANDS = set()
    HIDE_ABOVE = 0
    IMAGE_SIZE = None
    LOG = []

    def __init__(self, *args, **kwargs):
        pass

    def _allow(self, cmdname, ytop):
        if self.HIDE_COMMANDS == "*": return False
        if cmdname in self.HIDE_COMMANDS: return False
        if ytop <= self.HIDE_ABOVE: return False
        return True

    def _draw(self, str):
        self.LOG.append(str)

    def create_rectangle(self, x1, y1, x2, y2, width=None, fill=None, outline=None):
        x1 = maybeint(x1)
        x2 = maybeint(x2)
        y1 = maybeint(y1)
        y2 = maybeint(y2)
        width = maybeint(width)
        cmd = "create_rectangle: x1={} y1={} x2={} y2={} width={} fill={}".format(
            x1, y1, x2, y2, width, repr(fill))
        self._draw(cmd)
        if self._allow("create_rectangle", max(y1, y2)): print(cmd)

    def create_line(self, x1, y1, x2, y2, fill=None, width=None):
        x1 = maybeint(x1)
        x2 = maybeint(x2)
        y1 = maybeint(y1)
        y2 = maybeint(y2)
        width = maybeint(width)
        cmd = "create_line: x1={} y1={} x2={} y2={} width={} fill={}".format(
            x1, y1, x2, y2, width, repr(fill))
        self._draw(cmd)
        if self._allow("create_line", max(y1, y2)): print(cmd)

    def create_oval(self, x1, y1, x2, y2):
        x1 = maybeint(x1)
        x2 = maybeint(x2)
        y1 = maybeint(y1)
        y2 = maybeint(y2)
        cmd = "create_oval: x1={} y1={} x2={} y2={}".format(
            x1, y1, x2, y2)
        self._draw(cmd)
        if self._allow("create_oval", max(y1, y2)): print(cmd)

    def create_image(self, x, y, image):
        x = maybeint(x)
        y = maybeint(y)
        PhotoImage.DO_NOT_GC[image] = True
        if self.IMAGE_SIZE:
            assert self.IMAGE_SIZE == (image.w, image.h), \
                "Expecting a {}x{} image but got a {}x{} image".format(
                    *self.IMAGE_SIZE, image.w, image.h)
        self._draw(cmd)
        cmd = "create_oval: x={} y={} image={}".format(x, y, image)
        if self._allow("create_image", y + image.h): print(cmd)

    def create_text(self, x, y, text, font=None, anchor=None, fill=None):
        if text.isspace(): return
        if font or anchor:
            cmd = "create_text: x={} y={} text={} font={} anchor={}".format(
                x, y, text, font, anchor)
        else:
            cmd = "create_text: x={} y={} text={}".format(x, y, text)
        self._draw(cmd)
        y2 = y + font.metrics("linespace")
        if self._allow("create_text", y2): print(cmd)

    def pack(self, expand=None, fill=None):
        pass

    def delete(self, v):
        assert v == "all"
        self.LOG[:] = [] # clear

    @classmethod
    def hide_command(cls, name):
        cls.HIDE_COMMANDS.add(name)

    @classmethod
    def hide_above(cls, y):
        cls.HIDE_ABOVE = y

    @classmethod
    def hide_all(cls):
        cls.HIDE_COMMANDS = "*"

    @classmethod
    def require_image_size(cls, w, h):
        cls.IMAGE_SIZE = (w, h)

    @classmethod
    def reset(cls):
        cls.HIDE_COMMANDS = set()
        cls.HIDE_ABOVE = 0
        cls.IMAGE_SIZE = None
        cls.LOG = []

    @classmethod
    def all_rects(cls, rect):
        x1, x2 = rect.left, rect.right
        y1, y2 = rect.top, rect.bottom
        for line in cls.LOG:
            if line.startswith("create_rectangle: x1={} y1={} x2={} y2={}".format(x1, y1, x2, y2)):
                print(line)

original_tkinter_canvas = tkinter.Canvas

class Event:
    pass

class ClickEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class KeyEvent:
    def __init__(self, char):
        self.char = char

class ResizeEvent:
    def __init__(self, width, height):
        self.height = height
        self.width = width

def patch_canvas():
    MockCanvas.reset()
    tkinter.Canvas = MockCanvas

def patch_silent_canvas():
    MockCanvas.reset()
    tkinter.Canvas = SilentCanvas

def unpatch_canvas():
    tkinter.Canvas = original_tkinter_canvas


NORMALIZE_FONT = False
class MockFont:
    def __init__(self, size=None, weight=None, slant=None, style=None, family=None):
        self.size = size
        self.weight = weight
        self.slant = slant
        self.style = style
        self.family = family

    def measure(self, word):
        return self.size * len(word.replace("\xad", ""))

    def metrics(self, name=None):
        all = {"ascent": self.size * 0.75, "descent": self.size * 0.25,
               "linespace": self.size}
        if name:
            return all[name]
        return all

    def cget(self, option):
        if option == "size":
            return self.size
        if option == "weight":
            return self.weight
        if option == "slant":
            return self.slant
        if option == "style":
            return self.style
        if option == "family":
            return self.family
        assert False, f"bad option: {option}"

    def __repr__(self):
        if self.family and not NORMALIZE_FONT:
            return "Font size={} weight={} slant={} style={} family={}".format(
                self.size, self.weight, self.slant, self.style, self.family)
        else:
            return "Font size={} weight={} slant={} style={}".format(
                self.size, self.weight, self.slant, self.style)

class MockLabel:
    def __init__(self, font=None):
        pass

tkinter.font.Font = MockFont

tkinter.Label = MockLabel

def errors(f, *args, **kwargs):
    try:
        f(*args, **kwargs)
    except Exception:
        return True
    else:
        return False

def breakpoint(name, *args):
    args_str = (", " + ", ".join(["'{}'".format(arg) for arg in args]) if args else "")
    print("breakpoint(name='{}'{})".format(name, args_str))

builtin_breakpoint = builtins.breakpoint

def patch_breakpoint():
    builtins.breakpoint = breakpoint

def unpatch_breakpoint():
    builtins.breakpoint = builtin_breakpoint

