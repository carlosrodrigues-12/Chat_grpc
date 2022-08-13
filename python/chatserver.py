"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import chatserver_pb2
import chatserver_pb2_grpc


class Message(chatserver_pb2_grpc.MessageServicer):

    def SendMessage(self, request, context):
        # Print name
        return chatserver_pb2.ForwardMessage(message='Hello, %s!' % request.name)


def serve():
    print('Init')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    print('Server -> ' + server)
    chatserver_pb2_grpc.add_MessageServicer_to_server(Message(), server)
    print('Function add server')
    server.add_insecure_port('[::]:50051')
    print('Add server - IP/Port')
    server.start()
    print('Start server')
    server.wait_for_termination()
    print('Server terminated')


if __name__ == '__main__':
    print('Main - Init')
    logging.basicConfig()
    print('Logging - Basic Config')
    serve()
    print('Call serve')