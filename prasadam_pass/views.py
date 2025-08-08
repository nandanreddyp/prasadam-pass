import qrcode
import io
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Registration, Event


# home page to list events
def home(request):
    events = [event.to_dict() for event in Event.objects.all().order_by('-created_at')]

    return render(request, 'index.html', {
        'events': events
    })

# user registration page for an event
def event_registration(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'GET':
        registrations = "None"

        phone_number = request.GET.get('phone_number')
        if phone_number:
            registrations = [reg.to_dict() for reg in Registration.objects.filter(phone_number=phone_number, event_id=event_id)]

        return render(request, 'register.html', {
            'event': event.to_dict(),
            'registrations': registrations
        })
        
    elif request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        pincode = request.POST.get('pincode')
        slot = request.POST.get('slot')

        if not all([full_name, phone_number, pincode, slot]):
            return render(request, 'register.html', {
                'event': event,
                'error': 'All fields are required!'
            })

        registration = Registration.objects.create(
            event=event,
            full_name=full_name,
            phone_number=phone_number,
            pincode=pincode,
            slot=slot
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

def download_qr(request, token):
    registration = get_object_or_404(Registration, token=token)
    
    # Step 1: Generate QR code
    qr_img = qrcode.make(f"{request.build_absolute_uri('/checkin/' + token)}")
    
    # Step 2: Create a new canvas bigger than QR
    canvas_width = 400
    canvas_height = 500
    canvas = Image.new('RGB', (canvas_width, canvas_height), color=(255, 248, 240))  # light background
    
    # Step 3: Paste QR in center
    qr_size = 300
    qr_img = qr_img.resize((qr_size, qr_size))
    canvas.paste(qr_img, ((canvas_width - qr_size) // 2, 100))  # leave top space for text
    
    # Step 4: Draw text
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 24)  # You can replace with a custom font
    except:
        font = ImageFont.load_default()
    
    draw.text((canvas_width // 2, 20), registration.event.name, font=font, fill=(78, 38, 0), anchor="mm")
    draw.text((canvas_width // 2, 60), registration.full_name, font=font, fill=(163, 92, 0), anchor="mm")

    draw.text((canvas_width // 2, 480), "Prasadam Pass - " + registration.slot, font=font, fill=(163, 92, 0), anchor="mm")
    
    # Step 5: Send as downloadable image
    buffer = BytesIO()
    canvas.save(buffer, format="PNG")
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="PrasadamPass - {registration}.png"'
    return response


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
