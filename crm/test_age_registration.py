"""Лабораторная №8, вариант 1: чёрный ящик и границы 18–65."""
from datetime import date
from unittest.mock import patch
from django.test import SimpleTestCase
from .forms import ClientRegistrationForm


class AgeBoundaryTests(SimpleTestCase):
    def test_age_equivalence_and_boundaries(self):
        today = date(2026, 11, 2)
        with patch('crm.forms.registration_today', return_value=today):
            for age in (17, 18, 19, 64, 65, 66):
                with self.subTest(age=age):
                    birthday = date(today.year - age, today.month, today.day)
                    form = ClientRegistrationForm(data={'birth_date': birthday.isoformat()})
                    form.is_valid()
                    self.assertEqual('birth_date' not in form.errors, 18 <= age <= 65)

    def test_invalid_input_classes(self):
        for value in ('', 'abc', '2099-01-01'):
            with self.subTest(value=value):
                form = ClientRegistrationForm(data={'birth_date': value})
                form.is_valid()
                self.assertIn('birth_date', form.errors)

    def test_birthday_not_yet_reached(self):
        with patch('crm.forms.registration_today', return_value=date(2026, 11, 2)):
            form = ClientRegistrationForm(data={'birth_date': '2008-11-03'})
            form.is_valid()
            self.assertIn('birth_date', form.errors)
