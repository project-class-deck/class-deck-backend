from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, School


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'nickname', 'school', 'grade', 'classroom')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'nickname', 'school', 'grade',
                'classroom', 'is_active', 'is_staff'),
        }),
    )
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'nickname', 'school', 'grade', 'classroom')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'nickname')
    ordering = ('username',)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')  # Columns to display in the admin list view
    search_fields = ['name']  # Fields to be searchable in the admin
    list_filter = ('name',)  # Fields to filter in the admin sidebar

# Register the School model with the customized options
