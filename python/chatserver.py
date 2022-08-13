from concurrent import futures
import logging

import grpc
import chatserver_pb2
import chatserver_pb2_grpc

def Forward(remt,dest,ip_dest,msg):

    print(f"FROM: {remt} - DESTINATION -> {dest} || MESSAGE -> {msg}")
    with grpc.insecure_channel(ip_dest) as channel:
        stub = chatserver_pb2_grpc.MessageStub(channel)
        response = stub.SendMessage(chatserver_pb2.MessageData(remt=remt,dest=dest,ip_dest=ip_dest,msg=msg))
        print("Client received: " + response.message)

class Message(chatserver_pb2_grpc.MessageServicer):

    def SendMessage(self, request, context):
        
        Forward(request.remt,request.dest,request.ip_dest,request.msg)

        return chatserver_pb2.StatusMessage(message='ACK')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chatserver_pb2_grpc.add_MessageServicer_to_server(Message(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    print('\n')
    serve()