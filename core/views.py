from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Blog, Enquiry, GalleryItem, Project, TeamMember

import json
import os
import requests

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import ChatConversation, ChatMessage
from .services.openai_chat import get_ai_reply

def home(request):
    projects = Project.objects.filter(is_featured=True)[:3]
    gallery_items = GalleryItem.objects.all()[:8]
    featured_blogs = Blog.objects.filter(is_featured=True)[:3]

    context = {
        'projects': projects,
        'gallery_items': gallery_items,
        'featured_blogs': featured_blogs,
        'page_title': 'Roofmate | Brisbane Roof Painting, Repairs & Cleaning',
    }
    return render(request, 'core/index.html', context)


def about(request):
    team_members = TeamMember.objects.all()
    context = {
        'team_members': team_members,
        'page_title': 'About Roofmate',
    }
    return render(request, 'core/about.html', context)


def projects(request):
    all_projects = Project.objects.all()
    context = {
        'all_projects': all_projects,
        'page_title': 'Roofmate Projects',
    }
    return render(request, 'core/projects.html', context)


def gallery(request):
    gallery_items = GalleryItem.objects.all()
    context = {
        'gallery_items': gallery_items,
        'page_title': 'Roofmate Gallery',
    }
    return render(request, 'core/gallery.html', context)


def blog(request):
    blogs = Blog.objects.all()
    context = {
        'blogs': blogs,
        'page_title': 'Roofmate Blog',
    }
    return render(request, 'core/blog.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    recent_posts = Blog.objects.exclude(pk=post.pk)[:3]
    context = {
        'post': post,
        'recent_posts': recent_posts,
        'page_title': post.title,
    }
    return render(request, 'core/blog_detail.html', context)


def contact(request):
    context = {
        'page_title': 'Contact Roofmate',
    }
    return render(request, 'core/contact.html', context)


def submit_enquiry(request):
    if request.method == 'POST':
        Enquiry.objects.create(
            full_name=request.POST.get('full_name', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            suburb=request.POST.get('suburb', ''),
            service=request.POST.get('service', ''),
            message=request.POST.get('message', ''),
        )
        messages.success(request, 'Your enquiry has been submitted successfully.')
        return redirect('contact')

    return redirect('contact')

def _extract_lead_fields(conversation: ChatConversation, message: str):
    lower = message.lower()

    services = [
        "metal roof painting",
        "tile roof painting",
        "roof repairs",
        "roof pressure cleaning",
        "driveway painting",
        "driveway cleaning",
    ]

    for service in services:
        if service in lower:
            conversation.lead_service = service.title()
            conversation.is_lead = True

    # lightweight extraction only; keep simple
    if "brisbane" in lower and not conversation.suburb:
        conversation.suburb = "Brisbane"
        conversation.is_lead = True

    conversation.save()


@csrf_exempt
@require_POST
def chatbot_reply(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    message = (payload.get("message") or "").strip()
    session_id = (payload.get("session_id") or "").strip()

    if not message:
        return JsonResponse({"error": "Message is required."}, status=400)

    if not session_id:
        return JsonResponse({"error": "Session ID is required."}, status=400)

    conversation, _ = ChatConversation.objects.get_or_create(
        channel="website",
        session_id=session_id,
    )

    ChatMessage.objects.create(
        conversation=conversation,
        role="user",
        content=message,
    )

    _extract_lead_fields(conversation, message)

    history = [
        {"role": m.role, "content": m.content}
        for m in conversation.messages.all()
    ]

    try:
        ai_reply = get_ai_reply(message, history_messages=history[:-1])
    except Exception as e:
        return JsonResponse({"error": f"AI request failed: {str(e)}"}, status=500)

    ChatMessage.objects.create(
        conversation=conversation,
        role="assistant",
        content=ai_reply,
    )

    return JsonResponse({
        "reply": ai_reply,
        "conversation_id": conversation.id,
    })


def send_whatsapp_text(to_phone: str, body: str) -> dict:
    access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": body},
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


@require_GET
def whatsapp_webhook_verify(request):
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == verify_token:
        return HttpResponse(challenge, content_type="text/plain")

    return HttpResponse("Verification failed", status=403)


@csrf_exempt
@require_POST
def whatsapp_webhook(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"status": "invalid json"}, status=400)

    try:
        entries = payload.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                contacts = value.get("contacts", [])

                if not messages:
                    continue

                contact_name = ""
                if contacts:
                    contact_name = contacts[0].get("profile", {}).get("name", "")

                for incoming in messages:
                    if incoming.get("type") != "text":
                        continue

                    whatsapp_user_id = incoming.get("from")
                    user_text = incoming.get("text", {}).get("body", "").strip()

                    if not whatsapp_user_id or not user_text:
                        continue

                    conversation, _ = ChatConversation.objects.get_or_create(
                        channel="whatsapp",
                        whatsapp_user_id=whatsapp_user_id,
                        defaults={
                            "user_name": contact_name,
                            "user_phone": whatsapp_user_id,
                        }
                    )

                    if contact_name and not conversation.user_name:
                        conversation.user_name = contact_name
                        conversation.save()

                    ChatMessage.objects.create(
                        conversation=conversation,
                        role="user",
                        content=user_text,
                    )

                    _extract_lead_fields(conversation, user_text)

                    history = [
                        {"role": m.role, "content": m.content}
                        for m in conversation.messages.all()
                    ]

                    ai_reply = get_ai_reply(user_text, history_messages=history[:-1])

                    ChatMessage.objects.create(
                        conversation=conversation,
                        role="assistant",
                        content=ai_reply,
                    )

                    send_whatsapp_text(whatsapp_user_id, ai_reply)

    except Exception as e:
        return JsonResponse({"status": "error", "detail": str(e)}, status=500)

    return JsonResponse({"status": "ok"})