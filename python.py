import tkinter as tk
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import mplcursors
import math

applicationsToDo = 2000
deadline = datetime.datetime(2023, 7, 7)
today = datetime.datetime.now()
daysLeft = (deadline-today).days
startDate = datetime.datetime(2023, 5, 15)
appStartDate = datetime.datetime(2023, 5, 20)


daysPassed = (today-startDate).days+1
appDaysPassed = (today-appStartDate).days+1
totalDays = daysPassed+daysLeft
totalAppDays = appDaysPassed+daysLeft

arrAvgApps = []
prfxArrApps = []
arrApps = []


# Function to record the timestamp of a click on a checkbox
def record_click(checkbox):
    with open('clicks.txt', 'a') as f:
        f.write(f'{checkbox},{datetime.datetime.now()}\n')


def convert_to_datetime(number):
    date = datetime.datetime(1970, 1, 1) + datetime.timedelta(int(number))
    seconds = int((number % 1) * 86400)
    time = str(datetime.timedelta(seconds=seconds))
    return f"{date.date()} {time}"


# Function to format the data cursor text
def format_cursor_text(sel):
    x, y = sel.target
    if sel.artist.get_label() == 'Appl':
        y *= 10
    sel.annotation.set_text(f'Time: {convert_to_datetime(x)}\nCount: {y:.0f}')

# def plot_apps():
#     app_clicks = []
#     app_count = 0
#     app_total = 0
#     appsByDay = {}
#     arrAvgApps = []
#     prfxArrApps = []
#     arrApps = []

#     with open('clicks.txt', 'r') as f:
#         for line in f:
#             checkbox, timestamp = line.strip().split(',')
#             timestamp = datetime.datetime.fromisoformat(timestamp)
#             date = timestamp.strftime("%D")
            
#             if checkbox == 'Appl':
#                 app_count += 1
#                 appsByDay[date] = appsByDay.get(date,0)+1
#                 if app_count % 10 == 0:
#                     app_clicks.append(timestamp)
#                     app_total += 1
                          
#     firstDay = (appStartDate+datetime.timedelta(int(0))).strftime("%D")
#     arrAvgApps = [(firstDay,round(appsByDay.get(firstDay,0)/1,2))]
#     prfxArrApps = [(firstDay,appsByDay.get(firstDay,0))]
#     arrApps = [(firstDay,appsByDay.get(firstDay,0))]
#     print(arrAvgApps)
#     for i in range(1,appDaysPassed):
#         date = (appStartDate+datetime.timedelta(int(i))).strftime("%D")
#         arrApps.append((date,appsByDay.get(date,0)))
#         prfxArrApps.append((date,arrApps[i][1]+prfxArrApps[i-1][1]))
#         arrAvgApps.append(  ( date , round(prfxArrApps[i][1]/(i+1),2) )  )

#     x, y = zip(*arrAvgApps)
    
#     # Plot the data
#     plt.plot(x, y)

#     # Add dots at the data points
#     plt.plot(x, y, 'bo')

#     # Add grid lines
#     plt.grid(True)


#     # Add labels and title
#     plt.xlabel('Date')
#     plt.ylabel('Value')
#     plt.title('Line Chart')

#     # Show the plot
#     plt.show()

def plot_apps():
    app_clicks = []
    app_count = 0
    app_total = 0
    appsByDay = {}
    arrAvgApps = []
    prfxArrApps = []
    arrApps = []

    with open('clicks.txt', 'r') as f:
        for line in f:
            checkbox, timestamp = line.strip().split(',')
            timestamp = datetime.datetime.fromisoformat(timestamp)
            date = timestamp.strftime("%D")

            if checkbox == 'Appl':
                app_count += 1
                appsByDay[date] = appsByDay.get(date,0)+1
                if app_count % 10 == 0:
                    app_clicks.append(timestamp)
                    app_total += 1

    firstDay = (appStartDate+datetime.timedelta(int(0))).strftime("%D")
    
    arrAvgApps = [(firstDay,round(appsByDay.get(firstDay,0)/1,2))]
    prfxArrApps = [(firstDay,appsByDay.get(firstDay,0))]
    arrApps = [(firstDay,appsByDay.get(firstDay,0))]
    arrAvgReqApps = [(firstDay,(applicationsToDo -  prfxArrApps[0][1])/(totalAppDays-len(prfxArrApps)))]

    print(arrAvgApps)
    print()
    for i in range(1,appDaysPassed):
        date = (appStartDate+datetime.timedelta(int(i))).strftime("%D")
        arrApps.append((date,appsByDay.get(date,0)))
        prfxArrApps.append((date,arrApps[i][1]+prfxArrApps[i-1][1]))
        arrAvgApps.append( ( date , round(prfxArrApps[i][1]/(i+1),2) ) )
        arrAvgReqApps.append((date, int((applicationsToDo -  prfxArrApps[i][1])/(totalAppDays-len(prfxArrApps)))))

    print(arrApps)
    x_avg, y_avg = zip(*arrAvgApps)
    x_apps, y_apps = zip(*arrApps)
    x_avgAppsReq, y_avgAppsReq = zip(*arrAvgReqApps)

    plt.grid( which='major', color='darkgray', linewidth=0.5)
    plt.grid( which='minor', color='lightgray', linewidth=0.2)
    plt.minorticks_on()
    plt.grid(True)


    # Plot the data
    plt.plot(x_avgAppsReq, y_avgAppsReq, label='Avg. Req.',color='lightgreen')
    plt.bar(x_apps, y_apps, label='arrApps',width=0.1,color='pink')
    plt.plot(x_avg, y_avg, label='arrAvgApps',linewidth=2.2,color='lightblue')
    
    # Add dots at the data points
    plt.plot(x_avg, y_avg, 'bo',markersize=3)
    plt.plot(x_apps, y_apps, 'ro',markersize=5)
    plt.plot(x_avgAppsReq, y_avgAppsReq, 'go',markersize=3)

    # Add grid lines
    # Add major and minor grid lines
    
    
    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Line Chart')

    plt.xticks(rotation=45)


    # Add a legend
    plt.legend()

    # Add a tooltip that displays the data when hovering over a point
    cursor = mplcursors.cursor(hover=True)
    
    @cursor.connect("add")
    def on_add(sel):
        if sel.artist.get_label() == 'arrAvgApps':
            sel.annotation.set_text(f'Date: {x_avg[int(sel.target.index)]}\nValue: {(y_avg[int(sel.target.index)])}')
        elif sel.artist.get_label() == 'arrApps':
            sel.annotation.set_text(f'Date: {x_apps[sel.target.index]}\nValue: {y_apps[sel.target.index]}')

    # Show the plot
    plt.show()



# Function to plot the time series chart of clicks
def plot_clicks():
    hard_clicks = []
    medium_clicks = []
    app_clicks = []
    app_count = 0
    hard_total = 0
    medium_total = 0
    app_total = 0
    appsByDay = {}
    lcByDay = {}
    arrAvgApps = []
    prfxArrApps = []
    arrApps = []

    with open('clicks.txt', 'r') as f:
        for line in f:
            checkbox, timestamp = line.strip().split(',')
            timestamp = datetime.datetime.fromisoformat(timestamp)
            date = timestamp.strftime("%D")
            
            if checkbox == 'LeetCode Hard':
                hard_clicks.append(timestamp)
                hard_total += 1
                lcByDay[date] = lcByDay.get(date,0)+1

            elif checkbox == 'Appl':
                app_count += 1
                appsByDay[date] = appsByDay.get(date,0)+1
                if app_count % 10 == 0:
                    app_clicks.append(timestamp)
                    app_total += 1
                    
                
            elif checkbox == 'LeetCode Medium':
                medium_clicks.append(timestamp)
                medium_total += 1
                lcByDay[date] = lcByDay.get(date,0)+1

    
    firstDay = (appStartDate+datetime.timedelta(int(0))).strftime("%D")
    arrAvgApps = [round(appsByDay.get(firstDay,0)/1,2)]
    prfxArrApps = [appsByDay.get(firstDay,0)]
    arrApps = [appsByDay.get(firstDay,0)]
    for i in range(1,appDaysPassed):
        arrApps.append(appsByDay.get((appStartDate+datetime.timedelta(int(i))).strftime("%D"),0))
        prfxArrApps.append(arrApps[i]+prfxArrApps[i-1])
        arrAvgApps.append(round(prfxArrApps[i]/(i+1),2))

    fig, ax = plt.subplots()
    ax.plot(hard_clicks, range(1, len(hard_clicks)+1), 'b', label='LeetCode Hard',linewidth=0.8)
    ax.plot(medium_clicks, range(1, len(medium_clicks)+1), 'g', label='LeetCode Medium',linewidth=0.8)
    ax.plot(app_clicks, range(1, len(app_clicks)+1), 'r', label='Appl',linewidth=0.85)
    
    ax.plot(hard_clicks, range(1, len(hard_clicks)+1), 'bo',markersize=3)
    ax.plot(medium_clicks, range(1, len(medium_clicks)+1), 'go',markersize=3)
    ax.plot(app_clicks, range(1, len(app_clicks)+1), 'ro',markersize=3)
    ax.minorticks_on()
    # Position the legend outside of the plot area
    ax.legend()
    
    date_form = DateFormatter("%m-%d-%y")
    ax.xaxis.set_major_formatter(date_form)
    ax.grid(which='minor', color='#EEEEEE', linewidth=0.7)
    ax.grid(True)
    plt.title('Time Series Chart of Clicks')
    plt.xlabel('Time')
    plt.ylabel('Count of Clicks')
    
    # Calculate and display the average per day and total for each curve
    text_y = 0.95
    plt.text(1.04, text_y, f'Days passed: {daysPassed} | appDays passed: {appDaysPassed} ', transform=ax.transAxes,weight='bold')
    text_y -= 0.05
    plt.text(1.04, text_y, f'Days to go: {daysLeft} | Deadline: {deadline.strftime("%d-%m-%Y")}', transform=ax.transAxes,weight='bold')
    text_y -= 0.1
    # print(deadline.strftime("%d-%m-%Y"))
    if daysPassed > 0:
        plt.text(1.04, text_y, f'LeetCode Hard Total: {hard_total}', transform=ax.transAxes)
        text_y -= 0.05

        plt.text(1.04, text_y, f'LeetCode Medium Total: {medium_total}', transform=ax.transAxes)
        text_y -= 0.05
    
    plt.text(1.04, text_y, f'LeetCode Ratio (Medium:Hard) : [{medium_total/(hard_total):.2f}:1]', transform=ax.transAxes)
    text_y -= 0.05
    text_y -= 0.05
    totalQuestionDone = medium_total+hard_total    
    plt.text(1.04, text_y, f'Leetcode Total: {totalQuestionDone}', transform=ax.transAxes,weight='bold')
    text_y -= 0.05

    if daysPassed>0:
        leetcode_avg = totalQuestionDone/daysPassed
        plt.text(1.04, text_y, f'Leetcode Avg(/Day): [{leetcode_avg:.3f}]', transform=ax.transAxes,weight='bold')
        text_y -= 0.05
    
    QuestionsLeft = (200-totalQuestionDone)

    plt.text(1.04, text_y, f'LeetCode to do: {QuestionsLeft}', transform=ax.transAxes,weight='bold')
    text_y -= 0.05
    plt.text(1.04, text_y, f'Avg. LC req.: [{(QuestionsLeft)/(daysLeft):.3f}]', transform=ax.transAxes,weight='bold')
    text_y -= 0.05

    LC_Speed_req = 200/totalDays
    QuestionsDiff = totalQuestionDone - LC_Speed_req*daysPassed
    plt.text(1.04, text_y, f'Total Diff.(Lag): {math.floor(QuestionsDiff)}', transform=ax.transAxes,weight='bold')
    text_y -= 0.05
    LC_SpeedDiff = QuestionsLeft/daysLeft - LC_Speed_req
    plt.text(1.04, text_y, f'Speed Diff.(Lag): [{(LC_SpeedDiff):.3f}]', transform=ax.transAxes,weight='bold')
    text_y -= 0.10

    print(appsByDay)

    plt.text(1.04, text_y, f'Appl Total: {app_count} | Today : {appsByDay.get(today.strftime("%D"),0)} ', transform=ax.transAxes,weight='bold')
    text_y -= 0.05
    
    if appDaysPassed > 0:
        app_avg = app_count / appDaysPassed
        plt.text(1.04, text_y, f'Appl Avg(/Day)(/10):  ({(app_avg):.3f})/10 = [{app_avg/10:.3f}]', transform=ax.transAxes,weight='bold')
        text_y -= 0.05

    AppLeft = (applicationsToDo-app_count)
    plt.text(1.04, text_y, f'Total Appl. req.: {AppLeft}', transform=ax.transAxes,weight='bold')
    text_y -= 0.05
    plt.text(1.04, text_y, f'Avg. Appl. req.(/10):  ({AppLeft/(daysLeft):.3f})/10 = [{AppLeft/(daysLeft*10):.3f}]', transform=ax.transAxes,weight='bold')
    text_y -= 0.05

    App_SpeedReq = (applicationsToDo)/(appDaysPassed+daysLeft)
    App_Diff = app_count-App_SpeedReq*appDaysPassed
    
    plt.text(1.04, text_y, f'Total Diff. : {math.floor(App_Diff)}', transform=ax.transAxes,weight='bold')
    text_y -= 0.05
    App_SpeedDiff = AppLeft/daysLeft-App_SpeedReq
    plt.text(1.04, text_y, f'Avg. Diff. : ({App_SpeedDiff:.3f})/10 = [{App_SpeedDiff/10:.3f}]', transform=ax.transAxes,weight='bold')
    text_y -= 0.05
    
    cursor = mplcursors.cursor(hover=True)
    cursor.connect('add', format_cursor_text)

    # Adjust the size of the plot area to make room for the legend and text
    plt.subplots_adjust(right=0.71,left=0.075)

    plt.show()


# import datetime
# import matplotlib.pyplot as plt
# from matplotlib.dates import DateFormatter
# from collections import defaultdict

# def plot_clicks():
#     hard_clicks = defaultdict(int)
#     medium_clicks = defaultdict(int)
#     app_clicks = defaultdict(int)
#     with open('clicks.txt', 'r') as f:
#         for line in f:
#             checkbox, timestamp = line.strip().split(',')
#             timestamp = datetime.datetime.fromisoformat(timestamp)
#             date = timestamp.date()
#             if checkbox == 'LeetCode Hard':
#                 hard_clicks[date] += 1
#             elif checkbox == 'Appl':
#                 app_clicks[date] += 1
#             elif checkbox == 'LeetCode Medium':
#                 medium_clicks[date] += 1

#     dates = sorted(set(hard_clicks) | set(medium_clicks) | set(app_clicks))
#     hard_counts = [hard_clicks[date] for date in dates]
#     medium_counts = [medium_clicks[date] for date in dates]
#     app_counts = [app_clicks[date] for date in dates]

#     fig, ax = plt.subplots()
#     ax.bar(dates, hard_counts, label='LeetCode Hard')
#     ax.bar(dates, medium_counts, bottom=hard_counts, label='LeetCode Medium')
#     ax.bar(dates, app_counts, bottom=[sum(x) for x in zip(hard_counts, medium_counts)], label='Appl')

#     ax.legend()
#     date_form = DateFormatter("%m-%d")
#     ax.xaxis.set_major_formatter(date_form)
#     ax.grid(True)
#     plt.title('Stacked Bar Chart of Clicks')
#     plt.xlabel('Date')
#     plt.ylabel('Count of Clicks')

#     cursor = mplcursors.cursor(hover=True)
#     cursor.connect('add', format_cursor_text)

#     # Adjust the size of the plot area to make room for the legend and text
#     plt.subplots_adjust(right=0.7)

#     plt.show()


# Create the main window
root = tk.Tk()
root.title('Click Recorder')

# Create the checkboxes
medium_var = tk.BooleanVar()
medium_checkbox = tk.Checkbutton(root, text='Appl', variable=medium_var,
                                 command=lambda: record_click('Appl'))
medium_checkbox.pack()


hard_var = tk.BooleanVar()
hard_checkbox = tk.Checkbutton(root, text='LeetCode Hard', variable=hard_var,
                               command=lambda: record_click('LeetCode Hard'))
hard_checkbox.pack()


app_var = tk.BooleanVar()
app_checkbox = tk.Checkbutton(root, text='LeetCode Medium', variable=app_var,
                              command=lambda: record_click('LeetCode Medium'))
app_checkbox.pack()

# Create the plot button

plot_clicks_button = tk.Button(root, text='Plot Clicks', command=plot_clicks)
plot_apps_button = tk.Button(root, text='Plot Avg. Apps', command=plot_apps)

# Display both buttons
plot_clicks_button.pack()
plot_apps_button.pack()

# Run the main loop
root.mainloop()


# 85068202-1685320901