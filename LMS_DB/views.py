from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Entry
from datetime import datetime, date
from .models import *
from django.http import Http404
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, resolve
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.contrib.auth.models import User
import sys
import cgi
sys.path.append("..")
from event2.PayTM import Checksum
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.views import generic
MERCHANT_KEY = 'Paytm Merchant Key'


# Create your views here.
# Event add

class Add_Event(CreateView):
    model = Events_Master
    fields = ['Event_Name', 'Event_Type', 'Artist_Name', 'Event_Venue', 'Event_Description', 'Event_Poster',
              'Event_Date', 'Event_Time', 'Event_Price', 'Event_Capacity', 'Rows', 'Columns', 'Blocked_Seats']
    template_name = 'Events_Master_form2.html'
    def form_valid(self, form):
        if self.request.session._session_key == None:
            return HttpResponseRedirect(reverse('login'))

        self.object = form.save(commit=False)
        self.object.Event_Status = 'InActive'
        self.object.Artists_Unique_Id = 1213
        self.object.Event_By = self.request.session['user_id']
        self.object.save()
        return super(CreateView, self).form_valid(form)

    def get_success_url(self):
        if self.request.session['user_id'] == 'admin':
            return reverse_lazy('admin-panel')
        else:
            return reverse_lazy('dashboard_event', args=(self.request.session['user_id'],))

class Edit_event(UpdateView):
    model = Events_Master
    fields = ['Event_Name', 'Event_Type', 'Artist_Name', 'Event_Venue', 'Event_Description', 'Event_Poster',
              'Event_Date', 'Event_Time', 'Event_Price', 'Event_Capacity', 'Blocked_Seats']
    def get_object(self):
        return Events_Master.objects.get(Event_Unique_Id=self.kwargs.get('event_id'))
    def dispatch(self, request, *args, **kwargs):
        user_event = self.get_object()
        if self.request.session._session_key == None:
            return HttpResponseRedirect(reverse('login'))
        elif self.request.session['user_id'] == 'admin':
            self.fields = ['Event_Name', 'Event_Type', 'Artist_Name', 'Event_Venue', 'Event_Description',
                       'Event_Poster',
                       'Event_Date', 'Event_Time', 'Event_Price', 'Event_Capacity', 'Rows', 'Columns',
                       'Blocked_Seats']

        elif int(user_event.Event_By) != int(self.request.session['user_id']):
            request.session.flush()
            request.session.modified = True
            return HttpResponseRedirect(reverse('login'))
        else:
            pass
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)



    def get_success_url(self):
        if self.request.session == None:
            return reverse_lazy('login')
        elif self.request.session['user_id'] == 'admin':
                return reverse_lazy('admin-panel')
        else :
            return reverse_lazy('dashboard_event', args = (self.request.session['user_id'],))

def view_layout(request, event_id):
    try:
        u_id = request.session['user_id']
        if u_id =='admin':
            user = Users_Master.objects.get(Name = 'admin')
        else:
            user = Users_Master.objects.get(Users_unique_id=u_id)
    except:
        return HttpResponseRedirect(reverse('login'))
    user_event = Events_Master.objects.get(Event_Unique_Id = event_id)
    if user_event.Event_By == request.session['user_id'] or request.session['user_id'] == 'admin':
       return render(request, "../templates/view_layout.html", {'event':user_event, 'user': user})
    else:
        request.session.flush()
        request.session.modified = True
        return HttpResponseRedirect(reverse('login'))
# <!--    <a href="{% url 'Edit_layout' request.resolver_match.kwargs.event_id %}"><button>View Layout </button></a>-->
#  <!-- THis is beautiful ... request.resolver_match.kwargs is used to get the event_id stored in the current url
#  and pass it to the view -->

def index(request):
    if request.method != 'POST':
        raise Http404("Post is not configured/")
    try:
        m = Entry.objects.get(username=request.POST['email'])
        if m.password == request.POST['pass']:
            user = Users_Master.objects.get(Users_unique_id = int(m.user_id_id))
            user.User_last_Login = datetime.datetime.now()
            user.save()
            if m.username == 'admin':
                request.session['user_id'] = 'admin'
                request.session.modified = True
                return HttpResponseRedirect(reverse('admin-panel'))
            # html = "Welcome <a href=" +'{%url 'event_add' %}'+"> Click here to add event </a>"
            request.session['user_id'] = str(m.user_id_id)
            print(type(m.user_id_id), m.user_id_id)
            request.session['username'] = m.username
            request.session.modified = True
            return HttpResponseRedirect(reverse('dashboard', args=[m.user_id]))
        else:
            message = "Invalid Login ! Try again"
            return render(request, '../templates/login.html', {'message': message})
    except Entry.DoesNotExist:
        message = "Invalid Login ! Try again"
        return render(request, '../templates/login.html', {'message': message})

def sign_up(request):
    if request.method != 'POST':
            print(request.method)
            message = "Try Again !"
            return render(request, '../templates/signup.html', {'message': message})
    else:
        username = request.POST.get('Username')
        email = request.POST['email']
        name = request.POST['Name']
        surname = request.POST['Surname']
        contact = request.POST['Contact']
        country = request.POST['Country']
        state = request.POST['State']
        city = request.POST['City']
        password = request.POST['pass']

        user = Users_Master(Name = name, Surname = surname, Country = country, State = state, City = city, User_last_Login = 0, User_authentication = 'No', Contact_Number = contact, Email = email )
        user.save()
        entry = Entry(user_id_id = user.pk, username= username, password = password)
        entry.save()
        message = 'Login again to complete sign up'
        return render(request, '../templates/login.html', {'message': message})
# List Events
def events_list(request):

    all_events = Events_Master.objects.filter(Event_Status='Active')
    template = loader.get_template('../templates/events.html')
    context = {
        'all_events': all_events,
    }

    return render(request, '../templates/events.html', context)


# Event Details
def event_details(request, event_id):
    try:
        event2 = None
        artist1 = None

        event2 = Events_Master.objects.get(Event_Unique_Id=event_id)
        artist1 = Artists_Master.objects.get(Artist_Unique_Id=event2.Artists_Unique_Id)
    except ObjectDoesNotExist:
        raise Http404("Event Doesnot exist")
    # except artist1.DoesNotExist:
    #     raise Http404("Artist Problem")
    return render(request, '../templates/details.html', {'event1': event2, 'artist': artist1})


# def book_tickets(request, event_id):
#  event = Events_Master.objects.get(Event_Unique_Id = event_id)

# number = request.POST['number']

# return render(request,'../templates/confirm_booking.html',{'number':number})*/

# Reserve Seat
def reserve(request, event_id):
    event = Events_Master.objects.get(Event_Unique_Id=event_id)
    try:
        user = Users_Master.objects.get(Users_unique_id=request.session['user_id'])
    except:
        user = None
    return render(request, '../templates/select.html', {'event': event, 'user': user})


def payment(request, event_id):
    url = str(request.build_absolute_uri())

    url = url +'/handlerequest/'
    event = Events_Master.objects.get(Event_Unique_Id=event_id)
    seats = request.POST.get('SeatsDisplay1')
    number_of_seats = request.POST.get('NumberDisplay1')
    amount = event.Event_Price * int(number_of_seats)
    try:
        u_id = request.session['user_id']
        user = Users_Master.objects.get(Users_unique_id=u_id)
    except:
        message = "Login to book again !"
        return render(request, '../templates/login.html', {'message': message})

    username = user.Name
    ticket = Ticket_master(Event_Name=event.Event_Name, Event_Unique_Id=event.Event_Unique_Id, User_Name=username,
                           User_Unique_id=u_id, Organiser_Unique_Id=event.Organiser_Unique_Id,
                           Number_of_tickets=int(number_of_seats), Seat_no=seats, Payment_Method='paytm',
                           Payment_Amount=amount)
    ticket.save()
    id = ticket.pk

    # user.User_tickets = str(id) + ',' + str(user.User_tickets)
    # user.save()
    # if event.Event_Seats_Sold:
    #     update_x = str(str(event.Event_Seats_Sold) + ',' + str(seats))
    #     event.Event_Seats_Sold = str(update_x)
    # else:
    #     event.Event_Seats_Sold = str(seats)
    # x = len(event.Event_Seats_Sold.split(','))
    # event.Event_Tickets_Sold = int(x)
    # event.save()
    my_dict = {
        'MID': 'afBAZL04675482009721',
        'ORDER_ID': str(id),
        'TXN_AMOUNT': str(amount),
        'CUST_ID': str(user.Users_unique_id),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL':url,
    }

    my_dict['CHECKSUMHASH'] = Checksum.generate_checksum(my_dict, MERCHANT_KEY)
    return render(request, 'paytm.html', {'my_dict': my_dict})
    #html = "<h1>Database Successfully Updated.<br> Redirecting to payment gateway. <br>Amount to be paid  <B>:" + str(amount)+"</B></H1>" + "<h1><br><a href=" + '{% url 'reserve' %}' + ">Go back</a></h1>")

@csrf_exempt
def handlerequest(request, event_id):
    checksum=0
    form = request.POST
    response_dict = {}

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    print(verify)
    event = Events_Master.objects.get(Event_Unique_Id=event_id)
    ticket = Ticket_master.objects.get(id=int(response_dict['ORDERID']))
    if verify:
        if response_dict['RESPCODE'] == '01':
            # u_id = request.session['user_id']

            user = Users_Master.objects.get(Users_unique_id = ticket.User_Unique_id)
            if user.User_tickets:
                user.User_tickets = str(response_dict['ORDERID']) + ',' + str(user.User_tickets)
                user.save()
            else:
                user.User_tickets = str(user.User_tickets)
            if event.Event_Seats_Sold:
                update_x = str(str(event.Event_Seats_Sold) + ',' + str(ticket.Seat_no))
                event.Event_Seats_Sold = str(update_x)
            else:
                event.Event_Seats_Sold = str(ticket.Seat_no)
            x = len(event.Event_Seats_Sold.split(','))
            event.Event_Tickets_Sold = int(x)
            event.save()
            ticket.Payment_Status = 'Completed'
            ticket.save()
            print("order successful")
            return render(request, "../templates/ticket.html",
                          {'user': user, 'event': event, 'ticket': ticket })



        else:
            ticket.Payment_Status = 'TP'
            ticket.save()
            print("order unsuccessful because" + response_dict['RESPMSG'])
            return HttpResponse("Unsuccessful ! Retry")
    else:
        ticket.Payment_Status = 'VP'
        ticket.save()
        print("order unsuccessful because" + response_dict['RESPMSG'])
        return HttpResponse("Unsuccessful ! Retry")

# html = "Welcome <a href=" +'{%url 'event_add' %}'+"> Click here to add event </a>"
def dashboard(request, user):
    try:
        r = request.session['user_id']
        if int(r) != int(user):
            request.session.flush()
            request.session.modified = True
            return HttpResponseRedirect(reverse('login'))
        user = Users_Master.objects.get(Users_unique_id=r)
    except:
        return HttpResponseRedirect(reverse('logout'))
    return render(request, "../templates/dashboard.html", {'user': user})


def dashboard_settings(request, user):
    try:
        r = request.session['user_id']
        if r != user:
            return HttpResponseRedirect(reverse('logout'))
        user1 = Users_Master.objects.get(Users_unique_id=r)
    except:
       return HttpResponseRedirect(reverse('logout'))
    return render(request, "../templates/user-dashboard-settings.html", {'user': user1})


def dashboard_event(request, user):
    events = Events_Master.objects.filter(Event_By=user).order_by('Event_Date')

    return render(request, '../templates/user-dashboard-events.html', {'events': events})

def dashboard_history(request, user):
    try:
        r = request.session['user_id']
        print(r,user)
        if r != user:
            request.session.flush()
            request.session.modified = True
            return HttpResponseRedirect(reverse('login'))
        user = Users_Master.objects.get(Users_unique_id=r)
    except:
        return HttpResponseRedirect(reverse('logout'))
    dates = set()
    event_dates = {}
    tickets = Ticket_master.objects.filter(User_Unique_id=r).order_by('-Ticket_Registration_Time').values()
    for ticket in tickets:
        dates.add(ticket['Event_Unique_Id'])
    for i in dates:
        event_dates[i] = Events_Master.objects.filter(Event_Unique_Id= i).values()[0]['Event_Date']
        event_dates[i]= datetime.datetime.strptime(event_dates[i],'%Y-%m-%d')
        if event_dates[i]< datetime.datetime.today():
            event_dates[i] = 0
    return render(request, "../templates/user-dashboard-history.html", {'user': user,
                                                                        'tickets': tickets,
                                                                        'event_dates': event_dates})




# class dashboard_settings(CreateView): _CHANGE NAME HERE
#     def get_object(self):
#             return Users_Master.objects.get(Users_unique_id=self.kwargs.get('user'))
#     def check(self, request):
#         try:
#             user = Users_Master.objects.get(Users_unique_id = self.kwargs.get('user'))
#             r = request.session['user_id']
#             if r != user:
#                 return HttpResponseRedirect(reverse('login'))
#             user = Users_Master.objects.get(Users_unique_id=r)
#         except:
#             return HttpResponseRedirect(reverse('login'))
#     model = Users_Master
#     fields = ['Name', 'Surname', 'Country','State','City']
#     success_url = reverse_lazy('admin-panel')  # IT REDIRECTS TO THE SAME PAGE



def admin_panel(request, event=0):
    if request.method == 'POST':
        if 'activate_event_request' in request.POST:
            id1 = int(request.POST.get('activate_event_request'))
            try:
                event = Events_Master.objects.get(Event_Unique_Id=id1)
            except:
                raise Http404("Event Not found.")
            event.Event_Status = 'Active'
            event.save()

        elif 'make_event_inactive' in request.POST:
            id1 = int(request.POST.get('make_event_inactive'))
            event = Events_Master.objects.get(Event_Unique_Id=id1)
            event.Event_Status = 'InActive'
            event.save()
        elif 'remove_event_request' in request.POST:
            id1 = int(request.POST.get('remove_event_request'))
            event = Events_Master.objects.get(Event_Unique_Id=id1)
            event.Event_Status = 'InActive'
            event.save()
        elif 'edit' in request.POST:
            return HttpResponse("This will be edit page of event")
        else:
            return Http404("Big Error")
    else:
        try:
            r = request.session['user_id']
            if r != 'admin':
                request.session.flush()
                request.session.modified = True
                return HttpResponseRedirect(reverse('login'))
        except:
            return HttpResponseRedirect(reverse('login'))
    inactive = Events_Master.objects.filter(Event_Status='InActive').order_by('Event_Registration_Time')
    active = Events_Master.objects.filter(Event_Status='Active').order_by('Event_Registration_Time')
    return render(request, "../templates/admin-panel.html", {'inactive': inactive, 'active': active})


def logout(request):
    request.session.flush()
    request.session.modified = True
    return HttpResponseRedirect(reverse('home'))
