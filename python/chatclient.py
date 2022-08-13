"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import const

import grpc
import chatserver_pb2
import chatserver_pb2_grpc


def run(dest, msg):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    dest_addr = const.registry[dest]
    print(f"DESTINATION -> {dest} MESSAGE -> {msg}")
    print(f"ADDR -> {dest_addr}")
    with grpc.insecure_channel('172.17.0.2:50051') as channel:
        stub = chatserver_pb2_grpc.MessageStub(channel)
        response = stub.SendMessage(chatserver_pb2.MessageData(dest=dest_addr,name=msg))
        #print(response)
    #print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    while True:
        dest = input("ENTER DESTINATION: ")
        msg = input("ENTER MESSAGE: ")
        run(dest,msg)