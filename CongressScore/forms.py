from django import forms    
from haystack.forms import FacetedSearchForm, SearchForm
from CongressScore.models import Official, Committee, Law
import logging

class CommitteeForm(forms.ModelForm):
    class Meta:
        model = Committee
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CommitteeForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            #if self.instance.committee_officials:
                officials = Official.objects.filter(committee_officials=self.instance)

                rankingmember_field = self.fields['rankingMember'].widget
                chairperson_field = self.fields['chairperson'].widget
                rankingmember_choices = []
                rankingmember_choices.append(('', '------'))
                for official in officials:
                    rankingmember_choices.append((official.id, official.fullName()))
                rankingmember_field.choices = rankingmember_choices
                chairperson_field.choices = rankingmember_choices

class LawForm(forms.ModelForm):
    class Meta:
        model = Law
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(LawForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            #if self.instance.Law_Laws:
            officialsOpposing = Official.objects.exclude(officials_supporting=self.instance)
            officialsSupporting = Official.objects.exclude(officials_opposing=self.instance)
            if (self.instance.house == "HS"):
                officialsSupporting = officialsSupporting.filter(house='HS')
                officialsOpposing = officialsOpposing.filter(house='HS')
            elif (self.instance.house == "SN"):
                officialsSupporting = officialsSupporting.filter(house='SN')
                officialsOpposing = officialsOpposing.filter(house='SN')

            officialsOpposing_field = self.fields['officialsOpposing'].widget
            officialsSupporting_field = self.fields['officialsSupporting'].widget

            choicesOpposing = []
            for official in officialsOpposing:
                choicesOpposing.append((official.id, official.fullName()))
            officialsOpposing_field.choices = choicesOpposing

            choicesSupporting = []
            for official in officialsSupporting:
                choicesSupporting.append((official.id, official.fullName()))
            officialsSupporting_field.choices = choicesSupporting


class SpaceScoreFacetedSearchForm(FacetedSearchForm):

    def process_facets(self, sqs):
        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))
        return sqs

    def no_query_found(self):
        return self.process_facets(self.searchqueryset.all())

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        query_data = self.cleaned_data['q']

        if (query_data == ""):
            query_data = " "
        
        # if not query_data:
        #     return self.no_query_found()

        sqs = self._parse_query(query_data)

        if self.load_all:
            sqs = sqs.load_all()
            
        
        return self.process_facets(sqs)


    def _parse_query(self, query_content):
        words = iter(query_content.split())
        result_queryset = self.searchqueryset
        q_cont_op = ''
        for word in words:
            try:
                if word == 'AND':  # should not be next word if q_cont_op is set!
                    nextword = words.next()
                    if (nextword[0] == "\""):
                        sword = nextword
                        while (sword[-1] != "\""):
                            sword = words.next()
                            nextword = nextword + "+" + sword
                    result_queryset = result_queryset.filter_and(content=nextword)
                elif word == 'OR' :
                    nextword = words.next()
                    if (nextword[0] == "\""):
                        sword = nextword
                        while (sword[-1] != "\""):
                            sword = words.next()
                            nextword = nextword + "+" + sword
                    result_queryset = result_queryset.filter_or(content=nextword)
                elif word == 'NOT' or q_cont_op == 'NOT':
                    nextword = words.next()
                    if (nextword[0] == "\""):
                        sword = nextword
                        while (sword[-1] != "\""):
                            sword = words.next()
                            nextword = nextword + "+" + sword
                    result_queryset = result_queryset.exclude(content=nextword)
                else:
                    result_queryset = result_queryset.filter(content=word)
            except StopIteration:
                return result_queryset
        return result_queryset

class SpaceScoreSearchForm(SearchForm):
    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self._parse_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()
        
        return sqs      


    def _parse_query(self, query_content):
        words = iter(query_content.split())
        result_queryset = self.searchqueryset
        q_cont_op = ''
        for word in words:
            try:
                if word == 'AND':  # should not be next word if q_cont_op is set!
                    nextword = words.next()
                    if (nextword[0] == "\""):
                        sword = nextword
                        while (sword[-1] != "\""):
                            sword = words.next()
                            nextword = nextword + "+" + sword
                    result_queryset = result_queryset.filter_and(content=nextword)
                elif word == 'OR' :
                    nextword = words.next()
                    if (nextword[0] == "\""):
                        sword = nextword
                        while (sword[-1] != "\""):
                            sword = words.next()
                            nextword = nextword + "+" + sword
                    result_queryset = result_queryset.filter_or(content=nextword)
                elif word == 'NOT' or q_cont_op == 'NOT':
                    nextword = words.next()
                    if (nextword[0] == "\""):
                        sword = nextword
                        while (sword[-1] != "\""):
                            sword = words.next()
                            nextword = nextword + "+" + sword
                    result_queryset = result_queryset.exclude(content=nextword)
                else:
                    result_queryset = result_queryset.filter(content=word)
            except StopIteration:
                return result_queryset
        return result_queryset
