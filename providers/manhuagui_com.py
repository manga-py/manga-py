#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import execjs
import json
import random

LZjs = r'''var LZString=(function(){var f=String.fromCharCode;var keyStrBase64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";var baseReverseDic={};function getBaseValue(alphabet,character){if(!baseReverseDic[alphabet]){baseReverseDic[alphabet]={};for(var i=0;i<alphabet.length;i++){baseReverseDic[alphabet][alphabet.charAt(i)]=i}}return baseReverseDic[alphabet][character]}var LZString={decompressFromBase64:function(input){if(input==null)return"";if(input=="")return null;return LZString._0(input.length,32,function(index){return getBaseValue(keyStrBase64,input.charAt(index))})},_0:function(length,resetValue,getNextValue){var dictionary=[],next,enlargeIn=4,dictSize=4,numBits=3,entry="",result=[],i,w,bits,resb,maxpower,power,c,data={val:getNextValue(0),position:resetValue,index:1};for(i=0;i<3;i+=1){dictionary[i]=i}bits=0;maxpower=Math.pow(2,2);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}switch(next=bits){case 0:bits=0;maxpower=Math.pow(2,8);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}c=f(bits);break;case 1:bits=0;maxpower=Math.pow(2,16);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}c=f(bits);break;case 2:return""}dictionary[3]=c;w=c;result.push(c);while(true){if(data.index>length){return""}bits=0;maxpower=Math.pow(2,numBits);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}switch(c=bits){case 0:bits=0;maxpower=Math.pow(2,8);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}dictionary[dictSize++]=f(bits);c=dictSize-1;enlargeIn--;break;case 1:bits=0;maxpower=Math.pow(2,16);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}dictionary[dictSize++]=f(bits);c=dictSize-1;enlargeIn--;break;case 2:return result.join('')}if(enlargeIn==0){enlargeIn=Math.pow(2,numBits);numBits++}if(dictionary[c]){entry=dictionary[c]}else{if(c===dictSize){entry=w+w.charAt(0)}else{return null}}result.push(entry);dictionary[dictSize++]=w+entry.charAt(0);enlargeIn--;w=entry;if(enlargeIn==0){enlargeIn=Math.pow(2,numBits);numBits++}}}};return LZString})();String.prototype.splic=function(f){return LZString.decompressFromBase64(this).split(f)};'''
domainUri = 'http://www.manhuagui.com'
servers = [
    'i.hamreus.com:8080',
    'us.hamreus.com:8080',
    'dx.hamreus.com:8080',
    'eu.hamreus.com:8080',
    'lt.hamreus.com:8080',
]


def get_main_content(url, get=None, post=None):
    _id = re.search('/comic/(\d+)', url)
    if not _id:
        return ''
    return get('{}/comic/{}/'.format(domainUri, _id.groups()[0]))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content)
    chapters = parser.cssselect('.chapter-list li > a')
    if len(chapters) < 1:
        chapters = parser.cssselect('#__VIEWSTATE')[0].get('value')

        try:
            js = execjs.compile(LZjs).eval('LZString.decompressFromBase64("' + chapters + '")')
            if not js:
                return []
            chapters = document_fromstring(js).cssselect('.chapter-list li > a')
        except Exception:
            return []

    return [domainUri + i.get('href') for i in chapters]


def get_archive_name(volume, index: int = None):
    idx = re.search('comic/\d+/(\d+)', volume)
    frm = 'vol_{:0>3}'

    if idx:
        frm += '_{}'.format(idx.groups()[0])

    return frm.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    js = re.search('\](\(function\(.+\))\s?<', content)
    if not js:
        return []
    data = execjs.compile(LZjs).eval(js.groups()[0])
    data = re.search('cInfo=(.+)\|\|', data)
    if not data:
        return []
    data = json.loads(data.groups()[0])

    images = []
    for i in data['files']:
        prior = 3
        ln = len(servers)
        server = int(random.random() * (ln + prior))
        server = 0 if server < prior else server - prior
        images.append('http://{}{}{}'.format(servers[server], data['path'], i))

    return images


def get_manga_name(url, get=None):

    content = get(url)

    selector = 'h1'
    if re.search('/comic/\d+/\d+\.html', url):
        selector = 'h1 > a'

    _u = document_fromstring(content).cssselect(selector)

    return _u[0].text_content()


if __name__ == '__main__':
    print('Don\'t run this, please!')
