from collective.formsupport.counter import _
from collective.formsupport.counter.config import COUNTER_ANNOTATIONS_NAME
from persistent.dict import PersistentDict
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest
from zExceptions import NotFound
from zope.annotation.interfaces import IAnnotations


class CounterReset(Service):
    def check_block_id(self, block_id):
        blocks = getattr(self.context, "blocks", {})

        for id, block in blocks.items():
            if block.get("@type", "") == "form" and block_id == id:
                return True
        return False

    def reply(self):
        data = json_body(self.request)
        block_id = data.get("block_id", "")

        if not block_id:
            raise BadRequest(
                _("missing_block_id", default="Missing `block_id` parameter.")
            )

        has_block = self.check_block_id(block_id)

        if not has_block:
            raise NotFound(self.context, "", self.request)

        try:
            counter_value = int(data.get("counter_value", 0))

        except ValueError:
            raise BadRequest(
                _(
                    "wrong_counter_value",
                    default='Badly composed "counter_value" parameter, integer required.',
                )
            )

        annotations = IAnnotations(self.context)
        counter_object = annotations.setdefault(
            COUNTER_ANNOTATIONS_NAME, PersistentDict({})
        )
        counter_object[block_id] = counter_value

        return self.request.response.setStatus(204)
