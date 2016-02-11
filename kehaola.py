#!/usr/bin python
# -*- coding: utf-8 -*-

'''
Please replace these things first:
1. The default IP address and the default port number
2. The hard-coded MP3 file names (or you manually upload the MP3 files with Nao's built-in FTP server.
'''

__author__ = 'x1ang.li'


import time
import argparse
from naoqi import ALProxy, ALBroker, ALModule

class Kehaola(ALModule):

    def __init__(self, handle, ip, port):
        ALModule.__init__(self, handle)
        self._handle = handle
        self._ip = ip
        self._port = port

        tts = ALProxy('ALTextToSpeech', ip, port)
        tts.setLanguage('English')
        self._tts = tts

        aup = ALProxy('ALAudioPlayer', ip, port)
        self._aup = aup

    def sub_all(self):
        self.sub_feetbumper()
        self.sub_handshake()
        self.sub_head()
        self.sub_facerec()

    def unsub_all(self):
        self.unsub_feetbumper()
        self.unsub_handshake()
        self.unsub_head()
        self.unsub_facerec()

    def sub_head(self):
        memory.subscribeToEvent('FrontTactilTouched', self._handle, 'onHeadTouched' )
        memory.subscribeToEvent('RearTactilTouched', self._handle, 'onHeadTouched' )

    def unsub_head(self):
        try:
            memory.unsubscribeToEvent('FrontTactilTouched', self._handle)
            memory.unsubscribeToEvent('RearTactilTouched', self._handle)
        except Exception, e:
            pass

    def onHeadTouched(self, *_args):
        self.unsub_head()
        self._aup.playFile('/home/nao/mp3/kehaola.mp3')
        self.sub_head()

    def sub_feetbumper(self):
        memory.subscribeToEvent('LeftBumperPressed', self._handle, 'onBumperPressed')
        memory.subscribeToEvent('RightBumperPressed', self._handle, 'onBumperPressed')

    def unsub_feetbumper(self):
        memory.unsubscribeToEvent('LeftBumperPressed', self._handle)
        memory.unsubscribeToEvent('RightBumperPressed', self._handle)

    def onBumperPressed(self, *_args):
        self.unsub_feetbumper()
        self._aup.playFile('/home/nao/mp3/ouch_it_hurts.mp3')
        self.sub_feetbumper()

    def sub_handshake(self):
        memory.subscribeToEvent('HandRightBackTouched', self._handle, 'onHandTouched')
        memory.subscribeToEvent('HandRightLeftTouched', self._handle, 'onHandTouched')
        memory.subscribeToEvent('HandRightRightTouched', self._handle, 'onHandTouched')

    def unsub_handshake(self):
        memory.unsubscribeToEvent('HandRightBackTouched', self._handle)
        memory.unsubscribeToEvent('HandRightLeftTouched', self._handle)
        memory.unsubscribeToEvent('HandRightRightTouched', self._handle)

    def onHandTouched(self, *_args):
        self.unsub_handshake()
        self._aup.playFile('/home/nao/mp3/shakehands.mp3')
        self.sub_handshake()

    def sub_facerec(self):
        memory.subscribeToEvent('FaceDetected', self._handle, 'onFaceDetected')

    def unsub_facerec(self):
        memory.unsubscribeToEvent('FaceDetected', self._handle)

    def onFaceDetected(self, *_args):
        self.unsub_facerec()
        self._tts.say("Hi, yo!")
        time.sleep(45)
        self.sub_facerec()

def main(ip, port):

    broker = ALBroker('pythonBroker', '0.0.0.0', 9999, ip, port)

    global memory
    memory = ALProxy('ALMemory', ip, port)

    global kehaola
    kehaola = Kehaola('kehaola', ip, port)
    kehaola.sub_all()

    time.sleep(60)

    kehaola.unsub_all()
    broker.shutdown()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help="Robot ip address")
    parser.add_argument('--port', type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
