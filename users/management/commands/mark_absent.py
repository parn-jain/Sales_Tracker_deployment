# myapp/management/commands/mark_absent.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import AttendanceRecord, RegisterUser

class Command(BaseCommand):
    help = 'Mark all users as absent for the new day'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        users = RegisterUser.objects.all()

        for user in users:
            AttendanceRecord.objects.get_or_create(
                user=user,
                date=today,
                defaults={'status': 'Absent'}
            )

        self.stdout.write(self.style.SUCCESS('All users marked as absent for today'))
