from django.shortcuts import render
from .models import BroadcastMessage, ConsumerEventLog
from .producer import publish_broadcast_event


def broadcast_view(request):
    context = {
        "messages": BroadcastMessage.objects.all(),
    }

    if request.method == "POST":
        action = request.POST.get("action", "create").strip()
        message_id = request.POST.get("message_id", "").strip()
        message = request.POST.get("broadcast_message", "").strip()

        if action == "create" and message:
            event = publish_broadcast_event(action="create", message=message)
            context["success"] = f"Create event sent for ID {event['message_id']}."
        elif action == "update" and message_id and message:
            event = publish_broadcast_event(
                action="update",
                message=message,
                message_id=message_id,
            )
            context["success"] = f"Update event sent for ID {event['message_id']}."
        elif action == "delete" and message_id:
            event = publish_broadcast_event(
                action="delete",
                message_id=message_id,
            )
            context["success"] = f"Delete event sent for ID {event['message_id']}."
        else:
            context["error"] = "Please fill the required fields for the selected action."

        context["messages"] = BroadcastMessage.objects.all()

    return render(request, "broadcast/index.html", context)


def consumer_dashboard_view(request):
    context = {
        "messages": BroadcastMessage.objects.all(),
        "event_logs": ConsumerEventLog.objects.all()[:20],
    }
    return render(request, "broadcast/consumer.html", context)
