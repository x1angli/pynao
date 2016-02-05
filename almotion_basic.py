# -*- encoding: UTF-8 -*-

'''
    Wake up the robot, open his left hand, close that hand, and take a rest position.
    As a developer, you need to learn how to read the info provided by motion.getSummary()
'''


import sys, time
from naoqi import ALProxy

def main(ip, port):
    motion = ALProxy("ALMotion", ip, port)

    motion.wakeUp()
    print motion.getSummary()
    time.sleep(2)

    motion.openHand('LHand')
    time.sleep(2)

    motion.closeHand('LHand')
    time.sleep(2)

    motion.rest()
    print motion.getSummary()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", type=str, default='127.0.0.1', help="Robot ip address")
        parser.add_argument("--port", type=int, default=9559, help="Robot port number")

        args = parser.parse_args()
        ip = args.ip
        port = args.port
    else:
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read('local.ini')
        try:
            ip = config.get('Robot', 'ip')
        except Exception,e:
            ip = '127.0.0.1'
        try:
            port = config.getint('Robot', 'port')
        except Exception,e:
            port = 9559
    print ip, port
    main(ip, port)
