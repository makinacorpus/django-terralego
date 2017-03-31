from django.apps import apps


def convert_geodirectory_entry_to_model_instance(entry):
    if not entry['properties']['tags']:
        return entry
    model_name = entry['properties']['tags'][0]
    if '.' not in model_name:
        return entry
    try:
        model = apps.get_model(model_name)
    except LookupError:
        return entry
    try:
        return model.objects.get(terralego_id=entry['id'])
    except model.DoesNotExist:
        return entry
