from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from companies.views import UserCompanyVacancyView,\
    UserCompanyVacanciesView, UserCompanyView
from profile.views import LoginView, SignupView
from vacancies.views import VacancyView, VacanciesBySpecialtyView,\
    VacanciesInCompanyView, VacanciesView, \
    MainView, VacancyResponseSendView, custom_handler500, custom_handler404

handler_404 = custom_handler404
handler_500 = custom_handler500

urlpatterns = [
    # vacancies app
    path('', MainView.as_view()),
    path('vacancies/', VacanciesView.as_view()),
    path('vacancies/cat/<str:specialty>', VacanciesBySpecialtyView.as_view()),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view()),
    path('companies/<int:company_id>', VacanciesInCompanyView.as_view()),
    path('vacancies/<int:vacancy_id>/send', VacancyResponseSendView.as_view()),
    # companies app
    path('mycompany/', UserCompanyView.as_view()),
    path('mycompany/vacancies', UserCompanyVacanciesView.as_view()),
    path('mycompany/vacancies/<int:vacancy_id>', UserCompanyVacancyView.as_view()),
    # profile app
    path('login/', LoginView.as_view()),
    path('register/', SignupView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
