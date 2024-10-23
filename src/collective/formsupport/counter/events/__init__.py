from zope.annotation.interfaces import IAnnotations

from collective.formsupport.counter.config import (
    COUNTER_ANNOTATIONS_NAME,
    COUNTER_ENABLED_FORM_FLAG_NAME,
)


def add_counter(context, event):
    """Add forms counter on the context if form requires"""

    if not event.form.get(COUNTER_ENABLED_FORM_FLAG_NAME):
        return

    annotations = IAnnotations(context)
    counter = annotations.get(COUNTER_ANNOTATIONS_NAME)

    if counter is None:
        annotations[COUNTER_ANNOTATIONS_NAME] = 0

    annotations[COUNTER_ANNOTATIONS_NAME] += 1
