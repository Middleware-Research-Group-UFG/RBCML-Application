from .database.db import search
from .email import send
from json import loads


class Session:
    def __init__(self, session_id, creator, model_id, creation_date, start_date, expiration_date, participants):
        self.session_id = session_id
        self.creator = creator
        self.model_id = model_id
        self.creation_date = creation_date
        self.start_date = start_date
        self.expiration_date = expiration_date
        self.participants = loads(participants)

    def invite_participants(self, url_ip, url_port):
        for user in self.participants:
            email = search(user, "Tag", "User")[0][2]
            subject = f"Invitation" 
            content = f"""
                {self.creator} invited you to participate in session {self.session_id}
                as {self.participants[user]}
        
                You can access the session using the link:
                
                https://{url_ip}:{url_port}/invite?session={self.session_id}&user={user}
                
                Valid from: {self.start_date}
                      to: {self.expiration_date}"""

            send(subject, content, email)

