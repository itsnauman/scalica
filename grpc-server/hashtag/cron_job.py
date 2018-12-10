import schedule
import time
from sentiment import map_hashtags, reduce_hashtags, take_avg
from pyspark import SparkContext
import redis

r = redis.Redis(host='35.243.217.152', port=6379, db=0)
sc = SparkContext()


def job():
    textfile = sc.textFile("tweets_dump.txt")
    result = textfile.flatMap(map_hashtags)\
                     .reduceByKey(reduce_hashtags)\
                     .map(take_avg)

    for hashtag, (sentiment_score, sentiment_magnitude) in result.collect():
        r.set("@score@" + hashtag, sentiment_score)

job()

#schedule.every(30).minutes.do(job)

#while True:
    #schedule.run_pending()
    #time.sleep(1)
