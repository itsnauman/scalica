import schedule
import time
from sentiment import map_hashtags, reduce_hashtags, take_avg
from pyspark import SparkContext

def job():
    sc = SparkContext()
    textfile = sc.textFile("hashtags.txt")
    result = textfile.flatMap(map_hashtags)\
                     .reduceByKey(reduce_hashtags)\
                     .map(take_avg)

    result.saveAsTextFile("results.txt")

schedule.every(30).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
