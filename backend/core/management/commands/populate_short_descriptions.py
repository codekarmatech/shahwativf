from django.core.management.base import BaseCommand
from core.models import Service

class Command(BaseCommand):
    help = 'Populate short_description for all services'

    def handle(self, *args, **options):
        services_data = [
            {'slug': 'ivf', 'short_description': '''- In Vitro Fertilization for couples struggling with infertility
- Combines eggs and sperm in a lab to create embryos
- High success rates with personalized treatment plans'''},
            {'slug': 'ob-gynecology', 'short_description': '''- Comprehensive care for women's reproductive health
- Prenatal and postnatal services
- Treatment for gynecological disorders'''},
            {'slug': 'fertility', 'short_description': '''- Advanced fertility assessments and treatments
- Hormone therapies and lifestyle guidance
- Support for natural conception methods'''},
            {'slug': 'assisted-hatching', 'short_description': '''- Technique to improve embryo implantation
- Involves thinning the embryo's outer shell
- Recommended for older patients or previous IVF failures'''},
            {'slug': 'blastocyst-culture', 'short_description': '''- Extended embryo culture to day 5
- Improves selection of viable embryos
- Increases IVF success rates'''},
            {'slug': 'embryoscopy', 'short_description': '''- Time-lapse imaging of embryo development
- Non-invasive monitoring
- Enhances embryo selection accuracy'''},
            {'slug': 'counselling', 'short_description': '''- Emotional support for fertility patients
- Guidance on treatment options
- Coping strategies for infertility stress'''},
            {'slug': 'andrology', 'short_description': '''- Male fertility diagnostics and treatments
- Semen analysis and sperm preparation
- Solutions for male factor infertility'''},
            {'slug': 'endoscopy', 'short_description': '''- Minimally invasive procedures like hysteroscopy
- Diagnosis and treatment of uterine issues
- Improves IVF outcomes'''},
            {'slug': 'iui', 'short_description': '''- Intrauterine Insemination for mild infertility
- Places prepared sperm directly in uterus
- Less invasive than IVF'''},
            {'slug': 'icsi', 'short_description': '''- Intracytoplasmic Sperm Injection
- Direct injection of sperm into egg
- Effective for severe male infertility'''},
            {'slug': 'vitrification', 'short_description': '''- Rapid freezing of eggs or embryos
- Preserves fertility for future use
- High survival rates post-thaw'''},
            {'slug': 'embryo-egg-sperm-donation', 'short_description': '''- Donor programs for gametes and embryos
- Anonymous or known donors
- Helps overcome severe infertility issues'''}
        ]
        for data in services_data:
            try:
                service = Service.objects.get(slug=data['slug'])
                service.short_description = data['short_description']
                service.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated {service.title}'))
            except Service.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Service with slug {data["slug"]} not found'))