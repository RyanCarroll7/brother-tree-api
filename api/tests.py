from django.test import TestCase
from django.core.exceptions import ValidationError

from api.models import Brother


# Create your tests here.

class BrotherModelTests(TestCase):
    def test_cannot_set_self_as_big_brother(self):
        bro = Brother.objects.create(
            first_name="Test",
            last_name="User",
            grad_year=2020,
        )
        # assign self and attempt to save
        bro.big_brother = bro
        with self.assertRaises(ValidationError) as cm:
            bro.full_clean()
        self.assertIn("big_brother", cm.exception.message_dict)

    def test_can_set_different_big_brother(self):
        older = Brother.objects.create(
            first_name="Older",
            last_name="Bro",
            grad_year=2018,
        )
        younger = Brother.objects.create(
            first_name="Younger",
            last_name="Bro",
            grad_year=2020,
            big_brother=older,
        )
        # should not raise
        younger.full_clean()

    def test_cycle_detection_in_big_brother(self):
        bro1 = Brother.objects.create(
            first_name="Bro1",
            last_name="User",
            grad_year=2018,
        )
        bro2 = Brother.objects.create(
            first_name="Bro2",
            last_name="User",
            grad_year=2019,
            big_brother=bro1,
        )
        bro3 = Brother.objects.create(
            first_name="Bro3",
            last_name="User",
            grad_year=2020,
            big_brother=bro2,
        )
        # create a cycle: bro1 -> bro2 -> bro3 -> bro1
        bro1.big_brother = bro3
        with self.assertRaises(ValidationError) as cm:
            bro1.full_clean()
        self.assertIn("big_brother", cm.exception.message_dict)
