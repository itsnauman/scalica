from concurrent import futures
import time

import grpc

import hashtag_pb2
import hashtag_pb2_grpc

import redis

r = redis.Redis(host='35.243.217.152', port=6379, db=0, charset="utf-8", decode_responses=True)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class HashtagService(hashtag_pb2_grpc.HashtagsServicer):
    def __init__(self):
        super().__init__()
        self.fp = open('tweets_dump.txt', 'a+')

    def getTweetsByHashtag(self, request, context):
        hashtag = request.hashtag.lower()
        tweet_ids = r.lrange(hashtag, 0, -1)

        return hashtag_pb2.TweetsList(hashtag=hashtag, tweets=tweet_ids)

    def sendTweet(self, request, context):
        tags = request.tweet
        tweet_id = request.tweet_id

        # Strip hashtags from tweet
        hashtags = [i.lower() for i in tags.split() if i.startswith("#")]

        # Add hashtag as key and tweet id as value in redis
        for tag in hashtags:
            r.rpush(tag, tweet_id)

        # Dump tweets to a file
        self.fp.write(tags + '\n')
        self.fp.flush()

        return hashtag_pb2.Empty()

    def getTweetSentiment(self, request, context):
        sentiment_key = '@score@' + request.hashtag

        if not r.exists(sentiment_key):
            return hashtag_pb2.TweetSentiment(sentiment="")

        sentiment = r.get(sentiment_key)

        if float(sentiment) < float(0):
            return hashtag_pb2.TweetSentiment(sentiment="NEGATIVE")
        elif float(sentiment) > float(0):
            return hashtag_pb2.TweetSentiment(sentiment="POSITIVE")

        return hashtag_pb2.TweetSentiment(sentiment="NEUTRAL")

    def __del__(self):
        self.fp.close()


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
