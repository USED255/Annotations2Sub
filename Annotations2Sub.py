#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__authors__  = (
    'wrtyis@outlook.com'
 )

__license__ = 'GPLv3'
__version__ = '0.0.6'

"""
参考:
https://github.com/weizhenye/ASS/wiki/ASS-字幕格式规范
https://github.com/afrmtbl/AnnotationsRestored

"""

""" 
鸣谢:
https://archive.org/details/youtubeannotations
https://github.com/afrmtbl/AnnotationsRestored

"""

""" 
本脚本启发自:
https://github.com/nirbheek/youtube-ass ,https://github.com/afrmtbl/annotations-converter 您仍然可以从本脚本找到他们的痕迹。

"""

import os
import re
import json
import urllib.request 
import gettext
import argparse
import xml.etree.ElementTree
from datetime import datetime
from typing import Optional

try:
    t = gettext.translation(domain='en', localedir='locale',languages=['en_US'])
    t.install()
except:
    print("\033[0;33;40m\tWarning! locale not found, i18n Not loaded\033[0m")
    _ = gettext.gettext

if hex(os.sys.hexversion) < hex(0x03060000):
    print(_("\033[0;31;40m\t我需要大于3.6的Python!\033[0m"))
    exit(1)

def _download_for_invidious(id:str,invidious_domain:str='invidiou.site') -> str:
    api = '/api/v1/annotations/'
    url = 'https://' + invidious_domain + api + id
    file = "{}.xml".format(id)
    print(_("正在从 {} 下载注释文件".format(url)))
    urllib.request.urlretrieve(url,file)
    print(_("下载完成"))
    return file

def _preview_video(id:str,file:str,invidious_domain:str='invidiou.site') ->None:
    api = '/api/v1/videos/'
    url = 'https://' + invidious_domain + api + id
    sub = file
    r = urllib.request.Request(url)
    with urllib.request.urlopen(r) as f:
        data = json.loads(f.read().decode('utf-8'))
    audios = []
    videos = []
    for i in data.get('adaptiveFormats'):
        if re.match('audio', i.get('type')) is not None:
            audios.append(i)
        if re.match('video', i.get('type')) is not None:
            videos.append(i)
    audios.sort(key=lambda x:int(x.get('bitrate')),reverse=True)
    videos.sort(key=lambda x:int(x.get('bitrate')),reverse=True)
    audio = audios[0].get('url')
    video = videos[0].get('url')
    cmd = r'mpv "{}" --audio-file="{}" --sub-file="{}"'.format(video,audio,file)
    print(cmd)
    os.system(cmd)

def _generate_video(id:str,file:str,invidious_domain:str='invidiou.site') ->None:
    api = '/api/v1/videos/'
    url = 'https://' + invidious_domain + api + id
    sub = file
    r = urllib.request.Request(url)
    with urllib.request.urlopen(r) as f:
        data = json.loads(f.read().decode('utf-8'))
    audios = []
    videos = []
    for i in data.get('adaptiveFormats'):
        if re.match('audio', i.get('type')) is not None:
            audios.append(i)
        if re.match('video', i.get('type')) is not None:
            videos.append(i)
    audios.sort(key=lambda x:int(x.get('bitrate')),reverse=True)
    videos.sort(key=lambda x:int(x.get('bitrate')),reverse=True)
    audio = audios[0].get('url')
    video = videos[0].get('url')
    cmd = r'ffmpeg -i "{}" -i "{}" -vf "ass={}" "{}.mp4"'.format(video,audio,file,id)
    print(cmd)
    os.system(cmd)

def AnnotationsParser(File:str) -> list:
    def _main(File:str) -> list:
        annotations=[]
        string=open(File,'r',encoding="utf-8").read()
        _xml = xml.etree.ElementTree.fromstring(string)
        for each in _xml.find('annotations').findall('annotation'):
            annotation = _parser(each)
            if annotation is not None:
                annotations.append(annotation)
        return annotations
    
    def _parser(each) -> dict:
        type = each.get('type')
        if type is None or type is 'pause':
            return None
        
        _appearance = each.find('_appearance')
        if _appearance is None:
            return None
        
        _segment = each.find('segment').find('movingRegion').findall('rectRegion')
        if len(_segment) == 0:
            __segment = each.find('segment').find('movingRegion').findall('anchoredRegion')
        if len(_segment) == 0:
            return None
        
        Start = min(_segment[0].get('t'), _segment[1].get('t'))
        End = max(_segment[0].get('t'), _segment[1].get('t'))
        try:
            Start =datetime.strptime(Start,"%H:%M:%S.%f")
            End = datetime.strptime(End,"%H:%M:%S.%f")
        except:
            Start =datetime.strptime(Start,"%M:%S.%f")
            End = datetime.strptime(End,"%M:%S.%f")
        
        return {
        # type: 字符串格式的注释类型, 可能的值包括text和pause
        'type' : type,
        # id: 字符串格式的注释id
        'id' : each.get('id'),
        # style: 字符串格式的注释样式, 可能的值包括title, speech, popup, highlightText, anchored, 和branding
        'style' : each.get('style'),
        # Text: 字符串格式的注释文本
        'Text' : each.find('TEXT'),
        
        
        # Start: 整数格式的一秒为单位的注释的开始时间
        "Start":Start,
        # End: 整数格式的一秒为单位的注释的结束时间
        "End":End,
        
        # textSize: 浮点数格式的文字大小占影片高度的百分比。
        'textSize' : _appearance.get('textSize'),
        # bgAlpha: 浮点数格式的背景透明度, 范围从0到1
        'bgAlpha' : _appearance.get('bgAlpha'),
        # fgColor: 整数格式的十进制的注释前景色 RGB颜色 0-255
        'fgColor' : _appearance.get('fgColor'),
        # bgColor: 整数格式的十进制的注释背景色 RGB颜色 0-255
        'bgColor' : _appearance.get('bgColor'),
        
        # x: 浮点数格式的注释的x坐标, 以视频宽度的百分比表示
        'x' : float(_segment[0].get('x')),
        # y: 浮点数格式的注释的y坐标, 以视频宽度的百分比表示
        'y' : float(_segment[0].get('y')),
        # w: 浮点数格式的注释的宽度, 以视频宽度的百分比表示
        'w' : float(_segment[0].get('w')),
        # h: 浮点数格式的注释的高度, 以视频高度的百分比表示
        'h' : float(_segment[0].get('h')),
        # sx: 浮点数格式的语音气泡点x轴位置, 以视频宽度的百分比表示
        'sx' : float(_segment[0].get('sx')),
        # sy: 浮点数格式的语音气泡点y轴位置, 以视频高度的百分比表示
        'sy' : float(_segment[0].get('sy'))
        }
    
    return _main(File=File)

class AssTools():
    class FormatError(Exception):
        pass
    
    def __init__(self) -> None:
        self.info = self._info()
        self.style = self._style()
        self.event = self._event()
    
    def dump(self) -> str:
        data = ''
        data += self.info.dump()
        data += self.style.dump()
        data += self.event.dump()
        return data

    class _info(object):
        def __init__(self) -> None:
            self.HEAD = "[Script Info]\n"
            self.note = "; Script generated by Annotations2Sub\n"\
                        "; https://github.com/WRTYis/Annotations2Sub\n"
            self.data={
                'Title':'Default File',
                'ScriptType':'v4.00+'}
        
        def add(self,k:str,v:str) -> None:
            self.data[k]=v
        
        def dump(self) -> str:
            data = ''
            data += self.HEAD
            data += self.note
            for k, v in self.data.items():
                data += str(k)+': '+str(v)+'\n'
            data += '\n'
            return data

    class _style(object):
        def __init__(self) -> None:
            self.HEAD = "[V4+ Styles]\n"\
                        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            self.data = {}
            self.add(Name='Default')
        
        def add(self,Name:str,Fontname:str='Arial',Fontsize:str=20,PrimaryColour:str='&H00FFFFFF',SecondaryColour:str='&H000000FF',OutlineColour:str='&H00000000',BackColour:str='&H00000000',Bold:int=0,Italic:int=0,Underline:int=0,StrikeOut:int=0,ScaleX:int=100,ScaleY:int=100,Spacing:int=0,Angle:int=0,BorderStyle:int=1,Outline:int=2,Shadow:int=2,Alignment:int=2,MarginL:int=10,MarginR:int=10,MarginV:int=10,Encoding:int=1) -> None:
            self.data[Name] = self._check([Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding])
        
        def change(self,Name,Fontname:Optional[str]=None,Fontsize:Optional[str]=None,PrimaryColour:Optional[str]=None,SecondaryColour:Optional[str]=None,OutlineColour:Optional[str]=None,BackColour:Optional[str]=None,Bold:Optional[int]=None,Italic:Optional[int]=None,Underline:Optional[int]=None,StrikeOut:Optional[int]=None,ScaleX:Optional[int]=None,ScaleY:Optional[int]=None,Spacing:Optional[int]=None,Angle:Optional[int]=None,BorderStyle:Optional[int]=None,Outline:Optional[int]=None,Shadow:Optional[int]=None,Alignment:Optional[int]=None,MarginL:Optional[int]=None,MarginR:Optional[int]=None,MarginV:Optional[int]=None,Encoding:Optional[int]=None) -> None:
            for i,v in enumerate(self._check([Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding])):
                if v is not None:
                    self.data[Name][i] = v
        
        def dump(self) ->str:
            data = ''
            data += self.HEAD
            for Name, Style in self.data.items():
                data += 'Style: {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(Name, *Style)
            data += '\n'
            return data
        
        def _check(self,style:list) -> list:
            if None:
                raise FormatError('')
            return style

    class _event(object):
        def __init__(self) -> None:
            self.HEAD = "[Events]\n"\
                        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            self.data = []
        
        def add(self,EventType:str='Dialogue',Layer:int=0, Start:str='0:00:00.00', End:str='0:00:00.00', Style:str='Default', Name:str='', MarginL:int=0, MarginR:int=0, MarginV:int=0, Effect:str='',Text:str='') -> None:
            # EventType: Dialogue, Comment, Picture, Sound, Movie, Command 
            self.data.append(self._check([EventType,Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text]))
        
        def dump(self) ->str:
            data = ''
            data += self.HEAD
            for event in self.data:
                data += '{}: {},{},{},{},{},{},{},{},{},{}\n'.format(*event)
            data += '\n'
            return data
        
        def _check(self,event:list) -> list:
            if None:
                raise FormatError('')
            return event

class TabHelper():
    def __init__(self) -> None:
        self.Text=''
        self.PrimaryColour=''
        self.SecondaryColour=''
        self.BorderColor=''
        self.ShadowColor=''
        self.PosX=0.0
        self.PosY=0.0
        self.fontsize=0.0
        self.PrimaryAlpha=''
        self.SecondaryAlpha=''
        self.BorderAlpha=''
        self.ShadowAlpha=''
    
    def Generate(self) -> str:
        _tab = ''
        if (self.PosX,self.PosY) is not None:
            _an = r'\an7'
            _pos = "\\pos({},{})".format(self.PosX,self.PosY)
            _tab += _an + _pos 
        if self.PrimaryColour is not None:
            _c = r'\c' + self.PrimaryColour
            _tab += _c
        if self.SecondaryColour is not None:
            _2c = r'\2c' + self.SecondaryColour
            _tab += _2c
        if self.BorderColor is not None:
            _3c = r'\3c' + self.BorderColor
            _tab += _3c
        if self.ShadowColor is not None:
            _4c = r'\4c' + self.ShadowColor
            _tab += _4c
        if self.fontsize is not None:
            _fs = r'\fs' + self.fontsize
            _tab += _fs
        if self.PrimaryAlpha is not None:
            _1a = r'\1a' + self.PrimaryAlpha
            _tab += _1a
        if self.SecondaryAlpha is not None:
            _2a = r'\2a' + self.SecondaryAlpha
            _tab += _2a
        if self.BorderAlpha is not None:
            _3a = r'\3a' + self.BorderAlpha
            _tab += _3a
        if self.ShadowAlpha is not None:
            _4a = r'\4a' + self.ShadowAlpha
            _tab += _4a
        _text = r'{' + _tab + r'}' + self.Text
        return _text


def _annotation_to_tab(annotation:dict) -> TabHelper():
    tabhelper = TabHelper()
    FullyTransparent = r'&HFF&'
    Text = annotation.Text
    if Text is not  None:
        Text = Text.text.replace('\n',r'\N')
    else:
        Text = ''
    tabhelper.Text=Text
    tabhelper.PrimaryColour=r'&H'+str(hex(int(annotation.fgColor))).replace('0x','').zfill(6).upper()+r'&'
    tabhelper.SecondaryColour=FullyTransparent
    tabhelper.BorderColor=FullyTransparent
    tabhelper.ShadowColor=r'&H'+str(hex(int(annotation.bgColor))).replace('0x','').zfill(6).upper()+r'&'
    tabhelper.PosX=0.0
    tabhelper.PosY=0.0
    tabhelper.fontsize=0.0
    tabhelper.PrimaryAlpha=''
    tabhelper.SecondaryAlpha=''
    tabhelper.BorderAlpha=''
    tabhelper.ShadowAlpha=''
    return tabhelper

class EventHelper():
    def __init__(self,asstools:AssTools()) ->None:
        self.asstools = asstools
        # EventType: 事件类型
        self.EventType:Optional[str] = None
        
        # Layer: 大数值的图层会覆盖在小数值的图层上面
        self.Layer:Optional[int] = None
        
        # Start: 事件的开始时间
        self.Start:Optional[str] = None
        
        # End: 事件的结束时间
        self.End:Optional[str] = None
        
        # Style: 样式名
        self.Style:Optional[str] = None
        
        # Name: 角色名
        self.Name:Optional[str] = None
        
        # MarginL: 左边距覆写
        self.MarginL:Optional[int] = None
        
        # MarginR: 右边距覆写
        self.MarginR:Optional[int] = None
        
        # MarginV: 垂直边距覆写
        self.MarginV:Optional[int] = None
        
        # Effect: 过渡效果
        self.Effect:Optional[str] = None
        
        # Text: 字幕文本
        self.Text:Optional[str] = None
    
    def Commit(self) -> None:
        self.asstools.event.add(EventType=self.EventType,Layer=self.Layer,Start=self.Start,End=self.End,Style=self.Style,Name=self.Name,MarginL=self.MarginL,MarginR=self.MarginR,MarginV=self.MarginV,Effect=self.Effect,Text=self.Text)

def _annotation_to_event(annotation:dict) ->EventHelper() :
    event = EventHelper()
    event.Start = datetime.strftime(annotation.Start,"%H:%M:%S.%f")[:-4]
    event.End = datetime.strftime(annotation.End,"%H:%M:%S.%f")[:-4]
    event.Name = annotation.id
    Text = annotation.Text
    if Text is not  None:
        Text = Text.text.replace('\n',r'\N')
    else:
        Text = ''
    event.Text = Text
    return event

class Annotations2Sub():
    def __init__(self,File:str,Title:str='默认文件',libassHack:bool=False) -> None:
        self.asstools = AssTools()
        self.libassHack = libassHack
        self.asstools.info.add(k='Title',v=Title)
        self.asstools.info.add(k='PlayResX',v='100')
        self.asstools.info.add(k='PlayResY',v='100')
        self.asstools.style.change(Name='Default',Fontname='Microsoft YaHei UI')
        if libassHack is True:
            self.asstools.info.note+='libassHack=True\n'
        self._convert(File=File)
        self.asstools.event.data.sort(key=lambda x:x[1])
    
    def Save(self,File) -> str:
        with open(File + '.ass', 'w', encoding='utf-8') as f:
            f.write(self.asstools.dump())
            print(_("保存于 \"{}.ass\"".format(File)))
            return File + '.ass'
    
    def _convert_(self,File:str) -> None:
        for annotation in AnnotationsParser(File=File):
            event = _annotation_to_event(annotation=annotation)
            tab = _annotation_to_tab(annotation=annotation)
            if annotation.style == 'popup':
                pass
    
    def _convert(self,File) -> None:
        string=open(File,'r',encoding="utf-8").read()
        _xml = xml.etree.ElementTree.fromstring(string)
        for each in _xml.find('annotations').findall('annotation'):
            
            #提取 annotation id
            Name = each.get('id')
            
            #提取时间
            #h:mm:ss.ms
            _Segment = each.find('segment').find('movingRegion').findall('rectRegion')
            if len(_Segment) == 0:
                _Segment = each.find('segment').find('movingRegion').findall('anchoredRegion')
            if len(_Segment) == 0:
                Start = '0:00:00.00'
                End = '0:00:00.00'
            if len(_Segment) != 0:
                Start = min(_Segment[0].get('t'), _Segment[1].get('t'))
                End = max(_Segment[0].get('t'), _Segment[1].get('t'))
            if "never" in (Start, End):
                Start = '0:00:00.00'
                End = '999:00:00.00'
            else:
                try:
                    Start =datetime.strftime(datetime.strptime(Start,"%H:%M:%S.%f"),"%H:%M:%S.%f")[:-4]
                    End = datetime.strftime(datetime.strptime(End,"%H:%M:%S.%f"),"%H:%M:%S.%f")[:-4]
                except:
                    Start =datetime.strftime(datetime.strptime(Start,"%M:%S.%f"),"%H:%M:%S.%f")[:-4]
                    End = datetime.strftime(datetime.strptime(End,"%M:%S.%f"),"%H:%M:%S.%f")[:-4]
            
            #提取样式
            style = each.get('style')
            
            #提取文本
            Text = each.find('TEXT')
            if Text is not  None:
                Text = Text.text.replace('\n',r'\N')
            else:
                Text = ''
            
            
            if each.find('appearance') is None:
                fgColor = r'&HFFFFFF&'
                bgColor = r'&H000000&'
            else:
                fontsize = each.find('appearance').get('textSize')
                if each.find('appearance').get('bgAlpha') is None:
                    bgAlpha = None
                else:
                    bgAlpha = r'&H'+str(hex(int((1-float(each.find('appearance').get('bgAlpha')))*255))).replace('0x','')+r'&'
                if each.find('appearance').get('fgColor') == None:
                    fgColor = r'&HFFFFFF&'
                else:
                    fgColor = r'&H'+str(hex(int(each.find('appearance').get('fgColor')))).replace('0x','').zfill(6).upper()+r'&'
                if each.find('appearance').get('bgColor') == None:
                    bgColor = r'&H000000&'
                else:
                    bgColor = r'&H'+str(hex(int(each.find('appearance').get('bgColor')))).replace('0x','').zfill(6).upper()+r'&'
            
            '''
                x,y: 文本框左上角的坐标
                w,h: 文本框的宽度和高度
            '''
            (x, y, w, h) = map(float,(_Segment[0].get(i) for i in ('x','y','w','h')))
            FullyTransparent = r'&HFF&'
            if style == 'popup':
                Name += r'_popup'
                if self.libassHack == True:
                    w = str(float(w)*1.776)
                TextBox = "m 0 0 l {0} 0 l {0} {1} l 0 {1} ".format(w,h)
                TextBox = r'{\p1}'+ TextBox +r'{\p0}'
                TextBox=self._tab_helper(Text=TextBox,PrimaryColour=bgColor,PosX=x,PosY=y,fontsize=fontsize,PrimaryAlpha=bgAlpha,SecondaryAlpha=FullyTransparent,BorderAlpha=FullyTransparent,ShadowAlpha=FullyTransparent)
                self.asstools.event.add(Start=Start,End=End,Name=Name+r'_TextBox',Text=TextBox)
                Text= self._tab_helper(Text=Text,PrimaryColour=fgColor,PosX=x,PosY=y+4,fontsize=fontsize,SecondaryAlpha=FullyTransparent,BorderAlpha=FullyTransparent,ShadowAlpha=FullyTransparent)
                self.asstools.event.add(Start=Start,End=End,Name=Name,Text=Text)
            elif style == 'title':
                Name +=r'_title'
                fontsize = str(float(fontsize)/4)
                Text= self._tab_helper(Text=Text,PrimaryColour=fgColor,PosX=x,PosY=y,fontsize=fontsize,SecondaryAlpha=FullyTransparent,BorderAlpha=FullyTransparent,ShadowAlpha=FullyTransparent)
                self.asstools.event.add(Start=Start,End=End,Name=Name,Text=Text)
            else:
                print(_("抱歉这个脚本还不能支持 {} 样式. ({})").format(style,Name))
    
    def _tab_helper(self,Text:str='',PrimaryColour:Optional[str]=None,SecondaryColour:Optional[str]=None,BorderColor:Optional[str]=None,ShadowColor:Optional[str]=None,PosX:Optional[float]=None,PosY:Optional[float]=None,fontsize:Optional[str]=None,PrimaryAlpha:Optional[str]=None,SecondaryAlpha:Optional[str]=None,BorderAlpha:Optional[str]=None,ShadowAlpha:Optional[str]=None,p:Optional[str]=None) ->str:
        _tab = ''
        if (PosX,PosY) is not None:
            _an = r'\an7'
            _pos = "\\pos({},{})".format(PosX,PosY)
            _tab += _an + _pos 
        if PrimaryColour is not None:
            _c = r'\c' + PrimaryColour
            _tab += _c
        if SecondaryColour is not None:
            _2c = r'\2c' + SecondaryColour
            _tab += _2c
        if BorderColor is not None:
            _3c = r'\3c' + BorderColor
            _tab += _3c
        if ShadowColor is not None:
            _4c = r'\4c' + ShadowColor
            _tab += _4c
        if fontsize is not None:
            _fs = r'\fs' + fontsize
            _tab += _fs
        if PrimaryAlpha is not None:
            _1a = r'\1a' + PrimaryAlpha
            _tab += _1a
        if SecondaryAlpha is not None:
            _2a = r'\2a' + SecondaryAlpha
            _tab += _2a
        if BorderAlpha is not None:
            _3a = r'\3a' + BorderAlpha
            _tab += _3a
        if ShadowAlpha is not None:
            _4a = r'\4a' + ShadowAlpha
            _tab += _4a
        _text = r'{' + _tab + r'}' + Text
        return _text
        #{\2c&H2425DA&\pos(208,148)}test

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=_('一个可以把Youtube注释转换成ASS字幕的脚本'))
    parser.add_argument('File',type=str,nargs='+',metavar='File or ID',help=_('待转换的文件'))
    parser.add_argument('-l','--libassHack',action='store_true',help=_('针对libass修正'))
    parser.add_argument('-d','--download-for-invidious',action='store_true',help=_('尝试从invidious下载注释文件'))
    parser.add_argument('-i','--invidious-domain',default='invidiou.site', metavar='invidious.domain',help=_('指定invidious域名'))
    parser.add_argument('-p','--preview-video',action='store_true',help=_('预览视频(需要mpv)'))
    parser.add_argument('-g','--generate-video',action='store_true',help=_('生成视频(需要FFmpeg)'))
    args = parser.parse_args()
    libassHack = args.libassHack
    for File in args.File:
        if args.download_for_invidious or args.preview_video or args.generate_video is True:
            Id = File
            File = _download_for_invidious(id=Id,invidious_domain=args.invidious_domain)
        if args.preview_video or args.generate_video is True:
            libassHack = True
        ass = Annotations2Sub(File=File,Title=File,libassHack=libassHack)
        File = ass.Save(File=File)
        del ass
        if args.preview_video is True:
            _preview_video(id=Id,file=File,invidious_domain=args.invidious_domain)
        if args.generate_video is True:
            _generate_video(id=Id,file=File,invidious_domain=args.invidious_domain)
