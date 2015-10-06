import datetime
from haystack import indexes
from CongressScore.models import Official, Law, Committee, Amendment


class OfficialIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    firstName = indexes.CharField(model_attr='firstName')
    lastName = indexes.CharField(model_attr='lastName')
    description = indexes.CharField(model_attr='description')
    district = indexes.CharField(model_attr='district')
    verboseState = indexes.CharField(model_attr='state_verbose')
    districtState = indexes.CharField(model_attr='districtState')
    title = indexes.CharField(model_attr='title_verbose')
    house = indexes.CharField(model_attr='house', faceted=True)
    party = indexes.CharField(model_attr='party', faceted=True)
    nextReelection = indexes.DateTimeField(model_attr='nextReelection')
    lastElected = indexes.DateTimeField(model_attr='lastElected')
    firstElected = indexes.DateTimeField(model_attr='firstElected')
    baseScore = indexes.IntegerField(model_attr='baseScore', null=True)
    districtInt = indexes.IntegerField(model_attr='districtInt', null=True)
    quickInfo = indexes.CharField(model_attr='getQuickInfo', indexed=False, stored=True)
    microPortraitCode = indexes.CharField(model_attr='getMicroPortraitCode', indexed=False, stored=True)
    suggestions = indexes.FacetCharField()

    def prepare(self, obj):
        prepared_data = super(OfficialIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def prepare_districtState(self, obj):
        return "%s" % (obj.state_verbose())

    def get_model(self):
        return Official

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.order_by('-firstName')#filter(lastElected__lte=datetime.datetime.now())
        return self.get_model().objects.order_by('lastName')#.filter(lastElected__lte=datetime.datetime.now())

class CommitteeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Committee

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects

class AmendmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    parentLaw = indexes.CharField(model_attr='parentLaw')

    def get_model(self):
        return Amendment

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects

class LawIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    datePassed = indexes.DateTimeField(model_attr='datePassed', null=True, faceted=True)
    description = indexes.CharField(model_attr='description')
    editorialComment = indexes.CharField(model_attr='editorialComment')
    hsfComment = indexes.CharField(model_attr='hsfComment')
    unmannedsfComment = indexes.CharField(model_attr='unmannedsfComment')
    privatizationComment = indexes.CharField(model_attr='privatizationComment')
    house = indexes.CharField(model_attr='house', faceted=True)
    govtrackLink = indexes.CharField(model_attr='govtrackLink')
    dateIntroduced = indexes.DateTimeField(model_attr='dateIntroduced')
    quickInfo = indexes.CharField(model_attr='getQuickInfo', indexed=False, stored=True)
    microPortraitCode = indexes.CharField(model_attr='getMicroPortraitCode', indexed=False, stored=True)

    def get_model(self):
        return Law

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(dateIntroduced__lte=datetime.datetime.now())
