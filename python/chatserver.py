"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import chatserver_pb2
import chatserver_pb2_grpc

def Forward(remt,dest,ip_dest,msg):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    print(f"DESTINATION -> {dest} MESSAGE -> {msg}")
    # print(f"ADDR -> {dest_addr}")
    with grpc.insecure_channel(ip_dest) as channel:
        stub = chatserver_pb2_grpc.MessageStub(channel)
        response = stub.SendMessage(chatserver_pb2.MessageData(remt=remt,dest=dest,ip_dest=ip_dest,msg=msg))
        #print(response)
        print("Greeter client received: " + response.message)

class Message(chatserver_pb2_grpc.MessageServicer):

    def SendMessage(self, request, context):
        # Print name
        
        Forward(request.remt,request.dest,request.ip_dest,request.msg)

        return chatserver_pb2.StatusMessage(message='Return Server')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chatserver_pb2_grpc.add_MessageServicer_to_server(Message(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()