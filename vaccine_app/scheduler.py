from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Appointment
from twilio.rest import Client
import pytz
import logging

# Set up logging
logger = logging.getLogger(__name__)

def send_reminder_sms():
    now = timezone.localtime()  # Current time with time zone awareness

    # Loop through all appointments
    appointments = Appointment.objects.filter(reminder_sent=False)  # Only fetch appointments that have not had a reminder sent

    client = Client(
        "ACecacfbe10f23537acd4001281aa39fd7",
        "ba92c43fc51f5cd5a336352dfcda1d9a"
    )

    for appointment in appointments:
        scheduled_time = appointment.scheduled_time  # datetime.time object
        scheduled_date = appointment.scheduled_date  # Assuming this field exists

        # Combine date and time into a datetime object
        scheduled_datetime = datetime.combine(scheduled_date, scheduled_time)

        # Make the datetime aware if it is naive
        if timezone.is_naive(scheduled_datetime):
            scheduled_datetime = timezone.make_aware(scheduled_datetime)

        # time to send SMS: 5 minutes before the scheduled time
        reminder_time = scheduled_datetime - timedelta(minutes=5)  # 5 minutes before

        # Only send reminder if the current time is within the range of 5 minutes before the scheduled time
        if now >= reminder_time and now < scheduled_datetime:
            message = f"Reminder: Your child's vaccination is scheduled at {appointment.scheduled_time.strftime('%I:%M %p')} on {appointment.scheduled_date.strftime('%A, %B %d, %Y')}."
            phone = appointment.child.contact_number

            # Ensure the phone number is in international format (e.g., +977 for Nepal)
            if not phone.startswith('+'):
                phone = '+977' + phone  # Adding Nepal country code if it's missing

            try:
                client.messages.create(
                    body=message,
                    from_='+14054495877',
                    to=phone
                )
                logger.info(f"✅ Sent SMS to {phone}")

                # Flag this appointment as having received a reminder to prevent sending it again
                appointment.reminder_sent = True
                appointment.save()

            except Exception as e:
                # Log the exception without stopping the server
                logger.error(f"❌ Failed to send SMS to {phone}: {e}")
                continue  # Continue with the next appointment

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminder_sms, 'interval', minutes=1)  # Run every minute to check if reminder time has come
    scheduler.start()
