#!/usr/bin/python
# coding=utf-8

""" Models for SpaceScore/CongressScore """

import datetime
import sys
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.utils import timezone
from django.utils.html import format_html
from django.utils.encoding import smart_str, smart_unicode
from django import forms
from django.contrib.humanize.templatetags.humanize import ordinal
from localflavor.us.models import USStateField, PhoneNumberField
from localflavor.us.us_states import US_STATES
from django.db.models.signals import m2m_changed
from django.db.utils import IntegrityError
from sorl.thumbnail import ImageField as SorlImageField
from datetime import datetime
from django.utils.safestring import mark_safe

import requests

OFFICIAL_HOUSES = (('HS', 'House'),
                   ('SN', 'Senate'))
OFFICIAL_TITLE = (('HS', (('M', 'Congressman'), ('F', 'Congresswoman'))), ('SN', (('M', 'Senator'), ('F', 'Senator'))))
LAW_HOUSES = (('HS', 'House'),
              ('SN', 'Senate'),
              ('BT', 'Both'))
PARTIES = (('DEM', 'Democrat'),
           ('REP', 'Republican'),
           ('IND', 'Independent'))
SEXES = (('M', 'Male'),
         ('F', 'Female'))
RANKS = (('S', 'Senior'),
         ('J', 'Junior'))

reload(sys)
sys.setdefaultencoding("utf-8")


def get_display(key, list):
    d = dict(list)
    if key in d:
        return d[key]
    return None


def get_display2(key1, key2, mylist):
    d = dict(mylist)
    if key1 in d:
        d2 = dict(d[key1])
        if key2 in d2:
            return d2[key2]
    return None



class Official(models.Model):
    firstName = models.CharField("First Name", max_length=200, )
    lastName = models.CharField("Last Name", max_length=200, )
    district = models.CharField("Legislative District", max_length=200, blank=True, )
    districtState = USStateField("District State", default="NY", max_length=2, )
    house = models.CharField("House", max_length=2, choices=OFFICIAL_HOUSES, )
    firstElected = models.DateTimeField("Date First Elected", null=True, blank=True, )
    lastElected = models.DateTimeField("Date Last Elected", blank=True, )
    nextReelection = models.DateTimeField("Date of Next Election", blank=True, )
    nextReelection.allow_future = True
    dateOfBirth = models.DateTimeField("Date of Birth", blank=True, )
    placeOfResidence = models.CharField("Place of Residence", max_length=200, blank=True, )
    education = models.TextField(max_length=200, blank=True, )
    scienceExperience = models.BooleanField("Has Science Experience", default=False, )
    occupation = models.CharField(max_length=200, blank=True, )
    party = models.CharField("Party", max_length=3, choices=PARTIES, )
    description = models.TextField(blank=True, )
    editorialComment = models.TextField("Editorial Comment", blank=True, )
    hsfComment = models.TextField("Human Spaceflight Comment", blank=True, )
    unmannedsfComment = models.TextField("Unmanned Spaceflight Comment", blank=True, )
    privatizationComment = models.TextField("Commercial Comment", blank=True, )
    publicComment = models.TextField("Public Comment", blank=True, null=True, )
    picture = models.ImageField(upload_to="%Y/%m/%d", blank=True, null=True, max_length=500, )
    leadershipTitle = models.CharField("Leadership Title", max_length=200, blank=True, null=True, )
    cspanid = models.IntegerField(blank=True, null=True, )
    wikipediaID = models.CharField(blank=True, max_length=400, null=True, )
    sex = models.CharField("Sex", max_length=2, choices=SEXES, )
    twitterID = models.CharField("Twitter ID", max_length=400, blank=True, )
    phoneNumber = PhoneNumberField("Phone Number", blank=True, null=True, max_length=11, )
    senatorRank = models.CharField("Seniority Rank", max_length=2, choices=RANKS, blank=True, )
    website = models.URLField("Official Website", blank=True, null=True, max_length=400, )
    netWorth = models.IntegerField("Net Worth", blank=True, null=True, )
    govtrackLink = models.URLField("GovTrack.us Link", max_length=400, blank=True, )
    allow_future = True
    govtrackID = models.CharField("GovTrack ID", max_length=15, blank=True, )
    baseScore = models.IntegerField("Base Score", blank=True, null=True, )
    unmannedsfScore = models.IntegerField("Unmanned Spaceflight Score", blank=True, null=True, )
    hsfScore = models.IntegerField("Human Spaceflight Score", blank=True, null=True, )
    privatizationScore = models.IntegerField("Commercial Score", blank=True, null=True, )
    publicScore = models.IntegerField("Public Score", blank=True, null=True, )

    peoplesQuantity = models.IntegerField("Quantity of People Voting", default=0, )
    peoplesScore = models.FloatField("People's Score", default=0.0, )

    def friendly_district(self):
        """Returns ordinal of district"""
        return ordinal(self.district)

    def districtInt(self):
        if (self.district == ""):
            return None
        else:
            try:
                return int(self.district)
            except ValueError:  # we could not convert to integer
                return None  # no districtInt could be found

    def supportingAmendments(self):
        return Amendment.objects.filter(officials_supporting__id=self.id)

    def supportingLaws(self):
        return Law.objects.filter(officialsSupporting__id=self.id)

    def opposingLaws(self):
        return Law.objects.filter(officialsOpposing__id=self.id)

    def getPortraitUrl(self):
        """Method to return stored image for admin panel"""
        if (not self.picture):
            creditinfo = requests.get("https://www.govtrack.us/data/photos/%s-credit.txt" % self.govtrackID,
                                      stream=True).raw.read().rstrip()
            src = "https://www.govtrack.us/data/photos/{0}-200px.jpeg".format(self.govtrackID)
            return format_html(
                '<img id="portrait" src="{0}" width="200" alt="{1}"/><span id="portrait-credit">Source: {2}</span>',
                src, smart_str(self), creditinfo)
        else:
            return format_html('<img id="portrait" src="{0}" width="{1}" height="{2}" alt="{3}"/>', self.picture.url,
                               self.picture.width, self.picture.height, self)

    getPortraitUrl.allow_tags = True

    def getMicroPortraitCode(self):
        if (not self.picture):
            src = "https://www.govtrack.us/data/photos/{0}-50px.jpeg".format(self.govtrackID)
            return format_html('<img class="microportrait" src="{0}" alt="{1}"/>', src, smart_str(self))
        else:
            return format_html('<img class="microportrait" src="{0}" alt="{1}"/>', self.picture.url, smart_str(self))

    getMicroPortraitCode.allow_tags = True

    def party_verbose(self):
        return get_display(self.party, PARTIES)

    def state_verbose(self):
        return get_display(self.districtState, US_STATES)

    def house_verbose(self):
        return get_display(self.house, OFFICIAL_HOUSES)

    def title_verbose(self):
        if (self.leadershipTitle):
            return get_display(self.house, OFFICIAL_HOUSES) + " " + self.leadershipTitle
        else:
            return get_display2(self.house, self.sex, OFFICIAL_TITLE)

    def constituency_verbose(self):
        return (
        ((r'{0} District, {1}') if self.house == "HS" and self.district else r"{1}").format(self.friendly_district(),
                                                                                            self.districtState))

    def constituency_reversed(self):
        return ((r"{0}{1}").format(self.districtState, self.district))

    def fullName(self):
        return self.firstName + ' ' + self.lastName

    fullName.short_description = "Name"
    fullName.admin_order_field = "lastName"

    def addVote(self, score):
        myScore = float(score)  # score will be passed as a string by javascript from data-send
        self.peoplesScore *= (float(self.peoplesQuantity) / (self.peoplesQuantity + 1))
        self.peoplesQuantity += 1
        self.peoplesScore += (myScore / self.peoplesQuantity)

    def _baseScore(self):
        points = 0.00
        totalPoints = 0.00
        for amendment in self.supportingAmendments():
            if ((amendment.baseWeight >= 0) or not amendment.noBasePenalty):
                totalPoints += abs(amendment.baseWeight)
                points += amendment.baseWeight
        for law in self.supportingLaws():
            if ((law.baseWeight >= 0) or not law.noBasePenalty):
                totalPoints += abs(law.baseWeight)
                points += law.baseWeight
        for law in self.opposingLaws():
            if (not (law.baseWeight > 0) or not law.noBasePenalty):
                totalPoints += abs(law.baseWeight)
                points -= law.baseWeight
        if (totalPoints == 0):
            return None
        result = ((points / totalPoints) / 2) + 0.5
        return int(result * 100)

    def _hsfScore(self):
        points = 0.00
        totalPoints = 0.00
        for amendment in self.supportingAmendments():
            totalPoints += abs(amendment.hsfWeight)
            points += amendment.hsfWeight
        for law in self.supportingLaws():
            totalPoints += abs(law.hsfWeight)
            points += law.hsfWeight
        for law in self.opposingLaws():
            totalPoints += abs(law.hsfWeight)
            points -= law.hsfWeight
        if (totalPoints == 0):
            return None
        result = ((points / totalPoints) / 2) + 0.5
        return int(round(result, 2) * 100)

    def _unmannedsfScore(self):
        points = 0.00
        totalPoints = 0.00
        for amendment in self.supportingAmendments():
            totalPoints += abs(amendment.unmannedsfWeight)
            points += amendment.unmannedsfWeight
        for law in self.supportingLaws():
            totalPoints += abs(law.unmannedsfWeight)
            points += law.unmannedsfWeight
        for law in self.opposingLaws():
            totalPoints += abs(law.unmannedsfWeight)
            points -= law.unmannedsfWeight
        if (totalPoints == 0):
            return None
        result = ((points / totalPoints) / 2) + 0.5
        return int(round(result, 2) * 100)

    def _privatizationScore(self):
        points = 0.00
        totalPoints = 0.00
        for amendment in self.supportingAmendments():
            totalPoints += abs(amendment.privatizationWeight)
            points += amendment.privatizationWeight
        for law in self.supportingLaws():
            totalPoints += abs(law.privatizationWeight)
            points += law.privatizationWeight
        for law in self.opposingLaws():
            totalPoints += abs(law.privatizationWeight)
            points -= law.privatizationWeight
        if (totalPoints == 0):
            return None
        result = ((points / totalPoints) / 2) + 0.5
        return int(round(result, 2) * 100)

    def _publicScore(self):
        points = 0.00
        totalPoints = 0.00
        for amendment in self.supportingAmendments():
            totalPoints += abs(amendment.publicWeight)
            points += amendment.publicWeight
        for law in self.supportingLaws():
            totalPoints += abs(law.publicWeight)
            points += law.publicWeight
        for law in self.opposingLaws():
            totalPoints += abs(law.publicWeight)
            points -= law.publicWeight
        if (totalPoints == 0):
            return None
        result = ((points / totalPoints) / 2) + 0.5
        return int(round(result, 2) * 100)

    def updateScores(self):
        self.baseScore = self._baseScore()
        self.unmannedsfScore = self._unmannedsfScore()
        self.hsfScore = self._hsfScore()
        self.publicScore = self._publicScore()
        self.privatizationScore = self._privatizationScore()

    def save(self):
        self.updateScores()
        super(Official, self).save()

    def officialCommittees(self):
        return Committee.objects.filter(committee_officials__id=self.id)

    def officialChairperson(self):
        return Committee.objects.filter(chairperson_id=self.id)

    def officialRankingMember(self):
        return Committee.objects.filter(rankingMember_id=self.id)

    def officialSpecialInfo(self):
        return SpecialInfo.objects.filter(specialinfo_officials__id=self.id)

    def renderType(self):
        return "Official"

    def url(self):
        # Returns relative url of this bill
        return ("/CongressScore/Legislator/%s/" % self.id)

    def get_absolute_url(self):
        return self.url()

    def getQuickInfoText(self):
        specialInformation = r""
        for specialInfo in self.officialSpecialInfo():
            specialInformation += "&bull;" + specialInfo.name
        qinfo_raw = ((r"{0} &bull; " if self.leadershipTitle else "") +
                     r"{1} &bull; {2} &bull; " + (
                     ((r'{3} District, ') if self.house == "HS" and self.district else "") +
                     r"{4} &bull; Since {5} &bull; {6}% " + specialInformation))
        return format_html(qinfo_raw, self.leadershipTitle, self.party_verbose(), self.house_verbose(),
                           self.friendly_district(),
                           self.districtState, self.firstElected.strftime(r"%m/%d/%Y"),
                           int(self.baseScore) if self.baseScore != None else "?")

    def getQuickInfo(self):
        specialIcons = r""
        for specialInfo in self.officialSpecialInfo():
            specialIcons += specialInfo.getSpecialIcon()
        # if (self.scienceExperience):
        #    specialIcons += ('<img class="microportrait specialicon" src="https://media.spacescore.com/icon/2014/11/10/'+
        #        'Faculty_of_science_in_thai-icon.png" data-toggle="tooltip" title="Legislator has Science Experience"/>')
        qinfo_raw = mark_safe(r"<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}%</td><td>{6}</td>")
        return format_html(qinfo_raw, self.fullName(), self.party_verbose(), self.title_verbose(),
                           self.constituency_verbose(),
                           (self.firstElected.strftime(r"%m/%d/%Y")),
                           int(self.baseScore) if self.baseScore != None else "?", mark_safe(specialIcons))

    getQuickInfo.allow_tags = True

    def getQuickHeaderInfo(self):
        specialIcons = r""
        for specialInfo in self.officialSpecialInfo():
            specialIcons += specialInfo.getSpecialIcon()
        qinfo_raw = mark_safe(r"<p>{0} &bull; {1} &bull; {2} &bull; Since {3} &bull; {4}%</p><p>{5}</p>")

        return format_html(qinfo_raw, self.party_verbose(), self.title_verbose(), self.constituency_verbose(),
                           (self.firstElected.strftime(r"%m/%d/%Y")),
                           int(self.baseScore) if self.baseScore != None else "?", mark_safe(specialIcons))

    getQuickHeaderInfo.allow_tags = True

    def getLatestAction(self):
        supportingLawsNewest = True
        if (self.supportingLaws() and self.opposingLaws()):
            latestSupportingLaw = self.supportingLaws().order_by('-dateIntroduced')[0]
            global latestSupportingLaw
            latestOpposingLaw = self.opposingLaws().order_by('-dateIntroduced')[0]
            global latestOpposingLaw
            if (latestSupportingLaw.dateIntroduced < latestOpposingLaw.dateIntroduced):
                supportingLawsNewest = False
        elif (self.supportingLaws()):
            latestSupportingLaw = self.supportingLaws().order_by('-dateIntroduced')[0]
            global latestSupportingLaw
        elif (self.opposingLaws()):
            latestOpposingLaw = self.opposingLaws().order_by('-dateIntroduced')[0]
            global latestOpposingLaw
            supportingLawsNewest = False
        else:
            return "No activity recorded"
        if (supportingLawsNewest):
            qinfo_raw = 'Supporting <a href="{0}">{1}</a>\n({2})'
            return format_html(qinfo_raw, latestSupportingLaw.url(),
                               latestSupportingLaw, latestSupportingLaw.getQuickInfoText())
        else:
            qinfo_raw = 'Opposing <a href="{0}">{1}</a>\n({2})'
            return format_html(qinfo_raw, latestOpposingLaw.url(),
                               latestOpposingLaw, latestOpposingLaw.getQuickInfoText())

    def __unicode__(self):
        return unicode(self.fullName())

    class Meta:
        ordering = ['firstElected']


class Law(models.Model):
    officialsSupporting = models.ManyToManyField(Official, verbose_name=u'Officials Supporting',
                                                 related_name=u"officials_supporting", blank=True, )
    officialsOpposing = models.ManyToManyField(Official, verbose_name=u'Officials Opposing',
                                               related_name=u"officials_opposing", blank=True, )
    name = models.CharField(max_length=200, )
    dateIntroduced = models.DateTimeField("Date Introduced", blank=True, default=datetime.now, )
    datePassed = models.DateTimeField("Date Passed Congress", blank=True, null=True, )
    dateEnacted = models.DateTimeField("Date Enacted", blank=True, null=True, )
    passedHouse = models.DateTimeField("Date Passed House", blank=True, null=True, )
    passedSenate = models.DateTimeField("Date Passed Senate", blank=True, null=True, )
    passedCommittee = models.DateTimeField("Date Passed Committee", blank=True, null=True, )
    description = models.TextField(blank=True, )
    editorialComment = models.TextField("Editorial Comment", blank=True, )
    hsfComment = models.TextField("Human Spaceflight Comment", blank=True, )
    unmannedsfComment = models.TextField("Unmanned Spaceflight Comment", blank=True, )
    privatizationComment = models.TextField("Commercial Comment", blank=True, )
    publicComment = models.TextField("Public Comment", blank=True, null=True, )
    house = models.CharField(max_length=2, choices=LAW_HOUSES, )
    picture = models.ImageField(upload_to="%Y/%m/%d", blank=True, null=True, )
    baseWeight = models.FloatField("Basescore Weight", )
    hsfWeight = models.FloatField("Human Spaceflight Weight", )
    unmannedsfWeight = models.FloatField("Unmanned Spaceflight Weight", )
    privatizationWeight = models.FloatField("Commercial Weight", )
    publicWeight = models.FloatField("Public Weight", )
    noBasePenalty = models.BooleanField("No Penalty for BaseScore", default=False, )
    govtrackLink = models.URLField("GovTrack.us Link", blank=True, )
    govtrackID = models.CharField("GovTrack ID", max_length=10, )

    peoplesQuantity = models.IntegerField("Quantity of People Voting", default=0, )
    peoplesScore = models.FloatField("People's Score", default=0.0, )

    def addVote(self, score):
        myScore = float(score)  # score will be passed as a string by javascript from data-send
        self.peoplesScore *= (float(self.peoplesQuantity) / (self.peoplesQuantity + 1))
        self.peoplesQuantity += 1
        self.peoplesScore += (myScore / self.peoplesQuantity)

    def renderType(self):
        return "Law"

    def house_verbose(self):
        return get_display(self.house, LAW_HOUSES)

    def get_absolute_url(self):
        return self.url()

    def url(self):
        # Returns relative url of this bill
        return ("/CongressScore/Bill/%s/" % self.id)

    def getMicroPortraitCode(self):
        """Method to return stored image for admin panel"""
        if (not self.picture):
            return ""
        else:
            return format_html('<img id="context" src="{0}" alt="{1}"/>', self.picture.url, self)

    getMicroPortraitCode.allow_tags = True

    def lawCommittees(self):
        return Committee.objects.filter(committee_laws__id=self.id)

    def supportingAmendments(self):
        return Amendment.objects.filter(parentLaw__id=self.id)

    def getQuickInfo(self):
        qinfo_raw = r"<td>{0}</td><td>"
        # str relevantDate = ""
        if (self.dateEnacted):
            qinfo_raw += "{1}</td><td>Enacted</td>"
            relevantDate = self.dateEnacted.strftime(r"%m/%d/%Y")
        elif (self.datePassed):
            qinfo_raw += "{1}</td><td>Passed Congress</td>"
            relevantDate = self.datePassed.strftime(r"%m/%d/%Y")
        elif (self.passedHouse):
            qinfo_raw += "{1}</td><td>Passed House</td>"
            relevantDate = self.passedHouse.strftime(r"%m/%d/%Y")
        elif (self.passedSenate):
            qinfo_raw += "{1}</td><td>Passed Senate</td>"
            relevantDate = self.passedSenate.strftime(r"%m/%d/%Y")
        elif (self.passedCommittee):
            qinfo_raw += "{1}</td><td>Passed Committee</td>"
            relevantDate = self.passedCommittee.strftime(r"%m/%d/%Y")
        else:
            qinfo_raw += "{1}</td><td>Pending</td>"
            relevantDate = self.dateIntroduced.strftime(r"%m/%d/%Y")
        qinfo_raw += "<td>{2}</td><td></td>"
        return format_html(qinfo_raw, self.house_verbose(), relevantDate, '{:.0%}'.format(self.baseWeight))

    getQuickInfo.allow_tags = True

    def getQuickInfoText(self):
        qinfo_raw = r"{0} &bull; Weight {1} &bull; "
        # str relevantDate = ""
        if (self.dateEnacted):
            qinfo_raw += "Enacted {2}"
            relevantDate = self.dateEnacted.strftime(r"%m/%d/%Y")
        elif (self.datePassed):
            qinfo_raw += "Passed Congress {2}"
            relevantDate = self.datePassed.strftime(r"%m/%d/%Y")
        elif (self.passedHouse):
            qinfo_raw += "Passed House {2}"
            relevantDate = self.passedHouse.strftime(r"%m/%d/%Y")
        elif (self.passedSenate):
            qinfo_raw += "Passed Senate {2}"
            relevantDate = self.passedSenate.strftime(r"%m/%d/%Y")
        else:
            qinfo_raw += "Pending {2}"
            relevantDate = self.dateIntroduced.strftime(r"%m/%d/%Y")
        return format_html(qinfo_raw, self.house_verbose(), '{:.0%}'.format(self.baseWeight),
                           relevantDate)

    def __unicode__(self):
        return unicode(self.name)


class Amendment(models.Model):
    name = models.CharField(max_length=200, )
    description = models.TextField(blank=True, )
    officials_supporting = models.ManyToManyField(Official,
                                                  verbose_name=u'Officials Supporting Amendment',
                                                  related_name=u"amendment_officials_supporting", blank=True, )
    parentLaw = models.ForeignKey(Law, related_name=u"parentLaw", )
    isPartOfLaw = models.NullBooleanField("Is Part of Law", blank=True, null=True, )
    editorialComment = models.TextField("Editorial Comment", blank=True, )
    hsfComment = models.TextField("Human Spaceflight Comment", blank=True, )
    unmannedsfComment = models.TextField("Unmanned Spaceflight Comment", blank=True, )
    privatizationComment = models.TextField("Commercial Comment", blank=True, )
    publicComment = models.TextField("Public Comment", blank=True, null=True, )
    baseWeight = models.FloatField("Basescore Weight", )
    hsfWeight = models.FloatField("Human Spaceflight Weight", )
    unmannedsfWeight = models.FloatField("Unmanned Spaceflight Weight", )
    privatizationWeight = models.FloatField("Commercial Weight", )
    publicWeight = models.FloatField("Public Weight", )
    noBasePenalty = models.BooleanField("No Penalty for BaseScore", default=False, )

    def getQuickInfo(self):
        qinfo_raw = r"Amending {0} &bull; Weight {1} &bull; "
        if (self.isPartOfLaw):
            qinfo_raw += "Reconciled"
        if (self.isPartOfLaw == None):
            qinfo_raw += "Pending"
        else:
            qinfo_raw += "Rejected"
        return format_html(qinfo_raw, self.parentLaw.name, '{:.0%}'.format(self.baseWeight))

    def url(self):
        # Returns relative url of this bill
        return ("/CongressScore/Amendment/%s/" % self.id)

    def renderType(self):
        return "Amendment"

    def get_absolute_url(self):
        return self.url()

    def __unicode__(self):
        return unicode(self.name)


class SpecialInfo(models.Model):
    name = models.CharField(max_length=200, )
    picture = models.ImageField(upload_to="icon/%Y/%m/%d", max_length=500, )
    state = USStateField(blank=True, null=True, max_length=2, )
    description = models.TextField(blank=True, )
    specialinfo_officials = models.ManyToManyField(Official, verbose_name=
    u'Officials with Special Info', related_name=u"specialinfo_officials",
                                                   blank=True, )

    def getSpecialIcon(self):
        return format_html('<img class="microportrait specialicon"' +
                           ' src="{0}" data-toggle="tooltip" title="{1} - {2}"/>', self.picture.url,
                           self.name, self.description)

    getSpecialIcon.allow_tags = True

    def renderType(self):
        return u"SpecialInfo"

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = u"Special Info"
        verbose_name_plural = u"Special Information"


class Committee(models.Model):
    name = models.CharField(max_length=200, )
    description = models.TextField(blank=True, )
    committee_officials = models.ManyToManyField(Official, verbose_name=u'Officials in Committee',
                                                 related_name=u"committee_officials", blank=True, )
    committee_laws = models.ManyToManyField(Law, related_name=u"committee_laws", verbose_name=u'Laws in Committee',
                                            blank=True, )
    powerModifier = models.FloatField("Power Modifier", blank=True, null=True, )
    spaceRelatedness = models.FloatField("Space Relatedness", blank=True, null=True, )
    house = models.CharField("House", max_length=2, choices=OFFICIAL_HOUSES, )
    parentCommittee = models.ForeignKey("self", verbose_name=u'Parent Committee', blank=True, null=True, )
    chairperson = models.ForeignKey(Official, related_name=u"chairperson",
                                    blank=True, null=True, )
    rankingMember = models.ForeignKey(Official, related_name=u"rankingMember",
                                      blank=True, null=True, )

    def renderType(self):
        return u"Committee"

    def url(self):
        # Returns relative url of this bill
        return ("/CongressScore/Committee/%s/" % self.id)

    def subcommittees(self):
        return Committee.objects.filter(parentCommittee__id=self.id)

    def getQuickInfo(self):
        quickInfo = r"{0}"
        return format_html(quickInfo, self.house_verbose())

    getQuickInfo.allow_tags = True

    def getQuickInfoText(self):
        quickInfo = r"{0}"
        return format_html(quickInfo, self.house_verbose())

    getQuickInfoText.allow_tags = True

    def getQuickInfoHeader(self):
        if (self.parentCommittee):
            quickInfo = r'{0} (Subcommittee of <a href="{1}" alt="{2}">{2}</a>)'
            return format_html(quickInfo, self.house_verbose(), self.parentCommittee.url(), self.parentCommittee)
        else:
            quickInfo = r"{0}"
            return format_html(quickInfo, self.house_verbose())

    getQuickInfoHeader.allow_tags = True

    def house_verbose(self):
        return get_display(self.house, LAW_HOUSES)

    def get_absolute_url(self):
        return self.url()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = u"Committee"


class NewsInfo(models.Model):
    name = models.CharField(max_length=200, blank=True, )
    description = models.TextField(blank=True, )
    dateReleased = models.DateTimeField("Date Released", blank=True, null=True, )
    visible = models.BooleanField(default=False, )
    link = models.URLField("Read More", blank=True, null=True, max_length=400, )
    picture = SorlImageField(
        upload_to="%Y/%m/%d", )  # default="2014/09/09/Curt_Clawson_2014_Congressional_Photo-cropped.jpg",

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = u"News Item"
        verbose_name_plural = u"News Items"


@receiver(m2m_changed, sender=Amendment.officials_supporting.through)
def verify_uniqueness3(sender, **kwargs):
    action = kwargs.get('action', None)
    officials_supporting = kwargs.get('pk_set', None)
    if (action == 'post_add'):
        for official_supporting in officials_supporting:
            thisOfficial = Official.objects.get(pk=official_supporting)
            # thisOfficial.updateScores()
            thisOfficial.save()


@receiver(m2m_changed, sender=Law.officialsOpposing.through)
def verify_uniqueness(sender, **kwargs):
    action = kwargs.get('action', None)
    officials_opposing = kwargs.get('pk_set', None)
    if (action == 'post_add'):
        for official_opposing in officials_opposing:
            thisOfficial = Official.objects.get(pk=official_opposing)
            # thisOfficial.updateScores()
            thisOfficial.save()


@receiver(m2m_changed, sender=Law.officialsSupporting.through)
def verify_uniqueness2(sender, **kwargs):
    action = kwargs.get('action', None)
    officials_supporting = kwargs.get('pk_set', None)
    if (action == 'post_add'):
        for official_supporting in officials_supporting:
            thisOfficial = Official.objects.get(pk=official_supporting)
            # thisOfficial.updateScores()
            thisOfficial.save()
