from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
# from django.core.urlresolvers import reverse
from django.views import generic
# from django.shortcuts import render
from django.db.models import Avg
# from django.db import models
from django.template import RequestContext

import urllib
import logging

# from haystack.generic_views import FacetedSearchView
# from haystack.generic_views import SearchView, SearchMixin
# import haystack.views
from haystack.views import SearchView
# from haystack.query import SearchQuerySet
from haystack.forms import FacetedSearchForm
# import haystack.constants
# from CongressScore.forms import SpaceScoreFacetedSearchForm

from CongressScore.models import Official, Law, Committee, NewsInfo, Amendment

logger = logging.getLogger('SpaceScore')


class DetailsView(generic.DetailView):
    model = Official
    context_object_name = 'Official'
    template_name = 'CongressScore/Official/details.html'


class LawDetailsView(generic.DetailView):
    model = Law
    context_object_name = 'Law'
    template_name = 'CongressScore/Bill/details.html'


class AmendmentDetailsView(generic.DetailView):
    model = Amendment
    context_object_name = 'Amendment'
    template_name = 'CongressScore/Amendment/details.html'


class CommitteeDetailsView(generic.DetailView):
    model = Committee
    context_object_name = 'Committee'
    template_name = 'CongressScore/Committee/details.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeDetailsView, self).get_context_data(**kwargs)
        # id__in=Profile.category.all())
        # return Committee.objects.filter(publisher=publisher)
        if (self.object.chairperson):
            context['member_officials_dem'] = self.object.committee_officials.all().filter(
                party="DEM").exclude(id=self.object.rankingMember.id).exclude(id=self.object.chairperson.id)
            context['member_officials_rep'] = self.object.committee_officials.all().filter(
                party="REP").exclude(id=self.object.chairperson.id).exclude(id=self.object.rankingMember.id)
        else:
            context['member_officials_dem'] = self.object.committee_officials.all().filter(
                party="DEM")
            context['member_officials_rep'] = self.object.committee_officials.all().filter(
                party="REP")

        return context


# class FacetedSearchMixin(SearchMixin):
#     """
#     A mixin that allows adding in a Haystack search functionality with search
#     faceting.
#     """
#     form_class = FacetedSearchForm

#     def get_form_kwargs(self):
#         kwargs = super(FacetedSearchMixin, self).get_form_kwargs()
#         kwargs.update({
#             'selected_facets': self.request.GET.getlist("selected_facets")
#         })
#         return kwargs

#     def get_context_data(self, **kwargs):
#         context = super(FacetedSearchMixin, self).get_context_data(**kwargs)
#         context.update({'facets': self.queryset.facet_counts()})
#         return context

# class FacetedSearchView(FacetedSearchMixin, SearchView):
#     """
#     A view class for searching a Haystack managed search index with
#     facets
#     """
#     pass

# class OrderableFacetedSearchView(FacetedSearchView):
#     def get_queryset(self):
#         queryset = super(OrderableFacetedSearchView, self).get_queryset()

#         sort = self.request.GET.get('sort_by')

#         if sort:
#             return queryset.order_by('{0}'.format(sort))
#         else:
#             return queryset.order_by('lastName')

#     def get_context_data(self, *args, **kwargs):
#         context = super(OrderableFacetedSearchView, self).get_context_data(*args, **kwargs)
# do something
#         return context


# class SpaceScoreFacetedSearchView(OrderableFacetedSearchView):
#     queryset = SearchQuerySet().models(Official).facet('house')
#     form_class = SpaceScoreFacetedSearchForm
#     template_name = 'search/search_official.html'

class SpaceScoreFacetedSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        # Needed to switch out the default form class.
        if kwargs.get('form_class') is None:
            kwargs['form_class'] = FacetedSearchForm

        super(SpaceScoreFacetedSearchView, self).__init__(*args, **kwargs)

    def __call__(self, request):
        results_no = request.GET.get('results_no')
        if (results_no and int(results_no) > 0 and int(results_no) <= 100):
            self.results_per_page = int(results_no)
        return super(SpaceScoreFacetedSearchView, self).__call__(request)

    def get_results(self):
        sqs = super(SpaceScoreFacetedSearchView, self).get_results()
        uSort = self.request.GET.get('sort_by')

        if uSort:
            sort = urllib.unquote(uSort)
            if (',' in sort):
                splitStr = sort.split(',')
                atuple = ()
                for item in splitStr:
                    atuple = atuple + (item,)
                # here we expand the tuple we just built
                return sqs.order_by(*atuple)
            else:
                return sqs.order_by(sort)
        else:
            return sqs.order_by('-django_ct', 'lastName')

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        # This way the form can always receive a list containing zero or more
        # facet expressions:
        form_kwargs['selected_facets'] = self.request.GET.getlist(
            "selected_facets")

        return super(SpaceScoreFacetedSearchView, self).build_form(form_kwargs)

    def build_page(self):
        (paginator, page) = super(
            SpaceScoreFacetedSearchView, self).build_page()
        self.results_per_page = 50
        return (paginator, page)

    def extra_context(self):
        extra = super(SpaceScoreFacetedSearchView, self).extra_context()
        extra['facets'] = self.results.facet_counts()

        return extra


class SpaceScoreFacetedSearchViewGeneral(SpaceScoreFacetedSearchView):
    def __init__(self, *args, **kwargs):
        self.page_object_list = list()
        super(SpaceScoreFacetedSearchViewGeneral, self).__init__(
            *args, **kwargs)

    def build_page(self):
        (paginator, page) = super(
            SpaceScoreFacetedSearchViewGeneral, self).build_page()
        self.results_per_page = 50
        self.page_object_list = page.object_list
        return (paginator, page)

    def extra_context(self):
        extra = super(SpaceScoreFacetedSearchViewGeneral, self).extra_context()
        content_types = set()
        for result in self.page_object_list:
            content_types.add(result.content_type())
        extra['suggestiond'] = self.results.spelling_suggestion()

        # extra['request'] = RequestContext(self.request)
        extra['content_types'] = list(content_types)
        return extra


def OfficialVote(request, official_id):
    myOfficial = get_object_or_404(Official, pk=official_id)
    myOfficial.addVote(request.POST['userScore'])
    myOfficial.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    # redirect not necessary as we're using AJAX
    return HttpResponse(status=201)


def LawVote(request, law_id):
    myLaw = get_object_or_404(Law, pk=law_id)
    myLaw.addVote(request.POST['userScore'])
    myLaw.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    # redirect not necessary as we're using AJAX
    return HttpResponse(status=201)


def HomeView(request):
    avg_score = Official.objects.all().aggregate(
        Avg('baseScore'))['baseScore__avg']
    total_officials = len(Official.objects.all())
    usf_officials = Official.objects.filter(unmannedsfScore__gte=80)
    usf_officials_len = len(usf_officials)
    hsf_officials = Official.objects.filter(hsfScore__gte=80)
    hsf_officials_len = len(hsf_officials)
    pub_officials = Official.objects.filter(publicScore__gte=80)
    pub_officials_len = len(pub_officials)
    priv_officials = Official.objects.filter(privatizationScore__gte=80)
    priv_officials_len = len(priv_officials)
    high_basescore_officials = Official.objects.filter(baseScore__gte=90)
    high_basescore_officials_len = len(high_basescore_officials)

    newsInfo = NewsInfo.objects.filter(
        visible=True).order_by('-dateReleased')[:5]

    return render(request, 'home.html', {'avg_score': avg_score,
                                         'total_officials': total_officials, 'usf_officials': usf_officials,
                                         'hsf_officials': hsf_officials, 'pub_officials': pub_officials,
                                         'priv_officials': priv_officials,
                                         'high_basescore_officials': high_basescore_officials,
                                         'usf_officials_len': usf_officials_len,
                                         'hsf_officials_len': hsf_officials_len, 'pub_officials_len': pub_officials_len,
                                         'priv_officials_len': priv_officials_len,
                                         'high_basescore_officials_len': high_basescore_officials_len,
                                         'newsInfo': newsInfo})


def server_error(request, template_name='500.html'):
    from django.http import HttpResponseServerError
    from django.template.loader import get_template

    t = get_template(template_name)
    return HttpResponseServerError(t.render(RequestContext(request)))
