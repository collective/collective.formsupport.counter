from collective.volto.formsupport.restapi.services.form_data.csv import (
    FormDataExportGet,
    SKIP_ATTRS,
)
from collective.formsupport.counter.config import (
    COUNTER_ENABLED_FORM_FLAG_NAME,
    COUNTER_BLOCKS_FIELD_ID,
)


class FormDataExportGetCounter(FormDataExportGet):
    def get_ordered_keys(self, record):
        """
        We need this method because we want to maintain the fields order set in the form.
        The form can also change during time, and each record can have different fields stored in it.
        """

        record_order = record.attrs.get("fields_order", [])
        if record_order:
            if self.form_block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
                record_order.insert(0, COUNTER_BLOCKS_FIELD_ID)

            return record_order

        order = []
        # first add the keys that are currently in the form
        for k in self.form_fields_order:
            if k in record.attrs:
                order.append(k)
        # finally append the keys stored in the record but that are not in the form (maybe the form changed during time)
        for k in record.attrs.keys():
            if k not in order and k not in SKIP_ATTRS:
                order.append(k)

        if self.form_block.get(COUNTER_ENABLED_FORM_FLAG_NAME):
            order.insert(0, COUNTER_BLOCKS_FIELD_ID)

        return order
