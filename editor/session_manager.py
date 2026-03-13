import uuid
from db.sessions_repo import create_session, end_session
from db.documents_repo import create_document


class SessionManager:
    def __init__(self, user_id, device=None, app_version=None):
        self.user_id = user_id
        self.device = device
        self.app_version = app_version
        self.session_id = None
        self.doc_id = None

    def start(self):
        self.session_id = str(uuid.uuid4())
        self.doc_id = str(uuid.uuid4())
        create_session(self.session_id, self.user_id, self.device, self.app_version)
        create_document(self.doc_id, self.session_id, title="Untitled")
        return self.session_id, self.doc_id

    def end(self):
        if self.session_id:
            end_session(self.session_id)
