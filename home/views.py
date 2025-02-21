from django.shortcuts import render , redirect
from django.http import JsonResponse , HttpResponse
from scrap.models import result
from django.contrib.auth.models import User
from data.models import excle_model
from rest_framework.response import Response
from data.serializers import resultSerializer
from rest_framework.decorators import api_view
from .utils import *
from .models import chart_data
import plotly.express as ps
from account.models import Profile
from django.contrib.auth.decorators import login_required
from account.decorators import unauthorised
from scrap.views import driver
# Create your views here.

@api_view(['GET'])
def resp(request):
    main_data = result.objects.all()
    data = resultSerializer(main_data , many=True)
    return Response(data.data)



def under_dev(request):
    return render(request , 'account/under_dev.html')

@api_view(['GET'])
def get_chart(request):
    main_data = result.objects.all()
    data = resultSerializer(main_data , many=True)
    top_students()
    return Response(data.data)
    
@unauthorised
def home_public(request):
    #data_transer to update all data
    data_transfer()
    result_count = result.objects.all() #total datascraped till now
    total_user = User.objects.all()
    total_sheets = excle_model.objects.all()
    chart_ob = chart_data.objects.all()
    
    sem_options_temp =  [p.semester for p in chart_ob]
    year_options_temp = [p.year for p in chart_ob]
    branch_options_temp = [p.branch for p in chart_ob]
    
    selector_options = []
    
    for sem in set(sem_options_temp):
        for branch in set(branch_options_temp):
            for year in set(year_options_temp):      
                data = chart_data.objects.filter(branch = branch , semester = sem , year = year)
                if data.exists():
                    selector_options.append(f"{branch}-{year}-{sem}")
                    

    branch_option , year_option , semester_option = request.GET.get('selected_category' , selector_options[4]).split("-")
      
    
    fig = top_students(semester_option , year_option , branch_option)
    
    fig2 = reapear_batch(year_option , branch_option)
    
    fig_html2 = fig2.to_html(full_html = False , config={"displayModeBar": False})
    fig_html = fig.to_html(full_html=False , config={"displayModeBar": False})
    
    print(set(selector_options))

    message_info = {
        'total_scrap' : len(result_count),
        'total_users' : len(total_user),
        'total_sheets' : len(total_sheets),
        'plot_div' : fig_html,
        'plot_div2' : fig_html2,
        'all_options' : sorted(set(selector_options)),
        'user_name' :"Welcome User",
        'slogan' : "Dataset" if request.user.id!=None else f"Results",
        
    }
    
    if request.headers.get('HX-Request'):   
        return render(request, 'home/data_chart.html', message_info)
    
    #return the full page
    return render(request, 'home/Home.html', message_info)




@login_required(login_url='login')
def dashboard(request):
    data_transfer()

    
    print(request.user.id)
    result_count = result.objects.filter(user_id = request.user.id) #total datascraped till now
    total_user = User.objects.all()
    total_sheets = excle_model.objects.all()
    chart_ob = chart_data.objects.all()
    
    sem_options_temp =  [p.semester for p in chart_ob]
    year_options_temp = [p.year for p in chart_ob]
    branch_options_temp = [p.branch for p in chart_ob]
    
    selector_options = []
    
    for sem in set(sem_options_temp):
        for branch in set(branch_options_temp):
            for year in set(year_options_temp):     
                data = chart_data.objects.filter(branch = branch , semester = sem , year = year)
                if data.exists():
                    selector_options.append(f"{branch}-{year}-{sem}")
                    
    
    branch_option , year_option , semester_option = request.GET.get('selected_category' , selector_options[0]).split("-")
    
    fig = top_students(semester_option , year_option , branch_option)
    
    fig2 = reapear_batch(year_option , branch_option)
    
    fig_html2 = fig2.to_html(full_html = False , config={"displayModeBar": False})
    fig_html = fig.to_html(full_html=False , config={"displayModeBar": False})
    # print(request.user.first_name)
    message_info = {
        'total_scrap' : len(result_count),
        'total_users' : len(total_user),
        'total_sheets' : len(total_sheets),
        'plot_div' : fig_html,
        'plot_div2' : fig_html2,
        'all_options' : set(selector_options),
        'user_name' : f"Welcom Back, {request.user.first_name}",
        'slogan' : "Dataset" if request.user.id!=None else "Results",
    }
    
    if request.headers.get('HX-Request'):   
        return render(request, 'home/data_chart.html', message_info)
    
    # otherwise, return the full page
    return render(request, 'home/dashboard.html', message_info)
    
