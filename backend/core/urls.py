from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, DoctorViewSet, MediaCoverageViewSet, SuccessStoryViewSet, BlogPostViewSet, ContactInquiryCreateView, HomepageSlideViewSet, SocialMediaLinkViewSet, ContactInfoViewSet, TeamMemberViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'team-members', TeamMemberViewSet)
router.register(r'media-coverage', MediaCoverageViewSet)
router.register(r'success-stories', SuccessStoryViewSet)
router.register(r'blog-posts', BlogPostViewSet)
router.register(r'homepage-slides', HomepageSlideViewSet)
router.register(r'social-media-links', SocialMediaLinkViewSet)
router.register(r'contact-info', ContactInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', ContactInquiryCreateView.as_view(), name='contact-inquiry'),
]