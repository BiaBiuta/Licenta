from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
import json, requests, os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8001/predict")

# core/views_chat.py  (la fel în views_scheduler.py)

class ChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        u = self.request.user
        if u.is_authenticated:
            name  = (u.username  or "User").strip()
            email = u.email or ""
            uid   = u.id or 0
        else:
            name  = "Guest"
            email = ""          # ← placeholder sigur
            uid   = 0

        ctx["USER"] = {"name": name, "email": email, "id": uid}
        return ctx


# ───────── HTMX partial pentru fiecare bulă ─────────
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
import json

@csrf_protect
def chat_bubble(request):
    print("sunt intr-un chat bubble ")
    # values vin ca x-www-form-urlencoded
    msg   = request.POST.get("message","").strip()
    who   = request.POST.get("who","ai")
    quick = request.POST.get("quick","[]")
    try:
        quick = json.loads(quick)
    except json.JSONDecodeError:
        quick = []
    return render(request, "chat/partials/bubble.html",
                  {"message":msg,"who":who,"quick":quick})

# core/views_chat.py  (exemplu minimal)
def shift_table_fragment(request):
    items = json.loads(request.body)   # primeşte listă de dict-uri
    return render(request, "chat/partials/shift_table.html", {"items": items})


def handle_chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        response = {}

        # Logic to handle various intents (similar to original code)
        if user_message:
            iso_date = parse_abs_date(user_message) or resolve_relative_weekday(user_message)
            if iso_date:
                # Example: Returning a mock schedule
                response['message'] = f"Schedule set for {iso_date}."
                response['quick_replies'] = [
                    {"title": "Morning", "payload": "morning"},
                    {"title": "Afternoon", "payload": "afternoon"},
                    {"title": "Night", "payload": "night"},
                ]
            else:
                response['message'] = "Could not understand the date. Try again."

        return JsonResponse(response)

    return render(request, 'chat.html')