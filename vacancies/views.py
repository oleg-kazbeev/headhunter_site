from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Specialty, Vacancy
from companies.models import Company
from .forms import FeedbackForm


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        number_of_vacancies_by_specialty = {}

        for specialty in specialties:
            number_of_vacancies_by_specialty[specialty.code] = \
                Vacancy.objects.filter(specialty__code=specialty.code).count()

        companies = Company.objects.all()
        return render(request, 'vacancies/index.html', {'specialties': specialties,
                                                        'companies': companies,
                                                        'number_of_vacancies_by_specialty':
                                                            number_of_vacancies_by_specialty})


class AllVacanciesView(View):
    def get(self, request):
        jobs = Vacancy.objects.all()
        return render(request, 'vacancies/all-vacancies.html', {'jobs': jobs})


class VacanciesBySpecializationView(View):
    def get(self, request, specialty):
        jobs_sorted_by_specialty = Vacancy.objects.filter(specialty__code=specialty)
        return render(request, 'vacancies/vacancies.html', {'jobs': jobs_sorted_by_specialty,
                                                            'specialty': specialty})


class CompanyVacanciesView(View):
    def get(self, request, company_id):
        company_vacancies = Vacancy.objects.filter(company__id=company_id)
        company_name = Company.objects.filter(id=company_id).first()
        return render(request, 'vacancies/company.html', {'vacancies': company_vacancies,
                                                          'company_name': company_name})


class VacancyView(View):
    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        return render(request, 'vacancies/vacancy.html', {'vacancy': vacancy})

    def post(self, request, vacancy_id):
        application_form = FeedbackForm(data=request.POST)
        if application_form.is_valid():
            application = application_form.save(commit=False)
            vacancy = Vacancy.objects.filter(id=vacancy_id).first()
            user = request.user
            application.user = user
            application.vacancy = vacancy
            application.save()
            return redirect(f'{vacancy_id}/send')
        else:
            print(application_form.errors)
            redirect(f'{vacancy_id}')


class ResponseSendView(View):
    def get(self, request, vacancy_id):
        return render(request, 'vacancies/sent.html', {'vacancy_id': vacancy_id})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Что-то пошло не так...')


def custom_handler500(request, exception):
    return HttpResponseNotFound('К сожалению, данный ресурс временно не доступен :(')
