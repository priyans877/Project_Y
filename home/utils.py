from home.models import chart_data
from scrap.models import result
import pandas as pd
import plotly.express as px
from data.utils.extractor import branch_filter

def semester_filter(datax):
    data = datax
    for i in range(len(data)):
      
        if data[i][-2:] == "01":
            data[i] = "First Semester"
        elif data[i][-2:] == "02":
            data[i] = "Second Semester"
        elif data[i][-2:] == "03":
            data[i] = "Third Semester"
        elif data[i][-2:] == "04":
            data[i] = "Fourth Semester"
        elif data[i][-2:] == "05":
            data[i] = "Fifth Semester"
        elif data[i][-2:] == "06":
            data[i] = "Sixth Semester"
        elif data[i][-2:] == "07":
            data[i] = "Seventh Semester"
        else:
            data[i] = "Eight Semester"
            
    return data


def extract_year(texts):
    for i in range(len(texts)):
        parts = texts[i].split('_')
        for part in parts:
            if part.isdigit() and len(part) == 2 and int(part) >8:
                texts[i] = part
    return texts


def data_transfer():
    result_data = result.objects.all()
    names = [p.s_name for p in result_data]
    roll_nos = [p.roll_no for p in result_data]
    semesters = semester_filter([p.category for p in result_data])
    branch = branch_filter([p.category for p in result_data])
    years = extract_year([p.category for p in result_data])
    sgpa = [float(p.sgpa) if p.cgpa else 0 for p in result_data]

    recounts = [p.re_count for p in result_data]
   
    for i in range(len(names)):
        chart_ob = chart_data.objects.get_or_create(
            student_name = names[i],
            roll_no = roll_nos[i],
            semester = semesters[i],
            branch = branch[i],
            year = years[i],
            cgpa = sgpa[i],
            recount = recounts[i]
        )



def top_students(sem_option, year_option , branch_option):
    # Filter and prepare the data
    print(sem_option,"In reappear_batch" , year_option  , "In Branch"  , branch_option)
    objects = chart_data.objects.filter(semester=sem_option, year=year_option , branch = branch_option)
    data = list(objects.values())
    df = pd.DataFrame(data)
    if len(df)>5:
        df = df.sort_values(by='cgpa', ascending=False)[:5]
    else:
        df = df.sort_values(by='cgpa', ascending=False)
    
    #creating the bar chart
    fig = px.bar(
        df, 
        x='student_name', 
        y='cgpa', 
        text='cgpa'
    )
    
    #add roll number to hove
    fig.update_traces(
        customdata=df['roll_no'],  # Assuming roll_number is a column in the DataFrame
        hovertemplate=(
            "<b>Student Name:</b> %{x}<br>"
            "<b>SGPA:</b> %{y}<br>"
            "<b>Roll Number:</b> %{customdata}<extra></extra>"
        )
    )
    
    # Update layout for styling
    fig.update_layout(
        title=f'Top 5 Students by SGPA in {branch_option}-{sem_option} Batch {year_option}',
        xaxis_title='Student Name',
        yaxis_title='SGPA',
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(173, 216, 230, 0.8)',  # Light blue background for the chart
        plot_bgcolor='rgba(173, 216, 230, 0.8)',   # Light blue background for the plot area
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="darkblue"  # Darker text color
        ),
        bargap=0.2  # Adjust gap between bars
    )
    
    # Update bar colors and text
    fig.update_traces(
        marker=dict(
            color='rgba(0, 0, 139, 0.8)',  # Darker blue for bars
            line=dict(color='darkblue', width=1.5)  # Darker border for bars
        ),
        textposition='inside',  # Display CGPA values outside the bars
        textfont=dict(size=12, color='white')  # Darker text color for CGPA values
    )
    
    return fig

    
def reapear_batch(year_option , branch_option):
    print("In reappear_batch" , year_option , "Branch" , branch_option)
    
    objects = chart_data.objects.filter(year=year_option , branch = branch_option)
    df = pd.DataFrame(data = list(objects.values()))
     
    filter_df = df[df['recount']>0]
    # Step 1: Group by 'semester' and count 'Recount'
    filtered_semester_recounts = filter_df.groupby('semester')['recount'].count().reset_index()
    
    print("here is the dataframe",filtered_semester_recounts)
    fig = px.pie(filtered_semester_recounts, values='recount', names='semester', title=f'ReApeares Of {branch_option} Batch {year_option}')
    
    fig.update_layout(
        paper_bgcolor='#f0f0f0',  # Light gray background
        plot_bgcolor='#f0f0f0',
        font_color='#333333',     # Dark gray font color
        title={
            'text': "Recount Of Batch 21",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        legend={
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1,
            'xanchor': "center",
            'x': 0.5
        },
        autosize=False,  # Disable autosizing
        width=556,       # Fixed width
        height=388, 
    )


    return fig
            
