import os
import sys
import numpy as np
import datetime
import plotly.graph_objs as go
from plotly.offline import plot
import matplotlib.pyplot as plt
from django.db.models import Count
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, "..")
sys.path.append(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stpa.settings'
from users.models import RegisterUser,AttendanceRecord, Profile, DaysStatus
from sales_tracker.models import MiningData,LeadsData
from django.db import connection
from django.utils import timezone
from datetime import timedelta
import numpy as np
from scipy.interpolate import make_interp_spline

end_date = timezone.now().date()
start_date = end_date - timedelta(days=6)

# Query the data
week_attendance = AttendanceRecord.objects.filter(date__range=[start_date, end_date])


from collections import defaultdict

# Initialize dictionary to hold data
data = defaultdict(lambda: {'Present': 0, 'Absent': 0, 'Late': 0})

for record in week_attendance:
    date = record.date
    status = record.status
    data[date][status] += 1

# Convert the data into lists for plotting
dates = sorted(data.keys())
present_counts = [data[date]['Present'] for date in dates]
absent_counts = [data[date]['Absent'] for date in dates]
late_counts = [data[date]['Late'] for date in dates]  # New line for 'Late' status


x = np.arange(len(dates))
width = 0.25  # Width of the bars
def admin_attendence_graph():
    print("this is in admin attendece function")
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.gcf().set_facecolor('#262626')
    ax = plt.gca()
    ax.set_facecolor('#262626')

    
    ax.bar(x - width, present_counts, width, label='Present', color='#1f77b4')
    ax.bar(x, absent_counts, width, label='Absent', color='#ff7f0e')
    ax.bar(x + width, late_counts, width, label='Late', color='#2ca02c')

    # ax.bar(dates, present_counts, label='Present')
    # ax.bar(dates, absent_counts, bottom=present_counts, label='Absent')
    # ax.bar(dates, late_counts, bottom=[p + a for p, a in zip(present_counts, absent_counts)], label='Late')  # Stacked bar for 'Late'

    ax.set_xlabel('Date')
    ax.set_ylabel('Total Number of Employees')
    ax.set_title('Employee Attendance for Initial 7 Days')
    ax.set_xticks(x)
    ax.set_xticklabels([date.strftime('%Y-%m-%d') for date in dates], rotation=45)
    ax.legend(title='Status')
    # ax.set_xticklabels(dates, rotation=45)
    plt.tight_layout()
    plt.savefig('static/admin_attendence.png', bbox_inches='tight', facecolor='#262626')
    
def admin_attendance_graph(request):
    print("This is in admin attendance function")

    # Create a Plotly figure
    fig = go.Figure()

    # Add bars for 'Present'
    fig.add_trace(go.Bar(
        x=dates, 
        y=present_counts, 
        name='Present', 
        marker_color='#1f77b4',
        offsetgroup=0  # Position group
    ))

    # Add bars for 'Absent'
    fig.add_trace(go.Bar(
        x=dates, 
        y=absent_counts, 
        name='Absent', 
        marker_color='#ff7f0e',
        offsetgroup=1  # Position group
    ))

    # Add bars for 'Late'
    fig.add_trace(go.Bar(
        x=dates, 
        y=late_counts, 
        name='Late', 
        marker_color='#2ca02c',
        offsetgroup=2  # Position group
    ))

    # Customize the layout
    fig.update_layout(
        title='Employee Attendance for Initial 7 Days',
        xaxis_title='Date',
        yaxis_title='Total Number of Employees',
        barmode='group',  # This ensures that the bars are grouped side by side
        plot_bgcolor='#e0eaf6',
        paper_bgcolor='#e0eaf6',
        font=dict(color='black'),
        xaxis=dict(
            tickmode='array',
            tickvals=dates,
            tickformat='%Y-%m-%d'
        ),
        yaxis=dict(gridcolor='#555555'),
        legend=dict(title='Status')
    )

    # Render the Plotly figure to HTML and save it as an HTML file
    graph_html = plot(fig, output_type='div')
    return graph_html


# def admin_attendance_graph(request):
#     with connection.cursor() as cursor:
#         cursor.execute("""
#         SELECT 
#         A.date,
#         SUM(TIMESTAMPDIFF(
#             SECOND, 
#             CONCAT(A.date, ' ', A.check_in_time), 
#             IFNULL(CONCAT(A.date, ' ', A.check_out_time), NOW())
#         ))
#         AS time_worked
#         FROM 
#         users_attendancerecord as A
#         LEFT JOIN users_daysstatus as D
#         ON A.date = D.date
#         WHERE 
#         D.status = 'Working Day' 
#         AND A.date BETWEEN %s AND %s
#         GROUP BY A.date;
#         """, [start_date, end_date])
        
#         data = cursor.fetchall()
#         dates = []
#         hours_worked = []
#         for row in data:
#             date, total_sec = row
#             hours = total_sec / 3600
#             dates.append(date)
#             hours_worked.append(hours)
#     print("This is in admin attendance function")

#     # Create a Plotly figure
#     fig = go.Figure()

#     # Add bars for 'Present'
#     fig.add_trace(go.Bar(
#         x=dates, 
#         y=present_counts, 
#         name='Present', 
#         marker_color='#1f77b4',
#         offsetgroup=0  # Position group
#     ))

#     # Add bars for 'Absent'
#     fig.add_trace(go.Bar(
#         x=dates, 
#         y=absent_counts, 
#         name='Absent', 
#         marker_color='#ff7f0e',
#         offsetgroup=1  # Position group
#     ))

#     # Add bars for 'Late'
#     fig.add_trace(go.Bar(
#         x=dates, 
#         y=late_counts, 
#         name='Late', 
#         marker_color='#2ca02c',
#         offsetgroup=2  # Position group
#     ))

#     # Add line for hours worked (secondary y-axis)
#     fig.add_trace(go.Scatter(
#         x=dates,
#         y=hours_worked,
#         mode='lines+markers',
#         line=dict(color='#FFFF00'),
#         marker=dict(size=8),
#         name="Number of hours worked",
#         yaxis="y2"  # Assign to secondary y-axis
#     ))

#     # Customize the layout
#     fig.update_layout(
#         title='Employee Attendance for Initial 7 Days',
#         xaxis_title='Date',
#         yaxis_title='Total Number of Employees',
#         yaxis=dict(
#             title='Total Number of Employees',
#             gridcolor='#555555'
#         ),
#         yaxis2=dict(
#             title='Number of Hours Worked',
#             overlaying='y',
#             side='right',
#             gridcolor='#555555',
#             showgrid=False
#         ),
#         barmode='group',  # Group the bars side by side
#         plot_bgcolor='#262626',
#         paper_bgcolor='#262626',
#         font=dict(color='white'),
#         xaxis=dict(
#             tickmode='array',
#             tickvals=dates,
#             tickformat='%Y-%m-%d'
#         ),
#         legend=dict(title='Status')
#     )

#     # Render the Plotly figure to HTML and save it as an HTML file
#     graph_html = plot(fig, output_type='div')
#     return graph_html






attendence_percentage = []
late = []
a = RegisterUser.objects.count()
Total_att = a*7

TWend_date = timezone.now().date()
TWstart_date = TWend_date - timedelta(days=6)
OWend_date = timezone.now().date() - timedelta(days=6) 
OWstart_date = TWend_date - timedelta(days=12)
def Att_perct():
    TWattendance = AttendanceRecord.objects.filter(date__range=[TWstart_date, TWend_date],status__in=['Present', 'Late']).count()

    OWattendance = AttendanceRecord.objects.filter(date__range=[OWstart_date, OWend_date],status__in=['Present', 'Late']).count()
    attendence_percentage.append((OWattendance/Total_att)*100)
    attendence_percentage.append((TWattendance/Total_att)*100)
    perct_change = ((attendence_percentage[1]- attendence_percentage[0])/attendence_percentage[0])*100

    print(attendence_percentage)
    print(perct_change)
    return perct_change

def Late_perct():
    TWlate= AttendanceRecord.objects.filter(date__range=[TWstart_date, TWend_date],status__in=['Late']).count()
    OWLate = AttendanceRecord.objects.filter(date__range=[OWstart_date, OWend_date],status__in=['Late']).count()
    late.append((OWLate/Total_att)*100)
    late.append((TWlate/Total_att)*100)
    perct_changeLate = ((late[1]- attendence_percentage[0])/late[0])*100
    return perct_changeLate 
    print(late)
    print(perct_changeLate)








def Mining_Count():
    Total_Mining = MiningData.objects.count()
    Exp_M = AttendanceRecord.objects.values('date').distinct().count()
    MinerC = Profile.objects.filter(branch = "miner").count()
    Exp_Mining = Exp_M*MinerC*40

    # Data
    labels = ['Total Mining', 'Expected Mining']
    sizes = [Total_Mining, Exp_Mining]
    colors = ['#008080','#1E2A38' ]

    # Plot
    fig, ax = plt.subplots(figsize=(4.5, 4), subplot_kw=dict(aspect="equal"))
    plt.gcf().set_facecolor('#e0eaf6')
    ax.set_facecolor('#e0eaf6')

    # Create a pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4),textprops=dict(color='white'))

    # Beautify the plot
    plt.setp(autotexts, size=10, weight="bold",color='black')
    plt.setp(texts, size=12, color='black')
    ax.set_title("Mining vs Expected Mining", color='black')

    # Show plot
    plt.savefig('static/Mining_Count.png')

def Leads_Count():
    Total_Leads = LeadsData.objects.count()
    Exp_L = AttendanceRecord.objects.values('date').distinct().count()
    AgentC = Profile.objects.filter(branch = "agent").count()
    Exp_Leads = Exp_L*AgentC*4

    # Data
    labels = ['Total Mining', 'Expected Mining']
    sizes = [Total_Leads, Exp_Leads]
    colors = ['#ff9999','#66b3ff']

    # Plot
    fig, ax = plt.subplots(figsize=(4.5, 4), subplot_kw=dict(aspect="equal"))
    plt.gcf().set_facecolor('#262626')
    ax.set_facecolor('#262626')

    # Create a pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4),textprops=dict(color='white'))

    # Beautify the plot
    plt.setp(autotexts, size=10, weight="bold",)
    plt.setp(texts, size=12, color='white')
    ax.set_title("Leads vs Expected Leads", color='white')

    # Show plot
    plt.savefig('static/Leads_Count.png')




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
    labels = [f'target:{target}', f'acchieved:{acchieved}']
    sizes = [target, acchieved]
    colors = ['#ff9999','#66b3ff']

    # Plot
    fig, ax = plt.subplots(figsize=(4.5, 4), subplot_kw=dict(aspect="equal"))
    plt.gcf().set_facecolor('#262626')
    ax.set_facecolor('#262626')

    # Create a pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4),textprops=dict(color='white'))

    # Beautify the plot
    plt.setp(autotexts, size=10, weight="bold",)
    plt.setp(texts, size=12, color='white')
    ax.set_title("Mining vs Expected Mining", color='white')

    # Show plot
    plt.savefig('static/EachMinerTarget.png')

    return each_miner 
    # wd = DaysStatus.objects.filter(status='Working Day')
    # attendence = AttendanceRecord.objects.filter(user_id = id)
    # print(attendence)





def Time_worked(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)

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
        LEFT JOIN users_daysstatus as D
        ON A.date = D.date
        WHERE
        D.status = 'Working Day' 
        AND A.date BETWEEN %s AND %s
        GROUP BY A.date;
        """, [start_date, end_date])
        
        data = cursor.fetchall()
        dates = []
        hours_worked = []
        for row in data:
            date, total_sec = row
            hours = total_sec / 3600
            dates.append(date)
            hours_worked.append(hours)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=hours_worked,
            mode='lines+markers',
            line=dict(color='#FFFF00'),
            marker=dict(size=8),
            name="Number of hours worked"
        ))

        fig.update_layout(
            title="Date VS Number of hours worked",
            xaxis_title='Date',
            yaxis_title='Number of hours',
            plot_bgcolor='#262626',
            paper_bgcolor='#262626',
            font=dict(color='White'),
            xaxis=dict(
                tickmode='array',
                tickvals=dates,
                tickformat='%Y-%m-%d'
            ),
            yaxis=dict(gridcolor="black")
        )
        graph_html = plot(fig, output_type='div')
        return graph_html
    



# def Time_worked():
#     with connection.cursor() as cursor:
#         cursor.execute("""
#         SELECT 
#         A.date,
#         SUM(TIMESTAMPDIFF(
#             SECOND, 
#             CONCAT(A.date, ' ', A.check_in_time), 
#             IFNULL(CONCAT(A.date, ' ', A.check_out_time), NOW())
#         ))
#         AS time_worked
#         FROM 
#         users_attendancerecord as A
#         left join users_daysstatus as D
#         on A.date = D.date
#         where D.status = 'Working Day'
#         group by A.date;
#         """)
#         data = cursor.fetchall()
#         dates = []
#         hours_worked = []
#         for row in data:
#             date,total_sec = row
#             hours = total_sec / 3600
#             dates.append(date)
#             hours_worked.append(hours)
#             print(date,hours)
#             print(' ')
            
#         fig, ax = plt.subplots(figsize=(10, 6))
        
#         # Set face color
#         plt.gcf().set_facecolor('#262626')
#         ax.set_facecolor('#262626')
        
#         # Plotting the line graph
#         ax.plot(dates, hours_worked, marker='o', linestyle='-', color='b')
#         ax.set_xlabel('Date', color='white')
#         ax.set_ylabel('Hours Worked', color='white')
#         ax.set_title('Hours Worked vs. Date', color='white')
        
#         # Beautify the plot
#         plt.xticks(rotation=45, color='white')
#         plt.yticks(color='white')
#         plt.tight_layout()
#         plt.savefig('static/Time_worked.png')

# def Time_worked(request):
#     with connection.cursor() as cursor:
#         cursor.execute("""
#         SELECT 
#         A.date,
#         SUM(TIMESTAMPDIFF(
#             SECOND, 
#             CONCAT(A.date, ' ', A.check_in_time), 
#             IFNULL(CONCAT(A.date, ' ', A.check_out_time), NOW())
#         ))
#         AS time_worked
#         FROM 
#         users_attendancerecord as A
#         left join users_daysstatus as D
#         on A.date = D.date
#         where D.status = 'Working Day'
#         group by A.date;
#         """)
#         data = cursor.fetchall()
#         dates = []
#         hours_worked = []
#         for row in data:
#             date,total_sec = row
#             hours = total_sec / 3600
#             dates.append(date)
#             hours_worked.append(hours)
#             print(date,hours)
#             print(' ')
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(
#             x = dates,
#             y = hours_worked,
#             mode = 'lines + markers',
#             line = dict(color = '#FFFF00'),
#             marker = dict(size = 8),
#             name = "Number of hours worked"
#         ))

#         fig.update_layout(
#             title = "Date VS No of hours",
#             xaxis_title = 'Date',
#             yaxis_title = 'Number of hours',
#             plot_bgcolor = '#262626',
#             paper_bgcolor = '#262626',
#             font = dict(color = 'White'),
#             xaxis = dict(
#                 tickmode = 'array',
#                 tickvals = dates,
#                 tickformat = '%Y-%m-%d'
#             ),
#             yaxis = dict(gridcolor = "black")
#         )
#         graph_html = plot(fig,output_type = 'div')
#         return graph_html






def  TotalEmployees():
    c = RegisterUser.objects.count()
    print(c)
    return c


# def DailyAttendance():
#     now_date_time = datetime.datetime.now()
#     now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#     # now_date = datetime.datetime.now().strftime('%Y-%m-%d')

#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT A.status, count(*) as count  
#             FROM users_attendancerecord AS A
#             LEFT JOIN users_daysstatus AS D ON A.date = D.date
#             WHERE A.date = %s AND A.status IN ('Present', 'Late')
#             group by A.status;
#         """, [now_date])

#         data = cursor.fetchall()
#         print(data, "this is inside data")
#     if(DaysStatus.objects.filter(date = now_date).values('status')[0]['status']=='Working Day'):
#         x = TotalEmployees()
#         y = data[0][1]
#         fig,ax = plt.subplots(figsize = (4.5,4))
#         plt.gcf().set_facecolor('#262626')
#         ax.set_facecolor('#262626')
#         sizes = [x,y]
#         labels = ['Total', 'Present']
#         colors = ['#ff9999','#66b3ff']

#         wedge, texts, autotexts = ax.pie(sizes,labels = labels,colors=colors, autopct=lambda p: f'{int(p * sum(sizes) / 100)}', 
#                                          startangle=140, wedgeprops=dict(width=0.4),textprops=dict(color='white') )
#         plt.setp(autotexts, size=10, weight="bold",)
#         plt.setp(texts, size=12, color='white')
#         ax.set_title("Total VS Present", color='white')
#         plt.savefig('static/DailyAttendence.png')
#     else:
#         return "Today is holiday"
#         # plt.savefig('static/DailyAttendence.png')

    
#     now_date_time = datetime.datetime.now()
#     yesterdays_date = now_date_time - datetime.timedelta(days = 1)
#     now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#     # now_date = datetime.datetime.now().strftime('%Y-%m-%d')

#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT A.status, count(*) as count  
#             FROM users_attendancerecord AS A
#             LEFT JOIN users_daysstatus AS D ON A.date = D.date
#             WHERE A.date = %s AND A.status IN ('Present', 'Late')
#             group by A.status;
#         """, [yesterdays_date])
#         Ydata = cursor.fetchall()
    
#     print(Ydata)



# def generate_date_range(start_date, end_date):
#     """Generate a list of dates from start_date to end_date."""
#     delta = end_date - start_date
#     return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

# def Productivity():
#     end_date = timezone.now().date()
#     start_date = end_date - timedelta(days=6)

#     # Generate the full date range
#     date_range = generate_date_range(start_date, end_date)

#     # Fetch the counts for the existing dates
#     data = (
#         MiningData.objects.filter(date__range=[start_date, end_date])
#         .values('date')
#         .annotate(count=Count('created_by_id'))
#         .order_by('date')
#     )

#     # Convert the fetched data to a dictionary for easy lookup
#     data_dict = {entry['date']: entry['count'] for entry in data}

#     # Include dates with a count of 0
#     result = [{'date': d, 'count': data_dict.get(d, 0)} for d in date_range]
#     target_mining = 100
#     dates = [entry['date'] for entry in result]
#     counts = [entry['count'] for entry in result]
#     fig, ax = plt.subplots(figsize=(10, 6))
#     plt.gcf().set_facecolor('#262626')
#     ax.set_facecolor('#262626')

#     ax.plot(dates, counts, marker='o', linestyle='-', color='#66b3ff', label="Number of Minings")
#     ax.axhline(y=target_mining, color='red', linestyle='--', linewidth=2, label=f"Target Mining ({target_mining})")


#     # Beautify the chart
#     ax.set_xlabel('Date', color='white')
#     ax.set_ylabel('Number of Minings', color='white')
#     ax.set_title('Number of Minings vs. Days', color='white')
#     ax.tick_params(axis='x', colors='white')
#     ax.tick_params(axis='y', colors='white')

#     # Format the x-axis to display dates properly
#     ax.xaxis.set_major_formatter(plt.FixedFormatter(dates))
#     plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability

#     # Show grid
#     ax.grid(True, linestyle='--', color='#555555')
#     plt.savefig('static/Productivity.png')




def generate_date_range(start_date, end_date):
    """Generate a list of dates from start_date to end_date."""
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

def Productivity(request):
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
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in result]
    counts = [entry['count'] for entry in result]

    # Create a Plotly figure
    fig = go.Figure()

    # Add a line for the actual mining counts
    fig.add_trace(go.Scatter(
        x=dates, 
        y=counts, 
        mode='lines+markers', 
        line=dict(color='#66b3ff'),
        marker=dict(size=8),
        name="Number of Minings"
    ))

    # Add a target mining line
    fig.add_trace(go.Scatter(
        x=dates, 
        y=[target_mining] * len(dates), 
        mode='lines', 
        line=dict(color='red', dash='dash'),
        name=f"Target Mining ({target_mining})"
    ))

    # Customize layout
    fig.update_layout(
        title='Number of Minings vs. Days',
        xaxis_title='Date',
        yaxis_title='Number of Minings',
        plot_bgcolor='#262626',
        paper_bgcolor='#262626',
        font=dict(color='white'),
        xaxis=dict(
            tickmode='array',
            tickvals=dates,
            tickformat='%Y-%m-%d'
        ),
        yaxis=dict(gridcolor='#555555'),
    )

    # Render the Plotly figure to HTML and pass it to the template
    graph_html = plot(fig, output_type='div')
    return graph_html

# Productivity()