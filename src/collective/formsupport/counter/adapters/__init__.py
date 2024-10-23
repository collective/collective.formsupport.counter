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
        # if block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
        block["subblocks"].append({"field_id": COUNTER_BLOCKS_FIELD_ID})

        self._block = block

    def extract_data_from_request(self):
        form_data = super().extract_data_from_request()

        if not self.block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
            return form_data

        annotations = IAnnotations(self.context)

        form_data["data"].append(
            {
                "field_id": COUNTER_BLOCKS_FIELD_ID,
                "label": _("Form counter"),
                "value": annotations.get(COUNTER_ANNOTATIONS_NAME, 0) + 1,
            }
        )

        return form_data
