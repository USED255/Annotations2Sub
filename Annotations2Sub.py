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

class Annotations():
    def __init__(self):
        ## type: 字符串格式的注释类型, 可能的值包括text和pause
        self.type = None
        # id: 字符串格式的注释id
        self.id = None
        # style: 字符串格式的注释样式, 可能的值包括title, speech, popup, highlightText, anchored, 和branding
        self.style = None
        # Text: 字符串格式的注释文本
        self.Text = None
        
        # Start: time格式的注释的开始时间
        self.Start = None
        # End: time格式的注释的结束时间
        self.End = None
        
        # textSize: 浮点数格式的文字大小占影片高度的百分比。
        self.textSize = None
        # bgAlpha: 浮点数格式的背景透明度, 范围从0到1
        self.bgAlpha = None
        # fgColor: 整数格式的十进制的注释前景色 RGB颜色 0-255
        self.fgColor = None
        # bgColor: 整数格式的十进制的注释背景色 RGB颜色 0-255
        self.bgColor = None
        
        # x: 浮点数格式的注释的x坐标, 以视频宽度的百分比表示
        self.x = None
        # y: 浮点数格式的注释的y坐标, 以视频宽度的百分比表示
        self.y = None
        # w: 浮点数格式的注释的宽度, 以视频宽度的百分比表示
        self.w = None
        # h: 浮点数格式的注释的高度, 以视频高度的百分比表示
        self.h = None
        # sx: 浮点数格式的语音气泡点x轴位置, 以视频宽度的百分比表示
        self.sx = None
        # sy: 浮点数格式的语音气泡点y轴位置, 以视频高度的百分比表示
        self.sy = None
    
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
        def _p_f(_f):
            if _f is not None:
                return float(_f)
            else:
                return None
        
        type = each.get('type')
        if type is None or type == 'pause':
            return None
        
        _appearance = each.find('appearance')
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
        
        annotations = Annotations()

        annotations.type = type 
        annotations.id = each.get('id') 
        annotations.style = each.get('style') 
        annotations.Text = each.find('TEXT')
        
         
        annotations.Start = Start 
        annotations.End = End
         
        annotations.textSize = float(_appearance.get('textSize'))
        annotations.bgAlpha = float(_appearance.get('bgAlpha'))
        annotations.fgColor = float(_appearance.get('fgColor'))
        annotations.bgColor = float(_appearance.get('bgColor'))
         
        annotations.x = float(_segment[0].get('x')) 
        annotations.y = float(_segment[0].get('y')) 
        annotations.w = float(_segment[0].get('w')) 
        annotations.h = float(_segment[0].get('h')) 
        annotations.sx = _p_f(_segment[0].get('sx')) 
        annotations.sy = _p_f(_segment[0].get('sy'))
        
        return annotations
    
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
        self.Text = None
        self.PrimaryColour = None
        self.SecondaryColour = None
        self.BorderColor = None
        self.ShadowColor = None
        self.PosX = None
        self.PosY = None
        self.fontsize = None
        self.PrimaryAlpha = None
        self.SecondaryAlpha = None
        self.BorderAlpha = None
        self.ShadowAlpha = None
    
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
            _fs = r'\fs' + str(self.fontsize)
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
        if self.Text is None:
            self.Text = ''
        _text = r'{' + _tab + r'}' + self.Text
        return _text

def _annotation_to_tab(annotation:dict) -> TabHelper:
    tabhelper = TabHelper()
    tabhelper.PosX=annotation.x
    tabhelper.PosY=annotation.y
    tabhelper.fontsize=annotation.textSize
    tabhelper.SecondaryAlpha=r'&HFF&'
    tabhelper.BorderAlpha=r'&HFF&'
    tabhelper.ShadowAlpha=r'&HFF&'
    return tabhelper

class Colour():
    def __init__(self):
        self.bgAlpha = None
        self.fgColor = None
        self.bgColor = None
        self.FullyTransparent = None

def _colour_helper(annotation:dict) ->dict:
    colour = Colour()
    colour.bgAlpha = r'&H'+str(hex(int((1-float(annotation.bgAlpha) *255)))).replace('0x','')+r'&'
    colour.fgColor = r'&H'+str(hex(int(annotation.fgColor))).replace('0x','').zfill(6).upper()+r'&'
    colour.bgColor = r'&H'+str(hex(int(annotation.bgColor))).replace('0x','').zfill(6).upper()+r'&'
    colour.FullyTransparent = r'&HFF&'
    return colour

def _text_helper(annotation:dict) ->dict:
    if annotation.Text is not  None:
        return annotation.Text.text.replace('\n',r'\N')
    else:
        return ''

class EventHelper():
    def __init__(self,asstools:AssTools) ->None:
        self.asstools = asstools

        # EventType: 事件类型
        self.EventType:str = 'Dialogue'
        # Layer: 大数值的图层会覆盖在小数值的图层上面
        self.Layer:int = 0
        # Start: 事件的开始时间
        self.Start:str = '0:00:00.00'
        # End: 事件的结束时间
        self.End:str = '0:00:00.00'
        # Style: 样式名
        self.Style:str = 'Default'
        # Name: 角色名
        self.Name:str = ''
        # MarginL: 左边距覆写
        self.MarginL:int = 0
        # MarginR: 右边距覆写
        self.MarginR:int = 0
        # MarginV: 垂直边距覆写
        self.MarginV:int = 0
        # Effect: 过渡效果
        self.Effect:str = ''
        # Text: 字幕文本
        self.Text:str = ''
    
    def Commit(self) -> None:
        self.asstools.event.add(EventType=self.EventType,Layer=self.Layer,Start=self.Start,End=self.End,Style=self.Style,Name=self.Name,MarginL=self.MarginL,MarginR=self.MarginR,MarginV=self.MarginV,Effect=self.Effect,Text=self.Text)

def _annotation_to_event(annotation:dict,asstools:AssTools) ->EventHelper :
    event = EventHelper(asstools=asstools)
    event.Start = datetime.strftime(annotation.Start,"%H:%M:%S.%f")[:-4]
    event.End = datetime.strftime(annotation.End,"%H:%M:%S.%f")[:-4]
    event.Name = annotation.id
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
        self.asstools.event.data.sort(key=lambda x:x[2])
    
    def Save(self,File) -> str:
        with open(File + '.ass', 'w', encoding='utf-8') as f:
            f.write(self.asstools.dump())
            print(_("保存于 \"{}.ass\"".format(File)))
            return File + '.ass'
    
    def _convert(self,File:str) -> None:
        for annotation in AnnotationsParser(File=File):
            event = _annotation_to_event(annotation=annotation,asstools=self.asstools)
            tab = _annotation_to_tab(annotation=annotation)
            if annotation.style == 'popup':
                event.Name += r'_popup_TextBox'
                if self.libassHack == True:
                    annotation.w = annotation.w  *1.776
                TextBox = "m 0 0 l {0} 0 l {0} {1} l 0 {1} ".format(annotation.w,annotation.h)
                TextBox = r'{\p1}'+ TextBox +r'{\p0}'
                colour = _colour_helper(annotation=annotation)
                tab.Text = TextBox
                tab.PrimaryColour = colour.bgColor
                tab.PrimaryAlpha = colour.bgAlpha
                event.Text = tab.Generate()
                event.Commit()
                event.Name = annotation.id
                event.Name += r'_popup'
                tab.Text = _text_helper(annotation=annotation)
                event.Text = tab.Generate()
                event.Commit()
            elif annotation.style == 'title':
                event.Name += r'_title'
                tab.Text = _text_helper(annotation=annotation)
                tab.fontsize = tab.fontsize/4
                event.Text = tab.Generate()
                event.Commit()
            else:
                print(_("抱歉这个脚本还不能支持 {} 样式. ({})").format(annotation.style,annotation.id))

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
