import os
import datetime
from mastodon import Mastodon
from google.cloud import firestore
import re

JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")
GCP_PROJECT_ID = os.environ['GCP_PROJECT_ID']
db = firestore.Client(project=GCP_PROJECT_ID)

# mastodon
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
mastodon = Mastodon(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token = ACCESS_TOKEN,
    api_base_url = 'https://mistodon.cloud'
)

def get_notification(event, context):
    mentions = []
    for n in mastodon.notifications(mentions_only=True):
        if n["type"] == "mention":
            mentions.append(n)

    for notification in mentions:
        id = notification["id"]
        doc_ref = db.collection("mist_sita/@invocation/notification").document(str(id))
        doc = doc_ref.get()
        if not doc.exists:
            doc_ref.set({
                "id" : id,
                "status" : "registered"
            })
    
    return mentions

if __name__ =="__main__":
    mentions = get_notification(None, None)
    for notification in mentions:
        id = notification["id"]
        acct = notification["account"]["acct"]
        content = notification["status"]["content"]
        content = re.sub('<.*?>', '', content)
        content = re.sub('@sita', '', content)

        print(f"id:{id}\n{acct}\n{content}")