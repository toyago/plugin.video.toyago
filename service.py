# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import xbmcaddon
import threading
import urllib
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import toyago
import playlist
import uuid

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
addondir = xbmc.translatePath(addon.getAddonInfo('profile'))
server_enable = addon.getSetting('server_enable');
serviceType = addon.getSetting('server_service_type');
user = addon.getSetting('toya_go_user');
password = addon.getSetting('toya_go_pass');
deviceid = addon.getSetting('toya_go_device')

if deviceid == "":
    randomdev = str(uuid.uuid4().get_hex().upper()[0:10])
    addon.setSetting('toya_go_device', randomdev)
    deviceid = randomdev

API = toyago.GetInstance(deviceid, user, password)
server = None;

class MyHandler(BaseHTTPRequestHandler):
    global server;
    def do_GET(self):
        try:
            if 'playlist' in self.path:
                cids = []
                count = 0
                channels = API.channels(cids)
                playlistManager = playlist.Playlist("ToyaGo")
                for channel in channels:
                    count += 1
                    if channel.source != None:
                        playlistManager.addM3UChannel(count, channel.name, channel.thumbnail, channel.name, channel.name, channel.source)
                m3u = playlistManager.getM3UList()
                self.send_response(200)
                self.send_header('Content-type', 'application/x-mpegURL')
                self.send_header('Connection', 'close')
                self.send_header('Content-Length', len(m3u))
                self.end_headers()
                self.wfile.write(m3u.encode('utf-8'))
                self.finish()
        except Exception as e:
            xbmcgui.Dialog().notification("ToyaGO PVR", str(e), xbmcgui.NOTIFICATION_ERROR);


class AsyncCall(object):
    def __init__(self, fnc, callback=None):
        self.Callable = fnc
        self.Callback = callback

    def __call__(self, *args, **kwargs):
        self.Thread = threading.Thread(target=self.run, name=self.Callable.__name__, args=args, kwargs=kwargs)
        self.Thread.start()
        return self

    def wait(self, timeout=None):
        self.Thread.join(timeout)
        if self.Thread.isAlive():
            raise TimeoutError()
        else:
            return self.Result

    def run(self, *args, **kwargs):
        self.Result = self.Callable(*args, **kwargs)
        if self.Callback:
            self.Callback(self.Result)


class AsyncMethod(object):
    def __init__(self, fnc, callback=None):
        self.Callable = fnc
        self.Callback = callback

    def __call__(self, *args, **kwargs):
        return AsyncCall(self.Callable, self.Callback)(*args, **kwargs)


def Async(fnc=None, callback=None):
    if fnc == None:
        def AddAsyncCallback(fnc):
            return AsyncMethod(fnc, callback)

        return AddAsyncCallback
    else:
        return AsyncMethod(fnc, callback)


@Async
def startServer():
    global server;
    server_enable = addon.getSetting('server_enable');
    port = int(addon.getSetting('server_port'));
    try:
        server = SocketServer.TCPServer(('', port), MyHandler);
        server.serve_forever();

    except KeyboardInterrupt:
        if server != None:
            server.socket.close();


def stopServer():
    port = addon.getSetting('server_port');
    try:
        url = urllib.urlopen('http://localhost:' + str(port) + '/stop');
        code = url.getcode();
    except Exception as e:
        return;
    return;


def serverOnline():
    port = addon.getSetting('server_port');
    try:
        url = urllib.urlopen('http://localhost:' + str(port) + '/online');
        code = url.getcode();
        if code == 200:
            return True;
    except Exception as e:
        return False;
    return False;


if __name__ == '__main__':
    startServer();
