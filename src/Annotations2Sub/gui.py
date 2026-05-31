# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Optional

from Annotations2Sub.cli_utils import (
    AnnotationsStringIsEmptyError,
    AnnotationsXmlStringToSubtitlesString,
)
from Annotations2Sub.Annotations import NotAnnotationsDocumentError
from xml.etree.ElementTree import ParseError
from Annotations2Sub.i18n import _


class GUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(_("Annotations2Sub GUI"))
        self.root.geometry("600x500")

        self.queue: List[str] = []
        self.output_directory: Optional[str] = None

        self._setup_ui()

    def _setup_ui(self):
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 文件选择
        file_frame = ttk.LabelFrame(main_frame, text=_("文件选择"), padding="5")
        file_frame.pack(fill=tk.X, pady=5)

        self.file_listbox = tk.Listbox(file_frame, height=5)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        file_btn_frame = ttk.Frame(file_frame)
        file_btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        ttk.Button(file_btn_frame, text=_("添加文件"), command=self._add_files).pack(fill=tk.X)
        ttk.Button(file_btn_frame, text=_("清空列表"), command=self._clear_files).pack(fill=tk.X)

        # 参数设置
        config_frame = ttk.LabelFrame(main_frame, text=_("配置参数"), padding="5")
        config_frame.pack(fill=tk.X, pady=5)

        # 分辨率
        res_frame = ttk.Frame(config_frame)
        res_frame.pack(fill=tk.X, pady=2)
        ttk.Label(res_frame, text=_("分辨率 X:")).pack(side=tk.LEFT)
        self.res_x = tk.IntVar(value=1000)
        ttk.Entry(res_frame, textvariable=self.res_x, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(res_frame, text=_("分辨率 Y:")).pack(side=tk.LEFT)
        self.res_y = tk.IntVar(value=1000)
        ttk.Entry(res_frame, textvariable=self.res_y, width=10).pack(side=tk.LEFT, padx=5)

        # 字体
        font_frame = ttk.Frame(config_frame)
        font_frame.pack(fill=tk.X, pady=2)
        ttk.Label(font_frame, text=_("指定字体:")).pack(side=tk.LEFT)
        self.font_name = tk.StringVar(value=_("Microsoft YaHei"))
        ttk.Entry(font_frame, textvariable=self.font_name).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 其他选项
        opt_frame = ttk.Frame(config_frame)
        opt_frame.pack(fill=tk.X, pady=2)
        self.no_overwrite = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_frame, text=_("不覆盖已有文件"), variable=self.no_overwrite).pack(side=tk.LEFT)

        # 输出目录
        out_frame = ttk.Frame(main_frame)
        out_frame.pack(fill=tk.X, pady=5)
        ttk.Label(out_frame, text=_("输出目录:")).pack(side=tk.LEFT)
        self.out_dir_var = tk.StringVar(value=_("(默认原始目录)"))
        ttk.Entry(out_frame, textvariable=self.out_dir_var, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(out_frame, text=_("选择目录"), command=self._select_out_dir).pack(side=tk.RIGHT)

        # 进度条
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, pady=10)

        # 转换按钮
        self.convert_btn = ttk.Button(main_frame, text=_("开始转换"), command=self._start_conversion)
        self.convert_btn.pack(pady=5)

        # 可折叠日志
        log_ctrl_frame = ttk.Frame(main_frame)
        log_ctrl_frame.pack(fill=tk.X)
        self.log_visible = tk.BooleanVar(value=False)
        self.log_toggle_btn = ttk.Checkbutton(log_ctrl_frame, text=_("显示/隐藏日志"), variable=self.log_visible, command=self._toggle_log, style="Toggle.TButton")
        self.log_toggle_btn.pack(side=tk.LEFT)

        self.log_frame = ttk.Frame(main_frame)
        # 初始不 pack log_frame

        self.log_text = tk.Text(self.log_frame, height=8, state=tk.DISABLED)
        log_scroll = ttk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _toggle_log(self):
        if self.log_visible.get():
            self.log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        else:
            self.log_frame.pack_forget()

    def _add_files(self):
        files = filedialog.askopenfilenames(
            title=_("选择 XML 注释文件"),
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        for f in files:
            if f not in self.queue:
                self.queue.append(f)
                self.file_listbox.insert(tk.END, f)

    def _clear_files(self):
        self.queue.clear()
        self.file_listbox.delete(0, tk.END)

    def _select_out_dir(self):
        directory = filedialog.askdirectory(title=_("选择输出目录"))
        if directory:
            self.output_directory = directory
            self.out_dir_var.set(directory)

    def _log(self, message: str):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
        self.root.update_idletasks()

    def _start_conversion(self):
        if not self.queue:
            messagebox.showwarning(_("警告"), _("请先添加要转换的文件"))
            return

        self.convert_btn.configure(state=tk.DISABLED)
        self.progress["value"] = 0
        self.progress["maximum"] = len(self.queue)
        
        # 如果日志不可见，自动打开它以显示进度
        if not self.log_visible.get():
            self.log_visible.set(True)
            self._toggle_log()

        self._log(_("开始转换任务..."))
        
        success_count = 0
        for i, file_path in enumerate(self.queue):
            try:
                self._log(_("正在处理: {}").format(os.path.basename(file_path)))
                
                # 读取文件
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # 执行转换
                subtitle_string = AnnotationsXmlStringToSubtitlesString(
                    content,
                    self.res_x.get(),
                    self.res_y.get(),
                    self.font_name.get(),
                    os.path.basename(file_path)
                )

                # 确定输出路径
                if self.output_directory:
                    out_path = os.path.join(self.output_directory, os.path.basename(file_path) + ".ass")
                else:
                    out_path = file_path + ".ass"

                # 检查是否覆盖
                if self.no_overwrite.get() and os.path.exists(out_path):
                    self._log(_("跳过 (文件已存在): {}").format(out_path))
                else:
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(subtitle_string)
                    self._log(_("成功保存至: {}").format(out_path))
                    success_count += 1

            except NotAnnotationsDocumentError:
                self._log(_("错误: {} 不是有效的 Annotations 文件").format(file_path))
            except ParseError:
                self._log(_("错误: {} XML 解析失败").format(file_path))
            except AnnotationsStringIsEmptyError:
                self._log(_("错误: {} 是空文件").format(file_path))
            except Exception as e:
                self._log(_("未知错误 ({}): {}").format(file_path, str(e)))

            self.progress["value"] = i + 1
            self.root.update_idletasks()

        self._log(_("所有任务完成。成功: {}, 失败: {}").format(success_count, len(self.queue) - success_count))
        self.convert_btn.configure(state=tk.NORMAL)
        messagebox.showinfo(_("完成"), _("转换任务已结束"))


def RunGUI():
    root = tk.Tk()
    # 尝试设置图标（如果存在）
    # root.iconbitmap("path_to_icon.ico")
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    RunGUI()
