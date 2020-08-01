from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.URLField()


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.URLField()
    description = models.CharField(max_length=256)
    employee_count = models.IntegerField(default=1)


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, related_name='vacancies', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='vacancies', on_delete=models.CASCADE)
    skills = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
