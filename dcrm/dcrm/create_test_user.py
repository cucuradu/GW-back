import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

def create_test_user():
    User = get_user_model()

    # Check if the test user already exists
    if not User.objects.filter(username='test').exists():
        test_user = User.objects.create_user(username='test', password='testpass')
        print("Test user created successfully.")
    else:
        print("Test user already exists.")

if __name__ == "__main__":
    create_test_user()