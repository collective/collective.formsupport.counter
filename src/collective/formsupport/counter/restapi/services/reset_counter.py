from plone.restapi.services import Service
from zope.annotation.interfaces import IAnnotations

from collective.formsupport.counter.config import (
    COUNTER_ANNOTATIONS_NAME,
)


class CounterReset(Service):
    def reply(self):
        form_id = self.request.get("form_id")
        annotations = IAnnotations(self.context)
        counter_object = annotations.setdefault(COUNTER_ANNOTATIONS_NAME, {})

        counter_object[form_id] = 0

        self.request.response.setStatus(204)
