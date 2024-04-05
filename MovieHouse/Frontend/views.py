from django.contrib import messages
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.urls import reverse
from Backend.models import MovieDB,CastCrewDB,TheatreDB,ScreenDB,SeatDB,ShowDB
from Frontend.models import CustomUser,ReviewDB,UserProfile,BookSlotDB,ContactDB,BookingDB
from django.http import JsonResponse,HttpResponse
import random
from django.contrib.auth import login, authenticate,logout
from django.core.mail import send_mail
from django.conf import settings
from Frontend.forms import UserAdminCreationForm,ProfileUpdateForm,BookSlotForm,SearchForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import razorpay
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


# Create your views here.

def homepage(request):
    movie = MovieDB.objects.all()
    username = request.user.username
    current_date = datetime.now().date()
    return render(request,"Home_Page.html",{"movie":movie,"username":username,"current_date":current_date})


def get_movie_details(request,movie_id):
    try:
        movie_details = MovieDB.objects.get(id=movie_id)
        username = request.user.username
        current_date = datetime.now().date()
        reviews = ReviewDB.objects.filter(movie=movie_details.MovieName)
        cast_details = CastCrewDB.objects.filter(Movie=movie_details.MovieName)
        actors = [member for member in cast_details if member.ActorName]
        crews = [member for member in cast_details if member.CrewName]
        theatre = TheatreDB.objects.all()
        context = {
            'movie_details':movie_details,
            'actors':actors,
            'crews':crews,
            "reviews":reviews,
            "username": username,
            "current_date": current_date,
            "theatre":theatre,

        }
        return render(request,"Single_Movie.html",context)
    except MovieDB.DoesNotExist:
        return HttpResponse("Movie not found",status=404)

def single_movie(request,m_id):
    film = MovieDB.objects.get(id=m_id)
    cast = CastCrewDB.objects.filter(Movie=m_id)
    return render(request,"Single_Movie.html",{"film":film,"cast":cast})

def save_review(request,m_id):
    if request.method == "POST":
        user = request.user.username
        movie = MovieDB.objects.get(id=m_id)
        movie_name = movie.MovieName
        review = request.POST.get('review')
        rate = request.POST.get('rate')
        date = datetime.now().date()
        obj = ReviewDB(user=user,movie=movie_name,review=review,rate=rate,date=date)
        obj.save()
        return redirect(get_movie_details,movie_id=m_id)

def user_login(request):
    return render(request,"User_Login.html")

# def save_register(request):
#     if request.method == "POST":
#         na = request.POST.get('uname')
#         em = request.POST.get('email')
#         pwd = request.POST.get('password')
#         obj = RegistrationDB(Name=na,Email=em,Password=pwd)
#         obj.save()
#         return redirect(user_login)


# def user_signin(request):
#     if request.method == "POST":
#         un = request.POST.get('username')
#         pwd = request.POST.get('password')
#         if RegistrationDB.objects.filter(Name=un,Password=pwd).exists():
#             request.session['Name']=un
#             request.session['Password']=pwd
#             messages.success(request,"Welcome")
#             return redirect(homepage)
#         else:
#             messages.error(request,"Invalid username or password")
#             return redirect(user_login)
#     else:
#         messages.error(request,"Invalid username or password")
#         return redirect(user_login)

def user_logout(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect(login_signup)

def movie_details(request):
    username = request.user.username
    current_date = datetime.now().date()
    film = MovieDB.objects.all()
    languages = MovieDB.objects.values('Language').distinct()
    genres = MovieDB.objects.values('Genre').distinct()
    genre_filter = request.GET.get('Genre')
    language_filter = request.GET.get('Language')
    if genre_filter:
        film = MovieDB.filter(Genre=genre_filter)
    if language_filter:
        film = MovieDB.filter(Language=language_filter)
    return render(request,"Movie_Details.html",{"film":film,"languages":languages,"genres":genres,"username":username,"current_date":current_date})

def filter_data(request):
    languages=request.GET.getlist('Language[]')
    genres = request.GET.getlist('Genre[]')
    allMovies=MovieDB.objects.all().order_by('-id')
    if len(languages)>0:
        allMovies=allMovies.filter(Language_id_in=languages).distinct()
    if len(genres)>0:
        allMovies=allMovies.filter(Genre_id_in=genres).distinct()
    t = render_to_string('ajax/Movie_Details.html',{"data":allMovies})
    return JsonResponse({'data':t})

def filter_movies(request):
    selected_languages = request.GET.getlist('language')
    selected_genres = request.GET.getlist('genre')
    if selected_languages or selected_genres:
        filtered_movies = MovieDB.objects.filter(Language__in=selected_languages,Genre__in=selected_genres)
        data = [{'MovieName':movie.MovieName,'ReleaseDate':movie.ReleaseDate,'Language':movie.Language,'Genre':movie.Genre} for movie in filtered_movies]
    else:
        data = []

    return JsonResponse({'movies':data})

def contact_page(request):
    username = request.user.username
    current_date = datetime.now().date()
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,"Contact.html",{"username":username,"current_date":current_date,"user_profile":user_profile})

def save_contact(request):
    if request.method == "POST":
        na = request.POST.get('name')
        em = request.POST.get('email')
        ph = request.POST.get('phone')
        msg = request.POST.get('message')
        obj = ContactDB(Name=na,Email=em,Phone=ph,Message=msg)
        obj.save()
        messages.success(request,"Send Your Message Successfully!!")
        return redirect(contact_page)

# user login with otp

def home(request):
    return render(request,"home.html")

def login_signup(request):
    return render(request,"Login_Signup.html")

def register(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST, req.FILES)
        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(
                user=user,
                email=form.cleaned_data.get('email'),
            )
            messages.success(req, "Registered Successfully! Now you can Login.")
            return redirect(login_signup)
        else:
            print(form.errors)
            messages.error(req, "Invalid credentials")
            return redirect(login_signup)
    return render(req, 'Login_Signup.html', {"form": form})


def UserLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
            user = authenticate(request, email=email, password=password)
            if user is not None and not user.is_superuser:
                login(request, user)
                request.session['email'] = email
                request.session['password'] = password
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                message = "Your OTP for login:"
                send_mail(otp, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
                messages.info(request,"Check your mail for OTP Verification.!")
                return render(request, 'verify_otp.html', {'email': email})
            else:
                messages.error(request, "invalid")
                return redirect(login_signup)
        else:
            messages.error(request, "invalid")
            return redirect(login_signup)
    return render(request, "Login_Signup.html")


def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp1 = request.session.get('otp')
        if str(otp) == str(otp1):
            messages.success(request,"Successfully logged in.")
            username = request.user.username
            return redirect(homepage)
        else:
            messages.error(request,"invalid OTP")
            return redirect(login_signup)
    return render(request,"Login_Signup.html")



def seat_select(request,theatre_id,movie_id):
    username = request.user.username
    current_date = datetime.now().date()
    theatre = TheatreDB.objects.get(id=theatre_id)
    movie = MovieDB.objects.get(id=movie_id)
    shows = ShowDB.objects.filter(Theatre=theatre.TheatreName,Movie=movie.MovieName)
    total_seats = SeatDB.objects.get(Theatre_name=theatre.TheatreName).Total_seat
    seat_range = range(1,total_seats + 1)


    if shows.exists():
        first_show = shows.first()
        ticket_price = first_show.price
    else:
        ticket_price = None

    if request.method == "POST":
        form = BookSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(movie_checkout)
    else:
        form = BookSlotForm()
    context = {
        "username":username,
        "current_date":current_date,
        "theatre":theatre,
        "total_seats":total_seats,
        "seat_range":seat_range,
        "movie":movie,
        "shows":shows,
        "ticket_price":ticket_price,
        "form":form

    }
    return render(request,"seat_select.html",context)

def screen_list(request):
   pass


def profile_update(request):
    username = request.user.username
    current_date = datetime.now().date()
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()
    form = ProfileUpdateForm(instance=user_profile)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST,request.FILES,instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request,"updated")
            return redirect(homepage)
    return render(request,"user_profile.html",{"form":form,"username":username,"current_date":current_date})

def movie_checkout(request):
    username = request.user.username
    email = request.user.email
    current_date = datetime.now().date()
    data = BookSlotDB.objects.filter(UserName=username).order_by('Created_at').last()
    context = {
        "username":username,
        "email": email,
        "current_date": current_date,
        "data": data
    }

    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount_paid') * 10000)
        client = razorpay.Client(auth=("rzp_test_F6nhWoihwx4CSE", "sliIs5AdZZwqQlINyu1W2SrD"))
        payment = client.order.create({"amount": amount, "currency": 'INR'})
        print(payment)
        return render(request, "movie_checkout.html",)
    return render(request,"movie_checkout.html",context)

def about_page(request):
    username = request.user.username
    current_date = datetime.now().date()
    return render(request,"About.html",{"username":username,"current_date":current_date})

def save_slot(request):
    if request.method == "POST":
        name = request.user.username
        t_name = request.POST.get('theatre_name')
        t_address = request.POST.get('theatre_address')
        m_name = request.POST.get('movie_name')
        seat = request.POST.get('seatselected')
        date = request.POST.get('selected_date')
        time = request.POST.get('selected_time')
        price = request.POST.get('total_price')
        obj = BookSlotDB(UserName=name,TheatreName=t_name,TheatreAddress=t_address,MovieName=m_name,SeatNum=seat,Date=date,Time=time,TotalPrice=price)
        obj.save()
        messages.success(request,"added")
        return redirect(movie_checkout)


@csrf_exempt
def save_booking(request):
    if request.method == "POST":
        book_id = request.POST.get('booking_id')
        name = request.POST.get('name')
        movie_name = request.POST.get('movie_name')
        theatre_name = request.POST.get('theatre_name')
        theatre_address = request.POST.get('theatre_address')
        selected_seats = request.POST.get('seat_number')
        selected_date = request.POST.get('selected_date')
        selected_time = request.POST.get('selected_time')
        amount_paid = request.POST.get('amount_paid')
        obj = BookingDB(book_id=book_id,name=name,movie_name=movie_name,theatre_name=theatre_name,theatre_address=theatre_address,selected_seats=selected_seats,selected_date=selected_date,selected_time=selected_time,amount_paid=amount_paid)
        obj.save()
        messages.success(request,"success")
        return redirect(homepage)


def booking_history(request):
    username = request.user.username
    current_date = datetime.now().date()
    data = BookingDB.objects.filter(name=username)
    return render(request,"Booking_History.html",{"data":data,"username":username,"current_date":current_date})

def download_booking_details(request, booking_id):
    # Retrieve booking details from the database
    booking = BookingDB.objects.get(id=booking_id)

    # Create the text content for the file
    content = f"Booking ID: {booking.book_id}\n"
    content += f"Name: {booking.name}\n"
    content += f"Movie Name: {booking.movie_name}\n"
    content += f"Theatre Name: {booking.theatre_name}\n"
    content += f"Theatre Address: {booking.theatre_address}\n"
    content += f"Selected Seats: {booking.selected_seats}\n"
    content += f"Selected Date: {booking.selected_date}\n"
    content += f"Selected Time: {booking.selected_time}\n"
    content += f"Amount Paid: {booking.amount_paid}\n"

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="booking_{booking_id}.pdf"'

    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica",15)
    lines = content.split('\n')
    y = 750
    for line in lines:
        p.drawString(100, y, line)
        y -= 40
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def delete_history(request,booking_id):
    data = BookingDB.objects.filter(id=booking_id)
    data.delete()
    messages.error(request, "Deleted..!")
    return redirect(booking_history)

def search_view(request):
    username = request.user.username
    current_date = datetime.now().date()
    form = SearchForm(request.GET)
    results = None
    if form.is_valid():
        query = form.cleaned_data.get('query')
        results = MovieDB.objects.filter(MovieName__icontains=query)

    return render(request,"search.html",{'form':form,'results':results,'username':username,'current_date':current_date})

