from celery import shared_task
from django.core.mail import send_mail

@shared_task
def notify_admin(form_id, submission_id):
    send_mail(
        subject=f"New submission for Form {form_id}",
        message=f"A new submission {submission_id} has been received.",
        from_email="noreply@onboarding.com",
        recipient_list=["admin@company.com"],
    )

