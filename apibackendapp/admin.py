from django.contrib import admin

from .models import department, employee, projects, UserDetails
# from rest_framework.authtoken.models import Token

# Register your models here.

admin.site.register(department)
# admin.site.register(employee)
admin.site.register(projects)


#Inline class to display Many-to-Many relationship inside Employee admin
class ProjectInline(admin.TabularInline):
    #TabularInline displays the related data in a table-like format
    #This tells Django to use the intermediate(junction) table
    #.through property gives us access to the junction table
    model=projects.employees.through
    #Number of empty rows shown in admin for adding new relationships.
    extra=1

#customizing Employee admin panel
class EmployeeAdmin(admin.ModelAdmin):
    #This attached the inline to Employee admin page
    inlines=[ProjectInline]

#Register Employee model with the customized admin class
admin.site.register(employee,EmployeeAdmin)
#Register token model for authentication
# admin.site.register(Token)
admin.site.register(UserDetails)