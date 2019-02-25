# -*- coding: utf-8 -*-

import os
import tempfile
import subprocess
import requests
import json
import logging
logger = logging.getLogger(__name__)

def mp3_2_wav(_path = None, _byte = None):
    ''' MP3转WAV
    _path和_byte必须存在一个, 优先级_path > _byte
    :param _path:
    :param _byte:
    :return: wav的字节流
    '''
    try:
        if _path is None and _byte is None: return
        temp = None
        if _path is None: # 字节流存入临时文件
            temp = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
            temp.write(_byte)
            temp.seek(0)
            _path = temp.name
        if _path is None: return
        # 根据要求进行格式转换,-t 60 最大保存60秒, 采样率 16K, 默认单声道
        logger.info('mp3 ==> wav ========================')
        target_file = tempfile.NamedTemporaryFile(mode="w+b", delete=False, suffix='.wav')
        _perfix = r'ffmpeg'
        command = [_perfix, '-y', '-t', '60', '-i', _path, '-ar', '16K', target_file.name]
        return_code = subprocess.call(command)
        logger.info('mp3 ==> wav ==={}====================='.format(return_code))
        if return_code == 0:
            target_file.seek(0)
            _byte = target_file.read()
            target_file.close()
            os.remove(target_file.name)
            if temp is not None:
                temp.close()
                os.remove(temp.name)
            return _byte
    except Exception as e:
        logger.error('mp3_2_wav error [{}]'.format(e))



def BAIDU_ASR(_path):
    ''' 百度语音转文字

    :param _path:
    :return:
    '''
    from aip import AipSpeech
    """ 你的 APPID AK SK """
    APP_ID = '11799942'                                  #'你的 App ID'
    API_KEY = 'rHrU07N71C4QTRCGGXnc4ucz'                 #'你的 Api Key'
    SECRET_KEY = 'L4g3GzoagB3PTAd5qkT1QVMhu3sQL1ku'      #'你的 Secret Key'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.asr(mp3_2_wav(_path), 'pcm', 16000, {
        'dev_pid': '1537',
    })
    return result.get('result')[0]

def BAIDU_Speech_Recognizer(_byte):
    ''' 百度语音转文字

    :param _path:
    :return:
    '''
    from aip import AipSpeech
    """ 你的 APPID AK SK """
    APP_ID = '11799942'                                  #'你的 App ID'
    API_KEY = 'rHrU07N71C4QTRCGGXnc4ucz'                 #'你的 Api Key'
    SECRET_KEY = 'L4g3GzoagB3PTAd5qkT1QVMhu3sQL1ku'      #'你的 Secret Key'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.asr(_byte, 'pcm', 16000, {
        'dev_pid': '1537',
    })
    return result.get('result')[0]

from aip import AipSpeech

class SpeechRecognizer(object):
    def __init__(self, language="en", rate=44100, retries=3):
        self.language = language
        self.rate = rate
        self.retries = retries



    def __call__(self, data):
        try:
            for i in range(self.retries):

                try:
                    APP_ID = '11799942'  # '你的 App ID'
                    API_KEY = 'rHrU07N71C4QTRCGGXnc4ucz'  # '你的 Api Key'
                    SECRET_KEY = 'L4g3GzoagB3PTAd5qkT1QVMhu3sQL1ku'  # '你的 Secret Key'
                    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
                    resp = client.asr(data, 'wav', 16000, {
                        'dev_pid': '1536',
                    })
                except requests.exceptions.ConnectionError:
                    continue
                if resp.__contains__('result'):
                    result = ''.join(resp['result'])
                    print result
                    # if end with comma, remove it
                    if result.endswith(u'，'):
                        result = result[:-1]
                    return result


        except KeyboardInterrupt:
            return ''
