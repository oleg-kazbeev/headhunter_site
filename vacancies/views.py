from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from .models import Specialty, Vacancy
from companies.models import Company
from .forms import FeedbackForm


class MainView(View):
    def get(self, request):
        specialties_and_amount_of_vacancies = []
        specialties = Specialty.objects.all()

        for specialty in specialties:
            amount_of_vacancies_by_specialty = Vacancy.objects.filter(specialty__code=specialty.code).count
            specialties_and_amount_of_vacancies.append([specialty, amount_of_vacancies_by_specialty])

        companies = Company.objects.all()
        companies_and_amount_of_vacancies = []

        for company in companies:
            amount_of_company_vacancies = Vacancy.objects.filter(company=company).count
            companies_and_amount_of_vacancies.append([company, amount_of_company_vacancies])

        return render(request, 'vacancies/index.html', {'specialties': specialties_and_amount_of_vacancies,
                                                        'companies': companies_and_amount_of_vacancies})


class VacanciesView(View):
    def get(self, request):
        jobs = Vacancy.objects.all()
        return render(request, 'vacancies/all-vacancies.html', {'jobs': jobs})


class VacanciesBySpecialtyView(View):
    def get(self, request, specialty):
        vacancies = Vacancy.objects.filter(specialty__code=specialty)
        return render(request, 'vacancies/vacancies.html', {'vacancies': vacancies,
                                                            'specialty': specialty})


class VacanciesInCompanyView(View):
    def get(self, request, company_id):
        company = get_object_or_404(Company, id=company_id)
        company_vacancies = Vacancy.objects.filter(company=company)
        return render(request, 'vacancies/company.html', {'vacancies': company_vacancies,
                                                          'company': company})


class VacancyView(View):
    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        return render(request, 'vacancies/vacancy.html', {'vacancy': vacancy})

    def post(self, request, vacancy_id):
        feedback_form = FeedbackForm(data=request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            vacancy = Vacancy.objects.filter(id=vacancy_id).first()
            user = request.user
            feedback.user = user
            feedback.vacancy = vacancy
            feedback.save()
            return redirect(f'{vacancy_id}/send')
        else:
            print(feedback_form.errors)
            redirect(f'{vacancy_id}')


class VacancyResponseSendView(View):
    def get(self, request, vacancy_id):
        return render(request, 'vacancies/sent.html', {'vacancy_id': vacancy_id})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Что-то пошло не так...')


def custom_handler500(request, exception):
    return HttpResponseNotFound('К сожалению, данный ресурс временно не доступен :(')
