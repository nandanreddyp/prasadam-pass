import qrcode
import io
import base64

from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Registration, Event


# home page to list events
def home(request):
    events = [event.to_dict() for event in Event.objects.all()]

    return render(request, 'index.html', {
        'events': events
    })

# user registration page for an event
def event_registration(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'GET':
        return render(request, 'register.html', {'event': event})

    elif request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        pincode = request.POST.get('pincode')

        if not all([full_name, phone_number, pincode]):
            return render(request, 'register.html', {
                'event': event,
                'error': 'All fields are required!'
            })

        registration = Registration.objects.create(
            event=event,
            full_name=full_name,
            phone_number=phone_number,
            pincode=pincode
        )

        # send QR code to whatsapp of number given

        # Redirect to QR or success page
        return redirect('show_qr', token=registration.token)

# showing qr of a registration
def show_qr(request, token):
    registration = get_object_or_404(Registration, token=token)

    qr_data = request.build_absolute_uri(f'/checkin/{token}')
    qr = qrcode.make(qr_data)

    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'qr.html', {
        'registration': registration.to_dict(),
        'qr_code': img_base64,
        'checkin_url': qr_data,
    })

### volunteer routes ###
########################

@login_required
def scan_qr(request):
    return render(request, 'volunteer/scan_qr.html')

@login_required
def process_qr_checkin(request, token):
    registration = get_object_or_404(Registration, token=token)

    if request.method == 'POST':
        registration.is_checked_in = True
        registration.save()

    return render(request, 'volunteer/status.html', {
        'registration': registration
    })
