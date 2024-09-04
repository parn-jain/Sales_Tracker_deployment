import os
import sys
from users.models import  RegisterUser
import django
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, "..")
sys.path.append(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stpa.settings'
from django.db import connection
import matplotlib.pyplot as plt
def fetch_records():
    with connection.cursor() as cursor:
        # Execute a raw SQL query to fetch records data
        cursor.execute("select * from users_attendancerecord")
        # Fetch all rows from the result set
        records = cursor.fetchall()
        print(type(records))
        # print(records)

        # Process the records data
        for record in records:
            print(record)


def generate_bar_chart(request):
    users = request.user
    u = RegisterUser.objects.get(email=users)
    u = u.id
    print("this print statement is in bar chart functino in analysis.py")
    with connection.cursor() as cursor:
        cursor.execute("SELECT status, COUNT(*) FROM users_attendancerecord where user_id = %s GROUP BY status;",[u])
        data = cursor.fetchall()
    
    categories = [row[0] for row in data]
    counts = [row[1] for row in data]
        # categories, counts = zip(*data)
    plt.figure(figsize=(10, 6))

# Set the outer background color (the entire figure)
    plt.gcf().set_facecolor('#262626')

    # Create the bar chart with custom colors
    bar_colors = ['green', 'yellow', 'red']
    plt.bar(categories, counts, color=bar_colors)

    # Get the current axis
    ax = plt.gca()
    
    # Set the inner background color (the plot area)
    ax.set_facecolor('#262626')

    # Customize the grid (if needed, you can also remove it)
    ax.grid(False)

    # Set the labels and title with white text color
    plt.xlabel('Attendance Status', color='white')
    plt.ylabel('Number of Days', color='white')
    plt.title('Attendance Status Overview', color='white')

    # Customize the ticks color
    plt.xticks(color='white')
    plt.yticks(color='white')

    # Remove the borders of the graph
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')

    # Ensure the background is completely covered
    ax.patch.set_alpha(1.0)

    # Save the figure with the customizations
    plt.savefig('static/bar_chart.png', bbox_inches='tight', facecolor='#262626')





def generate_bar_chart2(id):
    print("this print statement is in bar chart functino in analysis.py")
    with connection.cursor() as cursor:
        cursor.execute("SELECT status, COUNT(*) FROM users_attendancerecord where user_id = %s GROUP BY status;",[id])
        data = cursor.fetchall()
    
    categories = [row[0] for row in data]
    counts = [row[1] for row in data]
        # categories, counts = zip(*data)
    plt.figure(figsize=(10, 6))

# Set the outer background color (the entire figure)
    plt.gcf().set_facecolor('#262626')

    # Create the bar chart with custom colors
    bar_colors = ['green', 'yellow', 'red']
    plt.bar(categories, counts, color=bar_colors)

    # Get the current axis
    ax = plt.gca()
    
    # Set the inner background color (the plot area)
    ax.set_facecolor('#262626')

    # Customize the grid (if needed, you can also remove it)
    ax.grid(False)

    # Set the labels and title with white text color
    plt.xlabel('Attendance Status', color='white')
    plt.ylabel('Number of Days', color='white')
    plt.title('Attendance Status Overview', color='white')

    # Customize the ticks color
    plt.xticks(color='white')
    plt.yticks(color='white')

    # Remove the borders of the graph
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')

    # Ensure the background is completely covered
    ax.patch.set_alpha(1.0)

    # Save the figure with the customizations
    plt.savefig('static/bar_chart.png', bbox_inches='tight', facecolor='#262626')    



def TotalDays(request):
    users = request.user
    u = RegisterUser.objects.get(email=users)
    u = u.id
    with connection.cursor() as cursor:
        cursor.execute("select count(distinct date) from users_attendancerecord;")
        Tdays = cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("select count(distinct date) from users_attendancerecord where status='Present' and user_id =%s;",[u])
        Pdays= cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("select count(distinct date) from users_attendancerecord where status='Absent'and user_id =%s;",[u])
        Adays= cursor.fetchone()
    with connection.cursor() as cursor:
        cursor.execute("select count(distinct date) from users_attendancerecord where status='Late'and user_id =%s;",[u])
        Ldays= cursor.fetchone()
    days ={'Tdays':Tdays[0],
           'Pdays' : Pdays[0],
           'Adays':Adays[0],
           'Ldays':Ldays[0]}
    return days

