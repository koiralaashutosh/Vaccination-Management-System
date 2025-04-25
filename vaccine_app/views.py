from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from vaccine_app.models import Vaccination, Child, Appointment
from django.shortcuts import render, redirect
from django.contrib import messages
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def index(request):
    # If the user is not logged in, redirect to login
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    # Ensure the user is an admin (staff member)
    if not request.user.is_staff:
        return redirect('login')  # Redirect to login if the user is not an admin

    return render(request, 'index.html')


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST.get('uname')
        p = request.POST.get('pwd')
        user = authenticate(username=u, password=p)
        if user is not None:
            try:
                if user.is_staff:
                    auth_login(request, user)
                    request.session['login_success'] = True  # ✅ set session flag
                    return redirect('home')
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    # Ensure the user is an admin before allowing logout
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    auth_logout(request)  # Use Django's logout method
    return redirect('login')

def vaccination(request):
    # Ensure the user is an admin before allowing logout
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    vac = Vaccination.objects.all()
    v = {'vac': vac}
    return render(request, 'view_vaccination.html', v)


def add_vaccination(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    error = ""

    if request.method == 'POST':
        name = request.POST.get('vaccination_name')
        time = request.POST.get('recommended_time')
        dose = request.POST.get('dose_number')
        notes = request.POST.get('vaccination_notes')

        try:
            Vaccination.objects.create(
                vaccination_name=name,
                recommended_time=time,
                dose_number=dose,
                vaccination_notes=notes
            )
            error = "no"
        except:
            error = "yes"

    return render(request, 'add_vaccination.html', {'error': error})


def delete_vaccination(request, pid):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    vaccination_to_delete = Vaccination.objects.get(id=pid)
    vaccination_to_delete.delete()

    return redirect('view_vaccination')

def add_child(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    error = ""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        parent_name = request.POST.get('parent_name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        medical_notes = request.POST.get('medical_notes')

        try:
            Child.objects.create(
                full_name=full_name,
                date_of_birth=date_of_birth,
                gender=gender,
                parent_name=parent_name,
                contact_number=contact_number,
                email=email,
                address=address,
                medical_notes=medical_notes
            )
            error = "no"
        except:
            error = "yes"

    return render(request, 'add_child.html', {'error': error})

def view_child(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    children = Child.objects.all()
    return render(request, 'view_child.html', {'children': children})

def add_appointment(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    error = ""
    children = Child.objects.all()
    vaccinations = Vaccination.objects.all()

    if request.method == 'POST':
        child_id = request.POST.get('child')
        vaccination_id = request.POST.get('vaccination')
        scheduled_date = request.POST.get('scheduled_date')
        scheduled_time = request.POST.get('scheduled_time')
        appointment_notes = request.POST.get('appointment_notes')

        try:
            child = Child.objects.get(id=child_id)
            vaccination = Vaccination.objects.get(id=vaccination_id)
            Appointment.objects.create(
                child=child,
                vaccination=vaccination,
                scheduled_date=scheduled_date,
                scheduled_time=scheduled_time,
                appointment_notes=appointment_notes
            )
            error = "no"
        except:
            error = "yes"

    return render(request, 'add_appointment.html', {'error': error, 'children': children, 'vaccinations': vaccinations})

def view_appointment(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    appointments = Appointment.objects.all()
    return render(request, 'view_appointment.html', {'appointments': appointments})


def delete_child(request, pid):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    try:
        child = Child.objects.get(id=pid)
        child.delete()
    except Child.DoesNotExist:
        pass

    return redirect('view_child')

# Your Twilio credentials
TWILIO_ACCOUNT_SID = 'ACecacfbe10f23537acd4001281aa39fd7'
TWILIO_AUTH_TOKEN = 'ba92c43fc51f5cd5a336352dfcda1d9a'
TWILIO_PHONE_NUMBER = '+14054495877'

@csrf_exempt
def send_sms_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('PhoneNumber')
        message_text = request.POST.get('Messages')

        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=message_text,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            messages.success(request, 'Message sent successfully!')
            return redirect('send_sms')
        except Exception as e:
            messages.error(request, f'Error sending message: {e}')
            return redirect('send_sms')

    return render(request, 'send_sms.html')

def delete_appointment(request, pid):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')

    try:
        appointment = Appointment.objects.get(id=pid)
        appointment.delete()
    except Appointment.DoesNotExist:
        pass

    return redirect('view_appointment')


