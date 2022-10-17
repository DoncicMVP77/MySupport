import logging

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from support_api.models import Message, Ticket
from support_api.permissions import IsOwnerOrReadOnly
from support_api.serializer import MessageSerializer, TicketSerializer
from support_api.tasks import (send_email_about_new_message_func,
                               send_email_about_ticket_create_func)

logger = logging.getLogger(__name__)


class TicketList(generics.ListAPIView):
    """
    get:
        Returns the list of tickets.
    """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="user"):
            return Ticket.objects.filter(user=user)

        return Ticket.objects.all()


class TicketMessageList(generics.ListAPIView):
    """
    get:
        Returns the list of messages on a particular ticket.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ticket = Ticket.objects.get(id=self.kwargs.get("slug"))
        return Message.objects.filter(ticket=ticket)


class TicketCreateView(generics.CreateAPIView):
    """
    post:
        Create a new message instance. Returns created post data.
        Send email to user about the created ticket.
        parameters: [slug, category, title, description]
    """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        send_email_about_ticket_create_func.delay(
            user_email=str(request.user.email),
            ticket_subject=request.data['title'],
            description=request.data['description'],
        )

        return self.create(request, *args, **kwargs)


class TicketDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a ticket instance. Searches ticket using
        slug in the url.

    put:
        Update an existing ticket. Returns updated ticket data.

        parameters: [slug, category, title, description, status]

    delete:
        Delete an existing ticket.
    """
    queryset = Ticket.objects.all()
    lookup_field = "slug"
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]


class MessageCreateAPIVIew(generics.CreateAPIView):
    """
    post:
        Create a new message instance. Returns created post data.
        Send email to user about create admin a message.
        parameters = [slug, text]
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def perform_create(self, serializer, *args, **kwargs):
        ticket = Ticket.objects.get(slug=self.kwargs.get('slug'))
        if serializer.is_valid():
            serializer.save(user=self.request.user, ticket=ticket)

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            ticket = Ticket.objects.get(slug=self.kwargs.get('slug'))
            user_email = ticket.user.email
            ticket_subject = ticket.title
            send_email_about_new_message_func(
                user_email=user_email,
                ticket_subject=ticket_subject,
                message_text=request.data["text"],
                )

        return self.create(request, *args, **kwargs)


class ListMessagesAPIView(generics.ListAPIView):
    """
    get:
        Returns the list of messages on a particular ticket
    """
    serializer_class = MessageSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        ticket = Ticket.objects.get(slug=slug)
        messages = ticket.message_set.all()
        return messages


class DetailMessageAPIVIew(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a message instance. Searches message using
        message id and ticket slug in the url.

    put:
        Update an existing message. Returns updated message data.

        parameters: [user, ticket, text]

    delete:
        Delete an existing message.
    """
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = ["slug", "pk"]
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug")
        ticket = Ticket.objects.get(slug=slug)
        message = ticket.message_set.all().get(pk=pk)
        return message
