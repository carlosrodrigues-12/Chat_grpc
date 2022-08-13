"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import const
import sys

import grpc
import chatserver_pb2
import chatserver_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('172.17.0.2:50051') as channel:
        stub = chatserver_pb2_grpc.MessageStub(channel)
        print(stub)
        response = stub.SendMessage(chatserver_pb2.MessageData(name='you'))
        print(response)
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    print(logging.basicConfig)
    me = str(sys.argv[1]) # User's name (as registered in the registry. E.g., Alice, Bob, ...)
    my_ip = const.registry[me][0]   # If using a proper naming service, client should know its
    my_port = const.registry[me][1] # addresses (which it would register in the ns)
    run()