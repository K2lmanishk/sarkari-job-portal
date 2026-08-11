from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
import random
from apps.jobs.models import Job, Category, State


class Command(BaseCommand):
    help = 'Create sample job listings (Police, SSC, UPSC, etc.)'

    def handle(self, *args, **options):
        # ---------- Categories ----------
        categories_data = [
            ('Police', 'police'),
            ('SSC', 'ssc'),
            ('UPSC', 'upsc'),
            ('Banking', 'banking'),
            ('Railway', 'railway'),
            ('Teaching', 'teaching'),
        ]
        categories = {}
        for name, slug in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'is_active': True}
            )
            categories[name] = cat
            self.stdout.write(f"Category ready: {name}")

        # ---------- States ----------
        states_data = [
            ('All India', 'all-india'),
            ('Uttar Pradesh', 'uttar-pradesh'),
            ('Delhi', 'delhi'),
            ('Rajasthan', 'rajasthan'),
            ('Maharashtra', 'maharashtra'),
        ]
        states = {}
        for name, slug in states_data:
            st, _ = State.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'is_active': True}
            )
            states[name] = st
            self.stdout.write(f"State ready: {name}")

        # ---------- Sample Jobs ----------
        today = timezone.now().date()
        sample_jobs = [
            {
                'title': 'UP Police Constable Recruitment 2026',
                'organization': 'Uttar Pradesh Police Recruitment Board',
                'category': categories['Police'],
                'state': states['Uttar Pradesh'],
                'qualification': '12th Pass',
                'short_description': 'UP Police has announced 4500+ Constable vacancies. Apply online now.',
                'total_vacancies': 4560,
                'application_start_date': today - timedelta(days=5),
                'application_last_date': today + timedelta(days=25),
                'exam_date': today + timedelta(days=80),
                'is_active': True,
            },
            {
                'title': 'SSC GD Constable 2026 Notification',
                'organization': 'Staff Selection Commission',
                'category': categories['SSC'],
                'state': states['All India'],
                'qualification': '10th Pass',
                'short_description': 'SSC GD Constable 2026 – Apply for 26,000+ posts in BSF, CISF, CRPF, etc.',
                'total_vacancies': 26146,
                'application_start_date': today - timedelta(days=2),
                'application_last_date': today + timedelta(days=40),
                'exam_date': today + timedelta(days=100),
                'is_active': True,
            },
            {
                'title': 'UPSC CAPF Assistant Commandant 2026',
                'organization': 'Union Public Service Commission',
                'category': categories['UPSC'],
                'state': states['All India'],
                'qualification': 'Graduation',
                'short_description': 'UPSC CAPF AC 2026 exam for BSF, CRPF, CISF, ITBP and SSB officers.',
                'total_vacancies': 253,
                'application_start_date': today + timedelta(days=3),
                'application_last_date': today + timedelta(days=33),
                'exam_date': today + timedelta(days=120),
                'is_active': True,
            },
            {
                'title': 'Rajasthan Police SI Recruitment 2026',
                'organization': 'Rajasthan Public Service Commission',
                'category': categories['Police'],
                'state': states['Rajasthan'],
                'qualification': 'Graduation',
                'short_description': 'Rajasthan Police Sub Inspector (SI) posts – 1200+ vacancies. Check details.',
                'total_vacancies': 1245,
                'application_start_date': today + timedelta(days=1),
                'application_last_date': today + timedelta(days=31),
                'exam_date': today + timedelta(days=90),
                'is_active': True,
            },
            {
                'title': 'SSC CGL 2026 Tier-1 Exam',
                'organization': 'Staff Selection Commission',
                'category': categories['SSC'],
                'state': states['All India'],
                'qualification': 'Graduation',
                'short_description': 'SSC Combined Graduate Level (CGL) 2026 – Apply for Group B and C posts.',
                'total_vacancies': 7500,
                'application_start_date': today - timedelta(days=10),
                'application_last_date': today + timedelta(days=20),
                'exam_date': today + timedelta(days=65),
                'is_active': True,
            },
            {
                'title': 'Delhi Police Head Constable Recruitment 2026',
                'organization': 'Delhi Police',
                'category': categories['Police'],
                'state': states['Delhi'],
                'qualification': '12th Pass',
                'short_description': 'Delhi Police Head Constable (Ministerial) 800+ vacancies.',
                'total_vacancies': 835,
                'application_start_date': today + timedelta(days=5),
                'application_last_date': today + timedelta(days=35),
                'exam_date': today + timedelta(days=95),
                'is_active': True,
            },
        ]

        created_count = 0
        for job_data in sample_jobs:
            slug = slugify(job_data['title'])
            if Job.objects.filter(slug=slug).exists():
                slug = f"{slug}-{random.randint(1000,9999)}"

            job, created = Job.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': job_data['title'],
                    'organization': job_data['organization'],
                    'category': job_data['category'],
                    'state': job_data['state'],
                    'qualification': job_data['qualification'],
                    'short_description': job_data['short_description'],
                    'total_vacancies': job_data['total_vacancies'],
                    'application_start_date': job_data['application_start_date'],
                    'application_last_date': job_data['application_last_date'],
                    'exam_date': job_data['exam_date'],
                    'is_active': job_data['is_active'],
                    'created_at': timezone.now(),
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {job.title}"))
            else:
                self.stdout.write(f"Already exists: {job.title}")

        self.stdout.write(self.style.SUCCESS(f"\n✅ Total sample jobs created: {created_count}"))