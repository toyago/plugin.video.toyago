# -*- coding: utf-8 -*-
import os
from xml.dom import minidom
from xml.dom.minidom import parse, parseString
# from datetime import datetime
import model

getAuth = 'toyago.GetAuth'
getChannels = 'toyago.GetProducts'
setVersion = 'toyago.SetVersion'
getEpg = 'toyago.GetEPGpf'
getChannel = 'toyago.GetObjects'
serviceTv = 'GOTV'

# toyaDate = '"%Y-%m-%dT%H:%M:%S.%fZ"'

thubmBase = 'https://toya.net.pl/telewizja/kanaly/logo/sid/'


class Request:
    def __init__(self):
        # global definitions should be here
        self.text = None

    def auth(self, deviceId, user, passw):
        self.doc = minidom.Document()
        methodCall = self.doc.createElement("methodCall")
        self.doc.appendChild(methodCall)
        methodName = self.doc.createElement("methodName")
        methodName.appendChild(self.doc.createTextNode('toyago.GetAuth'))
        methodCall.appendChild(methodName)
        params = self.doc.createElement("params")
        self.addStrVal(deviceId, params)
        self.addStrVal(user, params)
        self.addStrVal(passw, params)
        methodCall.appendChild(params)
        self.doc.appendChild(methodCall)
        # xml_str = self.doc.toprettyxml(encoding="utf-8")
        xml_str = self.doc.toxml(encoding="utf-8")
        # print(xml_str)
        return xml_str

    def version(self, deviceId, version, token):
        self.doc = minidom.Document()
        methodCall = self.doc.createElement("methodCall")
        self.doc.appendChild(methodCall)
        methodName = self.doc.createElement("methodName")
        methodName.appendChild(self.doc.createTextNode(setVersion))
        methodCall.appendChild(methodName)
        params = self.doc.createElement("params")
        self.addStrVal(deviceId, params)
        self.addStrVal(version, params)
        self.addStrVal(token, params)
        methodCall.appendChild(params)
        self.doc.appendChild(methodCall)
        # xml_str = self.doc.toprettyxml(encoding="utf-8")
        xml_str = self.doc.toxml(encoding="utf-8")
        # print(xml_str)
        return xml_str

    def getChannels(self, token, deviceId):
        self.doc = minidom.Document()
        methodCall = self.doc.createElement("methodCall")
        self.doc.appendChild(methodCall)
        methodName = self.doc.createElement("methodName")
        methodName.appendChild(self.doc.createTextNode(getChannels))
        methodCall.appendChild(methodName)
        params = self.doc.createElement("params")
        self.addStrVal(deviceId, params)
        self.addStrVal('channel', params)
        self.addArrayVal(None, params)
        self.addI4Val('0', params)
        self.addI4Val('300', params)
        self.addArrayVal(['0'], params)
        self.addBooleanVal('true', params)
        self.addStrVal(token, params)
        methodCall.appendChild(params)
        # xml_str = self.doc.toprettyxml(encoding="utf-8")
        xml_str = self.doc.toxml(encoding="utf-8")
        # print('ToyaGo getChannels xml request')
        # print(xml_str)
        return xml_str

    def getChannel(self, token, deviceId, productId, number, parent):
        prodId = 'products.id=' + str(productId)
        self.doc = minidom.Document()
        methodCall = self.doc.createElement("methodCall")
        self.doc.appendChild(methodCall)
        methodName = self.doc.createElement("methodName")
        methodName.appendChild(self.doc.createTextNode(getChannel))
        methodCall.appendChild(methodName)
        params = self.doc.createElement("params")
        self.addStrVal(deviceId, params)
        self.addI4Val(str(number), params)
        # self.addStrVal(serviceTv, params)
        self.addArrayVal([prodId], params)
        self.addI4Val('1', params)
        self.addI4Val('0', params)
        self.addArrayVal(['0'], params)
        self.addI4Val(str(parent), params)
        self.addBooleanVal('true', params)
        self.addStrVal(token, params)
        methodCall.appendChild(params)
        xml_str = self.doc.toprettyxml(encoding="utf-8")
        # xml_str = self.doc.toxml(encoding="utf-8")
        print('ToyaGo getChannel xml request')
        print(xml_str)
        return xml_str

    def getEPG(self, token, deviceId, cids):
        self.doc = minidom.Document()
        methodCall = self.doc.createElement("methodCall")
        self.doc.appendChild(methodCall)
        methodName = self.doc.createElement("methodName")
        methodName.appendChild(self.doc.createTextNode(getEpg))
        methodCall.appendChild(methodName)
        params = self.doc.createElement("params")
        self.addStrVal(deviceId, params)
        self.addArrayVal(cids, params)
        methodCall.appendChild(params)
        self.addStrVal('2015-06-19T09:00:00Z', params)
        self.addStrVal(token, params)
        # xml_str = self.doc.toprettyxml(encoding="utf-8")
        xml_str = self.doc.toxml(encoding="utf-8")
        # print(xml_str)
        return xml_str

    def addStrVal(self, text, params):
        paramElement = self.doc.createElement("param")
        valueElement = self.doc.createElement("value")
        valueElement.appendChild(self.doc.createTextNode(text))
        paramElement.appendChild(valueElement)
        params.appendChild(paramElement)

    def addBooleanVal(self, val, params):
        paramElement = self.doc.createElement("param")
        valueElement = self.doc.createElement("value")
        booleanElement = self.doc.createElement("boolean")
        booleanElement.appendChild(self.doc.createTextNode(val))
        valueElement.appendChild(booleanElement)
        paramElement.appendChild(valueElement)
        params.appendChild(paramElement)

    def addI4Val(self, val, params):
        paramElement = self.doc.createElement("param")
        valueElement = self.doc.createElement("value")
        i4Element = self.doc.createElement("i4")
        i4Element.appendChild(self.doc.createTextNode(val))
        valueElement.appendChild(i4Element)
        paramElement.appendChild(valueElement)
        params.appendChild(paramElement)

    def addArrayVal(self, values, params):
        paramElement = self.doc.createElement("param")
        valueElement = self.doc.createElement("value")
        arrayElement = self.doc.createElement("array")
        if values != None:
            dataElement = self.doc.createElement("data")
            arrayElement.appendChild(dataElement)
            for value in values:
                valueDataElem = self.doc.createElement("value")
                valueDataElem.appendChild(self.doc.createTextNode(value))
                dataElement.appendChild(valueDataElem)
        valueElement.appendChild(arrayElement)
        paramElement.appendChild(valueElement)
        params.appendChild(paramElement)


class Response:
    def __init__(self):
        self.cids = {}
    def parseToken(self, toyaResp):
        # TODO
        tokenResp = parseString(toyaResp)
        tokenElement = tokenResp.getElementsByTagName("string")[0]
        # print(tokenElement.firstChild.nodeValue)
        return tokenElement.firstChild.nodeValue

    def parseVersion(self, toyaResp):
        versionResp = parseString(toyaResp)
        versionElement = versionResp.getElementsByTagName("boolean")[0]
        # print(versionElement.firstChild.nodeValue)
        return versionElement.firstChild.nodeValue

    def parseEPG(self, toyaResp, epg):
        # dateObj = datetime.strptime('exampleDateHere', toyaDate)
        channelsResp = parseString(str(toyaResp))
        members = channelsResp.getElementsByTagName("member")
        # print('member')
        for member in members:
            nameNode = member.getElementsByTagName("name")[0]
            name = nameNode.firstChild.nodeValue
            # print(name)
            if (name == "products"):
                # print('products')
                # epg = {}
                epgNodes = member.getElementsByTagName("string")
                # channels = []
                channel = 'empty'
                for epgNode in epgNodes:
                    name = None
                    descr = None
                    next_title = None
                    epgXml = epgNode.firstChild.nodeValue
                    # print(epgXml)
                    epgObj = parseString(epgXml.encode('utf-8'))
                    epgObjAttr = epgObj.getElementsByTagName("object")
                    for epgAttr in epgObjAttr:
                        # print('attr')
                        channel_id = epgAttr.getAttribute('channel_id')
                        # print(channel_id)
                        if channel != channel_id:
                            channel = str(channel_id)
                            attributes = epgAttr.getElementsByTagName("attr")
                            for attr in attributes:
                                if attr.attributes["key"].value == "title":
                                    name = attr.getElementsByTagName("value")[0].firstChild.nodeValue
                                    # print(channel_id + ' ' + name)
                                if attr.attributes["key"].value == "description":
                                    descr = attr.getElementsByTagName("value")[0].firstChild.nodeValue
                            epg[channel_id] = model.EPG(name, descr, None)
                        else:
                            attributesNext = epgAttr.getElementsByTagName("attr")
                            for attrNext in attributesNext:
                                if attrNext.attributes["key"].value == "title":
                                    next_title = attrNext.getElementsByTagName("value")[0].firstChild.nodeValue
                            if epg[channel_id] != None:
                                epg[channel_id].next_title = next_title

                return epg


    def parseChannels(self, toyaResp, cids):
        # print('ToyaGo getChannels xml response')
        # print(str(toyaResp))

        channelsResp = parseString(str(toyaResp))
        members = channelsResp.getElementsByTagName("member")
        for member in members:
            nameNode = member.getElementsByTagName("name")[0]
            name = nameNode.firstChild.nodeValue
            # print(name)
            if (name == "products"):
                channelsNode = member.getElementsByTagName("string")
                channels = []
                for channelNode in channelsNode:
                    name = None
                    thumbnail = None
                    source = None
                    number = None
                    genre = None
                    channelXml = channelNode.firstChild.nodeValue
                    channelObj = parseString(channelXml.encode('utf-8'))
                    channelsObj = channelObj.getElementsByTagName("object")
                    for channelObj in channelsObj:
                        cid = channelObj.getAttribute('id')
                        cids.append(str(cid))
                        id = cid.replace('1111', '')
                        attributes = channelObj.getElementsByTagName("attr")
                        for attr in attributes:
                            if attr.attributes["key"].value == "name":
                                name = attr.getElementsByTagName("value")[0].firstChild.nodeValue
                            elif attr.attributes["key"].value == "thumbnail":
                                print()
                                # thumbnail = attr.getElementsByTagName("value")[0].firstChild.nodeValue
                            elif attr.attributes["key"].value == "source":
                                source = self.getElemVal(attr)
                            elif attr.attributes["key"].value == "number":
                                number = attr.getElementsByTagName("value")[0].firstChild.nodeValue
                            elif attr.attributes["key"].value == "genres":
                                genre = self.getElemVal(attr)
                            thumbnail = thubmBase + id + '?big=1'
                    channel = model.Channel(name,source ,thumbnail,number,genre,cid)
                    channels.append(channel)
                return channels

    def getElemVal(self, attr):
        elem = attr.getElementsByTagName("value")
        if elem != None:
            elemFirst = elem[0]
            if elemFirst != None:
                firstChild = elemFirst.firstChild
                if firstChild != None:
                    return firstChild.nodeValue


