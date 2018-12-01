from __future__ import print_function

import grpc

import hashtag_pb2
import hashtag_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub =  hashtag_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(hashtag_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + response.message)
        response = stub.SayHelloAgain(hashtag_pb2.HelloRequest(name='you'))
        print(response)


if __name__ == '__main__':
    run()
