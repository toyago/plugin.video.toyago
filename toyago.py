# -*- coding: utf-8 -*-
import client, xmlCommon

apiUrl = 'https://api-go.toya.net.pl/toyago/index.php'


class GetInstance:

    def __init__(self, devId, user, passw):
        self.deviceId = devId
        self.user = user
        self.passw = passw
        self.token = None
        self.xmlReq = xmlCommon.Request()
        self.xmlResp = xmlCommon.Response()

    def auth(self):
        authReq = self.xmlReq.auth(self.deviceId, self.user, self.passw)
        authResp = client.request(apiUrl, authReq)
        token = self.xmlResp.parseToken(authResp)
        # print(token)
        self.token = token
        verReq = self.xmlReq.version(self.deviceId, '2.0', self.token)
        verResp = client.request(apiUrl, verReq)
        # print(verResp)

    def channels(self, cids):
        self.auth()
        channelsReq = self.xmlReq.getChannels(self.token, self.deviceId)
        # print(channelsReq)
        channelsResp = client.request(apiUrl, channelsReq)
        # print(channelsResp)
        channels = self.xmlResp.parseChannels(channelsResp, cids)
        #for channel in channels:
        for i in range(1111173, 1111273):
            #   print('serviceId ' + str(i))
            #    print('cid ' + str(channel.cid))
            self.channel(i, 0)
            i += 1
            # break
        return channels

    def epg(self, cids, epg):
        # self.auth()
        epgStr = self.xmlReq.getEPG(self.token, self.deviceId, cids)
        # print(epgStr)
        epgResp = client.request(apiUrl, epgStr)
        # print(epgResp)
        self.xmlResp.parseEPG(epgResp, epg)

    def channel(self, cid, number):
        channelReq = self.xmlReq.getChannel(self.token, self.deviceId, cid, number)
        channelResp = client.request(apiUrl, channelReq)
        print('ToyaGo getChannel xml response 1: ' + str(cid) + ' ' + str(number))
        print(channelResp)
        # cid2 = cid.replace('1111', '')
        # channelReq2 = self.xmlReq.getChannel(self.token, self.deviceId, cid2, number)
        # channelResp2 = client.request(apiUrl, channelReq2)
        # print('ToyaGo getChannel xml response 2: ' + str(cid) + ' ' + str(number))
        # print(channelResp2)
        # channelReq3 = self.xmlReq.getChannel(self.token, self.deviceId, number, number)
        # channelResp3 = client.request(apiUrl, channelReq3)
        # print('ToyaGo getChannel xml response 3: ' + str(cid) + ' ' + str(number))
        # print(channelResp3)


if __name__ == "__main__":
    API = GetInstance('qwerty1234', 'user', 'password')
    cids = []
    channels = API.channels(cids)
    for channel in channels:
        print(channel.name)
        print(channel.thumbnail)
        print(channel.source)
        print(channel.number)
        # if channel.source != None:
        #   API.channel(channel.source)
    for cid in cids:
        print(cid)
    epg = {}
    API.epg(cids, epg)
    print(epg['1111142'].title)
    print(epg['1111142'].descr)
    print(epg['1111142'].next_title)
