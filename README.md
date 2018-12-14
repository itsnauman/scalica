## Scalica Hashtag

To accommodate the scalability requirement of the project we propose the following system architecture and pipeline consisting of a cluster of 4 nodes and a batch MapReduce sentiment analysis job.


# Architecture

![Architecture Diagram](https://github.com/itsnauman/scalica_hashtag/blob/master/documentation/architecture.jpg)

1. First, we have the node hosting the Application Server - running the Scalica web application. This is the server to which the client connects, written in Django. We add an API endpoint in Scalica for clients to connect to in order to view a stream of posts containing the particular hashtag.

2. Second, have the DB node, running an instance of MySQL that serves as the database for our Scalica app. This is where we store the posts’ text and other user data.

3. Third, we have the gRPC server running a Python server that listens for posts that get sent to it from the App Server node. This node is in charge of parsing the text of the raw text posts that are sent as an RPC, running a batch job, and populating the Redis store; which brings us to the fourth node →

4. The fourth and final node is our node running an instance of Redis store, a fast key-value store we use to store the data we care about on hashtags. The keys in Redis are the hashtag texts, and the value is a list of ids that are given by the Scalica Application when a user creates a new post.

5. Finally, we note the batch MapReduce job that processes posts with hashtags to calculate sentiment analysis for each hashtag. As per design considerations advised by Professor Sovran, our batch job is ran from the gRPC node (3), and populates the results of the MapReduce into the same Redis data node (4), just simply with a different key-value than the (hashtag → list_ids) store. We use Apache Spark to process large amounts of raw text data with hashtags and schedule the Spark script as a cron job running every 30 minutes on the node.

# Flow:
Thus, taking into account the preceding architecture, we present a sample flow of client-server interaction and background processing for using the hashtag feature with the Scalica service:

→
The user-client connects to the Scalica Application server (node 1), authenticates and creates a post with a hashtag included in the raw text. Subscribing to the stream of hashtag that was just created by the user renders a page that shows the newly created post, but the sentiment for the hashtag that is being searched is displayed as “not yet available”.
→
The post along with the entire text is stored in the MySQL database running on (node 2) after being assigned a unique id as per the data model, and is also sent over a remote procedure call to the gRPC server (node 3).
→
The server running on the gRPC node processes the text of the post sent, extracts the hashtags, and creates a mapping from hashtag to the post id that was just received from the Scalica App server. This server then pushes the key-value pairing into a Redis datastore over a remote procedure call, that updates the mapping of hashtag to a (potentially) growing list of post id’s that contain this particular hashtag (key). The final step that this gRPC server performs, is it writes (appends) the entire posts’ text to a dump file on the same node.
→
After the text of the post just processed is in the dump file, the scheduled cron job running the MapReduce in Spark runs and processes the dump file, pulling out hashtags and mapping, and then reducing their sentiment with Google Natural Language API. Once the job completes, the script pushes the results of the MapReduce into Redis (node 4) as a yet another remote procedure call, but now the key is appended with keyword “sentiment” and hashtag to denote the hashtag for which the sentiment is calculated for; the value is a double between [-1,1], -1 being the most negative sentiment and 1 the most positive.
→
Now, after the MapReduce job has run and the sentiment has been updated and pushed into Redis, the user refreshes the page.
→
The Scalica App server (node 1) makes an RPC to the gRPC server (node 3) and requests all post id’s for which posts contain that hashtag - this is our stream that the user wants to subscribe to.
→
the gRPC server makes a remote procedure call to the Redis datastore node (node 4), and fetches both the list of id’s and now, the available, and populated key-value for hashtag-to-sentiment. The server now sends this object with two fields back to the Scalica App server.
→
The Scalica App server receives the id’s of the posts for the stream that the user has requested and fetches the plain text of the posts (by their id’s) from the MySQL database via a remote procedure call. After receiving the posts, the Scalica server adds the sentiment received from the gRPC server from the previous step and sends it to render on the front-end UI.
→
The page is now populated with a stream of posts that contain the searched hashtag, as well as the sentiment for this hashtag that is displayed as ‘negative’ or ‘positive’ for the user to see.
