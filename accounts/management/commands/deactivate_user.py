from django.core.management.base import BaseCommand
from accounts.kick_ban_user import deactivate_user, delete_user
class Command(BaseCommand):

    
    help = 'Ban user by username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']
        deactivate_user(username)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deactivated user {username}'))