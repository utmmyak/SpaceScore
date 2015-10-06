from django.contrib import admin
import sys
from CongressScore.forms import CommitteeForm, LawForm
from CongressScore.models import Official, Law, Committee, SpecialInfo, NewsInfo, Amendment
from sorl.thumbnail.admin import AdminImageMixin
import reversion
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class SupportingLawInline(admin.TabularInline):
    verbose_name = u"Supported Law"
    verbose_name_plural = "Supports"
    model = Law.officialsSupporting.through
    extra = 0


class OpposingLawInline(admin.TabularInline):
    verbose_name = u"Opposed Law"
    verbose_name_plural = u"Opposes"
    model = Law.officialsOpposing.through
    extra = 0


class CommitteeInline(admin.TabularInline):
    verbose_name = u"Committee"
    verbose_name_plural = u"Committees"
    model = Committee.committee_officials.through
    extra = 0


class CommitteeLawsInline(admin.TabularInline):
    verbose_name = u"Committee"
    verbose_name_plural = u"Committees"
    model = Committee.committee_laws.through
    extra = 0


class SpecialInfoInline(admin.TabularInline):
    verbose_name = u"Special Info"
    verbose_name_plural = u"Special Information"
    model = SpecialInfo.specialinfo_officials.through
    extra = 0


class OfficialAmendmentInline(admin.TabularInline):
    verbose_name = u"Supports Amendment"
    verbose_name_plural = u"Supporting Amendments"
    model = Amendment.officials_supporting.through
    extra = 0


class LawAmendmentInline(admin.TabularInline):
    model = Amendment
    fk_name = "parentLaw"
    extra = 0


class AmendmentAdmin(reversion.VersionAdmin):
    # fieldsets = (
    #     ('Info', {'fields': ('name', 'description', 'isPartOfLaw',)}),
    #     ('Relationships', {'fields': ('parentLaw','officials_supporting',)}),
    #     ('Details', {'classes': ('collapse',), 'fields': (('editorialComment',), ('hsfComment', 'unmannedsfComment',), ('privatizationComment', 'publicComment',),)}),
    #     ('Weight', {'fields': ('baseWeight','hsfWeight','unmannedsfWeight','privatizationWeight','publicWeight',)}),
    # )
    fieldsets = (
        ('Info', {'fields': ('name', 'description', 'isPartOfLaw',)}),
        ('Relationships', {'fields': ('parentLaw', 'officials_supporting',)}),
        ('Details', {'classes': ('grp-collapse grp-closed',), 'fields': (
            ('editorialComment',), ('hsfComment', 'unmannedsfComment',), ('privatizationComment', 'publicComment',),)}),
        ('Weight', {'fields': ('baseWeight', 'hsfWeight', 'unmannedsfWeight', 'privatizationWeight', 'publicWeight',)}),
    )

    filter_horizontal = ('officials_supporting',)
    list_display = (
        'name', 'isPartOfLaw', 'baseWeight', 'hsfWeight', 'unmannedsfWeight', 'privatizationWeight', 'publicWeight',)
    search_fields = ('name', 'isPartOfLaw',)
    list_filter = ('isPartOfLaw',)
    view_on_site = True


class CommitteeAdmin(reversion.VersionAdmin):
    form = CommitteeForm
    fieldsets = (
        ('Info', {'fields': ('name', 'description', 'house',)}),
        ('Power Metrics', {'fields': ('powerModifier', 'spaceRelatedness',)}),
        ('Relationships', {'fields': (
            ('chairperson', 'rankingMember',), ('committee_officials', 'committee_laws', 'parentCommittee',),)})
    )
    filter_horizontal = ('committee_officials', 'committee_laws',)
    list_display = ('name', 'house', 'powerModifier', 'spaceRelatedness',)
    search_fields = ('name', 'house',)
    view_on_site = True
    list_filter = ('house', 'parentCommittee',)


class SpecialInfoAdmin(reversion.VersionAdmin):
    fieldsets = (
        ('Info', {'fields': ('name', 'description', 'picture',)}),
        ('Relationships', {'fields': ('specialinfo_officials',)})
    )
    filter_horizontal = ('specialinfo_officials',)
    list_display = ('name', 'state',)
    search_fields = ('name', 'state',)


class OfficialResource(resources.ModelResource):
    class Meta:
        model = Official
        exclude = ('id', 'peoplesQuantity', 'peoplesScore',)
        fields = ('firstName', 'lastName', 'district', 'districtState', 'house',
                  'firstElected', 'lastElected', 'nextReelection', 'dateOfBirth',
                  'placeOfResidence', 'education', 'scienceExperience', 'occupation',
                  'party', 'description', 'editorialComment', 'hsfComment', 'unmannedsfComment',
                  'privatizationComment', 'publicComment', 'picture', 'leadershipTitle', 'cspanid',
                  'sex', 'twitterID', 'phoneNumber', 'senatorRank', 'website', 'netWorth', 'govtrackLink',
                  'govtrackID', 'baseScore', 'unmannedsfScore', 'hsfScore', 'privatizationScore',
                  'publicScore', 'wikipediaID',)

    #@staticmethod
    #def get_instance(self, instance_loader, row):
    #    return False

    # def save_instance(self, instance, real_dry_run):
    #     if not real_dry_run:
    #         try:
    #             obj = .objects.get(some_val=instance.some_val)
    #             # extra logic if object already exist
    #         except NFCTag.DoesNotExist:
    #             # create new object
    #             obj = YourModel(some_val=instance.some_val)
    #             obj.save()

    @staticmethod
    def before_import(dataset, dry_run, **kwargs):
        if dataset.headers:
            # dataset.headers = [str(header).lower().strip() for header in dataset.headers]
            if 'id' not in dataset.headers:
                dataset.headers.append('id')
                # super(OfficialResource, self).before_import(self, dataset, dry_run, **kwargs)


class OfficialAdmin(ImportExportActionModelAdmin, reversion.VersionAdmin):
    resource_class = OfficialResource
    # fieldsets = (
    #     ('Basic', {'fields': (('firstName', 'lastName', 'sex',), ('districtState', 'district',), ('house', 'party',
    #        'leadershipTitle',),)}),
    #     ('Date Information', {'classes': ('collapse',), 'fields': (('firstElected', 'lastElected',),
    #       ('nextReelection', 'dateOfBirth',),)}),
    #     ('Background', {
    #         'classes': ('collapse',),
    #         'fields': ('placeOfResidence', 'education', 'occupation', 'netWorth', 'scienceExperience',)
    #     }),
    #     ('Details', {'classes': ('collapse',), 'fields': (('description', 'editorialComment',), ('hsfComment',
    #        'unmannedsfComment',), ('privatizationComment', 'publicComment',),)}),
    #     ('Picture', {'classes': ('collapse',), 'fields': ('picture',)}),
    #     ('Links and Communication', {'classes': ('collapse',), 'fields': (('govtrackLink', 'cspanid',), ('website',
    #        'twitterID', 'phoneNumber',),)}),
    #     ('Stats', {'classes': ('collapse',), 'fields': (('baseScore'),('peoplesScore','peoplesQuantity'),('hsfScore',
    #       'unmannedsfScore'),('privatizationScore','publicScore'),)})
    # )
    fieldsets = (  # for GRAPPELLI
                   ('Basic', {'fields': (('firstName', 'lastName', 'sex',), ('districtState', 'district',),
                                         ('house', 'party', 'leadershipTitle',),)}),
                   ('Date Information', {'classes': ('grp-collapse grp-closed',), 'fields': (
                       ('firstElected', 'lastElected',), ('nextReelection', 'dateOfBirth',),)}),
                   ('Background', {
                       'classes': ('grp-collapse grp-closed',),
                       'fields': ('placeOfResidence', 'education', 'occupation', 'netWorth', 'scienceExperience',)
                   }),
                   ('Details', {'classes': ('grp-collapse grp-closed',), 'fields': (
                       ('description', 'editorialComment',), ('hsfComment', 'unmannedsfComment',),
                       ('privatizationComment', 'publicComment',),)}),
                   ('Picture', {'classes': ('grp-collapse grp-closed',), 'fields': ('picture',)}),
                   ('Links and Communication', {'classes': ('grp-collapse grp-closed',), 'fields': (
                       ('govtrackLink', 'cspanid', 'wikipediaID',), ('website', 'twitterID', 'phoneNumber',),)}),
                   ('Stats', {'classes': ('grp-collapse grp-closed',), 'fields': (
                       'baseScore', ('peoplesScore', 'peoplesQuantity'), ('hsfScore', 'unmannedsfScore'),
                       ('privatizationScore', 'publicScore'),)})
                   )

    readonly_fields = (
        'baseScore', 'hsfScore', 'unmannedsfScore', 'privatizationScore', 'publicScore', 'peoplesScore',
        'peoplesQuantity')
    inlines = (CommitteeInline, SpecialInfoInline, SupportingLawInline, OpposingLawInline, OfficialAmendmentInline,)
    list_display = (
        'fullName', 'house', 'nextReelection', 'party', 'baseScore', 'hsfScore', 'unmannedsfScore',
        'privatizationScore',
        'publicScore',)
    list_filter = ('house', 'party', 'leadershipTitle', 'scienceExperience',)
    search_fields = ('firstName', 'lastName',)
    view_on_site = True


class LawAdmin(reversion.VersionAdmin):
    form = LawForm
    # fieldsets = (
    #     ('Basic', {'fields': ('name','house',)}),
    #     (None, {'fields': ('officialsSupporting',)}),
    #     (None, {'fields': ('officialsOpposing',)}),
    #     ('Date Information', {'classes': ('collapse',),
    #     'fields': ('dateEnacted','datePassed','passedHouse','passedSenate','passedCommittee','dateIntroduced',)}),
    #     ('Details', {'classes': ('collapse',), 'fields': ('description','editorialComment','hsfComment',
    #     'unmannedsfComment','privatizationComment','publicComment',)}),
    #     ('Weight', {'fields': ('baseWeight','hsfWeight','unmannedsfWeight','privatizationWeight','publicWeight',
    #     'noBasePenalty',)}),
    #     ('Stats', {'classes': ('collapse',), 'fields': (('peoplesScore','peoplesQuantity'),)}),
    #     ('Other', {'classes': ('collapse',), 'fields': ('picture','govtrackLink',)}),
    # )
    fieldsets = (  # for GRAPPELLI
                   ('Basic', {'fields': ('name', 'house',)}),
                   (None, {'fields': ('officialsSupporting',)}),
                   (None, {'fields': ('officialsOpposing',)}),
                   ('Date Information', {'classes': ('grp-collapse grp-closed',), 'fields': (
                       'dateEnacted', 'datePassed', 'passedHouse', 'passedSenate', 'passedCommittee',
                       'dateIntroduced',)}),
                   ('Details', {'classes': ('grp-collapse grp-closed',), 'fields': (
                       'description', 'editorialComment', 'hsfComment', 'unmannedsfComment', 'privatizationComment',
                       'publicComment',)}),
                   ('Weight', {'fields': (
                       'baseWeight', 'hsfWeight', 'unmannedsfWeight', 'privatizationWeight', 'publicWeight',
                       'noBasePenalty',)}),
                   ('Stats',
                    {'classes': ('grp-collapse grp-closed',), 'fields': (('peoplesScore', 'peoplesQuantity'),)}),
                   ('Other', {'classes': ('grp-collapse grp-closed',), 'fields': ('picture', 'govtrackLink',)}),
                   )

    readonly_fields = ('peoplesScore', 'peoplesQuantity')
    filter_horizontal = ('officialsSupporting', 'officialsOpposing',)
    inlines = (CommitteeLawsInline, LawAmendmentInline,)
    list_display = (
        'name', 'dateIntroduced', 'house', 'baseWeight', 'hsfWeight', 'unmannedsfWeight', 'privatizationWeight',
        'publicWeight', 'peoplesScore', 'peoplesQuantity',)
    search_fields = ('name', 'description',)
    list_filter = ('house', 'dateIntroduced',)
    view_on_site = True


class NewsInfoAdmin(reversion.VersionAdmin, AdminImageMixin):
    fieldsets = (
        ('Basic', {'fields': ('name', 'description', 'dateReleased', 'visible', 'link', 'picture',)}),
    )
    search_fields = ('name',)
    list_filter = ('dateReleased', 'visible',)
    list_display = ('name', 'dateReleased', 'visible',)


admin.site.register(Official, OfficialAdmin)
admin.site.register(Law, LawAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(SpecialInfo, SpecialInfoAdmin)
admin.site.register(NewsInfo, NewsInfoAdmin)
admin.site.register(Amendment, AmendmentAdmin)
