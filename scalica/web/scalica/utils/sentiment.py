from google.cloud import language
from pyspark import SparkContext

sc = SparkContext()
textfile = sc.textFile("hashtags.txt")

def map_hashtags(line):
    hashtag = line[1:line.index(":")]
    document = language.types.Document(
        content=line[line.index(":")+1],
        type=language.enums.Document.Type.PLAIN_TEXT,
    )
    client = language.LanguageServiceClient()
    full_sentiment = client.analyze_sentiment(document=document).document_sentiment
    score = full_sentiment.score
    magnitude = full_sentiment.magnitude
    return (hashtag, (score, magnitude, 1))

def reduce_hashtags(sentiment1, sentiment2):
    return (sentiment1[0] + sentiment2[0], sentiment1[1] + sentiment2[1], sentiment1[2] + sentiment2[2])

def take_avg(hash_with_sentiment):
    hashtag = hash_with_sentiment[0]
    sentiment = hash_with_sentiment[1]
    return hashtag, (sentiment[0] / sentiment[2], sentiment[1] / sentiment[2])

result = textfile.map(map_hashtags)\
                 .reduceByKey(reduce_hashtags)\
                 .map(take_avg)

result.saveAsTextFile("results.txt")
