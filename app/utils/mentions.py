import re

from app.models.user import User
from app.models.notification import Notification


def extract_mentions(content: str):

    pattern = r'@([a-zA-Z0-9_]+)'

    return re.findall(pattern, content)


def create_mention_notifications(
    db,
    content: str
):

    usernames = extract_mentions(content)

    for username in usernames:

        user = db.query(User).filter(
            User.name == username
        ).first()

        if user:

            notification = Notification(
                user_id=user.id,
                message=f"You were mentioned: {content}"
            )

            db.add(notification)