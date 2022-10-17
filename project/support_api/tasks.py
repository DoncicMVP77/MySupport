import datetime

from celery import shared_task
from django.core.mail import send_mail
from project import settings
from pytz import utc

from .models import Message, Ticket


@shared_task(bind=True)
def send_email_about_ticket_create_func(
        self, user_email, ticket_subject,
        description, *args, **kwargs):

    title = f"Ticket {ticket_subject}"

    message = f"Thank you for submitting your ticket. \n" \
              f"Here’s what we received: \n" \
              f"{description}\n" \
              f"Thanks so much,\n" \
              f"My Support"

    send_mail(
        subject=title,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=True,
    )

    return True


@shared_task(bind=True)
def send_email_about_new_message_func(
        self, user_email, ticket_subject,
        message_text, *args, **kwargs):

    title = f"Ticket {ticket_subject}"
    message = f"{message_text} \n" \
              f"Thanks so much,\n" \
              f"My Support"

    send_mail(
        subject=title,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=True,
    )

    return True


@shared_task(bind=True)
def check_last_message_in_ticket_and_send_email_about_change_status():

    tickets = Ticket.objects.all()
    for ticket in tickets:
        last_message = _get_last_message_from_ticket(ticket=ticket)
        time_dif = _check_count_days_after_last_message_ticket(last_message)
        _change_ticket_status(ticket, time_dif)
        _send_email_about_change_ticket_status(ticket)


def _send_email_about_change_ticket_status(ticket: Ticket) -> None:

    if ticket.status == "Froze":
        _send_email_about_froze_ticket_task(ticket=ticket)
    elif ticket.status == "Close":
        _send_email_about_close_ticket_task(ticket=ticket)


def _send_email_about_froze_ticket_task(ticket: Ticket) -> None:

    title = f"A follow up from MySupport regarding your ticket {ticket.title}"
    user_email = ticket.user.email
    message = "Thank you for working with us on this Service Request." \
              "We wanted to take a moment to follow up to confirm if you still needed our " \
              "assistance?" \
              "Kindly do respond back so we can continue to assist you or confirm that you do " \
              "not need additional assistance." \
              " Since it has been some time since your last update," \
              " we will move forward with closing the SR in 24 hours if we don't hear back." \
              "We look forward to hearing from you."

    send_mail(
        subject=title,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=True,
    )


def _send_email_about_close_ticket_task(ticket: Ticket) -> None:
    title = f"Close your ticket {ticket.title}"
    user = ticket.objects.select_related("user")
    user_email = user.email
    message = "This is an automated message." \
              "As noted in our earlier message, we have closed this ticket on your behalf." \
              " If you need further assistance please feel free to open a new ticket" \
              " and we’d be happy to continue working with you."
    send_mail(
        subject=title,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=True,
    )


def _change_ticket_status(ticket: Ticket, time_dif: int) -> None:
    if time_dif == 1:
        ticket.status = "Froze"
        ticket.save()
    elif time_dif > 1:
        ticket.status = "Close"
        ticket.save()


def _check_count_days_after_last_message_ticket(last_message: Message) -> int:
    try:
        if last_message is not None and last_message.user.groups.filter(name="user").exists():
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            time_dif = now - last_message.timestamp
            return time_dif.days
        return 0
    except Exception as ex:
        print(ex)


def _get_last_message_from_ticket(ticket: Ticket) -> Message or None:
    try:
        if Message.objects.filter(ticket=ticket):
            last_message = Message.objects.filter(ticket=ticket).order_by('-timestamp')[:1][0]
            return last_message
        return None
    except Exception as ex:
        print(ex)
