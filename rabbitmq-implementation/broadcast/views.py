from django.shortcuts import render
from .producer import publish_broadcast_event


def broadcast_view(request):
    context = {}

    if request.method == "POST":
        message = request.POST.get("broadcast_message", "").strip()

        if message:
            event = publish_broadcast_event(message)
            context["success"] = f"Broadcast sent: {event['message']}"
        else:
            context["error"] = "Broadcast message cannot be empty."

    return render(request, "broadcast/index.html", context)
