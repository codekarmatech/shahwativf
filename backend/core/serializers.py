from rest_framework import serializers
from .models import Service, Doctor, MediaCoverage, SuccessStory, BlogPost, ContactInquiry, HomepageSlide, SocialMediaLink, ContactInfo, TeamMember

class ServiceSerializer(serializers.ModelSerializer):
    related_services = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ['id', 'title', 'slug', 'description', 'short_description', 'content', 'image', 'related_services', 'is_featured']
    
    def get_related_services(self, obj):
        related = obj.related_services.all()
        return [{
            'id': service.id,
            'title': service.title,
            'slug': service.slug,
            'description': service.description,
            'image': service.image.url if service.image else None
        } for service in related]

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'url', 'is_active', 'order']

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['address', 'phone', 'email']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class MediaCoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCoverage
        fields = '__all__'

class SuccessStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessStory
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = '__all__'

class HomepageSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepageSlide
        fields = '__all__'