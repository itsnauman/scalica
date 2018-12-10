import schedule
import time
from sentiment import map_hashtags, reduce_hashtags, take_avg
from pyspark import SparkContext
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
sc = SparkContext()


def job():
    textfile = sc.textFile("hashtags.txt")
    result = textfile.flatMap(map_hashtags)\
                     .reduceByKey(reduce_hashtags)\
                     .map(take_avg)

    for hashtag, (sentiment_score, sentiment_magnitude) in result.collect():
        r.rpush("hashtag_sentiment_score:" + hashtag, sentiment_score)
        r.rpush("hashtag_sentiment_magnitude:" + hashtag, sentiment_magnitude)

schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
