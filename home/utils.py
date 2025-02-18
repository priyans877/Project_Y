from home.models import chart_data
from scrap.models import result
import pandas as pd
import plotly.express as px
from data.utils import branch_filter




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
    # print(sem_option,"In reappear_batch" , year_option  , "In Branch"  , branch_option)
        
    objects = chart_data.objects.filter(
    semester=sem_option, 
    year=year_option, 
    branch=branch_option
    ).order_by('-cgpa')[:5]

    df = pd.DataFrame(list(objects.values()))
  
    fig = px.bar(
        df, 
        x='student_name', 
        y='cgpa', 
        text='cgpa'
    )
    
    fig.update_traces(
        customdata=df['roll_no'],  
        hovertemplate=(
            "<b>Student Name:</b> %{x}<br>"
            "<b>SGPA:</b> %{y}<br>"
            "<b>Roll Number:</b> %{customdata}<extra></extra>"
        )
    )
    
    #updating Layout
    fig.update_layout(
        title=f'Top 5 Students by SGPA in {branch_option}-{sem_option} Batch {year_option}',
        xaxis_title='Student Name',
        yaxis_title='SGPA',
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(173, 216, 230, 0.8)', 
        plot_bgcolor='rgba(173, 216, 230, 0.8)', 
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="darkblue"  # darker text
        ),
        bargap=0.2  
    )
    
    # bar color and charts
    fig.update_traces(
        marker=dict(
            color='rgba(0, 0, 139, 0.8)',  # blue bars  
            line=dict(color='darkblue', width=1.5) 
            ),
        textposition='inside',  
        textfont=dict(size=12, color='white') 
    )


    return fig


def reapear_batch(year_option, branch_option):
    objects = chart_data.objects.filter(year=year_option, branch=branch_option)
    df = pd.DataFrame(data=list(objects.values()))
    filter_df = df[df['recount'] > 0]
    filtered_semester_recounts = filter_df.groupby('semester')['recount'].count().reset_index()
    
    fig = px.pie(
        filtered_semester_recounts,
        values='recount',
        names='semester',
        title=f'ReApeares Of {branch_option} Batch {year_option}'
    )

    fig.update_traces(
        textposition='outside',
        textinfo='label+value',
        pull=[0.02] * len(filtered_semester_recounts),
        hovertemplate="<b>%{label}</b><br>Reappear count: %{value}<br><extra></extra>"
    )
    
    fig.update_layout(
        paper_bgcolor='#f0f0f0',
        plot_bgcolor='#f0f0f0',
        font_color='#333333',
        title={
            'text': f"Recount Of Batch {year_option}",
            'y': 0.95,
            'x': 1,
            'xanchor': 'right',
            'yanchor': 'top'
        },
        showlegend=False,
        margin=dict(t=50, l=80, r=80, b=50),
        autosize=False,
        width=556,
        height=388,
        clickmode='event'
    )

    return fig
