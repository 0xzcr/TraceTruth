from db.events_repo import log_event


class EventLogger:
    def __init__(self, session_id):
        self.session_id = session_id

    def log(self, event_type, content=None, cursor_pos=None, selection_start=None, selection_end=None):
        log_event(
            self.session_id,
            event_type,
            content=content,
            cursor_pos=cursor_pos,
            selection_start=selection_start,
            selection_end=selection_end,
        )
