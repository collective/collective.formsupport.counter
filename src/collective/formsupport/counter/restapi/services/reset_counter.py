from plone.restapi.services import Service
from zope.annotation.interfaces import IAnnotations

from collective.formsupport.counter.config import (
    COUNTER_ANNOTATIONS_NAME,
)


class CounterReset(Service):
    def reply(self):
        annotations = IAnnotations(self.context)
        counter = annotations.get(COUNTER_ANNOTATIONS_NAME)

        if counter is None:
            self.request.response.setStatus(204)
            return

        annotations[COUNTER_ANNOTATIONS_NAME] = 0

        self.request.response.setStatus(204)
