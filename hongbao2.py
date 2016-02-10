#!/usr/bin python
# -*- coding: utf-8 -*-

import time
import argparse
from naoqi import ALProxy, ALBroker, ALModule

defaultIP = '127.0.0.1'

class Hongbao(ALModule):
    def __init__(self, handle, ip, port):
        ALModule.__init__(self, handle)
        self._handle = handle
        self._ip = ip
        self._port = port

        tts = ALProxy('ALTextToSpeech', ip, port)
        tts.setLanguage('Chinese')
        self._tts = tts

        aup = ALProxy('ALAudioPlayer', ip, port)
        self._aup = aup

        self._motion = ALProxy('ALMotion', self._ip, self._port)
        self._posture = ALProxy('ALRobotPosture', self._ip, self._port)

        self.initMotion()
        # self.caliberate()

    def sub_footpressed(self):
        memory.subscribeToEvent('LeftBumperPressed', self._handle, 'onBumperPressed')
        memory.subscribeToEvent('RightBumperPressed', self._handle, 'onBumperPressed')

    def unsub_footpressed(self):
        memory.unsubscribeToEvent('LeftBumperPressed', self._handle)
        memory.unsubscribeToEvent('RightBumperPressed', self._handle)

    def initMotion(self):
        motion = self._motion
        posture = self._posture

        motion.wakeUp()
        # posture.goToPosture('Stand', 0.5)

        joints = [
            'HeadYaw',
            'HeadPitch',
            'LShoulderPitch',
            'LShoulderRoll',
            'LElbowYaw',
            'LElbowRoll',
            'LWristYaw',
            'LHipYawPitch',
            'LHipRoll',
            'LHipPitch',
            'LKneePitch',
            'LAnklePitch',
            'LAnkleRoll',
            'RHipYawPitch',
            'RHipRoll',
            'RHipPitch',
            'RKneePitch',
            'RAnklePitch',
            'RAnkleRoll',
            'RShoulderPitch',
            'RShoulderRoll',
            'RElbowYaw',
            'RElbowRoll',
            'RWristYaw',
        ]
        angles_A = [
            -0.9,
            -0.5,
            1.52,
            0.7,
            0,
            -1.39,
            0.04,
            -0.17,
            0.1,
            0.13,
            -0.1,
            0.1,
            -0.13,
            -0.17,
            -0.1,
            0.13,
            -0.1,
            0.1,
            0.13,
            -1.76,
            -0.9,
            1.3,
            0.18,
            -0.42,
        ]
        angles_B = [
            -0.6,
            -0.3,
            1.52,
            0.7,
            0,
            -1.39,
            0.04,
            -0.19,
            0.11,
            -0.35,
            0.98,
            -0.44,
            -0.12,
            -0.19,
            -0.2,
            -0.29,
            0.94,
            -0.48,
            0.19,
            -1.76,
            -0.9,
            0,
            1.54,
            -0.42,
        ]

        motion.angleInterpolation(joints, [[x] for x in angles_B], [1] * len(joints) , True)


    def caliberate(self):
        motion = self._motion
        tts = self._tts
        time.sleep(1)
        tts.say("记录位置") # recording position

        motion.setStiffnesses('Head', 0)
        motion.setStiffnesses('RArm', 0)
        motion.setStiffnesses('LLeg', 0)
        motion.setStiffnesses('RLeg', 0)
        time.sleep(4)

        tts.say("记录完毕") # end-of recording position
        print motion.getSummary()
        motion.setStiffnesses('Head', 1)
        motion.setStiffnesses('RArm', 1)
        motion.setStiffnesses('LLeg', 1)
        motion.setStiffnesses('RLeg', 1)


    def onBumperPressed(self):
        self.unsub_footpressed()

        motion = self._motion

        joints = [
            'HeadYaw',
            'HeadPitch',
            'LShoulderPitch',
            'LShoulderRoll',
            'LElbowYaw',
            'LElbowRoll',
            'LWristYaw',
            'LHipYawPitch',
            'LHipRoll',
            'LHipPitch',
            'LKneePitch',
            'LAnklePitch',
            'LAnkleRoll',
            'RHipYawPitch',
            'RHipRoll',
            'RHipPitch',
            'RKneePitch',
            'RAnklePitch',
            'RAnkleRoll',
            'RShoulderPitch',
            'RShoulderRoll',
            'RElbowYaw',
            'RElbowRoll',
            'RWristYaw',
        ]

        angles_A = [
            -0.9,
            -0.5,
            1.52,
            0.7,
            0,
            -1.39,
            0.04,
            -0.17,
            0.1,
            0.13,
            -0.1,
            0.1,
            -0.13,
            -0.17,
            -0.1,
            0.13,
            -0.1,
            0.1,
            0.13,
            -1.76,
            -0.9,
            1.3,
            0.18,
            -0.42,
        ]
        angles_B = [
            -0.6,
            -0.3,
            1.52,
            0.7,
            0,
            -1.39,
            0.04,
            -0.19,
            0.11,
            -0.35,
            0.98,
            -0.44,
            -0.12,
            -0.19,
            -0.2,
            -0.29,
            0.94,
            -0.48,
            0.19,
            -1.76,
            -0.9,
            0,
            1.54,
            -0.42,
        ]

        theta = 0.4
        pos_seq = [angles_A, angles_B, angles_A, angles_B]
        angle_series = zip(*pos_seq)
        times = [theta * (i+1) for i in range(len(pos_seq))]

        time.sleep(3)
        motion.angleInterpolation(joints, angle_series, [times] * len(joints), True)

        time.sleep(1.5)
        motion.angleInterpolation(joints, angle_series, [times] * len(joints), True)

        self.sub_footpressed()

def main(ip, port):
    broker = ALBroker('pythonBroker', '0.0.0.0', 9999, ip, port)

    global memory
    memory = ALProxy('ALMemory', ip, port)

    global hongbao
    hongbao = Hongbao('hongbao', ip, port)
    try:
        hongbao.unsub_footpressed()
    except Exception,e:
        pass
    hongbao.sub_footpressed()

    time.sleep(600)

    hongbao.unsub_footpressed()
    broker.shutdown()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default=defaultIP,
                        help="Robot ip address")
    parser.add_argument('--port', type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
