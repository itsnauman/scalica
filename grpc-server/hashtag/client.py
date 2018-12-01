from __future__ import print_function

import grpc

import hashtag_pb2
import hashtag_pb2_grpc

def run():
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        stub =  hashtag_pb2_grpc.HashtagsStub(channel)

        response = stub.getTweetsByHashtag(hashtag_pb2.TweetHashtagRequest(hashtag='#Hello'))
        print(response.tweets)

if __name__ == '__main__':
    run()
