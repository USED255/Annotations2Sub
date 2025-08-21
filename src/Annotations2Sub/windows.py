import ctypes
import sys

from Annotations2Sub.i18n import _


def tips_double_clicked_on_windows():
    if sys.platform != "win32":
        return

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    array = (ctypes.c_uint * 1)()
    num = kernel32.GetConsoleProcessList(array, 1)

    # 如果是 GUI 启动，一般其他进程没附加控制台，num == 1（或 2 视具体环境而定）
    if num > 2:
        return

    message = _("这是一个命令行工具，请在命令提示符下运行。")
    title = _("提示")
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
