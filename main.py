from PySimpleGUI import theme, Window, WINDOW_CLOSED, Popup

from keys import fcm_api_key
from gui_utils import fill_timetable
from firestore_manager import FirestoreManager, form_message_body
from layout import main_layout
from constants import *
from pyfcm import FCMNotification
from transliterate import translit

from utils import trans_table, days, weeks, classes

db_manager = FirestoreManager()
push_service = FCMNotification(api_key=fcm_api_key)

theme('BlueMono')
layout = main_layout()
window = Window('Timetable Admin', layout)

input_stash = {}
week_id = 0

while True:
    event, values = window.read()

    if event == WINDOW_CLOSED:
        break
    elif event == CHAIR:
        db_manager.chair_id = values[CHAIR]
        groups = db_manager.get_group_ids()
        window[GROUP].update(values=groups, disabled=False)
    elif event == TERM:
        db_manager.term_id = values[TERM]
    elif event == GROUP:
        group = values[GROUP][0]
        db_manager.group_id = values[GROUP][0]
        week_id = 0  # reset for non-blinking groups
        window[WEEK].update(text=WEEKS[week_id])

        fill_timetable(window, db_manager, week_id)

        disabled = False if db_manager.group_is_blinking() else True

        window[WEEK].update(disabled=disabled)
        input_stash.clear()  # clear the previous inputs on selecting a new group
    elif event == WEEK:
        week_id = 0 if week_id else 1  # switch between weeks with 1 as True
        fill_timetable(window, db_manager, week_id)
        window[WEEK].update(text=WEEKS[week_id])
    elif event[0] == "Д":
        # All inputs' keys start with Д
        day_class, field = event.split(':')
        doc_id = f"Н{week_id + 1}-{day_class}"

        name_value = values[f"{day_class}:name"]
        value = values[event]

        try:
            input_stash[doc_id].update({field: value})
        except KeyError:
            input_stash[doc_id] = {field: value}
        finally:
            # Add the name of changed class to the input stash, so it could be send with FCM message
            # if other fields but name were changed
            if field != 'name':
                input_stash[doc_id].update({'name': name_value})
    elif event == SAVE:
        if db_manager.id_not_set():
            Popup("Откройте расписание выбрав нужную группу и день", title="Ошибка сохранения")
            continue

        if not input_stash:
            Popup("Вы не внесли никаких изменений в расписание", title="Ошибка сохранения")
            continue

        spec, code = values[GROUP][0].rstrip().split('-')
        spec = translit(spec, 'ru', reversed=True)
        code_split = code.split(' ', maxsplit=1)

        if len(code_split) > 1:
            code = translit(code_split[0], 'ru', reversed=True)
            postfix = trans_table[code_split[1]]
        else:
            postfix = ''
        
        topic = spec + code + postfix

        for doc_id, fields in input_stash.items():
            db_manager.update_timetable(doc_id, fields)
            w, d, c = doc_id.split('-')

            if db_manager.group_is_blinking():
                message_title = f"Изменение в расписании: ({weeks[w]}) {days[d]}, {classes[c]}"
            else:
                message_title = f"Изменение в расписании: {days[d]}, {classes[c]}"

            message_body = form_message_body(
                fields.get('name', ''),
                fields.get('prof', ''),
                fields.get('kind', ''),
                fields.get('place', '')
            )

            result = push_service.notify_topic_subscribers(topic, message_body, message_title)
        else:
            Popup("Расписание успешно сохранено")
            input_stash.clear()  # clear previously updated inputs on save
    else:
        print(f"Event {event} happened")

window.close()
