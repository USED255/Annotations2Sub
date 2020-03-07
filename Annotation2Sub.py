#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__  = (
    'wrtyis@outlook.com'
	)

__license__ = 'WTFPL'
__version__ = '0.0.1'

"""
ASS 字幕格式规范:
https://github.com/weizhenye/ASS/wiki/ASS-%E5%AD%97%E5%B9%95%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83

"""

#祝 Google 亲妈爆炸!

import xml.etree.ElementTree
import sys

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print("Usage: {0} <file> " .format(sys.argv[0]))
        exit(0)
    xml_file=sys.argv[1]
    xml_data = open(xml_file,'r',encoding="utf-8").read()
    ass = Annotations2Sub(xml_data)
    ass.save("{0}.ass".format(xml_file))

class Annotations2Sub(object):
    def _init_(self,string):
        self.xml = xml.etree.ElementTree.fromstring(string)
        self.convert(self.xml) 

    def convert(self,string):
        AssTools.init
        AssTools.info.change
        
        while(True):
            AssTools.events.add

class AssTools(object):
    def init(self,Title,ScaledBorderAndShadow,PlayResX,PlayResY):
        self.info.init()
        self.styles.init()
        self.events.init()

    def save(self,filename):
        self.data += self.info.dump
        self.data += self.styles.dump
        self.data += self.events.dump
        with open(filename, 'w',encoding='utf-8') as f:
            f.write(self.data)

    def info(self):
        def init(self,Title,ScaledBorderAndShadow,PlayResX,PlayResY):
            self.Script_Info =      "[Script Info]\n" \
                                    "; Script generated by Annotations2Sub\n"\
                                    "; https://github.com/WRTYis/Annotations2Sub\n"\
                                    "Title: Default file\n"\
                                    "ScriptType: v4.00+\n"\
                                    "WrapStyle: 0\n"\
                                    "ScaledBorderAndShadow: yes\n"\
                                    "YCbCr Matrix: None\n"\
                                    "PlayResX: 1920\n"\
                                    "PlayResY: 1080\n"\
                                    "\n"

        def change(self,Title,ScaledBorderAndShadow,PlayResX,PlayResY):
            pass

        def dump(self):
            pass

    def styles(self):
        def init(self):
            self.V4_Styles =        "[V4+ Styles]\n"\
                                    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"
            self.styles = {}
            self.styles.add()

        def add(styles,Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding):
            pass
        
        def dump(self):
            pass

    def events(self):
        def init(self):
            self.Events =           "[Events]\n"\
                                    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

            self.events = {}

        def add(Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text):
            pass

        def dump(self):
            pass

    def tab_helper(self,string):
        pass
        return '0'

if __name__ == "__main__":
    main()
