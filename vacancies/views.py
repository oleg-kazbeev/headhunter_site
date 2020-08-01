from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import View

from .models import Specialty, Company, Vacancy


class MainPageView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        return render(request, 'index.html', {'specialties': specialties,
                                              'companies': companies})


class AllVacanciesPageView(View):
    def get(self, request):
        jobs = Vacancy.objects.all()
        return render(request, 'all-vacancies.html', {'jobs': jobs})


class VacanciesBySpecializationView(View):
    def get(self, request, specialty):
        jobs_sorted_by_specialty = Vacancy.objects.filter(specialty__code=specialty)
        return render(request, 'vacancies.html', {'jobs': jobs_sorted_by_specialty,
                                                  'specialty': specialty})


class CompanyView(View):
    def get(self, request, id):
        company_vacancies = Vacancy.objects.filter(company__id=id)
        company_name = Company.objects.filter(id=id).first()
        return render(request, 'company.html', {'vacancies': company_vacancies,
                                                'company_name': company_name})


class VacancyView(View):
    def get(self, request, id):
        vacancy = Vacancy.objects.filter(id=id).first()
        return render(request, 'vacancy.html', {'vacancy': vacancy})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Что-то пошло не так...')


def custom_handler500(request, exception):
    return HttpResponseNotFound('К сожалению, данный ресурс временно не доступен :(')