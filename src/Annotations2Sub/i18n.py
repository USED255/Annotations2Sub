# -*- coding: utf-8 -*-

"""On n'habite pas un pays, on habite une langue. Une patrie, c'est cela et rien d'autre."""

import gettext
import locale
import os
import sys


def internationalization():
    def f():
        def get_locales_path():
            def f1():
                from importlib import resources
                package = __package__ or 'Annotations2Sub'
                locales = str(resources.files(package) / "locales")
                return locales

            def f2():
                locales = os.path.join(os.path.split(os.path.realpath(__file__))[0], "locales")
                return locales

            try:
                return f1()
            except (ImportError, FileNotFoundError):
                return f2()

        locales = get_locales_path()

        # https://stackoverflow.com/a/8377533
        if sys.platform == "win32":
            if os.getenv("LANG") == None:
                lang, __ = locale.getdefaultlocale()
                if lang != None:
                    os.environ["LANG"] = lang

        en = gettext.translation(
            "Annotations2Sub",
            locales,
            languages=["en"],
        )
        translate = gettext.translation(
            "Annotations2Sub",
            locales,
        )
        translate.add_fallback(en)
        return translate.gettext

    try:
        return f()
    except FileNotFoundError:
        print("\033[31m翻译文件加载失败\033[0m", file=sys.stderr)
        return gettext.gettext


_ = internationalization()
