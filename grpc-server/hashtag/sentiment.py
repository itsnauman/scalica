from google.cloud import language

def map_hashtags(post):
    hashtags = []
    for word in post.split():
        if word[0] == "#":
            hashtags.append(word)
    document = language.types.Document(
        content=post,
        type=language.enums.Document.Type.PLAIN_TEXT,
    )
    client = language.LanguageServiceClient()
    full_sentiment = client.analyze_sentiment(document=document).document_sentiment
    score = full_sentiment.score
    magnitude = full_sentiment.magnitude
    ret_list = []
    for hashtag in hashtags:
        ret_list.append((hashtag, (score, magnitude, 1)))
    return ret_list

def reduce_hashtags(sentiment1, sentiment2):
    return (sentiment1[0] + sentiment2[0], sentiment1[1] + sentiment2[1], sentiment1[2] + sentiment2[2])

def take_avg(hash_with_sentiment):
    hashtag = hash_with_sentiment[0]
    sentiment = hash_with_sentiment[1]
    return hashtag, (sentiment[0] / sentiment[2], sentiment[1] / sentiment[2])
