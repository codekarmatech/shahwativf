from django.contrib import admin
from .models import Service, Doctor, MediaCoverage, SuccessStory, BlogPost, ContactInquiry, HomepageSlide, SocialMediaLink, ContactInfo, TeamMember

@admin.register(HomepageSlide)
class HomepageSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'button_link', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'button_link']
    search_fields = ['title', 'subtitle']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'created_at']
    fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'order', 'is_active']

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active', 'order']
    list_filter = ['platform', 'is_active']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'platform']
    fields = ['platform', 'url', 'is_active', 'order']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'email', 'updated_at']
    fields = ['address', 'phone', 'email']
    
    def has_add_permission(self, request):
        # Only allow one ContactInfo instance
        return not ContactInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of ContactInfo
        return False

@admin.register(MediaCoverage)
class MediaCoverageAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'source', 'display_size', 'display_priority', 'is_featured', 'date']
    list_filter = ['media_type', 'display_size', 'is_featured', 'date', 'source']
    search_fields = ['title', 'description', 'source']
    list_editable = ['display_priority', 'is_featured', 'display_size']
    ordering = ['-display_priority', '-date']
    fields = [
        'title', 'description', 'media_type', 'source', 
        'image', 'video', 'external_url',
        'display_size', 'display_priority', 'is_featured', 'date'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if obj:  # editing existing object
            fields.extend(['created_at', 'updated_at'])
        return fields

admin.site.register(Service)
admin.site.register(Doctor)
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'category', 'is_active', 'display_order']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'designation', 'qualifications']
    list_editable = ['is_active', 'display_order']
    ordering = ['display_order', 'name']

admin.site.register(SuccessStory)
admin.site.register(BlogPost)
admin.site.register(ContactInquiry)