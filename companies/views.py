from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from companies.forms import CompanyForm
from companies.models import Company
from vacancies.forms import VacancyForm
from vacancies.models import Vacancy, Specialty


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
        else:
            print(company_form.errors)
        return redirect('/mycompany')


class UserCompanyVacanciesView(View):
    def get(self, request):
        user_company = Company.objects.get(owner=request.user)
        user_vacancies = Vacancy.objects.filter(company=user_company)
        return render(request,  'companies/vacancy-list.html',
                      {'vacancies': user_vacancies})

    def post(self, request):
        user_company = get_object_or_404(Company, owner=request.user)
        user_vacancy = Vacancy.objects.create(company=user_company,
                                              specialty=Specialty.objects.get(id=1))
        return render(request, 'companies/vacancy-edit.html',
                      {'vacancy': user_vacancy})


class UserCompanyVacancyView(View):
    def get(self, request, vacancy_id):
        user_vacancy = Vacancy.objects.get(id=vacancy_id)
        return render(request, 'companies/vacancy-edit.html',
                      {"vacancy": user_vacancy})

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        vacancy_form = VacancyForm(data=request.POST, instance=vacancy)
        if vacancy_form.is_valid():
            vacancy_form.save()
        else:
            print(vacancy_form.errors)
        return redirect(f'/mycompany/vacancies/{vacancy_id}')
