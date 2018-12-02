from __future__ import print_function

import grpc

import hashtag_pb2
from hashtag_pb2 import TweetRequest
import hashtag_pb2_grpc

def run():
    with grpc.insecure_channel('127.0.0.1:50051') as channel:
        stub =  hashtag_pb2_grpc.HashtagsStub(channel)

        stub.sendTweet(TweetRequest(tweet="#aps #sucks", tweet_id=2))

        response = stub.getTweetsByHashtag(hashtag_pb2.TweetHashtagRequest(hashtag='#aps'))
        print(response.tweets)

if __name__ == '__main__':
    run()
