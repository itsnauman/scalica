from __future__ import print_function

import grpc

import hashtag_pb2
from hashtag_pb2 import TweetRequest
import hashtag_pb2_grpc

def run():
    with grpc.insecure_channel('35.185.58.180:50051') as channel:
        stub =  hashtag_pb2_grpc.HashtagsStub(channel)

        stub.sendTweet(TweetRequest(tweet="#Hello hello hello", tweet_id=1))
        stub.sendTweet(TweetRequest(tweet="#Large scale demo demo", tweet_id=2))
        stub.sendTweet(TweetRequest(tweet="#Andrew dsdsd sd sd sdsd", tweet_id=3))

        response = stub.getTweetsByHashtag(hashtag_pb2.TweetHashtagRequest(hashtag='#Large'))
        print(response.tweets)

if __name__ == '__main__':
    run()
