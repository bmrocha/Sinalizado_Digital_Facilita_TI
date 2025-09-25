import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sinalizacao_digital.settings')

# Setup Django
django.setup()

from apps.users.models import User

# List all users
users = User.objects.all()
print("Users in database:")
for user in users:
    print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Active: {user.is_active}, Role: {user.role}")
