from django.urls import path

from support_api.views import (DetailMessageAPIVIew, ListMessagesAPIView,
                               MessageCreateAPIVIew, TicketCreateView,
                               TicketDetailAPIView, TicketList,
                               TicketMessageList)

urlpatterns = [
    path('tickets', TicketList.as_view(), name='tickets'),
    path('messages', TicketMessageList.as_view(), name='messages'),

    path('ticket/create', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/<slug:slug>', TicketDetailAPIView.as_view(), name='message_create'),
    path('ticket/<slug:slug>/messages', ListMessagesAPIView.as_view(), name='message_create'),
    path('ticket/<slug:slug>/message/create', MessageCreateAPIVIew.as_view(),
         name='message_create'),
    path('ticket/<slug:slug>/message/<int:pk>', DetailMessageAPIVIew.as_view(),
         name='message_detail'),
]
