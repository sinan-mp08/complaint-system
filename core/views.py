from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint, Category
from .forms import ComplaintForm


from .models import AdminRole

def is_admin(user):
    return AdminRole.objects.filter(user=user).exists()


@login_required
def student_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/student_dashboard.html', {'complaints': complaints})


@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Complaint submitted successfully!")
            return redirect('student_dashboard')
    else:
        form = ComplaintForm()
    
    return render(request, 'core/submit_complaint.html', {'form': form})


@login_required
def complaint_detail(request, id):
    complaint = get_object_or_404(Complaint, id=id, user=request.user)
    return render(request, 'core/complaint_detail.html', {'complaint': complaint})

@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'core/admin_dashboard.html', {'complaints': complaints})




@login_required
def update_status(request, id):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    complaint = get_object_or_404(Complaint, id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        complaint.status = new_status
        complaint.save()
        messages.success(request, "Status updated!")
        return redirect('admin_dashboard')

    return render(request, 'core/update_status.html', {'complaint': complaint})





from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now login.")
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()

    return render(request, 'core/signup.html', {'form': form})



from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    else:
        return redirect('/accounts/login/')



@login_required
def after_login(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    return redirect('student_dashboard')





from .models import UserProfile
from django.contrib.auth.models import User


@login_required
def profile(request):
    # Create profile if missing
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        if request.FILES.get("photo"):
            profile.photo = request.FILES["photo"]

        profile.phone = request.POST.get("phone")
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "core/profile.html", {"profile": profile})
