from __future__ import print_function

import grpc

import hashtag_pb2
from hashtag_pb2 import TweetRequest
import hashtag_pb2_grpc

def run():
    with grpc.insecure_channel('35.185.58.180:50051') as channel:
        stub =  hashtag_pb2_grpc.HashtagsStub(channel)

        # stub.sendTweet(TweetRequest(tweet="I am very #happy and #excited today", tweet_id=1))
        # stub.sendTweet(TweetRequest(tweet="I don't know what the fuck Im saying #neutral", tweet_id=2))
        # stub.sendTweet(TweetRequest(tweet="Shut up andrew #Andrew. I'm very fucking angry", tweet_id=3))

        response = stub.getTweetSentiment(hashtag_pb2.TweetHashtagRequest(hashtag='#happy'))
        print(response)

if __name__ == '__main__':
    run()
