#!/usr/bin/env python3

import argparse
import json
import os
import re
import socket
import struct
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Lock as ProcLock
from multiprocessing import Manager
from threading import Lock as ThreadLock

WRITE_LOCK_PROC = ProcLock()
WRITE_LOCK_THREAD = ThreadLock()


def findIPs(start, end):
    ipstruct = struct.Struct('>I')
    start, = ipstruct.unpack(socket.inet_aton(start))
    end, = ipstruct.unpack(socket.inet_aton(end))
    return [socket.inet_ntoa(ipstruct.pack(i)) for i in range(start, end + 1)]


def isIPv4(ip_str):
    compile_ip = re.compile('^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
    if compile_ip.match(ip_str):
        return True
    else:
        return False


class BaseException(Exception):
    """An error occurred."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message or self.__class__.__doc__


class InvalidAttribute(BaseException):
    pass


class HostScanner:
    def __init__(self, function, number, method,
                 port_range=None, ip_range=None, verbose=False, write_json=False, json_file='./result.json'):
        self.function = function
        self.number = number
        self.method = method
        self.port_range = port_range
        self.ip_range = ip_range
        self.write_json = write_json
        self._verbose = verbose
        self.json_file = json_file

        self._PoolExecutor = ThreadPoolExecutor if self.method == 'thread' else ProcessPoolExecutor
        self.que = Manager().Queue(1)

    def _update_json_file(self):
        if self._verbose:
            print(f"Write the results in the queue to {self.json_file}")
        json_update = {}
        while not self.que.empty():
            json_update.update(self.que.get())

        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as fr:
                json_content = json.loads(fr.read())
                json_content.update(json_update)

            with open(self.json_file, 'w') as fw:
                fw.write(json.dumps(json_content, indent=4))
        else:
            with open(self.json_file, 'w') as fw:
                fw.write(json.dumps(json_update, indent=4))

    def _ping_host_ip(self, ip):
        if self._verbose:
            print("pid is %s" % os.getpid())
        try:
            res = subprocess.call('ping -c 2 -t 2 %s' % ip, shell=True, stdout=subprocess.PIPE)
            status = 'Active' if res == 0 else 'Inactive'
            print(f'{ip} {status}')

            if self.write_json:
                if self.method == 'proc':
                    with WRITE_LOCK_PROC:
                        if self.que.full():
                            self._update_json_file()
                elif self.method == 'thread':
                    with WRITE_LOCK_THREAD:
                        if self.que.full():
                            self._update_json_file()
                self.que.put({ip: status})

        except Exception as e:
            print('Failed to get status for {}: {}'.format(ip, e))

    def _scan_host_port(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ip_range, port))

            print(f'{port} OPEN')
            if self.write_json:
                if self.method == 'proc':
                    with WRITE_LOCK_PROC:
                        if self.que.full():
                            self._update_json_file()
                elif self.method == 'thread':
                    with WRITE_LOCK_THREAD:
                        if self.que.full():
                            self._update_json_file()
                self.que.put({port: 'OPEN'})
        except Exception as e:
            # Ignore the failed port
            pass
        finally:
            s.close()

    def _runMultiWorks(self):
        with self._PoolExecutor(self.number) as Executor:
            if self.function == 'tcp':
                print(f'The scanned host is {self.ip_range}')
                Executor.map(self._scan_host_port, list(self.port_range))
            elif self.function == 'ping':
                Executor.map(self._ping_host_ip, self.ip_range)

    def run(self):
        # In order to support multiple debugging,
        # delete the generated json file in the first run
        if os.path.exists(self.json_file):
            os.remove(self.json_file)

        if self._verbose:
            print('Start')
            print('*' * 20)

        start_time = time.time()
        self._runMultiWorks()
        end_time = time.time()

        if self._verbose:
            print('*' * 20)
            print('End')
            print("Total time spent: %0.2f" % (end_time - start_time))

        if self.write_json:
            print("Writing into {}".format(self.json_file))
            self._update_json_file()


class ScannerShell:

    def _args_handle_and_check(self, input_fields):

        fields = input_fields.copy()
        try:
            if input_fields['function'] == 'tcp':
                assert isIPv4(input_fields['ip_range']), "-ip parameter requires a legal ip address"
                assert re.match(r'^\d+-\d+$', input_fields['port_range']), "-p parameter requires an 'int-int' format"
                port_range = list(map(int, input_fields['port_range'].split('-')))
                fields['port_range'] = range(port_range[0],
                                             port_range[1] + 1)
            elif input_fields['function'] == 'ping':
                assert re.match(r'^[0-9.]+-[0-9.]+$', input_fields['ip_range']), \
                    "-ip parameter requires an 'ip-ip' format"
                ip_range = input_fields['ip_range'].split('-')
                assert isIPv4(ip_range[0]), "The starting ip is not a legal address"
                assert isIPv4(ip_range[1]), "The ending ip is not a legal address"
                fields['ip_range'] = findIPs(ip_range[0], ip_range[1])

        except Exception as e:
            raise InvalidAttribute(e)

        return fields

    def get_parser(self):
        parser = argparse.ArgumentParser(
            description="A host scanner",
        )

        # position arguments
        parser.add_argument('function', type=str, metavar='function', choices=['ping', 'tcp'],
                            help='Specify the required function, '
                                 '"ping" means ip address scanning, '
                                 '"tcp" means port scanning')

        # optional arguments
        parser.add_argument('-n', '--number', type=int, default=3, metavar='number',
                            help='The number of threads or processes to be created, 3 by default')

        parser.add_argument('-m', '--method', type=str, metavar='method',
                            choices=['proc', 'thread'], default='thread',
                            help='The method used by the scanning program. '
                                 '"proc" stands for multi-process, "thread" stands for multi-thread')

        parser.add_argument('-ip', '--ip_range', type=str, metavar='ip_range',
                            help='IP address range used for scanning. e.g: 192.168.0.1-192.168.0.254')

        parser.add_argument('-p', '--port_range', type=str, metavar='port_range',
                            help='Port range used for scanning. e.g: 1-1024')

        parser.add_argument('-v', '--verbose', default=False, action='store_true',
                            help='Specify to display program running time')

        parser.add_argument('-w', '--write_json', default=False, action='store_true',
                            help='Specify the output file name')

        return parser

    def main(self, argv):
        parser = self.get_parser()
        args = parser.parse_args(argv)
        input_fields = dict((k, v) for (k, v) in vars(args).items())
        fields = self._args_handle_and_check(input_fields)
        scanner_executor = HostScanner(**fields)
        scanner_executor.run()


def main():
    try:
        ScannerShell().main(sys.argv[1:])
    except KeyboardInterrupt as e:
        print(f'Caught: {e}, aborting')
        sys.exit(0)
    except IOError as e:
        print(f'IOError occured: {e}')
        sys.exit(0)
    except Exception as e:
        print(f'Error : {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    # ./host_scanner.py ping -n 5 -m proc -ip 10.127.10.192-10.127.10.200 -v -w
    # ./host_scanner.py ping -n 5 -m thread -ip 10.127.10.192-10.127.10.200 -v -w
    # ./host_scanner.py tcp -n 5 -m thread -ip 10.127.10.192 -p 30-1024 -v -w
    # ./host_scanner.py tcp -n 5 -m proc -ip 10.127.10.192 -p 30-1024 -v -w
    main()
