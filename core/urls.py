from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('gallery/', views.gallery, name='gallery'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('chatbot/reply/', views.chatbot_reply, name='chatbot_reply'),
    path('whatsapp/webhook/', views.whatsapp_webhook_verify, name='whatsapp_webhook_verify'),
    path('whatsapp/webhook/post/', views.whatsapp_webhook, name='whatsapp_webhook'),
]