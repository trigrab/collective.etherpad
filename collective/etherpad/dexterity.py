# there are no import of archetypes in .archetypes just the way fields are
# retrieved
from zope import schema
from zope.component import getUtility
from collective.etherpad import archetypes
from plone.app.textfield.interfaces import IRichText
from plone.dexterity.interfaces import IDexterityFTI


class EtherpadSyncForm(archetypes.EtherpadSyncForm):

    def __init__(self, context, request):
        super(EtherpadSyncForm, self).__init__(context, request)
        self.dexterity_fti = None

    def save(self):
    #get siteMArkupLanguage
    siteMarkupLanguage = self.settings.seitMarkupLanguage
    #get the content from etherpad in the right format
    if siteMarkupLanguage == "text/html":
        html = self.etherpad.getHTML(padID=self.padID)
        if html and 'html' in html:
            setattr(
                self.context,
                self.field.getName(),
                self.field.fromUnicode(html['html'])
            )
    else:
        text = self.etherpad.getText(PadID=self.padID)
        if text and 'text' in text:
            setattr(
                self.context,
                self.field.getName(),
                self.field.fromUnicode(html[siteMarkupLanguage])
            )
            

class EtherpadEditView(archetypes.EtherpadEditView):
    """Implement etherpad for Archetypes content types"""
    form_instance_class = EtherpadSyncForm

    def __init__(self, context, request):
        super(EtherpadEditView, self).__init__(context, request)
        self.dexterity_fti = None
        self.model = None

    def update(self):
        if self.dexterity_fti is None:
            self.dexterity_fti = getUtility(
                IDexterityFTI,
                name=self.context.portal_type
            )
        if self.model is None:
            self.model = self.dexterity_fti.lookupSchema()
        super(EtherpadEditView, self).update()

    def getEtherpadField(self):
        fields = schema.getFields(self.model)
        for name in fields:
            field = fields[name]
            if IRichText.providedBy(field):
                return field
