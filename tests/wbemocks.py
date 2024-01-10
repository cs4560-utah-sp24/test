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
from unittest import mock
from ssl import SSLCertVerificationError


def normalize_display_list(dl):
    dl = [(float(t[0]), float(t[1]), t[2].replace("\xad", ""), *t[3:]) for t in dl]
    return dl

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
            beginning, self.body = self.request.decode("latin1").split("\r\n\r\n")
            headers = [item.split(":", 1) for item in beginning.split("\r\n")[1:]]
            content_length = None
            for tup in headers:
                key, val = tup
                if key.lower() == "content-length":
                    content_length = val.strip()
            assert content_length is not None, "Content-Length not present in headers"
            assert len(self.body) == int(content_length), len(self.body)

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
            assert self.body == self.URLs[url][2], (self.body, self.URLs[url][2])
        if binary:
            return io.BytesIO(output)
        return io.StringIO(output.decode(encoding).replace(newline, "\n"), newline)

    def close(self):
        self.connected = False

    @classmethod
    def patch(cls):
        return mock.patch("socket.socket", wraps=cls)

    @classmethod
    def respond(cls, url, response, method="GET", body=None):
        if NO_CACHE:
            response = response.replace(b"\r\n\r\n",
                                        b"\r\nCache-Control: no-store\r\n\r\n")
        cls.URLs[url] = [method, response, body]

    @classmethod
    def respond_200(cls, url, body):
        response = ("HTTP/1.0 200 OK\r\n" +
                    "\r\n" +
                    body).encode()
        cls.respond(url, response, "GET")

    @classmethod
    def respond_ok(cls, url, body):
        response = ("HTTP/1.0 200 OK\r\n" +
                    "\r\n" +
                    body).encode()
        cls.respond(url, response, "GET")

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

    def load_default_certs(self):
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

    def create_line(self, x1, y1, x2, y2, fill=None):
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


def check_bookmark_button(fill_color):
    rec_calls = [call for call in TK_CANVAS_CALLS
                 if call.startswith("create_rectangle")]
    for rec_call in rec_calls:
        parts = rec_call.split()
        x1 = float(parts[1].split("=")[1])
        y1 = float(parts[2].split("=")[1])
        x2 = float(parts[3].split("=")[1])
        y2 = float(parts[4].split("=")[1])
        fill = parts[6].split("=")[1][1:-1]

        if (755 < x1 < 775 and
           40 < y1 < 60 and
           780 < x2 < 800 and
           80 < y2 < 100 and
           fill == fill_color):
            return True

    return False

def check_not_bookmarked():
    return check_bookmark_button("white")

def check_bookmarked():
    return check_bookmark_button("yellow")


tkinter.Canvas = SilentCanvas

class MockCanvas:
    def __init__(self, *args, **kwargs):
        pass

    def create_rectangle(self, x1, y1, x2, y2, width=None, fill=None, outline=None):
        print("create_rectangle: x1={} y1={} x2={} y2={} width={} fill={}".format(
            x1, y1, x2, y2, width, repr(fill)))

    def create_line(self, x1, y1, x2, y2, fill=None):
        pass

    def create_oval(self, x1, y1, x2, y2):
        pass

    def create_polygon(self, *args, **kwargs):
        pass

    def create_text(self, x, y, text, font=None, anchor=None, fill=None):
        if text.isspace():
            return
        if font or anchor:
            print("create_text: x={} y={} text={} font={} anchor={}".format(
                x, y, text, font, anchor))
        else:
            print("create_text: x={} y={} text={}".format(
                x, y, text))

    def pack(self, expand=None, fill=None):
        pass

    def delete(self, v):
        pass

original_tkinter_canvas = tkinter.Canvas

class SkipChromeCanvas:
    def __init__(self, *args, **kwargs):
        pass

    def create_text(self, x, y, text, font=None, anchor=None, fill=None):
        if text.isspace() or y < 100:
            return
        if font or anchor:
            print("create_text: x={} y={} text={} font={} anchor={}".format(
                x, y, text, font, anchor))
        else:
            print("create_text: x={} y={} text={}".format(
                x, y, text))

    def create_rectangle(self, x1, y1, x2, y2, width=None, fill=None, outline=None):
        if y1 > 100 and fill != "blue":
            print("create_rectangle: x1={} y1={} x2={} y2={} width={} fill={}".format(
                x1, y1, x2, y2, width, repr(fill)))

    def create_line(self, x1, y1, x2, y2, fill=None):
        pass

    def create_oval(self, x1, y1, x2, y2):
        pass

    def create_polygon(self, *args, **kwargs):
        pass

    def pack(self, expand=None, fill=None):
        pass

    def delete(self, v):
        pass


class resize_event:
    def __init__(self, width, height):
        self.height = height
        self.width = width

class mousewheel_event:
    def __init__(self, delta):
        self.delta = delta
        self.num = "??"

class key_event:
    def __init__(self, char):
        self.char = char

class backspace_event:
    def __init__(self):
        pass

class enter_event:
    def __init__(self):
        pass

class tab_event:
    def __init__(self):
        pass

def patch_canvas():
    tkinter.Canvas = MockCanvas

def patch_skip_chrome_canvas():
    tkinter.Canvas = SkipChromeCanvas

def patch_silent_canvas():
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

tkinter.font.Font = MockFont

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

class Event:
    def __init__(self, x, y):
        self.x = x
        self.y = y
