"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

from concurrent import futures
from time import sleep
import logging
import threading
import const

import grpc
import chatserver_pb2
import chatserver_pb2_grpc

class Message(chatserver_pb2_grpc.MessageServicer):

    def SendMessage(self, request, context):
        # Print name
        # dest_addr = request.dest
        # print(request.dest)
        # print(request.name)
        print(request.name)
        # return chatserver_pb2.ForwardMessage(message='Hello, %s!' % request.name)

def Recv():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chatserver_pb2_grpc.add_MessageServicer_to_server(Message(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def run(dest, msg):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    dest_addr = const.registry[dest]
    # print(f"DESTINATION -> {dest} MESSAGE -> {msg}")
    # print(f"ADDR -> {dest_addr}")
    with grpc.insecure_channel(const.CHAT_SERVER_HOST) as channel:
        stub = chatserver_pb2_grpc.MessageStub(channel)
        response = stub.SendMessage(chatserver_pb2.MessageData(dest=dest_addr,name=msg))
        #print(response)
        print("Greeter client received: " + response.message)

if __name__ == '__main__':
    logging.basicConfig()

    # recv_handler = RecvHandler(client_sock)
    # recv_handler.start()
    thread = threading.Thread(target=Recv)
    thread.start()

    while True:
        dest = input("ENTER DESTINATION: ")
        msg = input("ENTER MESSAGE: ")
        run(dest,msg)