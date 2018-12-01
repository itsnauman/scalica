from concurrent import futures
import time

import grpc

import hashtag_pb2
import hashtag_pb2_grpc

import redis
r = redis.Redis(host='localhost', port=6379, db=0)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class HashtagService(hashtag_pb2_grpc.HashtagsServicer):
    def getTweetsByHashtag(self, request, context):
        hashtag = request.hashtag
        print(hashtag)
        return hashtag_pb2.TweetsList(hashtag="#Hello", tweets=['#Hello world'])

    # def SayHello(self, request, context):
    #     r.set('foo', 'bar')
    #     return hashtag_pb2.HelloReply(message='Hello, %s!' % request.name)

    # def SayHelloAgain(self, request, context):
    #     return hashtag_pb2.HelloReply(message=r.get('dp'))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hashtag_pb2_grpc.add_HashtagsServicer_to_server(HashtagService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
