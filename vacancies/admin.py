from django.contrib import admin

from .models import Vacancy, Feedback, Specialty


class CompanyAdmin(admin.ModelAdmin):
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    pass


class SpecialtyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Feedback, ApplicationAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
