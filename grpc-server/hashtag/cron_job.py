import time
from sentiment import map_hashtags, reduce_hashtags, take_avg
from pyspark import SparkContext

import redis
import os

r = redis.Redis(host=os.environ['REDIS_HOST_URL'], port=6379, db=0)
sc = SparkContext()

textfile = sc.textFile("tweets_dump.txt")
result = textfile.flatMap(map_hashtags)\
                 .reduceByKey(reduce_hashtags)\
                 .map(take_avg)

for hashtag, (sentiment_score, sentiment_magnitude) in result.collect():
    r.set("@score@" + hashtag, sentiment_score)
