class Session:
    def __init__(self, session_id, creator, model_id, creation_date, start_date, expiration_date, participants):
        self.session_id = session_id
        self.creator = creator
        self.model_id = model_id
        self.creation_date = creation_date
        self.start_date = start_date
        self.expiration_date = expiration_date
        self.participants = participants

