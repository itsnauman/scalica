from __future__ import print_function

import grpc

import hashtag_pb2
from hashtag_pb2 import TweetRequest
import hashtag_pb2_grpc
import os

def run():
    with grpc.insecure_channel(os.environ['GRPC_HOST_URL']) as channel:
        stub =  hashtag_pb2_grpc.HashtagsStub(channel)

        stub.sendTweet(TweetRequest(tweet="I am very #happy and #excited today", tweet_id=1))

if __name__ == '__main__':
    run()
