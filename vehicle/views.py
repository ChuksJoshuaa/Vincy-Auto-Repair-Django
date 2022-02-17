from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import auth
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from .forms import Account, AdminUpdateMechanic, RequestForm, \
    MechanicUpdateStatus, MechanicUpdateForm
from .models import Contact, News
from .models import Customer, Mechanic, Admin, Attendance, Feedback, Request, About


def home(request):
    if request.method == "POST":
        message = "i want to subscribe to your newsletter alerts"
        email = request.POST.get('email')
        news = News(email=email)
        news.save()
        if email:
            send_mail(
                'Newsletter Subscription',
                message,
                email,
                ['chuksmbanasoj@gmail.com'],
                fail_silently=True
            )
            messages.success(request, f"Thanks for subscribing to our newsletter. Stay tune!!")
            return redirect("home")
        else:
            messages.warning(request, f"Please, fill in the form completely. ")
            return redirect("home")
    return render(request, "others/home.html", {})


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        contact = Contact(name=name, email=email, message=message, phone=phone)
        contact.save()

        if email and name and message and phone:
            send_mail(
                'Contact Inquiry',
                message,
                email,
                ['chuksmbanasoj@gmail.com'],
                fail_silently=True
            )
            messages.success(request, 'Thank you for contacting us, the admin will get back to you soon')
            return redirect('contact')
        else:
            messages.warning(request, 'Please, kindly fill in the form before sending us a message')
            return redirect('contact')
    return render(request, "others/contact.html", {})


def admin_dashboard(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        username = request.session['username']
        name = Admin.objects.get(username=username)
        enquiry = Request.objects.all()
        customer_count = Customer.objects.all().count()
        mechanic = Mechanic.objects.all().count()
        feedback = Feedback.objects.all().count()
        number = Request.objects.all().count()
        customers = []
        for enq in enquiry:
            customer = Customer.objects.get(id=enq.customer_id)
            customers.append(customer)

        context = {
            "admin": name,
            "customer_count": customer_count,
            "mechanic": mechanic,
            "request": number,
            "feedback": feedback,
            "data": zip(customers, enquiry),
        }
        return render(request, "admin/admin_dashboard.html", context)
    else:
        return redirect('admin_login')


def admin_view_all_personnel(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        customer = Customer.objects.all()
        mechanic = Mechanic.objects.all()
        context = {
            "customer": customer,
            "mechanic": mechanic,
        }
        return render(request, "admin/view_personnel.html", context)
    else:
        return redirect('admin_login')


def delete_request(request, id):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        post = Request.objects.get(id=id)
        post.delete()
        messages.warning(request, f"You have deleted the request for \
        {post.customer} with the vehicle_no {post.vehicle_no} ")
        return redirect('admin_dashboard')
    else:
        return redirect('admin_login')


class UpdateRequest(UpdateView):
    form_class = RequestForm
    template_name = "admin/request_form.html"
    queryset = Request.objects.all()

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return get_object_or_404(Request, id=id)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"Request has been updated successfully")
        return "/admin_dashboard/"


def get_single_customer(request, id):
    customer = Customer.objects.get(id=id)

    context = {
        "customer": customer,
    }

    return render(request, "admin/single_customer.html", context)


def delete_customer(request, id):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        # username = request.session['username']
        customer = Customer.objects.get(id=id)
        customer.delete()
        messages.success(request, f"You have deleted {customer} from the record")
        return redirect('view_personnel')
    else:
        return redirect('admin_login')


def get_single_mechanic(request, id):
    mechanic = Mechanic.objects.get(id=id)

    context = {
        "mechanic": mechanic,
    }

    return render(request, "admin/single_mechanic.html", context)


def delete_mechanic(request, id):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        # username = request.session['username']
        mechanic = Mechanic.objects.get(id=id)
        mechanic.delete()
        messages.success(request, f"You have deleted {mechanic} from the record")
        return redirect('view_personnel')
    else:
        return redirect('admin_login')


class UpdateMechanic(UpdateView):
    form_class = AdminUpdateMechanic
    template_name = "admin/update_mechanic.html"
    queryset = Mechanic.objects.all()

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return get_object_or_404(Mechanic, id=id)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"Mechanic Profile has been updated successfully")
        return "/admin_dashboard/"


def view_contact(request):
    cont = Contact.objects.all()

    context = {
        "contact": cont
    }
    return render(request, "admin/contact.html", context)


def view_attendance(request):
    attendance = Attendance.objects.all()

    context = {
        'attendance': attendance
    }
    return render(request, "admin/attendance.html", context)


def delete_attendance(request, id):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        requests = Attendance.objects.get(id=id)
        requests.delete()
        return redirect('admin_attendance')
    else:
        return redirect('admin_login')


def admin_feedback(request):
    feedback = Feedback.objects.all().order_by('-date')

    context = {
        'feedback': feedback
    }
    return render(request, "admin/feedback.html", context)


def delete_feedback(request, id):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        requests = Feedback.objects.get(id=id)
        requests.delete()
        return redirect('admin_feedback')

    else:
        return redirect('admin_login')


def letter(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        newsletter = News.objects.all()

        context = {
            'newsletter': newsletter
        }
        return render(request, "admin/newsletter.html", context)
    else:
        return redirect('admin_login')


def delete_letter(request, id):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        requests = News.objects.get(id=id)
        requests.delete()
        return redirect('admin_letter')
    else:
        return redirect('admin_login')


def user_dashboard(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        # customer = Customer.objects.get(id=request.user.id)
        username = request.session.get('username')
        customer = Customer.objects.get(username=username)
        obi = customer.email
        status = Request.objects.filter(customer_id=customer).order_by('-id')

        progress = Request.objects.all().filter(customer_id=customer.id, status='Repairing').count()
        completed = Request.objects.all().filter(customer_id=customer.id).filter(
            Q(status="Repairing Done") | Q(status="Released")).count()
        new_request = Request.objects.all().filter(customer_id=customer.id).filter(
            Q(status="Pending") | Q(status="Approved")).count()
        pending = Request.objects.all().filter(customer_id=customer.id, status='Pending').count()

        context = {
            "customer": customer,
            "progress": progress,
            "completed": completed,
            "request": new_request,
            "status": status,
            "pending": pending,
            "obi": obi,
        }

        return render(request, "customers/user_dashboard.html", context)

    else:
        return redirect('user_login')


def customer_request(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        username = request.session['username']
        if request.method == 'POST':
            customer = Customer.objects.get(username=username)
            category = request.POST.get('category')
            vehicle_name = request.POST.get('vehicle_name')
            vehicle_model = request.POST.get('vehicle_model')
            vehicle_brand = request.POST.get('vehicle_brand')
            problem_description = request.POST.get('problem_description')
            vehicle_no = request.POST.get('vehicle_no')
            problem = Request(
                customer=customer,
                category=category,
                vehicle_no=vehicle_no,
                vehicle_name=vehicle_name,
                vehicle_brand=vehicle_brand,
                vehicle_model=vehicle_model,
                problem_description=problem_description
            )
            problem.save()
            if customer and category and vehicle_no and vehicle_name and vehicle_brand and vehicle_model and problem_description:
                messages.success(request, f"Your request was sent successfully,\
                we will get back to you shortly")
                return redirect("home")
            else:
                messages.warning(request, f"Please, fill in the request completely. ")
                return redirect("customer_request")
        return render(request, "customers/request_form.html", {})


def leave_feedback(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        username = request.session['username']
        if request.method == 'POST':
            username = Customer.objects.get(username=username)
            name = request.POST.get('name')
            email = username.email
            message = request.POST.get('message')
            feedback = Feedback(username=username, message=message)
            feedback.save()
            if name and message:
                send_mail(
                    'Feedback Inquiry',
                    message,
                    email,
                    ['chuksmbanasoj@gmail.com'],
                    fail_silently=True
                )
                messages.success(request, 'Thanks for leaving a feedback')
                return redirect('user_dashboard')
            else:
                messages.warning(request, 'Please, kindly fill in the form completely')
                return redirect('user_dashboard')
        return render(request, "customers/leave_feedback.html", {})


def mechanic_dashboard(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        # mechanic = Mechanic.objects.get(id=request.user.id)
        username = request.session.get('username')
        mechanic = Mechanic.objects.get(username=username)
        work_in_progress = Request.objects.all().filter(mechanic_id=mechanic.id, status='Repairing').count()
        work_completed = Request.objects.all().filter(mechanic_id=mechanic.id, status='Repairing Done').count()
        new_work_assigned = Request.objects.all().filter(mechanic_id=mechanic.id, status='Approved').count()
        work = Request.objects.all().filter(mechanic_id=mechanic.id).filter(
            Q(status="Repairing Done") | Q(status="Released")).count()
        number = Request.objects.all().count()
        enquiry = Request.objects.all()
        customers = []
        for enq in enquiry:
            customer = Customer.objects.get(id=enq.customer_id)
            customers.append(customer)

        context = {
            'work_in_progress': work_in_progress,
            'work_completed': work_completed,
            'new_work_assigned': new_work_assigned,
            'mechanic': mechanic,
            'work': work,
            "request": number,
            "data": zip(customers, enquiry),
        }
        return render(request, 'mechanics/mechanic_dashboard.html', context)
    else:
        return redirect('mechanic_login')


def mechanic_attendance(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        username = request.session['username']
        if request.method == 'POST':
           mechanic = Mechanic.objects.get(username=username)
           present_status = request.POST.get('present_status')
           attendance = Attendance(mechanic=mechanic, present_status=present_status)
           attendance.save()
           messages.success(request, f"Your Attendance has been recorded!!")
           return redirect("mechanic_dashboard")
        else:
            print('Oga, na error be this o')

        return render(request, "mechanics/mechanic_attendance.html", {})
    else:
        redirect('mechanic_login')


def user_login(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not len(username):
            messages.warning(request, "Username field is empty")
            return redirect('user_login')
        elif not len(password):
            messages.warning(request, "Password field is empty")
            return redirect('user_login')
        else:
            pass
        if Customer.objects.filter(username=username):
            if Customer.objects.filter(username=username):
                user = Customer.objects.filter(username=username)[0]
                password_hash = user.password
                res = check_password(password, password_hash)
                if res == 1:
                    request.session['username'] = username
                    request.session['type'] = 'customer'
                    return redirect('home')
                else:
                    user = Customer.objects.filter(password=password).exists()
                    password_hash = user
                    if res:
                        res = check_password(password, password_hash)
                    else:
                        messages.warning(request, "Password is incorrect")
                        return redirect('user_login')
                    if res == 1:
                        request.session['username'] = username
                        request.session['type'] = 'customer'
                        user = auth.authenticate(username=username, password=password)
                        auth.login(request, user)
                        return redirect('home')
                    else:
                        messages.warning(request, "Password is incorrect")
                        return redirect('user_login')
            else:
                messages.warning(request, "username does not exist")
                return redirect('user_login')
        else:
            messages.warning(request, "No account exist for the given Username")
            return redirect('user_login')
    else:
        redirect('user_login')
    return render(request, 'accounts/user_login.html', {})


def mechanic_login(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not len(username):
            messages.warning(request, "Username field is empty")
            return redirect('mechanic_login')
        elif not len(password):
            messages.warning(request, "Password field is empty")
            return redirect('mechanic_login')
        else:
            pass
        if Mechanic.objects.filter(username=username):
            user = Mechanic.objects.filter(username=username)[0]
            password_hash = user.password
            res = check_password(password, password_hash)
            if res:
                request.session['username'] = username
                request.session['type'] = 'mechanic'
                return redirect('home')
            else:
                user = Mechanic.objects.filter(password=password).exists()
                password_hash = user
                if res:
                    res = check_password(password, password_hash)
                else:
                    messages.warning(request, "Password is incorrect")
                    return redirect('mechanic_login')
                if res == 1:
                    request.session['username'] = username
                    request.session['type'] = 'mechanic'
                    user = auth.authenticate(username=username, password=password)
                    auth.login(request, user)
                    return redirect('home')
                else:
                    messages.warning(request, "Password is incorrect")
                    return redirect('mechanic_login')
        else:
            messages.warning(request, "No account exist for the given Username")
            return redirect('mechanic_login')
    else:
        redirect('mechanic_login')
    return render(request, 'accounts/mechanic_login.html', {})


def admin_login(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not len(username):
            messages.warning(request, "Username field is empty")
            return redirect('admin_login')
        elif not len(password):
            messages.warning(request, "Password field is empty")
            return redirect('admin_login')
        else:
            pass
        if Admin.objects.filter(username=username):
            user = Admin.objects.filter(username=username)[0]
            password_hash = user.password
            res = check_password(password, password_hash)
            if res:
                request.session['username'] = username
                request.session['type'] = 'admin'
                return redirect('home')
            else:
                user = Admin.objects.filter(password=password).exists()
                password_hash = user
                if res:
                    res = check_password(password, password_hash)
                else:
                    messages.warning(request, "Password is incorrect")
                    return redirect('admin_login')
                if res == 1:
                    request.session['username'] = username
                    request.session['type'] = 'admin'
                    user = auth.authenticate(username=username, password=password)
                    auth.login(request, user)
                    return redirect('home')
                else:
                    messages.warning(request, "Password is incorrect")
                    return redirect('admin_login')
        else:
            messages.warning(request, "No account exist for the given Username")
            return redirect('admin_login')
    else:
        redirect('admin_login')
    return render(request, 'accounts/admin_login.html', {})


def user_signup(request):
    # form = Account()
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.method == "POST":
        # form = Account(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        location = request.POST['location']
        phone = request.POST['phone']
        image = request.FILES.get('image', None)
        password = request.POST['password']
        if username and email:
            if Customer.objects.filter(username=username).exists():
                messages.warning(request, "Username already exist, Try another one")
                return redirect('user_signup')
            elif Customer.objects.filter(email=email).exists():
                messages.warning(request, "Email already exist, Try another one")
                return redirect('user_signup')
            else:
                password_hash = make_password(password)
                user = Customer(
                    username=username,
                    email=email,
                    image=image,
                    location=location,
                    password=password_hash,
                    phone=phone
                )
                user.save()
                messages.success(request, "Account Created Successfully, Please login to continue")
                return redirect('user_login')
        else:
            messages.warning(request, "Username does not exist.")
            return redirect('user_signup')
    else:
        # form = Account()
        return render(request, 'accounts/user_signup.html', {})


def mechanic_signup(request):
    # form = Account()
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.method == "POST":
        # form = Account(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        location = request.POST['location']
        skill = request.POST['skill']
        phone = request.POST['phone']
        image = request.FILES.get('image', None)
        password = request.POST['password']

        if username and email:
            if Mechanic.objects.filter(username=username).exists():
                messages.warning(request, "Username already exist, Try another one")
                return redirect('mechanic_signup')
            elif Mechanic.objects.filter(email=email).exists():
                messages.warning(request, "Email already exist, Try another one")
                return redirect('mechanic_signup')
            else:
                password_hash = make_password(password)
                user = Mechanic(
                    username=username,
                    email=email,
                    image=image,
                    password=password_hash,
                    location=location,
                    phone=phone,
                    skill=skill
                )
                user.save()
                messages.success(request, "Account Created Successfully, Please login to continue")
                return redirect('mechanic_login')
        else:
            messages.warning(request, "Username does not exist.")
            return redirect('mechanic_signup')
    else:
        # form = Account()
        return render(request, 'accounts/mechanic_signup.html', {})


def admin_signup(request):
    # form = Account()
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'mechanic':
        return redirect('mechanic_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'admin':
        return redirect('admin_dashboard')
    if request.method == "POST":
        # form = Account(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if username:
            if Admin.objects.filter(username=username).exists():
                messages.warning(request, "Account already exist, please login to continue")
                return redirect('admin_login')
            else:
                password_hash = make_password(password)
                user = Admin(
                    username=username,
                    email=email,
                    password=password_hash,
                    phone=phone
                )
                user.save()
                messages.success(request, "Account Created Successfully, Please login to continue")
                return redirect('admin_login')
        else:
            messages.warning(request, "Username does not exist.")
            return redirect('admin_signup')
    else:
        # form = Account()
        return render(request, 'accounts/admin_signup.html', {})


def logout(request):
    if request.session.get('username', None):
        del request.session['username']
        del request.session['type']
        return render(request, "accounts/user_logout.html", {})
    else:
        return render(request, "accounts/user_login.html", {})


def about(request):
    post = About.objects.all()

    context = {
        'about': post
    }

    return render(request, "others/about.html", context)
