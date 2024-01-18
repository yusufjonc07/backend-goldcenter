import firebase_admin
from firebase_admin import credentials, messaging
from app.models.notification import Notification

cred = credentials.Certificate("./app/utils/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def sendPush(tokens, title, msg):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg,
        ),
        data=None,
        tokens=tokens,
    )

    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    print('Successfully sent to tokens:', tokens)
