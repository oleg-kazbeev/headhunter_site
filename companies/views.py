from django.shortcuts import render, redirect
from django.views.generic import View

from companies.forms import CompanyForm
from companies.models import Company


class UserCompanyView(View):
    def get(self, request):
        user = request.user
        company = Company.objects.filter(owner=user).first()
        if company:
            template = 'companies/company-edit.html'
        else:
            template = 'companies/company-create.html'
        return render(request, template, {'company': company})

    def post(self, request):
        company = Company.objects.get_or_create(owner=request.user)[0]
        company_form = CompanyForm(data=request.POST, instance=company)
        if company_form.is_valid():
            company_form.save()
        else:
            print(company_form.errors)
        return redirect('/mycompany')


class UserCompanyVacanciesView(View):
    def get(self, request):
        return render(request, 'mycompany/vacancy-list.html', {})


class CompanyCertainVacancyView(View):
    def get(self, request):
        return render(request, 'mycompany/vacancy-edit.html', {})
