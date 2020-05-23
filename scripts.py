from threading import *
from datetime import datetime
from termcolor import colored
import optparse, socket, subprocess, sys


def context_menu():
    parser = optparse.OptionParser('[?] Usage of program: '
                                   + '-H <target host> -p <target port>')

    # parser todo
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target ports separated by comma')

    (options, args) = parser.parse_args()

    tgtHost_ = options.tgtHost  # list
    tgtPorts = str(options.tgtPort).split(',')  # splited list

    if tgtHost_ is None or tgtPorts[0] is None:
        print(parser.usage)
    else:
        port_scaning(tgtHost_, tgtPorts)


def port_scaning(host, ports):
    try:
        targetIP = socket.gethostbyname(host)
        targetNAME = socket.gethostbyaddr(targetIP)
        subprocess.call("cls", shell=True)
        print('-' * 60)
        print(colored(f"[+] Trying to connect to {targetIP} via TCP", 'green'))
        print('-' * 60)
        for port in ports:
            tr = Thread(target=connection_scan, args=(targetIP, int(port)))
            tr.start()
    except Exception:
        print(colored(f"[-] Hostname could not be resolver. Exiting", 'red'))


def connection_scan(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(colored(f"[+] TCP port opened: {port}", 'green'))
    except Exception:
        print(colored(f"[-] TCP port {port} closed. Can't connect to it!", 'red'))


def port_scan(host):
    subprocess.call('cls', shell=True)
    # remoteServer = str(input("Enter a remote server to scan: "))
    remoteServerIP = socket.gethostbyname(host)
    print('-' * 60)
    print('Please wait, scanning remote host', remoteServerIP)
    print('-' * 60)

    starting_time = datetime.now()

    try:
        for port in range(141):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            print(result)
            if result == 0:
                print(colored(f"Port is opened: {port}", 'green'))
            sock.close()
    except KeyboardInterrupt:
        print("You pressed Ctrl+c. Terminating the process.")
        sys.exit()
    except socket.gaierror:
        print("Hostname could not be resolver. Exiting")
        sys.exit()
    except socket.error:
        print("Could not connect to server")
        sys.exit()

    end_time = datetime.now()
    print("Scanning completed in : {}".format(end_time - starting_time))
