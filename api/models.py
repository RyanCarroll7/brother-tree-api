from datetime import date

from django.db import models
from django.core.exceptions import ValidationError
import django.core.validators as validators


# Create your models here.
class Brother(models.Model):
    class Meta:
        ordering = ["-grad_year", "first_name", "last_name"]

    id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=100, null=True, blank=True)

    initiation_date = models.DateField(validators=[validators.MinValueValidator(date(1938, 4, 23))], null=True, blank=True)
    grad_year = models.IntegerField(validators=[validators.MinValueValidator(1938)])
    major = models.CharField(max_length=100, null=True, blank=True)

    big_brother: models.ForeignKey["Brother"] = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="little_brothers",
    )

    @property
    def full_name(self):
        return f'{self.first_name}{f" {self.middle_name[0]}." if self.middle_name else ""} {self.last_name}{f", {self.suffix}" if self.suffix else ""} \'{self.grad_year % 100}'

    @property
    def initiation_term(self):
        if self.initiation_date:
            # TODO: Spring 1938 or Charter Member
            # TODO: Not fully true prior to 2000
            result = f"{'Fall' if self.initiation_date.month >= 7 else 'Spring'} {self.initiation_date.year}"
            if result == "Spring 1938":
                return "Charter Member"
            return result
        return None

    def clean(self):
        if self.big_brother is not None and self.big_brother.id == self.id:
            raise ValidationError(
                {"big_brother": "Brother cannot be their own big brother."}
            )
        else:
            ancestor = self.big_brother
            while ancestor:
                if ancestor.id == self.id:
                    raise ValidationError(
                        {"big_brother": "Cycle detected in brother hierarchy."}
                    )
                ancestor = ancestor.big_brother

    def __str__(self):
        return self.full_name
