from django.contrib import admin

from api.models import Brother


class BrotherInline(admin.TabularInline):
    model = Brother
    extra = 0
    verbose_name = "Little Brother"
    fields = ("id",)
    can_delete = False
    show_change_link = True
    max_num = 0


# Register your models here.
@admin.register(Brother)
class BrotherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "big_brother", "initiation_term", "major", "grad_year")
    list_filter = ("grad_year", "major", "big_brother", "initiation_date")
    list_editable = ("big_brother",)
    search_fields = ("first_name", "middle_name", "last_name", "suffix")
    autocomplete_fields = ("big_brother",)
    inlines = (BrotherInline,)
