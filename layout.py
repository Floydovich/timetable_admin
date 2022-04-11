from PySimpleGUI import Button, CloseButton, InputText, Listbox, Tab, TabGroup, Text, Combo, Submit

from constants import *
from utils import current_term


def input_field(day_id, class_id, key_id, length, tooltip=None):
    return InputText(key=f'Д{day_id}-П{class_id}:{key_id}', size=(length, 10), enable_events=True, tooltip=tooltip)


def input_fields_row(day_id, class_id):
    return [Text(class_id),
            input_field(day_id, class_id, 'name', 75),
            input_field(day_id, class_id, 'kind', 5, "л - лекция, с - семинар, л/з - лаб. занятие)"),
            input_field(day_id, class_id, 'prof', 50),
            input_field(day_id, class_id, 'place', 10)]


def tab_layout(day_id):
    return [[Text(" " * 40 + "Название предмета" + " " * 66 + "Тип занятия" + " " * 33 + "Преподаватель" + " " * 33 + "Ауд./корпус")]] + \
           [input_fields_row(day_id + 1, class_id + 1) for class_id in range(6)]


def main_layout():
    top = [Text("Выберите кафедру и семестр"),
           Combo(CHAIRS, key=CHAIR, size=(30, 7), default_value="Кафедра",
                 enable_events=True, readonly=True),
           Combo(TERMS, key=TERM, size=(20, 1), default_value=current_term(),
                 enable_events=True, readonly=True)]

    group_title = "После выбора кафедры загрузится список групп. При выборе группы откроется её расписание."
    group_row = [Text(group_title, size=(22, 6), justification='left'),
                 Listbox([], key=GROUP, size=(30, 6), enable_events=True, disabled=True)]

    week_button = [Button("Неделя I", key=WEEK, enable_events=True, disabled=True,
                          tooltip="Переключить неделю (только для групп сс)")]

    tabs = [TabGroup([[Tab(DAYS[day_id], tab_layout(day_id)) for day_id in range(5)]])]

    bottom_buttons = [Submit("Сохранить", key=SAVE, tooltip="Сохранить изменения в расписании"),
                      CloseButton("Выйти")]

    layout = [top, group_row, week_button, tabs, bottom_buttons]

    return layout
