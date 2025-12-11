from collective.formsupport.counter import _
from collective.formsupport.counter.config import COUNTER_BLOCKS_FIELD_ID
from collective.formsupport.counter.config import COUNTER_ENABLED_FORM_FLAG_NAME
from collective.formsupport.counter.interfaces import ICollectiveFormsupportCounterLayer
from collective.volto.formsupport.datamanager.catalog import FormDataStore
from collective.volto.formsupport.interfaces import IFormDataStore
from collective.volto.formsupport.utils import get_blocks
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from zope.component import adapter
from zope.interface import implementer


@implementer(IFormDataStore)
@adapter(IDexterityContent, ICollectiveFormsupportCounterLayer)
class FormDataStoreWithCounter(FormDataStore):
    def get_form_block(self):
        blocks = get_blocks(self.context)
        if not blocks:
            return {}
        for id, block in blocks.items():
            if id != self.block_id:
                continue
            block_type = block.get("@type", "")
            if block_type == "form":
                return block
        return {}

    def get_form_fields(self):
        """
        Patch: add form_counter to fields list
        """
        subblocks = super().get_form_fields()
        if not subblocks:
            return subblocks

        form_block = self.get_form_block()
        if form_block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
            subblocks.append(
                {
                    "field_id": COUNTER_BLOCKS_FIELD_ID,
                    "label": api.portal.translate(
                        _("form_counter_label", default="Counter")
                    ),
                }
            )

        return subblocks
