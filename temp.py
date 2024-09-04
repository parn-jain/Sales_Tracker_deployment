import os
import django
from django.utils import timezone
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
from django.db.models import Count
# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stpa.settings')
from django.db import connection
# Setup Django
django.setup()

# Now you can import your models
from users.models import RegisterUser, Profile, AttendanceRecord, DaysStatus
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



def EachMinerTarget(id):
    with connection.cursor() as cursor:
        cursor.execute("""
        select A.status, COUNT(*) as count 
        from users_attendancerecord as A
        left join users_daysstatus as D
        ON D.date = A.date
        where A.user_id = %s and D.status = 'Working Day'
        group by A.status;
        """,[id])
        data = cursor.fetchall()
        print(data) 
        target = sum(row[1] for row in data)*40
        print(target)
    acchieved = MiningData.objects.filter(created_by_id = id).count()
    print(acchieved) 
    each_miner = {"Target":target, "Acchieve":acchieved}
    return each_miner 
    # wd = DaysStatus.objects.filter(status='Working Day')
    # attendence = AttendanceRecord.objects.filter(user_id = id)
    # print(attendence)



def Time_worked():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT 
        A.date,
        SUM(TIMESTAMPDIFF(
            SECOND, 
            CONCAT(A.date, ' ', A.check_in_time), 
            IFNULL(CONCAT(A.date, ' ', A.check_out_time), NOW())
        ))
        AS time_worked
        FROM 
        users_attendancerecord as A
        left join users_daysstatus as D
        on A.date = D.date
        where D.status = 'Working Day'
        group by A.date;
        """)
        data = cursor.fetchall()
        dates = []
        hours_worked = []
        for row in data:
            date,total_sec = row
            hours = total_sec / 3600
            dates.append(date)
            hours_worked.append(hours)
            print(date,hours)
            print(' ')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Set face color
        plt.gcf().set_facecolor('#262626')
        ax.set_facecolor('#262626')
        
        # Plotting the line graph
        ax.plot(dates, hours_worked, marker='o', linestyle='-', color='b')
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Hours Worked', color='white')
        ax.set_title('Hours Worked vs. Date', color='white')
        
        # Beautify the plot
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        plt.tight_layout()
        plt.show()
# Time_worked()


# def DailyAttendence():
    # now_date_time = datetime.datetime.now()
    # now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"



def  ToalEmployees():
    c = RegisterUser.objects.count()
    print(c)
    return c


def DailyAttendance():
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    # now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT A.status, count(*) as count  
            FROM users_attendancerecord AS A
            LEFT JOIN users_daysstatus AS D ON A.date = D.date
            WHERE A.date = %s
            group by A.status;
        """, [now_date])

        data = cursor.fetchall()
    if(DaysStatus.objects.filter(date = now_date).values('status')[0]['status']=='Working Day'):
        x = ToalEmployees()
        y = data[0][1]
        fig,ax = plt.subplots(figsize = (4.5,4))
        plt.gcf().set_facecolor('#262626')
        ax.set_facecolor('#262626')
        sizes = [x,y]
        labels = ['Total', 'Present']
        colors = ['#ff9999','#66b3ff']

        wedge, texts, autotexts = ax.pie(sizes,labels = labels,colors=colors, autopct=lambda p: f'{int(p * sum(sizes) / 100)}', 
                                         startangle=140, wedgeprops=dict(width=0.4),textprops=dict(color='white') )
        plt.setp(autotexts, size=10, weight="bold",)
        plt.setp(texts, size=12, color='white')
        ax.set_title("Total VS Present", color='white')
        plt.show()
        # plt.savefig('static/DailyAttendence.png')
    print(data)
    # return data

# DailyAttendance()
def temp():
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    print(DaysStatus.objects.filter(date = now_date).values('status')[0]['status'])
    # return 
# temp()

end_date = timezone.now().date()
start_date = end_date - timedelta(days=6)

def generate_date_range(start_date, end_date):
    """Generate a list of dates from start_date to end_date."""
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

def Productivity():
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)

    # Generate the full date range
    date_range = generate_date_range(start_date, end_date)

    # Fetch the counts for the existing dates
    data = (
        MiningData.objects.filter(date__range=[start_date, end_date])
        .values('date')
        .annotate(count=Count('created_by_id'))
        .order_by('date')
    )

    # Convert the fetched data to a dictionary for easy lookup
    data_dict = {entry['date']: entry['count'] for entry in data}

    # Include dates with a count of 0
    result = [{'date': d, 'count': data_dict.get(d, 0)} for d in date_range]
    target_mining = 100
    dates = [entry['date'] for entry in result]
    counts = [entry['count'] for entry in result]
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.gcf().set_facecolor('#262626')
    ax.set_facecolor('#262626')

    ax.plot(dates, counts, marker='o', linestyle='-', color='#66b3ff', label="Number of Minings")
    ax.axhline(y=target_mining, color='red', linestyle='--', linewidth=2, label=f"Target Mining ({target_mining})")


    # Beautify the chart
    ax.set_xlabel('Date', color='white')
    ax.set_ylabel('Number of Minings', color='white')
    ax.set_title('Number of Minings vs. Days', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Format the x-axis to display dates properly
    ax.xaxis.set_major_formatter(plt.FixedFormatter(dates))
    plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability

    # Show grid
    ax.grid(True, linestyle='--', color='#555555')
    plt.show()


Productivity()