# -*- coding: utf-8 -*-
"""
LM75A_tool
~~~~~~~~~~~~~
:license: MIT
"""
import os
import sys
import argparse


def parse_args(in_args):
    """
    Parses arguments and passes them to the main function
    """
    parser = argparse.ArgumentParser(description='Set the temperature ranges for LM75A')

    parser.add_argument(
    '-a', '--all',
    help='Upload all',
    dest='all',
    default=0x4f)

    parser.add_argument(
    '-d', '--del',
    help='delete all',
    dest='del',
    default='1')

    return parser.parse_args(in_args)


class Uploader():
    def __init__(self, args: str):
        self._filelist = filelist
        self._port = PORT
        self._baud = BAUD

    def add_all(self):
        filelist = os.listdir()
        PORT = '/dev/ttyUSB0'
        BAUD = '115200'

        print('Python files found:')
        for f in self._filelist:
            if f.endswith('py'):
                print('\t{0}'.format(f))

        for f in self._filelist:
            if f.endswith('py'):
                status = os.system('ampy -p {0} -b {1} put {2}'.format(self._port, self._baud, f))
                if status == 256:
                    print('Uploading {0} failed'.format(f))
                elif status == 0:
                    print('{0}\t\tuploaded successfully'.format(f))
                else:
                    print('{0}\t\tuploaded with status {1}'.format(f, status))

    def delete_all(self):
        pass


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    filelist = os.listdir()
    PORT = '/dev/ttyUSB0'
    BAUD = '115200'
    tool = LM75A_tool(args, filelist, PORT, BAUD)
