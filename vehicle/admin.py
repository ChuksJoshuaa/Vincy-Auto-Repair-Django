from django.contrib import admin
from .models import Customer, Admin, Mechanic, Attendance, Request, Feedback, Contact, News, About


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'phone', 'email']
    ordering = ['username']
    list_editable = ['email', 'phone']
    list_per_page = 10
    list_filter = ['username', 'location']
    search_fields = ['username']


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'phone', 'email']
    ordering = ['username', 'email']
    list_per_page = 10
    list_filter = ['username']
    search_fields = ['username']


@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'skill', 'phone', 'hired']
    ordering = ['username', 'email', 'skill']
    list_editable = ['skill']
    list_per_page = 10
    list_filter = ['username', 'skill']
    search_fields = ['username', 'skill']


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer', 'mechanic']
    date_hierarchy = 'date'
    list_display = ['vehicle_no', 'vehicle_name', 'customer', 'mechanic', 'status', 'cost']
    list_editable = ['cost']
    radio_fields = {
        "category": admin.VERTICAL,
        "status": admin.HORIZONTAL
    }
    list_per_page = 10
    exclude = ['problem_description']
    list_filter = ['status', 'category', 'mechanic', 'vehicle_no', 'vehicle_name']
    search_fields = ['status', 'category', 'mechanic', 'vehicle_no', 'vehicle_name']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['mechanic']
    list_display = ['mechanic', 'present_status', 'date']
    ordering = ['mechanic', 'present_status']
    list_editable = ['present_status']
    radio_fields = {
        "present_status": admin.VERTICAL,
    }
    list_per_page = 10
    list_filter = ['mechanic']
    search_fields = ['mechanic', 'present_status']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['username', 'date']
    list_per_page = 10
    list_filter = ['username']
    search_fields = ['username']
    ordering = ['-date']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    list_per_page = 10
    list_filter = ['name']
    search_fields = ['name']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_per_page = 10
    list_filter = ['email']
    search_fields = ['email']


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 10
    list_filter = ['title']
    search_fields = ['title']



