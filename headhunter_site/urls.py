from django.contrib import admin
from django.urls import path
from vacancies.views import *

handler_404 = custom_handler404
handler_500 = custom_handler500

urlpatterns = [
    path('', MainPageView.as_view()),
    path('vacancies/', AllVacanciesPageView.as_view()),
    path('vacancies/cat/<str:specialty>', VacanciesBySpecializationView.as_view()),
    path('companies/<int:id>', CompanyView.as_view()),
    path('vacancies/<int:id>', VacancyView.as_view()),
    path('admin/', admin.site.urls),
]
