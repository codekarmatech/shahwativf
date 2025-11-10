from rest_framework import viewsets, generics
from .models import Service, Doctor, MediaCoverage, SuccessStory, BlogPost, ContactInquiry, HomepageSlide, SocialMediaLink, ContactInfo, TeamMember
from .serializers import ServiceSerializer, DoctorSerializer, MediaCoverageSerializer, SuccessStorySerializer, BlogPostSerializer, ContactInquirySerializer, HomepageSlideSerializer, SocialMediaLinkSerializer, ContactInfoSerializer, TeamMemberSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'slug'

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer

class MediaCoverageViewSet(viewsets.ModelViewSet):
    queryset = MediaCoverage.objects.all()
    serializer_class = MediaCoverageSerializer

class SuccessStoryViewSet(viewsets.ModelViewSet):
    queryset = SuccessStory.objects.all()
    serializer_class = SuccessStorySerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'

class ContactInquiryCreateView(generics.CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer

class HomepageSlideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomepageSlide.objects.filter(is_active=True)
    serializer_class = HomepageSlideSerializer

class SocialMediaLinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SocialMediaLink.objects.filter(is_active=True)
    serializer_class = SocialMediaLinkSerializer

class ContactInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer