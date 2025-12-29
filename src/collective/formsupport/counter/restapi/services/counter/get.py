from collective.formsupport.counter.config import COUNTER_ANNOTATIONS_NAME
from plone.restapi.services import Service
from zExceptions import NotFound
from zope.annotation.interfaces import IAnnotations


class CounterGet(Service):
    def get_block_ids(self, block_id):
        """
        :param block_id: The block id with a form block.

        Return a list of form block ids in current context.
        If a block_id is provided, return only that id if it is a form block.
        """

        blocks = getattr(self.context, "blocks", {})

        if not blocks:
            return []
        ids = []
        for id, block in blocks.items():
            if block.get("@type", "") != "form":
                continue
            if block_id:
                if block_id == id:
                    ids.append(id)
                    break
            else:
                ids.append(id)
        return ids

    def reply(self):
        block_ids = self.get_block_ids(self.request.get("block_id"))

        if not block_ids:
            raise NotFound(self.context, "", self.request)

        annotations = IAnnotations(self.context)
        counter_object = annotations.get(COUNTER_ANNOTATIONS_NAME, {})

        data = {}
        for block_id in block_ids:
            data[block_id] = counter_object.get(block_id, 0)
        return data
