from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from companies.views import CompanyCertainVacancyView, UserCompanyVacanciesView, UserCompanyView
from profile.views import MyLoginView, MySignupView
from vacancies.views import VacancyView, VacanciesBySpecializationView, CompanyVacanciesView, AllVacanciesView, \
    MainView, ResponseSendView, custom_handler500, custom_handler404

handler_404 = custom_handler404
handler_500 = custom_handler500

urlpatterns = [
    # vacancies app
    path('', MainView.as_view()),
    path('vacancies/', AllVacanciesView.as_view()),
    path('vacancies/cat/<str:specialty>', VacanciesBySpecializationView.as_view()),
    path('companies/<int:company_id>', CompanyVacanciesView.as_view()),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view()),
    path('vacancies/<int:vacancy_id>/send', ResponseSendView.as_view()),
    # companies app
    path('mycompany/', UserCompanyView.as_view()),
    path('mycompany/vacancies', UserCompanyVacanciesView.as_view()),
    path('mycompany/vacancies/<vacancy_id>', CompanyCertainVacancyView.as_view()),
    # profile app
    path('login/', MyLoginView.as_view()),
    path('register/', MySignupView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
