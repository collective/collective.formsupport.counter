from collective.formsupport.counter.testing import (
    COLLECTIVE_FORMSUPPORT_COUNTER_API_FUNCTIONAL_TESTING,
)
from datetime import datetime
from io import StringIO
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from plone.testing.zope import Browser
from Products.MailHost.interfaces import IMailHost
from zope.component import getUtility

import base64
import csv
import os
import transaction
import unittest


class TestCounter(unittest.TestCase):
    layer = COLLECTIVE_FORMSUPPORT_COUNTER_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.mailhost = getUtility(IMailHost)

        self.api_session = RelativeSession(self.portal.absolute_url())
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.document = api.content.create(
            type="Document",
            title="Example context",
            container=self.portal,
        )

        self.document.blocks = {
            "form-1": {
                "@type": "form",
                "store": True,
                "counter_enabled": True,
                "subblocks": [
                    {
                        "label": "Message",
                        "field_id": "message",
                        "field_type": "text",
                    },
                ],
            },
            "form-2": {
                "@type": "form",
                "store": True,
                "counter_enabled": True,
                "subblocks": [
                    {
                        "label": "Message",
                        "field_id": "message",
                        "field_type": "text",
                    },
                ],
            },
            "form-3": {
                "@type": "form",
                "store": True,
                "subblocks": [
                    {
                        "label": "Message",
                        "field_id": "message",
                        "field_type": "text",
                    },
                ],
            },
        }
        self.document_url = self.document.absolute_url()
        transaction.commit()

    def tearDown(self):
        self.api_session.close()

        # set default block
        self.document.blocks = {
            "text-id": {"@type": "text"},
            "form-id": {"@type": "form"},
        }
        transaction.commit()

    def submit_form(self, data):
        url = f"{self.document_url}/@submit-form"
        response = self.api_session.post(
            url,
            json=data,
        )
        transaction.commit()
        return response

    def test_when_post_data_increase_counter_of_selected_block(self):
        counter = self.api_session.get(f"{self.document_url}/@counter").json()
        self.assertEqual(counter, {"form-1": 0, "form-2": 0, "form-3": 0})

        response = self.submit_form(
            data={
                "from": "john@doe.com",
                "data": [
                    {"field_id": "message", "value": "just want to say hi"},
                ],
                "subject": "test subject",
                "block_id": "form-1",
            }
        )
        self.assertEqual(response.status_code, 200)

        counter = self.api_session.get(f"{self.document_url}/@counter").json()
        self.assertEqual(counter, {"form-1": 1, "form-2": 0, "form-3": 0})

    def test_when_post_data_to_not_enabled_counter_do_not_increase_it(self):
        counter = self.api_session.get(f"{self.document_url}/@counter").json()
        self.assertEqual(counter, {"form-1": 0, "form-2": 0, "form-3": 0})

        response = self.submit_form(
            data={
                "from": "john@doe.com",
                "data": [
                    {"field_id": "message", "value": "just want to say hi"},
                ],
                "subject": "test subject",
                "block_id": "form-3",
            }
        )
        self.assertEqual(response.status_code, 200)

        counter = self.api_session.get(f"{self.document_url}/@counter").json()
        self.assertEqual(counter, {"form-1": 0, "form-2": 0, "form-3": 0})

    def test_counter_endpoint_return_all_data_by_default(self):
        counter = self.api_session.get(f"{self.document_url}/@counter").json()
        self.assertEqual(counter, {"form-1": 0, "form-2": 0, "form-3": 0})

    def test_counter_endpoint_return_counter_of_selected_block(self):
        counter = self.api_session.get(
            f"{self.document_url}/@counter?block_id=form-1"
        ).json()
        self.assertEqual(counter, {"form-1": 0})

    def test_path_to_set_counter_for_a_form(self):
        counter = self.api_session.get(f"{self.document_url}/@counter").json()
        self.assertEqual(counter, {"form-1": 0, "form-2": 0, "form-3": 0})

        url = f"{self.document_url}/@counter"
        response = self.api_session.patch(
            url,
            json={"block_id": "form-1", "counter_value": 123},
        )
        transaction.commit()

        self.assertEqual(response.status_code, 204)

        counter = self.api_session.get(f"{self.document_url}/@counter").json()
        self.assertEqual(counter, {"form-1": 123, "form-2": 0, "form-3": 0})
