from copy import deepcopy

from zope.interface import implementer
from zope.component import adapter
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotations

from collective.volto.formsupport.interfaces import IFormData
from collective.volto.formsupport.adapters import FormDataAdapter

from collective.formsupport.counter import _
from collective.formsupport.counter.config import (
    COUNTER_ENABLED_FORM_FLAG_NAME,
    COUNTER_ANNOTATIONS_NAME,
    COUNTER_BLOCKS_FIELD_ID,
)
from collective.formsupport.counter.interfaces import ICollectiveFormsupportCounterLayer


@implementer(IFormData)
@adapter(Interface, ICollectiveFormsupportCounterLayer)
class FormDataAdapterWithCounter(FormDataAdapter):

    _block = {}

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, new_value):
        block = deepcopy(new_value)

        if block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
            block["subblocks"].append({"field_id": COUNTER_BLOCKS_FIELD_ID})

        self._block = block

    def extract_data_from_request(self):
        form_data = super().extract_data_from_request()
        block_id = form_data.get("block_id", "")
        block = None

        if block_id:
            block = self.get_block_data(block_id=block_id)

        if not block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
            return form_data

        annotations = IAnnotations(self.context)

        form_data["data"].append(
            {
                "field_id": COUNTER_BLOCKS_FIELD_ID,
                "label": _("Form counter"),
                "value": annotations.get(COUNTER_ANNOTATIONS_NAME, {}).get(block_id)
                + 1,
            }
        )

        return form_data
