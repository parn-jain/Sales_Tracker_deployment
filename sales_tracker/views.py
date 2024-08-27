# from typing import Any
# from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.db.models import Count, OuterRef, Subquery
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from typing import Any
from django.db import connection
from django.db.models import Count
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
# import pymysql
from django.contrib.auth import get_user_model
from users.models import Profile, RegisterUser
from .models import MiningData, ContactData, LeadsData, OpportunityData, QuotesData , CallingAgent
from .forms import MiningForm, ContactForm, LeadForm, OpportunityForm, QuoteForm
from .analysis import generate_bar_chart, TotalDays
from .admin_analysis import Att_perct,Late_perct ,Mining_Count,Leads_Count
from .requirements import timer
from django.http import HttpResponseForbidden
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import AttendanceRecord







def get_timer_value(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    return JsonResponse({
        'hrs': int(elapsed_time[0]),
        'min': int(elapsed_time[1]),
        'sec': int(elapsed_time[2])
    })


# Create your views here.
class IndexView(TemplateView):
    template_name = "sales_tracker/index.html"
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.branch != 'miner': 
            return HttpResponseForbidden("You do not have access to this page.")
        return super().dispatch(request, *args, **kwargs)
    # def dispatch(self, request, *args, **kwargs):
    #     print("Thisis ")
    #     if self.request.user.profile.branch == 'agent': 
    #         self.template_name = "sales_tracker/agent.html"
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        context["user"] = user.username
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        today_mining = MiningData.objects.filter(date = now_date)
        today_mining_count = today_mining.count()
        context["mining_count"] = today_mining_count
        today_lead = LeadsData.objects.filter(date = now_date)
        today_lead_count = today_lead.count()
        context["lead_count"] = today_lead_count
        today_contact = ContactData.objects.filter(date = now_date)
        today_contact_count = today_contact.count()
        context["contact_count"] = today_contact_count
        today_Opportunity = OpportunityData.objects.filter(date = now_date)
        today_Opportunity_count = today_Opportunity.count()
        context["Opportunity_count"] = today_Opportunity_count
        return context


class Agent(TemplateView):
    template_name = "sales_tracker/agent.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        users = request.user
        u = RegisterUser.objects.get(email=users)
        u = u.id
        ToCall = MiningData.objects.filter(assigned_to=u)
        context["user"] = u
        context["Tocall"] = ToCall
        return context


# class MiningView(CreateView):
#     model = MiningData
#     form_class = MiningForm
#     template_name = "sales_tracker/mining.html"
#     success_url = "mining"
#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         request = self.request
#         user = request.user
#         utc_login_time = user.last_login
#         elapsed_time = timer(utc_login_time)
#         context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         today_mining = MiningData.objects.filter(date = now_date)
#         today_mining_count = today_mining.count()
#         context["mining_count"] = today_mining_count
#         return context
    


def assign_miningCt():
    # user = request.user
    least_occurring_assigned_to_id = (
    MiningData.objects
    .filter(assigned_to__profile__branch='agent')
    .values('assigned_to')
    .annotate(count=Count('assigned_to'))
    .order_by('count')
    .first()
)
    # return least_occurring_assigned_to_id
    assigned_to_id = least_occurring_assigned_to_id['assigned_to']
    return RegisterUser.objects.get(id=assigned_to_id)






# def assign_miningCt():
#     # Get IDs of profiles with branch='agent'
#     agent_profile_ids = Profile.objects.filter(branch='agent').values_list('user_id', flat=True)
    
#     # Subquery to get the least occurring assigned_to ID
#     least_occurring_subquery = MiningData.objects.filter(
#         assigned_to__in=agent_profile_ids
#     ).values('assigned_to').annotate(count=Count('assigned_to')).order_by('count').values('assigned_to')[:1]

#     # Use the subquery to get the least occurring assigned_to
#     least_occurring_assigned_to_id = Subquery(least_occurring_subquery)

#     # Get the corresponding RegisterUser
#     assigned_to_user = RegisterUser.objects.filter(
#         user_id=least_occurring_assigned_to_id
#     ).first()

#     return assigned_to_user


# ---------------------------------------------------------------------
# def assign_miningCt():
#     # Raw SQL query to find the least occurring `assigned_to` ID
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT M.assigned_to_id
#             FROM sales_tracker_miningdata as M
#             LEFT JOIN users_profile as P
#             ON M.assigned_to_id = P.user_id
#             WHERE P.branch = 'agent'
#             GROUP BY P.user_id
#             LIMIT 1;
#         """)
        
#         # Fetch the result
#         result = cursor.fetchone()
    
#     if result:
#         assigned_to_id = result[0]
#         # Fetch and return the RegisterUser object
#         return RegisterUser.objects.get(id=assigned_to_id)
#     else:
#         print("None is returned")
#         return None




# def assign_miningCt():
#     # Raw SQL query to find the least occurring `assigned_to` ID
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT assigned_to_id
#             FROM sales_tracker_miningdata
#             JOIN users_registeruser ON sales_tracker_miningdata.assigned_to_id = users_registeruser.id
#             JOIN users_profile ON users_registeruser.id = users_profile.user_id
#             WHERE users_profile.branch = %s
#             GROUP BY assigned_to_id
#             ORDER BY COUNT(*) ASC
#             LIMIT 1
#         """, ['agent'])
        
#         # Fetch the result
#         result = cursor.fetchone()
#         if result:
#             assigned_to_id = result[0]
#             # Debugging: Print the fetched ID
#             print(f"Fetched assigned_to_id: {assigned_to_id}")
#             try:
#                 # Fetch and return the RegisterUser object
#                 return RegisterUser.objects.get(id=assigned_to_id)
#             except RegisterUser.DoesNotExist:
#                 # Handle case where the RegisterUser object is not found
#                 print(f"RegisterUser with id {assigned_to_id} does not exist.")
#                 return None
#         else:
#             print("No result returned from the query.")
#             return None



def mining_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = MiningForm(request.POST)
        try:
            MiningData.objects.get(organisation_name = form.data.get("organisation_name"))
            print("hello world")
        except:
            assignTo = assign_miningCt()
            now_date_time = datetime.datetime.now()
            now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
            username = request.user.username
            mining_details = MiningData(
                organisation_name = form.data.get("organisation_name"),
                customer_first_name = form.data.get("customer_first_name"),
                customer_last_name = form.data.get("customer_last_name"),
                customer_address = form.data.get("customer_address"),
                customer_contact_number = form.data.get("customer_contact_number"),
                customer_mobile_number = form.data.get("customer_mobile_number"),
                customer_email = form.data.get("customer_email"),
                company_revenue = form.data.get("company_revenue"),
                company_emp_size = form.data.get("company_emp_size"),
                customer_offering = form.data.get("customer_offering"),
                competition_of_AT = form.data.get("competition_of_AT"),
                stock_market_registered = form.data.get("stock_market_registered"),
                influncer = form.data.get("influncer") == "on",
                desition_maker = form.data.get("desition_maker") == "on",
                IT_spending_budget = form.data.get("IT_spending_budget"),
                source_of_data_mining = form.data.get("source_of_data_mining"),
                date = now_date,
                assigned_to = assignTo
            )
            mining_details.save()
            print("Hello world 4")
            return redirect("mining")    
        
        print("Hello world 2")
        return render(request, "sales_tracker/mining.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = MiningForm()
    return render(request, "sales_tracker/mining.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})

# class DataView(ListView):
#     template_name = "sales_tracker/data.html"
#     model = MiningData
#     context_object_name = "mined_data"

#     def get_queryset(self):
#         base_query =  super().get_queryset()
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         data = base_query.filter(date = f"{now_date}")
#         return data
    
#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         request = self.request
#         user = request.user
#         utc_login_time = user.last_login
#         elapsed_time = timer(utc_login_time)
#         context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         today_mining = MiningData.objects.filter(date = now_date)
#         today_mining_count = today_mining.count()
#         context["mining_count"] = today_mining_count
#         return context
    
class DetailDataView(DetailView):
    template_name = "sales_tracker/detail.html"
    model = MiningData
    context_object_name = "detail"  

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        today_mining = MiningData.objects.filter(date = now_date)
        today_mining_count = today_mining.count()
        context["mining_count"] = today_mining_count
        return context

class CallView(TemplateView):
    template_name = "sales_tracker/call.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        today_mining = MiningData.objects.filter(date = now_date)
        today_mining_count = today_mining.count()
        context["mining_count"] = today_mining_count
        return context

class VideoCallView(TemplateView):
    template_name = "sales_tracker/videocall.html"


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt
def join_meet(request):
    if request.method == "POST":
        room_id = request.POST["id"]
        return redirect(f'/videocall?roomID={room_id}')
    return render(request, "sales_tracker/join.html")


class Agent(TemplateView):
    template_name = "sales_tracker/agent.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        users = request.user
        u = RegisterUser.objects.get(email=users)
        u = u.id
        ToCall = MiningData.objects.filter(assigned_to=u)
        context["user"] = u
        context["ToCall"] = ToCall
        return context
# class ContactCreateView(CreateView):
#     model = ContactData
#     form_class = ContactForm
#     template_name = "sales_tracker/create_contact.html"
#     success_url = "message"
    
    
class Message(TemplateView):
    template_name = "sales_tracker/message.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["message"] = "data stored successfully"
        return context

# class LeadCreateView(CreateView):
#     model = LeadsData
#     form_class = LeadForm
#     template_name = "sales_tracker/create_contact.html"
#     success_url = "message"
    

# def assign_contact_to_agent():
#     # Get all agents who are active and can accept contacts
#     agents = Profile.objects.filter(branch='agent', can_login=True)

#     # Find the agent with the least assigned contacts   
#     agent = agents.annotate(num_contacts=Count('user_id')).order_by('num_contacts').first()
#     print(agent,"this is agent ")

#     return agent




def Create_contact_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = ContactForm(request.POST)
        try:
            ContactData.objects.get(email_id = form.data.get("email_id"))
        except:
            # assigned_agent = assign_contact_to_agent()
            now_date_time = datetime.datetime.now()
            now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
            username = request.user.username
            # claid = request.POST.get("calling_agent")
            contact_details = ContactData(
                first_name = form.data.get("first_name"),
                last_name = form.data.get("last_name"),
                email_id = form.data.get("email_id"),
                contact_number = form.data.get("contact_number"),
                job_title = form.data.get("job_title"),
                address = form.data.get("address"),
                organization = MiningData.objects.get(organisation_name = form.data.get("organization")),
                date = now_date,
                # assigned_to=assigned_agent.user,
                
                # assigned_to = get_user_model().objects.get(username=username),
                # calling_agent = CallingAgent.objects.get(calling_agent_id=claid),
            )
                # calling_agent=CallingAgent.objects.get(id=form.calling_agent.get("calling_agent"))
            contact_details.save()

            return redirect("create_contact")
        
        return render(request, "sales_tracker/create_contact.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count,"calling_agents": CallingAgent.objects.all()})


    else:
        form = ContactForm()
    return render(request, "sales_tracker/create_contact.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count,"calling_agents": CallingAgent.objects.all()})


def Create_lead_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = LeadForm(request.POST)
        try:
            LeadsData.objects.get(contact_link = ContactData.objects.get(pk = form.data.get("contact_link")))
        except:
            now_date_time = datetime.datetime.now()
            now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
            username = request.user.username
            contact_details = LeadsData(
                lead_name = form.data.get("lead_name"),
                first_name = form.data.get("first_name"),
                last_name = form.data.get("last_name"),
                email_id = form.data.get("email_id"),
                contact_number = form.data.get("contact_number"),
                job_title = form.data.get("job_title"),
                address = form.data.get("address"),
                contact_link = ContactData.objects.get(pk = form.data.get("contact_link")),
                date = now_date,
                assigned_to = get_user_model().objects.get(username=username)
            )
            print("hello bhai")
            contact_details.save()

            return redirect("create_lead")
        
        return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = LeadForm()
    return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


def Create_opportunity_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = OpportunityForm(request.POST)
        
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        username = request.user.username
        contact_details = OpportunityData(
            opportunity_name = form.data.get("opportunity_name"),
            amount = form.data.get("amount"),
            sales_stage = form.data.get("sales_stage"),
            probability = form.data.get("probability"),
            next_step = form.data.get("next_step"),
            description = form.data.get("description"),
            expected_close_date = form.data.get("expected_close_date"),
            lead_source = form.data.get("lead_source"),
            lead = LeadsData.objects.get(pk = form.data.get("lead")),
            date = now_date,
            assigned_to = get_user_model().objects.get(username=username)

        )
        contact_details.save()

        return redirect("message")
        
        # return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = OpportunityForm()
    return render(request, "sales_tracker/create_opportunity.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})

def Create_quote_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = QuoteForm(request.POST)
        
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        username = request.user.username
        quote_details = QuotesData(
            title = form.data.get("title"),
            valid_until = form.data.get("valid_until"),
            approval_status = form.data.get("approval_status"),
            opportunity = OpportunityData.objects.get(pk = form.data.get("opportunity")),
            quote_stage = form.data.get("quote_stage"),
            invoice_status = form.data.get("invoice_status"),
            approval_issues_description = None if form.data.get("approval_issues_description") == "" else form.data.get("approval_issues_description"),
            lead_source = form.data.get("lead_source"),
            account = form.data.get("account"),
            contact = form.data.get("contact"),
            billing_address = form.data.get("billing_address"),
            shipping_address = form.data.get("shipping_address"),
            total = form.data.get("total"),
            discount = form.data.get("discount"),
            sub_total = form.data.get("sub_total"),
            shipping = form.data.get("shipping"),
            shipping_tax = form.data.get("shipping_tax"),
            tax = form.data.get("tax"),
            grandtotal = form.data.get("grandtotal"),
            date = now_date,
            assigned_to = get_user_model().objects.get(username=username)

        )
        quote_details.save()

        return redirect("message")
        
        # return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = QuoteForm()
    return render(request, "sales_tracker/create_quote.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})



from django.views import View
from .forms import SortForm

class MiningsView(View):
    def get(self, request):
        form = SortForm()
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        datas = MiningData.objects.filter(date = now_date)
        return render(request, "sales_tracker/view_data.html", {"form":form, "datas": datas})
    def post(self, request):
        form = SortForm(request.POST)
        time = form.data.get("select")
        if time == "week":
            from datetime import date, timedelta
            today = date.today()
            days_ago = today - timedelta(days=7)
            datas = MiningData.objects.filter(date__lte = today, date__gte = days_ago )
        elif time == "month":
            from datetime import date, timedelta
            today = date.today()
            days_ago = today - timedelta(days=30)
            
            datas = MiningData.objects.filter(date__lte = today, date__gte = days_ago )
        elif time == "day":
            from datetime import date, timedelta
            today = date.today()
            datas = MiningData.objects.filter(date = today)
        return render(request, "sales_tracker/view_data.html", {"form":form, "datas": datas})
    





# class LeadView(ListView):
#     template_name = "sales_tracker/data2.html"
#     model = LeadsData
#     context_object_name = "lead_data"

#     def get_queryset(self):
#         base_query =  super().get_queryset()
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         data = base_query.filter(date = f"{now_date}")
#         return data

#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         request = self.request
#         user = request.user
#         utc_login_time = user.last_login
#         elapsed_time = timer(utc_login_time)
#         context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         todays_lead = LeadsData.objects.filter(date = now_date)
#         today_lead_count = todays_lead.count()
#         context["lead_count"] = today_lead_count
#         return context
    

class BaseListView(ListView):
    template_name = "sales_tracker/data.html"
    model = None
    context_object_name = "data_list"
    context_count_name = None
    def get_queryset(self):
        base_query =  super().get_queryset()
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        data = base_query.filter(date = f"{now_date}")
        return data
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        todays_lead = LeadsData.objects.filter(date = now_date)
        today_lead_count = todays_lead.count()
        context[self.context_count_name] = today_lead_count
        return context
    
    
class DataView(BaseListView):
    template_name = "sales_tracker/data.html"
    model = MiningData
    count_context_name = 'mining_count'    

class LeadView(BaseListView):
    template_name = "sales_tracker/data.html"
    model = LeadsData
    count_context_name = 'lead_count'
class OpportunityView(BaseListView):
    template_name = "sales_tracker/data.html"
    model = OpportunityData
    count_context_name = 'opportunity_count'







# def Tocall(request):
#     context = {}
#     user = request.user
#     utc_login_time = user.last_login
#     elapsed_time = timer(utc_login_time)
#     formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
#     now_date_time = datetime.datetime.now()
#     now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}" 
#     orgs = ContactData.objects.filter(date=now_date) 
#     orgs_list = [orgsN.organization for orgsN in orgs]
#     context['orgs_list'] = orgs_list
#     context['timer'] = formated_timer

#     return render(request, "sales_tracker/data2.html", context)


class Tocall(TemplateView):
    template_name = "sales_tracker/data2.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}" 
        orgs = ContactData.objects.filter(date=now_date) 
        orgs_list = [orgsN.organization for orgsN in orgs]
        context['orgs_list'] = orgs_list
        return context



def Tocall_detail(request, pk):
    context = {}
    context['pk'] = pk
    user = request.user
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    print("hwllo")
    mining_data = get_object_or_404(MiningData, organisation_name=pk)
    # Retrieve the related ContactData entries

    contact_data_list = ContactData.objects.filter(organization=mining_data,date=now_date)
    
    # Prepare the data to be sent to the template       
    context = {
        'mining_data': mining_data,
        'contact_data_list': contact_data_list
    }
    # contact = ContactData.objects.get(organization=pk)
    # context['contact'] = contact
    return render(request, "sales_tracker/Detailtocall.html", context)

def DetailCalling(request, pk):
    context = {}
    context['pk'] = pk
    mining_data = get_object_or_404(MiningData, organisation_name=pk)
    context = {
        'mining_data': mining_data
    }

    return render(request,"sales_tracker/detailcalling.html",context)

    pass








# def get_call_center_data():
#     # Connect to the external MySQL database
#     connection = pymysql.connect(
#         host='localhost',        # Replace with your database host
#         user='root',    # Replace with your database username
#         password='Pj@123456',# Replace with your database password
#         database='CallCenter',           # Replace with your database name
#         port=3306                # Replace with your database port if different
#     )

#     try:
#         with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#             # Execute an SQL query
#             sql = "SELECT * FROM CallingAgent"  # Replace with your SQL query
#             cursor.execute(sql)

#             # Fetch all the rows from the result
#             result = cursor.fetchall()
#             return result
#     finally:
#         connection.close()

# def call_center_view(request):
#     context = {}
#     data = get_call_center_data()
#     context['data'] = data
#     return render(request, "sales_tracker/call_center.html",context)
#     # return JsonResponse({'data': data})



def get_calling_agents(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM CallingAgent")
        rows = cursor.fetchall()
        
        # Optionally, you can format the data as needed
        data = [
            {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'contact': row[3],
                'call_date': row[4]
            }
            for row in rows
        ]
        context['data'] = data
        return render(request, "sales_tracker/call_center.html",context)
  



def Attendence(request):    
    # generate_bar_chart()
    context = {}
    user = request.user
    days = TotalDays(request)
    u = RegisterUser.objects.get(email=user)
    context['u'] = u.username
    context['days'] = days
    return render(request, "sales_tracker/MinerAttendence.html",context)


def attendance_list(request):
    attendances = AttendanceRecord.objects.all()
    return render(request, "sales_tracker/ADMIN.html", {'attendances': attendances})



class Admin(TemplateView):
    template_name = "sales_tracker/admin.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attendances = AttendanceRecord.objects.all()
        att = Att_perct()
        late = Late_perct()
        context['admin_message'] = "Welcome to the Admin Page"
        context['attendances'] = attendances
        context['att'] = att
        context['late'] = Late_perct 
        return context

class Admin_reports(TemplateView):
    template_name = "sales_tracker/reports.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        return context


class MinerActivity(TemplateView):
    template_name = "sales_tracker/MinerActivity.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Mining_Count()
        Miner = Profile.objects.filter(branch = "miner")
        MinerC = Profile.objects.filter(branch = "miner").count()
        Total_Mining = MiningData.objects.count()
        Exp_Mining =   AttendanceRecord.objects.values('date').distinct().count()
        context['Miner'] = Miner
        context['Total_Mining'] = Total_Mining
        context['Exp_Mining'] = Exp_Mining*MinerC*40
        # context['MinerC'] = MinerC
        return context
    



class LeadsActivity(TemplateView):
    template_name = "sales_tracker/LeadsActivity.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Leads_Count()
        Agents = Profile.objects.filter(branch = "agent")
        AgentsC = Profile.objects.filter(branch = "agent").count()
        Total_Leads = LeadsData.objects.count()
        Exp_Leads =   AttendanceRecord.objects.values('date').distinct().count()
        context['Agents'] = Agents
        context['Total_Leads'] = Total_Leads
        context['Exp_Leads'] = Exp_Leads*AgentsC*4
        # context['MinerC'] = MinerC
        return context
    
