from __future__ import print_function
from concurrent import futures
from time import sleep
import logging
import threading
import const
import sys

import grpc
import chatserver_pb2
import chatserver_pb2_grpc

class Message(chatserver_pb2_grpc.MessageServicer):

    def SendMessage(self, request, context):
        
        print('\n')
        print(f"(NEW MESSAGE) FROM: {request.remt} - TO: {request.dest}")
        print(f"MESSAGE: {request.msg}\n")
        return chatserver_pb2.StatusMessage(message='ACK')

def Recv():
    #print('Server-Client Init')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chatserver_pb2_grpc.add_MessageServicer_to_server(Message(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def run(remt,dest,ip_dest,msg):

    #print(f"DESTINATION -> {dest} MESSAGE -> {msg}")
    # print(f"ADDR -> {dest_addr}")
    with grpc.insecure_channel(const.CHAT_SERVER_HOST) as channel:
        stub = chatserver_pb2_grpc.MessageStub(channel)
        response = stub.SendMessage(chatserver_pb2.MessageData(remt=remt,dest=dest,ip_dest=ip_dest,msg=msg))
        #print(response)

def inputdados():
    dest = input("ENTER DESTINATION: ")
    msg = input("ENTER MESSAGE: ")
    return dest,msg

if __name__ == '__main__':
    logging.basicConfig()

    recv = threading.Thread(target=Recv)
    recv.daemon = False
    recv.start()

    remt = str(sys.argv[1])
    print(remt)

    while True:
        dest,msg=inputdados()
        ip_dest = const.registry[dest]
        run(remt,dest,ip_dest,msg)