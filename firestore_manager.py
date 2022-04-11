from PySimpleGUI import Popup
from firebase_admin import firestore, credentials, initialize_app

from keys import certificate_path
from utils import current_term, has_internet_connection, days, classes, weeks


def init_app():
    if not has_internet_connection():
        Popup("Нет соединения с Интернетом. Откройте программу заново после установления соединения.")
        exit(1)
    initialize_app(credentials.Certificate(certificate_path))


def form_message_body(name, prof, kind, place):
    kind = kind and f" ({kind})" or kind
    prof = prof and f" - {prof}" or prof
    place = place and f" - {place}" or place
    if name:
        return f"{name}{kind}{prof}{place}"
    else:
        return "Окно"


class FirestoreManager:

    def __init__(self):
        init_app()
        self.db = firestore.client()
        self.term_id = current_term()
        self.chair_id = None
        self.group_id = None

    def get_chair_ids(self):
        return [col.id for col in self.db.collections()]

    def get_group_ids(self):
        return [doc.id for doc in self.chair_ref().list_documents()]

    def chair_ref(self):
        return self.db.collection(self.chair_id)

    def group_ref(self):
        return self.chair_ref().document(self.group_id)

    def term_ref(self):
        term_ref = self.group_ref().collection(self.term_id)
        return term_ref

    def group_is_blinking(self):
        return self.group_ref().get().get("isBlinking")

    def get_timetable(self, week_id):
        return self.term_ref().where('week_id', '==', week_id)

    def iter_classes(self, week_id):
        """
        Get class document fields as a dictionary to fill the layout's input values
        """
        for snapshot in self.get_timetable(week_id).stream():
            yield snapshot.to_dict()

    def id_not_set(self):
        return None in (self.chair_id, self.group_id)

    def update_timetable(self, doc_id, classes):
        self.term_ref().document(doc_id).update(classes)
