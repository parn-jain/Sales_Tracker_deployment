from django.contrib import admin
from .models import MiningData, ContactData, LeadsData, OpportunityData, QuotesData 

# Register your models here.
admin.site.register(MiningData)
admin.site.register(ContactData)
admin.site.register(LeadsData)
admin.site.register(OpportunityData)
admin.site.register(QuotesData)


