from concurrent import futures
import time

import grpc

import hashtag_pb2
import hashtag_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(hashtag_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return hashtag_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        return hashtag_pb2.HelloReply(message='Hello Hello Hello')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hashtag_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
