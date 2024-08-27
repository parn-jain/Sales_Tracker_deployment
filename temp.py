import os
import django
from django.utils import timezone
from datetime import timedelta
# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stpa.settings')

# Setup Django
django.setup()

# Now you can import your models
from users.models import RegisterUser, Profile, AttendanceRecord
from sales_tracker.models import MiningData 

# Perform your ORM operations
attendence_percentage = []
late = []
a = RegisterUser.objects.count()
Total_att = a*7
TWend_date = timezone.now().date()
TWstart_date = TWend_date - timedelta(days=6)
a = RegisterUser.objects.count()
# print(a)
OWend_date = timezone.now().date() - timedelta(days=6) 
OWstart_date = TWend_date - timedelta(days=12)

TWattendance = AttendanceRecord.objects.filter(date__range=[TWstart_date, TWend_date],status__in=['Present', 'Late']).count()
# print(TWattendance)
OWattendance = AttendanceRecord.objects.filter(date__range=[OWstart_date, OWend_date],status__in=['Present', 'Late']).count()
attendence_percentage.append((OWattendance/Total_att)*100)
attendence_percentage.append((TWattendance/Total_att)*100)
perct_change = ((attendence_percentage[1]- attendence_percentage[0])/attendence_percentage[0])*100
# print((OWattendance/Total_att)*100)
print(attendence_percentage)
print(perct_change)
# print("Hello")



# late


TWlate= AttendanceRecord.objects.filter(date__range=[TWstart_date, TWend_date],status__in=['Late']).count()
OWLate = AttendanceRecord.objects.filter(date__range=[OWstart_date, OWend_date],status__in=['Late']).count()
late.append((OWLate/Total_att)*100)
late.append((TWlate/Total_att)*100)
perct_changeLate = ((late[1]- attendence_percentage[0])/late[0])*100
print(late)
print(perct_changeLate)



#Reporting

MinerC = Profile.objects.filter(branch = "miner").count()
Miner = Profile.objects.filter(branch = "miner")
print(Miner)
MinerId = []
miner_usernames = [miner.user.username for miner in Miner]
print(miner_usernames)
print(MiningData.objects.count())


# for i in range(0,MinerC):
#     MinerId.append(Miner[i].user_id)
#     k = RegisterUser.objects.get(id = MinerId).username
#     print(k)


