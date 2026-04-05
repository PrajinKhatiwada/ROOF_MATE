from django.contrib import admin
from .models import Enquiry, Project, GalleryItem, Blog, TeamMember


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'service', 'suburb', 'phone', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'suburb', 'message')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'suburb', 'created_at', 'is_featured')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'suburb', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'read_time', 'is_featured')
    list_filter = ('is_featured', 'published_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'display_order')
    search_fields = ('name', 'role', 'bio')