from django.contrib import admin
from scenarios.models import Scenarios


class ScnariosAdmin(admin.ModelAdmin):
    list_display = ["name", "types", "lines", "permeability","file"]

admin.site.register(Scenarios, ScnariosAdmin)