from django.core.management.base import BaseCommand
from core.models import Service

class Command(BaseCommand):
    help = 'Update remaining service descriptions with detailed content'

    def handle(self, *args, **options):
        services_data = [
            {
                'title': 'Counselling',
                'slug': 'counselling',
                'description': 'Support for IVF patients including donor programmes and genetic testing.',
                'content': 'Our counselling service includes support for all IVF patients as well as specialist counselling for our donor programmes and genetic testing. All patients of Shashwat IVF are offered private counselling sessions prior to commencing hormone stimulation and just before embryo transfer. We find this places couples in the best possible emotional state for their treatment. Research shows that emotional and mental stability can have a positive impact on the procedure.\n\nWe work closely with individuals and couples to help them cope with:\n- Successfully managing the fertility roller coaster\n- Replacing fears and anxiety with relaxation along their fertility journey\n- Staying mentally and emotionally calm while undergoing fertility treatment\n- Early pregnancy challenges and preparing for birth\n- Coping with grief and loss after miscarriage or stillbirth',
                'is_featured': True
            },
            {
                'title': 'Andrology',
                'slug': 'andrology',
                'description': 'Diagnostic and treatment services for male infertility.',
                'content': 'Andrology Services include:\nA. Diagnostic Semen Analysis: Measures sperm count, motility, and other parameters according to WHO guidelines.\nB. Semen Analysis with Strict Morphology and Vitality Staining: Details morphological abnormalities and vitality.\nC. Retrograde Ejaculate Testing: Evaluates sperm in urine for retrograde ejaculation.\nTesting of Sperm for Anti-sperm Antibodies for Male and Female.\nSperm wash for Intra-Uterine Insemination (IUI).\nCryopreservation of Semen.\nD. Testicular Epididymal Sperm Aspiration (TESA): Retrieves sperm directly from testicles.',
                'is_featured': True
            },
            {
                'title': 'Endoscopy',
                'slug': 'endoscopy',
                'description': 'Hysteroscopy and Laparoscopy to improve IVF success.',
                'content': 'The role of Hysteroscopy in the success of IVF: Conducted under general anaesthesia to diagnose and surgically improve the womb, detecting abnormalities like polyps, fibroids, adhesions.\n\nImproving IVF success rates with Laparoscopy: Visualizes reproductive organs to treat tubal disease, ovarian cysts, fibroids, and adhesions.',
                'is_featured': True
            },
            {
                'title': 'IUI',
                'slug': 'iui',
                'description': 'Intrauterine Insemination for specific infertility cases.',
                'content': 'Intrauterine insemination (IUI) places sperm directly into the uterus. Recommended for patients with cervical mucus issues, decreased sperm production/motility, unexplained infertility, or mild endometriosis. Performed during natural or induced ovulation cycles.',
                'is_featured': True
            },
            {
                'title': 'ICSI',
                'slug': 'icsi',
                'description': 'Intracytoplasmic Sperm Injection for male infertility.',
                'content': 'ICSI involves injecting a single sperm into a mature egg. Recommended for male infertility or previous IVF failure. Embryos are transferred 3-5 days later.',
                'is_featured': True
            },
            {
                'title': 'Embryo/Egg/Sperm Donation',
                'slug': 'embryo-egg-sperm-donation',
                'description': 'Donation options for couples with severe infertility factors.',
                'content': 'Egg donation: Eggs from a healthy donor fertilized with partner\'s sperm.\nEmbryo Adoption: Donor eggs fertilized with donor sperm.\nSperm Donation: For cases with no viable sperm. All involve anonymous donors screened for health.',
                'is_featured': True
            },
            {
                'title': 'Vitrification',
                'slug': 'vitrification',
                'description': 'Rapid freezing of embryos for better survival rates.',
                'content': 'Vitrification converts embryos into a glass-like solid without ice crystals, improving post-thaw survival and pregnancy rates. Often used for blastocyst stage embryos.',
                'is_featured': True
            },
        ]
        for data in services_data:
            Service.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'description': data['description'],
                    'content': data['content'],
                    'is_featured': data.get('is_featured', False),
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully updated remaining services'))