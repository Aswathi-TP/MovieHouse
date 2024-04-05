from django.shortcuts import render,redirect
from Backend.models import TheatreDB,ScreenDB,MovieDB,CastCrewDB,SeatDB,ShowDB
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages
from Frontend.models import CustomUser,ContactDB,UserProfile,BookingDB



# Create your views here.
def index_page(request):
    current_time = datetime.now().time()
    if current_time<datetime.strptime("12:00","%H:%M").time():
        greeting = "Good Morning"
    elif current_time<datetime.strptime("18:00","%H:%M").time():
        greeting = "Good AfterNoon"
    else:
        greeting = "Good Evening"
    date = datetime.now().date()
    return render(request,"index.html",{"greeting":greeting,"date":date})




def add_theatre(request):
    return render(request,"Add_Theatre.html")

def save_theatre(request):
    if request.method == "POST":
        a = request.POST.get('tname')
        b = request.POST.get('taddress')
        c = request.POST.get('tcontact')
        d = request.POST.get('temail')
        e = request.POST.get('tscreen')
        f = request.POST.get('tcapacity')
        g = request.POST.get('tstatus')
        h = request.FILES['timage']
        obj = TheatreDB(TheatreName=a,TheatreAddress=b,Contact=c,Email=d,Screen=e,Capacity=f,Status=g,TheatreImage=h)
        obj.save()
        messages.success(request,"Added Theatre Successfully!!!")
        return redirect(add_theatre)

def display_theatre(request):
    data = TheatreDB.objects.all()
    return render(request,"Display_Theatre.html",{"data":data})

def edit_theatre(request,t_id):
    tdata = TheatreDB.objects.get(id=t_id)
    return render(request,"Edit_Theatre.html",{"tdata":tdata})

def update_theatre(request,t_id):
    if request.method == "POST":
        a = request.POST.get('tname')
        b = request.POST.get('taddress')
        c = request.POST.get('tcontact')
        d = request.POST.get('temail')
        e = request.POST.get('tscreen')
        f = request.POST.get('tcapacity')
        g = request.POST.get('tstatus')
        try:
            img = request.FILES['timage']
            fs = FileSystemStorage()
            file = fs.save(img.name,img)
        except MultiValueDictKeyError:
            file = TheatreDB.objects.get(id=t_id).TheatreImage
        TheatreDB.objects.filter(id=t_id).update(TheatreName=a,TheatreAddress=b,Contact=c,Email=d,Screen=e,Capacity=f,Status=g,TheatreImage=file)
        messages.success(request, "Updated Theatre Successfully!!!")
        return redirect(display_theatre)


def delete_theatre(request,t_id):
    data = TheatreDB.objects.filter(id=t_id)
    data.delete()
    messages.error(request, "Deleted..!")
    return redirect(display_theatre)


def add_screen(request):
    Tname = TheatreDB.objects.all()
    return render(request,"Add_Screen.html",{"Tname":Tname})

def save_screen(request):
    if request.method == "POST":
        a = request.POST.get('tname')
        b = request.POST.get('sname')
        c = request.POST.get('seat')
        d = request.POST.get('pseat')
        e = request.POST.get('Sseat')
        obj = ScreenDB(Theatre=a,ScreenName=b,TotalSeat=c,PremiumSeat=d,StandardSeat=e)
        obj.save()
        messages.success(request,"Added Screen Successfully!!!")
        return redirect(add_screen)

def display_screen(request):
    data = ScreenDB.objects.all()
    return render(request,"Display_Screen.html",{"data":data})

def edit_screen(request,s_id):
    Tname = TheatreDB.objects.all()
    scrn = ScreenDB.objects.get(id=s_id)
    return render(request,"Edit_Screen.html",{"Tname":Tname,"scrn":scrn})

def update_screen(request,s_id):
    if request.method == "POST":
        a = request.POST.get('tname')
        b = request.POST.get('sname')
        c = request.POST.get('seat')
        d = request.POST.get('pseat')
        e = request.POST.get('Sseat')
        ScreenDB.objects.filter(id=s_id).update(Theatre=a,ScreenName=b,TotalSeat=c,PremiumSeat=d,StandardSeat=e)
        messages.success(request,"Updated Screen Successfully!!!")
        return redirect(display_screen)


def delete_screen(request,s_id):
    data = ScreenDB.objects.filter(id=s_id)
    data.delete()
    messages.error(request,"Deleted..!")
    return redirect(display_screen)

def add_movies(request):
    return render(request,"Add_Movies.html")

def save_movie(request):
    if request.method == "POST":
        a = request.POST.get('mname')
        b = request.POST.get('synopsis')
        c = request.POST.get('genre')
        d = request.POST.get('Language')
        e = request.POST.get('date')
        f = request.FILES['image1']
        g = request.FILES['image2']
        h = request.FILES['image3']
        i = request.POST.get('duration')
        j = request.POST.get('tlink')
        obj = MovieDB(MovieName=a,Synopsis=b,Genre=c,Language=d,ReleaseDate=e,Poster1=f,Poster2=g,Poster3=h,Duration=i,TrailerLink=j)
        obj.save()
        messages.success(request,"Added Movie Successfully!!!")
        return redirect(add_movies)

def display_movies(request):
    movie = MovieDB.objects.all()
    return render(request,"Display_Movies.html",{"movie":movie})

def edit_movie(request,m_id):
    film = MovieDB.objects.get(id=m_id)
    return render(request,"Edit_Movie.html",{"film":film})

def update_movie(request,m_id):
    if request.method == "POST":
        a = request.POST.get('mname')
        b = request.POST.get('synopsis')
        c = request.POST.get('genre')
        d = request.POST.get('Language')
        e = request.POST.get('date')
        i = request.POST.get('duration')
        j = request.POST.get('tlink')
        try:
            f = request.FILES['image1']
            fs = FileSystemStorage()
            file1 = fs.save(f.name,f)
        except MultiValueDictKeyError:
            file1 = MovieDB.objects.get(id=m_id).Poster1
        try:
            g = request.FILES['image2']
            gs = FileSystemStorage()
            file2 = gs.save(g.name,g)
        except MultiValueDictKeyError:
            file2 = MovieDB.objects.get(id=m_id).Poster2
        try:
            h = request.FILES['image3']
            hs = FileSystemStorage()
            file3 = hs.save(h.name,h)
        except MultiValueDictKeyError:
            file3 = MovieDB.objects.get(id=m_id).Poster3
        MovieDB.objects.filter(id=m_id).update(MovieName=a, Synopsis=b, Genre=c, Language=d, ReleaseDate=e, Poster1=file1,Poster2=file2,Poster3=file3, Duration=i, TrailerLink=j)
        messages.success(request,"Updated Movie Successfully!!!")
        return redirect(display_movies)

def delete_movie(request,m_id):
    movie = MovieDB.objects.filter(id=m_id)
    movie.delete()
    messages.error(request,"Deleted..!")
    return redirect(display_movies)

def add_cast(request):
    mov = MovieDB.objects.all()
    return render(request,"Add_Cast.html",{"mov":mov})

def save_cast_crew(request):
    if request.method == "POST":
        m = request.POST.get('movie')
        a = request.POST.get('actor')
        b = request.POST.get('character')
        c = request.FILES['actorimg']
        d = request.POST.get('crew')
        e = request.POST.get('role')
        f = request.FILES['crewimg']
        obj = CastCrewDB(Movie=m,ActorName=a,Character=b,ActorImage=c,CrewName=d,Role=e,CrewImage=f)
        obj.save()
        messages.success(request,"Added Cast and Crew Successfully!!!")
        return redirect(add_cast)

def display_cast_crew(request):
    cast = CastCrewDB.objects.all()
    return render(request,"Display_Cast.html",{"cast":cast})

def edit_cast_crew(request,c_id):
    mov = MovieDB.objects.all()
    cst = CastCrewDB.objects.get(id=c_id)
    return render(request,"Edit_Cast.html",{"mov":mov,"cst":cst})

def update_cast_crew(request,c_id):
    if request.method == "POST":
        m = request.POST.get('movie')
        a = request.POST.get('actor')
        b = request.POST.get('character')
        d = request.POST.get('crew')
        e = request.POST.get('role')
        try:
            c = request.FILES['actorimg']
            fs = FileSystemStorage()
            file1 = fs.save(c.name,c)
        except MultiValueDictKeyError:
            file1 = CastCrewDB.objects.get(id=c_id).ActorImage
        try:
            img = request.FILES['crewimg']
            rs = FileSystemStorage()
            image = rs.save(img.name,img)
        except MultiValueDictKeyError:
            image = CastCrewDB.objects.get(id=c_id).CrewImage
        CastCrewDB.objects.filter(id=c_id).update(Movie=m,ActorName=a,Character=b,ActorImage=file1,CrewName=d,Role=e,
                                                  CrewImage=image)
        messages.success(request,"Updated Cast and Crew Successfully!!!")
        return redirect(display_cast_crew)

def delete_cast_crew(request,c_id):
    cast = CastCrewDB.objects.filter(id=c_id)
    cast.delete()
    messages.error(request,"Deleted..!")
    return redirect(display_cast_crew)

def add_show(request):
    show = TheatreDB.objects.all()
    mov = MovieDB.objects.all()
    return render(request,"Add_Shows.html",{"show":show,"mov":mov})

def save_show(request):
    if request.method == "POST":
        a = request.POST.get('theatre')
        c = request.POST.get('show1')
        k = request.POST.get('show2')
        l = request.POST.get('show3')
        v = request.POST.get('show4')
        w = request.POST.get('show5')
        d = request.POST.get('movie')
        e = request.POST.get('time')
        g = request.POST.get('price')
        obj = ShowDB(Theatre=a,Show1=c,Show2=k,Show3=l,Show4=v,Show5=w,Movie=d,Time=e,price=g)
        obj.save()
        messages.success(request, "Added Show time Successfully!!!")
        return redirect(add_show)

def display_show(request):
    show = ShowDB.objects.all()
    return render(request,"Display_Show.html",{"show":show})

def edit_show(request,s_id):
    shows = ShowDB.objects.get(id=s_id)
    show = TheatreDB.objects.all()
    mov = MovieDB.objects.all()
    return render(request,"Edit_Show.html",{"shows":shows,"show":show,"mov":mov})

def update_show(request,s_id):
    if request.method == "POST":
        a = request.POST.get('theatre')
        c = request.POST.get('show1')
        k = request.POST.get('show2')
        l = request.POST.get('show3')
        v = request.POST.get('show4')
        w = request.POST.get('show5')
        d = request.POST.get('movie')
        e = request.POST.get('time')
        g = request.POST.get('price')
        ShowDB.objects.filter(id=s_id).update(Theatre=a,  Show1=c,Show2=k,Show3=l,Show4=v,Show5=w, Movie=d,Time=e,price=g)
        messages.success(request, "Updated Show Successfully!!!")
        return redirect(display_show)

def delete_show(request,s_id):
    show = ShowDB.objects.filter(id=s_id)
    show.delete()
    messages.error(request, "Deleted..!")
    return redirect(display_show)


def admin_login_page(request):
    return render(request,"Admin_Login.html")

def adminlogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
            user = authenticate(email=email,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Welcome Admin")
                request.session['email']=email
                request.session['password']=pwd
                return redirect(index_page)
            else:
                messages.error(request,"Invalid username or password")
                return redirect(admin_login_page)
        else:
            messages.error(request,"Invalid username or password")
            return redirect(admin_login_page)


def adminlogout(request):
    del request.session['email']
    del request.session['password']
    messages.success(request,"Logout Successfully!!!")
    return redirect(admin_login_page)



def add_seat(request):
    Tname = TheatreDB.objects.all()
    return render(request,"Add_Seat.html",{"Tname":Tname})


def save_seat(request):
    if request.method == "POST":
        a = request.POST.get('tname')
        c = request.POST.get('seat')
        d = request.POST.get('available')
        obj = SeatDB(Theatre_name=a, Total_seat=c, Available=d)
        obj.save()
        messages.success(request, "Added Seat Successfully!!!")
        return redirect(add_seat)

def display_seat(request):
    seat = SeatDB.objects.all()
    return render(request,"Display_Seat.html",{"seat":seat})

def edit_seat(request,s_id):
    seats = SeatDB.objects.get(id=s_id)
    Tname = TheatreDB.objects.all()
    return render(request, "Edit_Seat.html", {"seats": seats, "Tname": Tname})

def update_seat(request,s_id):
    if request.method == "POST":
        a = request.POST.get('tname')
        c = request.POST.get('seat')
        d = request.POST.get('available')
        SeatDB.objects.filter(id=s_id).update(Theatre_name=a, Total_seat=c, Available=d)
        messages.success(request, "Updated Seat Successfully!!!")
        return redirect(display_seat)


def delete_seat(request,s_id):
    seat = SeatDB.objects.filter(id=s_id)
    seat.delete()
    messages.error(request, "Deleted..!")
    return redirect(display_show)


def display_contact(request):
    data = ContactDB.objects.all()
    return render(request,"Display_Contact.html",{"data":data})

def delete_contact(request,c_id):
    data = ContactDB.objects.filter(id=c_id)
    data.delete()
    messages.error(request, "Deleted..!")
    return redirect(display_contact)

def display_user(request):
    user = UserProfile.objects.all()
    return render(request,"View_User.html",{"user":user})

def display_booking(request):
    data = BookingDB.objects.all()
    return render(request,"Display_Booking.html",{"data":data})