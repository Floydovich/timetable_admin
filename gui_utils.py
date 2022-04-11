def fill_class(window, items):
    # Из day_id и class_id документа создается key текстового поля
    day_id = items['day_id'] + 1
    class_id = items['class_id'] + 1
    for i in ['name', 'kind', 'prof', 'place']:
        input_key = f'Д{day_id}-П{class_id}:{i}'
        window[input_key].update(items[i])


def fill_timetable(window, db_manager, week_id):
    for class_item in db_manager.iter_classes(week_id):
        fill_class(window, class_item)
