from django.conf.urls import patterns, url
from CongressScore.forms import SpaceScoreSearchForm, SpaceScoreFacetedSearchForm
from CongressScore.models import Official, Law, Committee
from CongressScore.views import OfficialVote, LawVote, SpaceScoreFacetedSearchView, SpaceScoreFacetedSearchViewGeneral
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, FacetedSearchView, search_view_factory

from CongressScore import views
sqsAll = SearchQuerySet().filter_or(content='law').filter_or(content='official')
sqsLaws = SearchQuerySet().filter_or(content='law')#.load_all()

#sqsLawsIntroduced = SearchQuerySet().models(Law).order_by("-dateIntroduced")
sqsOfficials = SearchQuerySet().filter(content='official').facet('house')#.facet('party')#.load_all()
#sqsOfficialsNextElection = SearchQuerySet().models(Official).order_by("nextReelection")
#sqsOfficialsBaseScore = SearchQuerySet().models(Official).order_by("-baseScore")
#sqsOfficialsParty = SearchQuerySet().models(Official).order_by("party")
#sqsOfficialsTitle = SearchQuerySet().models(Official).order_by("house", "leadershipTitle")
#sqsOfficialsState = SearchQuerySet().models(Official).order_by("districtState")
#
#sqsOfficialsHouseState = sqsOfficialsState.filter(house='HS')
#sqsOfficialsHouseBaseScore = sqsOfficialsBaseScore.filter(house='HS')
#sqsOfficialsHouseNextElection = sqsOfficialsNextElection.filter(house='HS')
#sqsOfficialsHouse = sqsOfficials.filter(house='HS')
#sqsOfficialsSenateState = sqsOfficialsState.filter(house='SN')
#sqsOfficialsSenateBaseScore = sqsOfficialsBaseScore.filter(house='SN')
#sqsOfficialsSenateNextElection = sqsOfficialsNextElection.filter(house='SN')


urlpatterns = patterns('haystack.views',
    #url(r'^$', SearchView(template='search/search.html', searchqueryset=sqsAll, form_class=SpaceScoreSearchForm), name='haystack_search'),
    url(r'^$', SpaceScoreFacetedSearchViewGeneral(template='search/search.html',searchqueryset=sqsAll,form_class=SpaceScoreFacetedSearchForm), name='haystack_search'),
    url(r'^Legislator/(?P<pk>\d+)/$', views.DetailsView.as_view(), name='details'),
    url(r'^Legislator/(?P<official_id>\d+)/vote/$', views.OfficialVote, name='vote'),
    url(r'^Bill/(?P<pk>\d+)/$', views.LawDetailsView.as_view(), name='law_details'),
    url(r'^Bill/(?P<law_id>\d+)/vote/$', views.LawVote, name='law_vote'),
    url(r'^Committee/(?P<pk>\d+)/$', views.CommitteeDetailsView.as_view(), name='committee_details'),
    url(r'^Amendment/(?P<pk>\d+)/$', views.AmendmentDetailsView.as_view(), name='amendment_details'),
    #url(r'^Bill/$', SearchView(template='search/search_law.html',searchqueryset=sqsLaws,form_class=SpaceScoreSearchForm), name='haystack_search_bill'),
    url(r'^Bill/$', SpaceScoreFacetedSearchViewGeneral(template='search/search_law.html',searchqueryset=sqsLaws,form_class=SpaceScoreFacetedSearchForm), name='haystack_search_law'),
    #url(r'^Bill/Introduced/$', SearchView(template='search/search_law_sortby_introduced.html',searchqueryset=sqsLawsIntroduced,form_class=SpaceScoreSearchForm), name='haystack_search_bill_introduced'),
    #url(r'^Official/$', SpaceScoreFacetedSearchView.as_view(), name='haystack_search_official'),
    url(r'^Legislator/$', SpaceScoreFacetedSearchViewGeneral(template='search/search_official.html',searchqueryset=sqsOfficials,form_class=SpaceScoreFacetedSearchForm), name='haystack_search_official'),
    #url(r'^Official/sort:EndOfTerm/$', SearchView(template='search/search_official.html',searchqueryset=sqsOfficialsNextElection,form_class=SpaceScoreSearchForm), name='haystack_search_official_endterm'),
    #url(r'^Official/sort:State/$', SearchView(template='search/search_official.html',searchqueryset=sqsOfficialsState,form_class=SpaceScoreSearchForm), name='haystack_search_official_state'),
    #url(r'^Official/sort:BaseScore/$', SearchView(template='search/search_official.html',searchqueryset=sqsOfficialsBaseScore,form_class=SpaceScoreSearchForm), name='haystack_search_official_basescore'),
    #url(r'^Official/sort:Party/$', SearchView(template='search/search_official.html',searchqueryset=sqsOfficialsParty,form_class=SpaceScoreSearchForm), name='haystack_search_official_party'),
    #url(r'^Official/sort:Title/$', SearchView(template='search/search_official.html',searchqueryset=sqsOfficialsTitle,form_class=SpaceScoreSearchForm), name='haystack_search_official_title'),
    #url(r'^Official/filter:House/$', SearchView(template='search/search_official.html',searchqueryset=sqsOfficialsHouse,form_class=SpaceScoreSearchForm), name='haystack_search_official_house'),
    #url(r'^Official/filter:House/sort:EndOfTerm/$', SearchView(template='search/search_official.html',searchqueryset=sqsOfficialsHouseNextElection,form_class=SpaceScoreSearchForm), name='haystack_search_official_house_endterm'),
    #url(r'^Official/filter:House/sort:State/$', SearchView(template='search/search_official.html',searchqueryset=sqsOfficialsHouseState,form_class=SpaceScoreSearchForm), name='haystack_search_official_house_state'),
    #url(r'^Official/filter:House/sort:BaseScore/$', SearchView(template='search/search_official.html',searchqueryset=sqsOfficialsHouseBaseScore,form_class=SpaceScoreSearchForm), name='haystack_search_official_house_basescore'),
    #url(r'^MyOfficials/$', SearchView(template='search/search_myofficials.html',searchqueryset=sqsOfficials,form_class=SpaceScoreSearchForm), name='haystack_search_myofficials')
    url(r'^MyLegislators/$', SpaceScoreFacetedSearchViewGeneral(template='search/search_myofficials.html',searchqueryset=sqsOfficials,form_class=SpaceScoreFacetedSearchForm), name='haystack_search_myofficials'),
)
