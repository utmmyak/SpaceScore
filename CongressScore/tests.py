from django.test import TestCase

# Create your tests here.
from CongressScore.models import Official, Law

class GenericTestCase(TestCase):
    def setUp(self):
        jSmith = Official.objects.create(firstName="John", lastName="Smith", house="SN", party="DEM", sex='M')
        aSmith = Official.objects.create(firstName="Alexander", lastName="Smith", house="SN", party="DEM", sex='F')
        alaw = Law.objects.create(name="generic_law", baseWeight=1, hsfWeight=(-.5), unmannedsfWeight=(-.3), house="SN",
        	privatizationWeight=1, publicWeight=1)
        alaw.officialsSupporting += jSmith
        alaw.officialsOpposing += aSmith



    def test_scores_are_calculated(self):
        """Test scores are calculated correctly"""
        jSmith = Official.objects.get(firstName="John")
        aSmith = Official.objects.get(firstName="Alexander")
        aSmith.save()
        jSmith.save()
        self.assertEqual((aSmith.baseScore < jSmith.baseScore), True)
        #self.assertEqual(cat.speak(), 'The cat says "meow"')
