# Loan Disc Cloan System

celery -A loan_management_system worker --loglevel=info

celery -A loan_management_system beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info