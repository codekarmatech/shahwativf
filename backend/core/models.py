from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.TextField(blank=True, help_text='Concise point-wise description for homepage')
    content = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    related_services = models.ManyToManyField('self', blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)
    bio = models.TextField()
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    # Extended fields from recent migration for robust doctor profiling
    degrees = models.CharField(max_length=300, blank=True, help_text='Medical degrees and certifications')
    qualifications = models.CharField(max_length=300, blank=True)
    achievements = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_consultant = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['display_order', 'name']

class TeamMember(models.Model):
    CATEGORY_CHOICES = [
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('admin', 'Administrative Staff'),
        ('technician', 'Technician'),
        ('support', 'Support Staff'),
        ('management', 'Management'),
    ]

    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    qualifications = models.CharField(max_length=300, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='support')
    image = models.ImageField(upload_to='team_members/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    social_media = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

class MediaCoverage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('news', 'News Article'),
        ('interview', 'Interview'),
        ('award', 'Award/Recognition'),
        ('research', 'Research Publication'),
        ('conference', 'Conference/Speaking'),
        ('testimonial', 'Patient Testimonial'),
        ('achievement', 'Achievement'),
        ('social_impact', 'Social Impact'),
        ('technology', 'Technology Innovation'),
        ('statistics', 'Success Statistics'),
    ]
    
    DISPLAY_SIZE_CHOICES = [
        ('small', 'Small (1x1)'),
        ('medium', 'Medium (2x1)'),
        ('large', 'Large (2x2)'),
        ('wide', 'Wide (2x1)'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(help_text='Brief description with character limit for display')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='news')
    source = models.CharField(max_length=100, blank=True, help_text='Media source (e.g., Times of India, NDTV)')
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    external_url = models.URLField(blank=True, help_text='Link to external article/video')
    display_size = models.CharField(max_length=10, choices=DISPLAY_SIZE_CHOICES, default='small')
    display_priority = models.PositiveIntegerField(default=0, help_text='Higher numbers appear first')
    is_featured = models.BooleanField(default=False, help_text='Show in featured section')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-display_priority', '-date']
        verbose_name = 'Media Coverage'
        verbose_name_plural = 'Media Coverage'

    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"

class SuccessStory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    publish_date = models.DateField()

    def __str__(self):
        return self.title

class ContactInquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name}"

class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField(help_text='Full URL to your social media profile')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text='Display order')
    
    class Meta:
        ordering = ['order', 'platform']
        verbose_name = 'Social Media Link'
        verbose_name_plural = 'Social Media Links'
    
    def __str__(self):
        return f"{self.get_platform_display()}"

class ContactInfo(models.Model):
    address = models.TextField(help_text='Hospital address')
    phone = models.CharField(max_length=20, help_text='Contact phone number')
    email = models.EmailField(help_text='Contact email address')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'
    
    def __str__(self):
        return "Contact Information"

class HomepageSlide(models.Model):
    URL_CHOICES = [
        ('/', 'Home'),
        ('/about', 'About Us'),
        ('/services', 'Our Services'),
        ('/team', 'Our Team'),
        ('/media-coverage', 'Media Coverage'),
        ('/success-stories', 'Success Stories'),
        ('/blog', 'Blog'),
        ('/contact', 'Contact Us'),
        ('/book-consultation', 'Book Consultation'),
        ('', 'No Link (Display Only)'),
    ]
    
    title = models.CharField(max_length=200, help_text='Slide title/heading')
    subtitle = models.TextField(blank=True, help_text='Slide subtitle/description')
    image = models.ImageField(upload_to='homepage_slides/', help_text='Background image for the slide')
    button_text = models.CharField(max_length=100, blank=True, help_text='Call-to-action button text')
    button_link = models.CharField(
        max_length=100, 
        choices=URL_CHOICES, 
        blank=True,
        help_text="Select a page to link to, or leave empty for display-only slides"
    )
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower numbers appear first)')
    is_active = models.BooleanField(default=True, help_text='Whether this slide is currently active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Homepage Slide'
        verbose_name_plural = 'Homepage Slides'

    def __str__(self):
        return self.title