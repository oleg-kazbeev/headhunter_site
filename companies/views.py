from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages

from companies.forms import CompanyForm
from companies.models import Company
from vacancies.forms import VacancyForm
from vacancies.models import Vacancy, Specialty, Feedback


class UserCompanyView(View):
    def get(self, request):
        user = request.user
        user_company = Company.objects.filter(owner=user).first()
        if user_company:
            template = 'companies/company-edit.html'
        else:
            template = 'companies/company-create.html'
        return render(request, template, {'company': user_company})

    def post(self, request):
        user_company = Company.objects.get_or_create(owner=request.user)[0]
        company_form = CompanyForm(data=request.POST, instance=user_company)
        if company_form.is_valid():
            company_form.save()
            messages.success(request, 'Компания обновлена', extra_tags='alert alert-info')
        else:
            print(company_form.errors)
        return redirect('/mycompany')


class UserCompanyVacanciesView(View):
    def get(self, request):
        user_company = Company.objects.get(owner=request.user)
        user_vacancies = Vacancy.objects.filter(company=user_company)
        vacancies_and_amount_of_feedbacks = []

        for vacancy in user_vacancies:
            feedbacks_amount = Feedback.objects.filter(vacancy=vacancy).count
            vacancies_and_amount_of_feedbacks.append([vacancy, feedbacks_amount])

        return render(request,  'companies/vacancy-list.html',
                      {'vacancies': vacancies_and_amount_of_feedbacks})

    def post(self, request):
        user_company = get_object_or_404(Company, owner=request.user)
        user_vacancy = Vacancy.objects.create(company=user_company,
                                              specialty=Specialty.objects.get(id=1))
        return render(request, 'companies/vacancy-edit.html',
                      {'vacancy': user_vacancy})


class UserCompanyVacancyView(View):
    def get(self, request, vacancy_id):
        user_vacancy = Vacancy.objects.get(id=vacancy_id)
        feedbacks = Feedback.objects.filter(vacancy=user_vacancy)
        specialties = Specialty.objects.all()
        amount_of_feedback = feedbacks.count
        return render(request, 'companies/vacancy-edit.html',
                      {"vacancy": user_vacancy,
                       "feedbacks": [feedbacks, amount_of_feedback],
                       'specialties': specialties})

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        vacancy_form = VacancyForm(data=request.POST, instance=vacancy)
        if vacancy_form.is_valid():
            vacancy_form.save()
            messages.success(request, "Вакансия обновлена", extra_tags='alert alert-info')
        else:
            print(vacancy_form.errors)
        return redirect(f'/mycompany/vacancies/{vacancy_id}')
