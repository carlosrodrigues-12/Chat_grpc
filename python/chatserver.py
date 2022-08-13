"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import chatserver_pb2
import chatserver_pb2_grpc


class Message(chatserver_pb2_grpc.MessageServicer):

    def SendMessage(self, request, context):
        # Print name
        print('Message Function')
        return chatserver_pb2.ForwardMessage(message='Hello, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chatserver_pb2_grpc.add_MessageServicer_to_server(Message(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()