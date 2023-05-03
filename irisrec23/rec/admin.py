from django.contrib import admin
from .models import profile, branch, company,posts, cgpa, application_details

# Register your models here.
@admin.register(branch)
class BranchModel(admin.ModelAdmin):
    productlist_display = ('name', 'students', 'company')

@admin.register(company)
class CompanyModel(admin.ModelAdmin):
    productlist_display = ('name', 'decription', 'poc', 'branches_open', 'isactive')

admin.site.register(profile)
admin.site.register(posts)
admin.site.register(cgpa)
admin.site.register(application_details)