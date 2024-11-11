"""
This module is where the game is run from.

We are following the javadoc docstring format which is:
@param tag describes the input parameters of the function
@return tag describes what the function returns
@raise tag describes the errors this function can raise
"""

from GameLogic import GameLogic
import sys

from socket import *
def network_init():
    """
    This function sets up a network connection to the ICS servers incase you want to play against another AI connected to the network.
    @return response, mode: a tuple that returns the response from the ICS servers, and sends a string with either host or client to indicate whether this AI is hosting the game session or joining a session.
    """
    while True:
        serverPort = 12002
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(('syn2-1.ics.uci.edu', serverPort))
        #clientSocket.connect(('127.0.0.1', serverPort))

        sentence = "REQUEST_STATES"
        clientSocket.send(sentence.encode())
        result = clientSocket.recv(1024).decode()
        clientSocket.close()



        #clientSocket.connect(('127.0.0.1', serverPort)) # ONLY FOR TESTING
        result_list = result.split("|")
        rooms = result_list[0]
        rule_set = eval(result_list[1])
        print(rooms)
        print("Enter which room you want to join, or create a new room.")

        while True:
            command = input('{# of room/create/refresh}')
            if command == "refresh":
                break
            try:
                int(command)
                sentence = "REQUEST_JOIN|"+command
                mode = 'client'
            except:
                if command != "create":
                    print("Unknown Command")
                    continue
                else:
                    for i, rule in enumerate(rule_set):
                        print(i,":",rule)
                    rule_num = int(input('Please enter which game rule you want to create {int}'))
                    sentence = "REQUEST_OPEN|"+ rule_set[rule_num]
                    mode = 'host'
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            clientSocket.connect(('syn2-1.ics.uci.edu', serverPort))
            clientSocket.send(sentence.encode())

            response = eval(clientSocket.recv(1024).decode())
            clientSocket.close()
            return response,mode, response[2].split()


if __name__ == "__main__":
    # To run under manual mode, please use this command "python3 main.py {row} {col} {k} m {order}"
    # e.g. "python3 main.py 7 7 2 m 0"
    # e.g. "python3 main.py 7 7 2 l {AI_path 1} {AI_path 2}"
    # e.g. "python3 main.py 7 7 2 n {AI_path}"

    # Because the initialization of network mode is different from the normal modes,
    # the initialization of network mode is separated from other modes.
    if len(sys.argv) == 3:
        mode = sys.argv[1]
        if mode == 'n' or mode == 'network':
            ai_path = sys.argv[2]
            response,host_flag, rule = network_init()

            rule = list(map(lambda x:int(x),rule))

            col, row, k, order = rule

            main = GameLogic(col, row, k, 'n', debug=True)
            try:
                main.Run(mode=host_flag, ai_path=ai_path, info=response, time=1200)
            except:
                import traceback
                traceback.print_exc()
                import threading
                for timer in threading.enumerate():
                    if type(timer) == threading.Timer:
                        timer.cancel()
            exit(0)
        else:
            print("Invalid Parameters")
            sys.exit(-1)

    if len(sys.argv) < 5:
        print("Invalid Parameters")
        sys.exit(-1)

    col = int(sys.argv[1])
    row = int(sys.argv[2])
    k = int(sys.argv[3])
    mode = sys.argv[4]

    main = GameLogic(col,row,k,mode,debug=True)

    if mode == 'm' or mode == 'manual':
        order = sys.argv[5]
        order =main.Run(mode=mode,order=order)

    elif mode == 't':
        main.Run(mode=mode)

    elif mode == 's' or mode == 'self':
        order = sys.argv[5]
        main.Run(mode=mode,order=order)

    elif mode == 'l':
        ai_path_1,ai_path_2 =  sys.argv[5],sys.argv[6]
        main.Run(mode=mode,ai_path_1=ai_path_1,ai_path_2=ai_path_2,time=1200)
