from django.db import models
from users.models import RegisterUser
from django.conf import settings





class CallingAgent(models.Model):
    calling_agent_id = models.AutoField(primary_key=True)
    calling_agent_name = models.CharField(max_length=50)
    calling_agent_email = models.EmailField(max_length=50)
    calling_agent_contact = models.CharField(max_length=15)

    class Meta:
        managed = False  # Prevent Django from managing the table (no migrations)
        db_table = 'CallingAgent' 
    def __str__(self):
        return f"{self.calling_agent_id}"

#have to change this database 

# Create your models here.

class MiningData(models.Model):
    organisation_name = models.CharField( max_length=50, primary_key=True)
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_address = models.TextField()
    customer_contact_number = models.CharField(max_length=15)
    customer_mobile_number = models.CharField(max_length=15)
    customer_email = models.EmailField()
    company_revenue = models.CharField( max_length=50)
    company_emp_size = models.IntegerField()
    customer_offering = models.CharField(max_length=30)
    competition_of_AT = models.CharField(max_length=50)
    stock_market_registered = models.CharField(max_length=20)
    influncer = models.BooleanField()
    desition_maker = models.BooleanField()
    IT_spending_budget = models.CharField(max_length=30)
    source_of_data_mining = models.CharField(max_length=50)
    date = models.DateField()
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1, null = True, blank = True)
    

    def __str__(self):
        return f"{self.organisation_name}"
    
class ContactData(models.Model):
    first_name = models.CharField( max_length=50)
    last_name = models.CharField( max_length=50)
    email_id = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    job_title = models.CharField( max_length=50)
    address = models.TextField( )
    date = models.DateField(default="2000-10-10")
    organization = models.ForeignKey(MiningData, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1)
    # calling_agent = foreign key to agent profile to which call is assigned
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class LeadsData(models.Model):
    lead_name = models.CharField( max_length=50)
    first_name = models.CharField( max_length=50)
    last_name = models.CharField( max_length=50)
    email_id = models.EmailField()
    contact_number = models.IntegerField()
    job_title = models.CharField( max_length=50)
    address = models.TextField( )
    date = models.DateField(default="2000-10-10")
    contact_link = models.ForeignKey(ContactData, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1)

    def __str__(self):
        return f"{self.lead_name}"
    
class OpportunityData(models.Model):
    opportunity_name =  models.CharField( max_length=50)
    amount = models.IntegerField()
    sales_stage = models.CharField(max_length=50, choices=(
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('needs', 'Needs'),
        ('value proposition', 'Value Proposition'),
        ('identifying decision makers', 'Identifying Decision Makers'),
        ('preception Analysis', 'Perception Analysis'),
        ('Proposal/price quote', 'Proposal/Prise Quote'),
        ('negotiation/review', 'Negotiation/Review'),
        ('closed won', 'Closed Won'),
        ('closed lost', 'Closed lost'),
    ))
    probability = models.IntegerField()
    next_step = models.CharField(max_length=50)
    description = models.TextField()
    expected_close_date = models.DateField()
    lead_source = models.CharField(max_length=50)
    date = models.DateField(default="2000-10-10")
    lead = models.ForeignKey(LeadsData, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1)

class QuotesData(models.Model):
    title = models.CharField(max_length= 50)
    valid_until = models.DateField()
    approval_status = models.CharField(max_length=50, choices=(
        ('approved', 'Approved'),
        ('not approved', 'Not Approved'),
    ))

    opportunity = models.ForeignKey(OpportunityData, on_delete=models.CASCADE)
    quote_stage = models.CharField(max_length=50, choices=(
        ('draft', 'Draft'),
        ('negotiation', 'Negotiation'),
        ('delivered', 'delivered'),
        ('on hold', 'On Hold'),
        ('confirmed', 'Confirmed'),
        ('closed Accepted', 'Closed Accepted'),
        ('closed lost', 'Closed Lost'),
        ('closed dead', 'Closed Dead'),
    ))
    invoice_status = models.CharField(max_length=50, choices=(
        ('not invoiced', 'Not Invoiced'),
        ('invoiced', 'Invoiced'),
    ))
    approval_issues_description = models.TextField(null=True, blank=True)

    lead_source = models.CharField(max_length= 50)
    account = models.CharField(max_length= 50)
    contact = models.CharField(max_length= 50)
    billing_address = models.TextField()
    shipping_address = models.TextField()

    total = models.CharField(max_length=50)
    discount = models.CharField(max_length=50)
    sub_total = models.CharField(max_length=50)
    shipping = models.CharField(max_length=50)
    shipping_tax = models.CharField(max_length=50)
    tax = models.CharField(max_length=50)
    grandtotal = models.CharField(max_length=50)
    date = models.DateField(default="2000-10-10")
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1)