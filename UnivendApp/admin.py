# UnivendApp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Campus, Department, CustomUser, Category, Listing, ListingImage,
    Message, Review, Transaction, KYC
)
from django.utils.safestring import mark_safe

# Inline for ListingImage
class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ('image', 'image_preview', 'is_cover')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover;" />')
            except:
                return "Image not available"
        return "No image"
    image_preview.short_description = "Preview"

# CustomUser Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'campus', 'is_staff', 'date_joined')
    list_filter = ('campus', 'department', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'campus', 'department', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number', 'campus', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

# Campus Admin
@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')
    list_filter = ('location',)

# Department Admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus')
    search_fields = ('name',)
    list_filter = ('campus',)

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_product', 'icon')
    search_fields = ('name',)
    list_filter = ('is_product',)

# Listing Admin
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'price_type', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'tags', 'seller__username')
    list_filter = ('category', 'price_type', 'condition', 'is_active', 'created_at')
    raw_id_fields = ('seller', 'category')
    filter_horizontal = ('saves',)
    inlines = [ListingImageInline]  # Add inline

# ListingImage Admin
@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'is_cover', 'image')
    search_fields = ('listing__title',)
    list_filter = ('is_cover',)

# Message Admin
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'listing', 'sent_at', 'is_read')
    search_fields = ('content', 'sender__username', 'receiver__username')
    list_filter = ('sent_at', 'is_read')
    raw_id_fields = ('sender', 'receiver', 'listing')

# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewed', 'listing', 'rating', 'created_at')
    search_fields = ('comment', 'reviewer__username', 'reviewed__username')
    list_filter = ('rating', 'created_at')
    raw_id_fields = ('reviewer', 'reviewed', 'listing')

# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'seller', 'listing', 'amount', 'status', 'created_at')
    search_fields = ('buyer__username', 'seller__username', 'listing__title')
    list_filter = ('status', 'created_at')
    raw_id_fields = ('buyer', 'seller', 'listing')

# KYC Admin
@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_status', 'submitted_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('verification_status', 'submitted_at')
    raw_id_fields = ('user',)
    filter_horizontal = ('interests',)
    actions = ['approve_kyc', 'reject_kyc']

    def approve_kyc(self, request, queryset):
        queryset.update(verification_status='approved')
        self.message_user(request, "Selected KYC records have been approved.")
    approve_kyc.short_description = "Approve selected KYC records"

    def reject_kyc(self, request, queryset):
        queryset.update(verification_status='rejected')
        self.message_user(request, "Selected KYC records have been rejected.")
    reject_kyc.short_description = "Reject selected KYC records"

# Register CustomUser with custom admin
admin.site.register(CustomUser, CustomUserAdmin)