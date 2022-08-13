"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

from concurrent import futures
import logging
import threading
import const

import grpc
import chatserver_pb2
import chatserver_pb2_grpc

class Th(threading.Thread):
    def __init__ (self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        print("Hello!")
        print(self.num)

"""class RecvHandler(threading.Thread):
  def __init__(self, sock):
    threading.Thread.__init__(self)
    self.client_socket = sock

  def run(self):
    while True:
        #print('Client receiving handler is ready.')
        (conn, addr) = self.client_socket.accept() # accepts connection from server
        #print('Server connected to me.')
        marshaled_msg_pack = conn.recv(1024)   # receive data from server
        msg_pack = pickle.loads(marshaled_msg_pack) # unmarshal message pack
        print("MESSAGE: " + msg_pack[0] + " - FROM: " + msg_pack[1])
        conn.send(pickle.dumps("ACK")) # simply send the server an Ack to confirm
        conn.close()
    return # We need a condition for graceful termination
"""
class Message(chatserver_pb2_grpc.MessageServicer):

    def SendMessage(self, request, context):
        # Print name
        # dest_addr = request.dest
        # print(request.dest)
        # print(request.name)
        return chatserver_pb2.ForwardMessage(message='Hello, %s!' % request.name)

def run(dest, msg):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    dest_addr = const.registry[dest]
    print(f"DESTINATION -> {dest} MESSAGE -> {msg}")
    print(f"ADDR -> {dest_addr}")
    with grpc.insecure_channel('172.17.0.2:50051') as channel:
        stub = chatserver_pb2_grpc.MessageStub(channel)
        #response = stub.SendMessage(chatserver_pb2.MessageData(dest=dest_addr,name=msg))
        #print(response)
    #print("Greeter client received: " + response.message)

def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chatserver_pb2_grpc.add_MessageServicer_to_server(Message(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()

    # recv_handler = RecvHandler(client_sock)
    # recv_handler.start()
    Th.start(1)

    while True:
        dest = input("ENTER DESTINATION: ")
        msg = input("ENTER MESSAGE: ")
        run(dest,msg)