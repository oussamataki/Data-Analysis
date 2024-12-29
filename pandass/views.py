# views.py
import pandas as pd
from django.shortcuts import render,redirect
from .forms import CSVUploadForm
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.base import ContentFile
import csv
from pandass import urls

import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import UploadedFile

from django.http import HttpResponse

from urllib.parse import unquote
from io import StringIO  # Import StringIO from the io module
from urllib.parse import urlparse

def uploadLink(request):
   
    if request.method == 'POST':
        link = request.POST.get('choice')
        print(link)

        li = request.POST.get('dropdown1')
        print('Li:')

        print(li)
        try:
            if link == 'html':

                tables = pd.read_html(li)
            elif link == 'link':
                tables = pd.read_csv(li)


            print('tables:')

            print(tables)
            if tables:
                df = tables[0]

                print(df)

                

                # Extract a meaningful name from the link and use it as the filename
                parsed_url = urlparse(li)
                filename = f"en_{parsed_url.path.replace('/', '_')}.csv"
                print('filename')
                print(filename)
                # Save the DataFrame to the database with the dynamic name
                uploaded_file = UploadedFile()
                csv_content = pd.DataFrame(tables[0]).to_csv(index=False)

                # Assuming 'uploaded_file' is a FileField or ImageField in your Django model
                if uploaded_file and hasattr(uploaded_file, 'file'):
                    uploaded_file.file.save(filename, ContentFile(csv_content))
                else:
                    # Handle the case where 'uploaded_file' is None or doesn't have a 'file' attribute
                    print("Error: 'uploaded_file' is None or does not have a 'file' attribute")
                uploaded_file.save()
                


        except Exception as e:
            print('thisssssssssssssssss')
            print(e)
    return redirect('showM')

def download(request):
      if request.method == 'POST':
        # Retrieve the serialized DataFrame from the POST data
        df = request.POST.get('data', '')
        df = pd.read_csv(StringIO(df), sep='\t')

        print(type(df))

        delimiter = ','
        df = pd.DataFrame(df)
       
        csv_data = df.to_csv(index=False, sep=delimiter)

   
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=data.csv'

        return response
    

def upload(request):
    context = {}

    if request.method == 'POST':
      
            form = CSVUploadForm(request.POST, request.FILES)

            if form.is_valid():
                file_data = form.cleaned_data['csv_file']

                # Check the file type
                if file_data.name.endswith('.csv'):
                    # Handle CSV file
                    df = pd.read_csv(file_data)
                elif file_data.name.endswith(('.xls', '.xlsx')):
                    # Handle Excel file
                    df = pd.read_excel(file_data)
                else:
                    return render(request, 'upload.html', {'form': form, 'error_message': 'Unsupported file type'})

                # Save the uploaded file with a dynamic name
                uploaded_file = UploadedFile(file=file_data)
                uploaded_file.save()

                context['datahtml'] = df
                context['lendata'] = len(df)
                context['columns'] = df.columns

    
    else:
        form = CSVUploadForm()

    context['form'] = form
    return render(request, 'upload.html', context)
def index(request):
    context = {}
    aggregations = {
    'Mean': 'mean',
    'Sum': 'sum',
    'Max': 'max',
    'Min': 'min',
    'Median':'median',
    'Count': 'count',
    }
    context['agg'] = aggregations
    uploaded_files = UploadedFile.objects.all()
    context['uploaded_files'] = uploaded_files
    print(context)
    return render(request, 'index.html',context)


def list_uploaded_files(request):
    context = {}
    aggregations = {
    'Mean': 'mean',
    'Sum': 'sum',
    'Max': 'max',
    'Min': 'min',
    'Median':'median',
    'Count': 'count',
}
    context['agg'] = aggregations
    uploaded_files = UploadedFile.objects.all()
    context['uploaded_files'] = uploaded_files
    print("11111")

    try:
     if request.method == 'POST':
        
        filename1 = request.POST.get('dropdown1', None)
        filename = filename1.split("uploaded_csv/")[1]
        
        

        # Filter UploadedFile objects based on the file name
        uploaded_files = UploadedFile.objects.filter(file__contains=filename)

        if uploaded_files.exists():
            print(4444)
            # Assuming you want to work with the first matching file
            uploaded_file = uploaded_files.first()

            print(uploaded_file.file.path)

            # Check the file type
            if uploaded_file.file.name.endswith('.csv'):
                # Handle CSV file
                df = pd.read_csv(uploaded_file.file.path)
            elif uploaded_file.file.name.endswith(('.xls', '.xlsx')):
                # Handle Excel file
                df = pd.read_excel(uploaded_file.file.path)
            else:
                # Handle other file types or show an error message
                return render(request, 'upload.html', {'form': uploaded_file, 'error_message': 'Unsupported file type'})



            context['datahtml'] = df
            context['lendata'] = len(df)
            context['selected'] = filename1
            context['columns'] = df
        
    
        numerical_columns = list(df.select_dtypes(include=['number']).columns)
        if numerical_columns:
            context['numerical'] = numerical_columns

               
    
        selected_columns = request.POST.getlist('selected_columns')
    
        
        print('Selected Columns:', selected_columns)
        if selected_columns:
            if selected_columns != 'all':
                context['datahtml'] = df[selected_columns]


        # Accessing head and tail checkboxes
        slice_option = request.POST.get('slice_option', '')
        print('Slice Option:', slice_option)
        if slice_option == 'head':
            context['datahtml'] = context['datahtml'].head()
        elif slice_option == 'tail':
            context['datahtml'] = context['datahtml'].tail()

        

        

        # Accessing line1 and line2 inputs
        line1_value = int(request.POST.get('line1',0))
        line2_value = int(request.POST.get('line2', 0))

        

        if line2_value == 0 and line1_value != 0:
            print(line1_value)
            print(context['datahtml'].loc[line1_value])

            context['datahtml'] = context['datahtml'].loc[[line1_value]]
        elif line2_value != 0 and line1_value != 0:
            context['datahtml'] = context['datahtml'].loc[line1_value:line2_value]
     


        print('Line 1 Value:', line1_value)
        print('Line 2 Value:', line2_value)

        sample_value = int(request.POST.get('sample', 0))
        if sample_value:
           context['datahtml']= context['datahtml'].sample(n=sample_value)
        print('Sample Value:', sample_value)


        # Accessing group by select and selected columns
        group_by_column = request.POST.get('group', '')
        print('Group By Column:', group_by_column)

        group_by_selected_columns = request.POST.getlist('selected_columns2')
        print('Group By Selected Columns:', group_by_selected_columns)
        
        agg = request.POST.get('agg', '')
        print(' agg:', agg)

      
        if group_by_column and group_by_selected_columns:
            if agg == 'Mean':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].mean()
            elif agg == 'Sum':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].sum()
            elif agg == 'Max':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].max()
            elif agg == 'Min':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].min()
            elif agg == 'Median':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].median()
            elif agg == 'Count':
                context['datahtml'] = context['datahtml'].groupby(group_by_column)[group_by_selected_columns].count()

        context['lendata'] = len(context['datahtml'])
        print(context['datahtml'])
        print("heeeeeeeere")
    except ValueError as ve:
        
        context['error_message'] = str(ve)
        print(context['error_message'])
    except Exception as e:
        # Handle other exceptions if needed
        context['error_message'] = f"An error occurred: {e}"
        if 'agg function failed' in str(e) and 'dtype->object' in str(e):
            context['error_message'] = "An error occurred: choose a column with numerical values"


    return render(request, 'index.html', context)
