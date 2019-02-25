# -*- coding: utf-8 -*-

# 使用的工具是ffmpeg, ffmpeg的安装和配置请自行百度。

import tempfile
import subprocess
import os

class FLACConverter(object):
    def __init__(self, source_path, include_before=0.25, include_after=0.25):
        self.source_path = source_path
        self.include_before = include_before
        self.include_after = include_after

    def __call__(self, region):
        try:
            start, end = region
            start = max(0, start - self.include_before)
            end += self.include_after
            #temp = tempfile.NamedTemporaryFile(suffix='.flac')
            temp = tempfile.NamedTemporaryFile(suffix='.wav')
            command = ["ffmpeg","-ss", str(start), "-t", str(end - start),
                       "-y", "-i", self.source_path,
                       "-loglevel", "error", temp.name]
            subprocess.check_output(command, stdin=open(os.devnull))
            return temp.read()

        except KeyboardInterrupt:
            return
