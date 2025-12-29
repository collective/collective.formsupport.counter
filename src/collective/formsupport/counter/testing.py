from collective.volto.formsupport.testing import VoltoFormsupportLayer
from collective.volto.formsupport.testing import VoltoFormsupportRestApiLayer
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.testing import z2

import collective.formsupport.counter


class CollectiveFormsupportCounterLayer(VoltoFormsupportLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=collective.formsupport.counter)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(portal, "collective.formsupport.counter:default")


class CollectiveFormsupportCounterRestApiLayer(VoltoFormsupportRestApiLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=collective.formsupport.counter)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)

        applyProfile(portal, "collective.formsupport.counter:default")


COLLECTIVE_FORMSUPPORT_COUNTER_FIXTURE = CollectiveFormsupportCounterLayer()
COLLECTIVE_FORMSUPPORT_COUNTER_API_FIXTURE = CollectiveFormsupportCounterRestApiLayer()

COLLECTIVE_FORMSUPPORT_COUNTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_FORMSUPPORT_COUNTER_FIXTURE,),
    name="CollectiveFormsupportCounterLayer:IntegrationTesting",
)


COLLECTIVE_FORMSUPPORT_COUNTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FORMSUPPORT_COUNTER_FIXTURE,),
    name="CollectiveFormsupportCounterLayer:FunctionalTesting",
)

COLLECTIVE_FORMSUPPORT_COUNTER_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_FORMSUPPORT_COUNTER_API_FIXTURE,),
    name="CollectiveFormsupportCounterRestApiLayer:IntegrationTesting",
)


COLLECTIVE_FORMSUPPORT_COUNTER_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FORMSUPPORT_COUNTER_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectiveFormsupportCounterRestApiLayer:FunctionalTesting",
)
