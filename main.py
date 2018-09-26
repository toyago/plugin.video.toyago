import sys
from urlparse import parse_qsl
import xbmcgui
import xbmcaddon
import xbmcplugin
import toyago
import service
import uuid
import time

addon = xbmcaddon.Addon()
_url = sys.argv[0]
_handle = int(sys.argv[1])

user = addon.getSetting('toya_go_user');
password = addon.getSetting('toya_go_pass');
sortType = addon.getSetting('toya_go_sort');
deviceid = addon.getSetting('toya_go_device')
addonname = addon.getAddonInfo('name')
if deviceid == "":
    randomdev = str(uuid.uuid4().get_hex().upper()[0:10])
    addon.setSetting('toya_go_device', randomdev)
    deviceid = randomdev

API = toyago.GetInstance(deviceid, user, password)


def getChannels():
    cids = []
    channels = API.channels(cids)
    epg = {}
    API.epg(cids, epg)
    listing = []
    for channel in channels:
        if channel.source != None:
            channelThumb = channel.thumbnail
            # title = '[COLOR green]' + channel.name + '[/COLOR]'
            title = '[B]' + channel.name + '[/B]'
            descr = ""
            epgTitle = ""
            next_title = ""
            if str(channel.cid) in epg:
                epgObj = epg[str(channel.cid)]
                if epgObj != None:
                    title += '[I]' + ' - " ' + epgObj.title + ' "' + '[/I]'
                    descr = epgObj.descr
                    epgTitle = epgObj.title
                    next_title = 'Nastepnie: ' + '[B]' + epgObj.next_title + '[/B]\n'
                    next_title += 'Teraz: ' + '[B]' + epgObj.title + '[/B]'
            list_item = xbmcgui.ListItem(label=title, thumbnailImage=channelThumb)
            list_item.setProperty('fanart_image', channelThumb)
            list_item.setInfo('video', {'title': title, 'genre': channel.genre, 'plot': next_title + '\n' + descr,
                                        'plotoutline ': epgTitle, 'originaltitle': epgTitle})
            list_item.setArt({'landscape': channelThumb})
            list_item.setProperty('IsPlayable', 'true')
            url = '{0}?action=play&video={1}'.format(_url, channel.source)
            is_folder = False
            listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    if sortType == "1":
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            print('listing')
        elif params['action'] == 'play':
            play_video(params['video'])
        elif params['action'] == 'stopServer':
            stopServer()
        elif params['action'] == 'startServer':
            startServer()
    else:
        getChannels()


def startServer():
    port = addon.getSetting('server_port');
    if service.serverOnline():
        xbmcgui.Dialog().notification(addonname, 'Server already started. Port: ' + str(port),
                                      xbmcgui.NOTIFICATION_INFO);
    else:
        service.startServer();
        time.sleep(5);
        if service.serverOnline():
            xbmcgui.Dialog().notification(addonname, 'Server started. Port: ' + str(port), xbmcgui.NOTIFICATION_INFO);
        else:
            xbmcgui.Dialog().notification(addonname, 'Server not started. Wait one moment and try again. ', xbmcgui.NOTIFICATION_ERROR);


def stopServer():
    if service.serverOnline():
        service.stopServer()
        time.sleep(5);
        xbmcgui.Dialog().notification(addonname, 'Server stopped.', xbmcgui.NOTIFICATION_INFO);
    else:
        xbmcgui.Dialog().notification(addonname, 'Server is already stopped.', xbmcgui.NOTIFICATION_INFO);


if __name__ == '__main__':
    router(sys.argv[2][1:])
