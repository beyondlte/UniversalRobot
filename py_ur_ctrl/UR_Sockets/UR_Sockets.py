import socket
import threading
import SocketServer
import time
import Queue

recvdata = ""
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.queue = server.queue
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        global recvdata
        # self.queue.get() is on time thing
        # if we use if self.queue.get() != "something", then self.queue is empty already
        while True:
            if self.queue.empty() != True:
                queueContent = self.queue.get()
                if queueContent == "s1":
                    print "get command s1 from control"
                    print "self.queue = ", queueContent 
                    self.request.sendall('[0]\\10')
                    recvdata = str(self.request.recv(1024))
                    cur_thread = threading.current_thread()
                    response = bytes("{}: {}".format(cur_thread.name, recvdata))
                    print "response =", response
                elif queueContent == "s2":
                    print "get command s2 from control"
                    print "self.queue = ", queueContent 
                    # if I send two, I will get two responses
                    self.request.sendall('[12]\\10')
                    recvdata = str(self.request.recv(1024))
                    cur_thread = threading.current_thread()
                    response = bytes("{}: {}".format(cur_thread.name, recvdata))
                    print "response =", response
                elif queueContent == "s3":
                    print "get command s3 from control"
                    print "self.queue = ", queueContent 
                    # if I send two, I will get two responses
                    self.request.sendall('[16, 1]\\10')
                    recvdata = str(self.request.recv(1024))
                    cur_thread = threading.current_thread()
                    response = bytes("{}: {}".format(cur_thread.name, recvdata))
                    print "response =", response

                elif queueContent == "s4":
                    print "get command s4 from control"
                    self.request.sendall('[-99]\\10')
                    break
            else:
                # print "get nothing from control"
                pass

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, queue=None):
        self.queue = queue
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

def client(ip, port, message, respnum = 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(bytes(message))
        response = str(sock.recv(1024))
        print("Received: {}".format(response))
        if respnum == 2:
            response = str(sock.recv(1024))
            print("Received 2: {}".format(response))

        return response

    finally:
        sock.close()

if __name__ == "__main__":
    # port 0 means to select an arbitrary unused port
    SERVERIP, SPORT = "172.31.1.100", 50000 

    q = Queue.Queue()

    server = ThreadedTCPServer((SERVERIP, SPORT), ThreadedTCPRequestHandler, queue=q)
    ip, port = server.server_address

    # start a thread with the server. 
    # the thread will then start one more thread for each request.
    server_thread = threading.Thread(target=server.serve_forever)

    # exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    CLIENTIP, CPORT = "172.31.1.147", 29999

    respmsg = client(CLIENTIP, CPORT, "get loaded program\n", 2)
    if "No program loaded" in respmsg:
        respmsg = client(CLIENTIP, CPORT, "load /programs/a3/a3.urp\n", 2)
        print respmsg

    time.sleep(0.5)
    respmsg = client(CLIENTIP, CPORT, "brake release\n", 2)
    print respmsg
    time.sleep(1.0)
    respmsg = client(CLIENTIP, CPORT, "play\n", 2)
    print respmsg

    startTime = time.clock()
    elapsedTime = 0.0

    runningCheck = False
    # it takes about 13s to start the program
    id = 1
    while elapsedTime < 15.0 and  runningCheck == False:
        respmsg = client(CLIENTIP, CPORT, "running\n", 2)
        print("{}: {}".format(id, respmsg))
        runningCheck = ('Program running: true' in respmsg)
        time.sleep(1.0)
        elapsedTime = time.clock() - startTime
        id += 1


    print "recvdata = ", recvdata
    elapsedTime = 0.0
    startTime = time.clock()
    q.put("s1")
    # wait 3 seconds to get "Connection established"
    while "Connection established" not in recvdata and elapsedTime <3.0:
        print "recvdata1 = ", recvdata
        time.sleep(1.0)
        elapsedTime = time.clock() - startTime

    elapsedTime = 0.0
    startTime = time.clock()

    """
    q.put("s2")
    time.sleep(0.1)
    # wait 10 seconds to get "move to home" done 
    while "SET cmd_code 0" not in recvdata and elapsedTime < 10.0:
        print "recvdata2 = ", recvdata
        time.sleep(1.0)
        elapsedTime = time.clock() - startTime
    """

    elapsedTime = 0.0
    startTime = time.clock()
    q.put("s3")
    while "SET cmd_status 2" not in recvdata and elapsedTime < 20.0:
        print "recvdata3 = ", recvdata
        time.sleep(1.0)
        elapsedTime = time.clock() - startTime

    """
    elapsedTime = 0.0
    startTime = time.clock()
    q.put("s4")
    while "SET cmd_status 0" not in recvdata and elapsedTime < 3.0:
        print "recvdata4 = ", recvdata
        time.sleep(1.0)
        elapsedTime = time.clock() - startTime
    """

    # if don't call shutdown(), it will raise [Error 9] Bad file descriptor error !!!
    # shutdown tells the serve_forever() loop to stop and wait until it does

    # Strictly speaking, you're supposed to use shutdown on a socket before you close it. The shutdown is an advisory to
    # the socket at the other end. Depending on the argument you pass it, it can mean "I'm not going to send anymore,
    # but I'll still listen", or "I'm not listening, good riddance!". Most socket libraries, however, are so used to
    # programmers neglecting to use this piece of etiquette that normally a close is the same as shutdown(); close(). So
    # in most situations, an explicit shutdown is not needed
    server.shutdown()
    server.server_close()
    time.sleep(1.0)

