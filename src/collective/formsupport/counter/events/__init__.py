from zope.annotation.interfaces import IAnnotations

from collective.formsupport.counter.config import (
    COUNTER_ANNOTATIONS_NAME,
    COUNTER_ENABLED_FORM_FLAG_NAME,
)


def add_counter(context, event):
    """Add forms counter on the context if form requires"""

    if not event.form.get(COUNTER_ENABLED_FORM_FLAG_NAME):
        return

    form_id = event.form_data.get("block_id")

    annotations = IAnnotations(context)
    counter_object = annotations.setdefault(COUNTER_ANNOTATIONS_NAME, {})

    counter = counter_object.get(form_id)

    if counter is None:
        counter_object[form_id] = 0

    counter_object[form_id] += 1
