from django.shortcuts import render
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
import numpy as np
from pandass.models import UploadedFile
import plotly.express as px
import plotly.graph_objects as go
from django.http import HttpResponseServerError
# Create your views here.

# def show1(request):
#     context = {}
#     uploaded_files = UploadedFile.objects.all()
#     context['uploaded_files'] = uploaded_files
#     charts = {

#               'Line_Plot':'Line Plot',
#               'Scatter_Plot':'Scatter Plot',
#               'box_plot':'Box Plot',
#               'Histogram':'Histogram',
#               'Image':'Image',
#               'Kde_Plot':'Kde Plot',
#               'Violin_Plot':'Violin Plot',
#               'Bar_plot':'Bar Plot',
#               'Heatmap':'Heatmap',
#               'Pie_chart':'Pie Chart'

#              }
#     context['charts']= charts
#     print("heeeeeeeeeeeeeeeeeeeeere")
#     return render(request, 'chart_view.html',context )

def calculate_statistics(df, selected_column_name2):
    # Calculate your custom statistics
    mean_value = df[selected_column_name2].mean()
    median_value = df[selected_column_name2].median()
    mode_value = df[selected_column_name2].mode().iloc[0]
    range_value = df[selected_column_name2].max() - df[selected_column_name2].min()
    variance_value = df[selected_column_name2].var()
    std_deviation_value = df[selected_column_name2].std()
    count_value = df[selected_column_name2].count()

    # Create a dictionary to store the statistics
    statistics_dict = {
        'Moyenne': mean_value,
        'Médiane': median_value,
        'Mode': mode_value,
        'Variance': variance_value,
        'Écart-type': std_deviation_value,
        'Nombre': count_value,
    }

    # Convert the dictionary to a DataFrame for better formatting
    statistics_df = pd.DataFrame(list(statistics_dict.items()), columns=[f'Statistic {selected_column_name2}', 'Value'])
    return statistics_df.to_html(classes='table table-striped table-bordered', index=False)




def show(request):
    context = {}
    uploaded_files = UploadedFile.objects.all()
    context['uploaded_files'] = uploaded_files
    

    charts = {

              'Line_Plot':'Line Plot',
              'Scatter_Plot':'Scatter Plot',
              'box_plot':'Box Plot',
              'Histogram':'Histogram',
              'Image':'Image',
              'Kde_Plot':'Kde Plot',
              'Violin_Plot':'Violin Plot',
              'Bar_plot':'Bar Plot',
              'Heatmap':'Heatmap',
              'Pie_chart':'Pie Chart'

             }
    
    try:
        if request.method == 'POST':
            print("2222")
            filename1 = request.POST.get('dropdown1', None)
            filename = filename1.split("uploaded_csv/")[1]
            print("3333"+filename)
            # Filter UploadedFile objects based on the file name
            uploaded_files = UploadedFile.objects.filter(file__contains=filename)

            if not uploaded_files.exists():
                raise ValueError("No matching uploaded file found.")

            
            
            if uploaded_files.exists():
                print(4444)
                # Assuming you want to work with the first matching file
                uploaded_file = uploaded_files.first()

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
            non_numerical_columns = [col for col in df.columns if col not in numerical_columns]
            if numerical_columns:
                context['numerical'] = numerical_columns
            if non_numerical_columns:
                context['nonumerical'] = non_numerical_columns
            
            
            selected_chart_key = request.POST.get('selected_chart')
            print(selected_chart_key)
            # Accessing selected columns
            print("hello")
            selected_columns = request.POST.getlist('selected_columns')
            print('Selected Columns:', selected_columns)
            if selected_columns[0] in numerical_columns:
                context['stats1'] = calculate_statistics(df,selected_columns[0])

            if selected_columns[1] in numerical_columns:
                context['stats2'] = calculate_statistics(df,selected_columns[1])
           
            if selected_columns:
                if selected_columns != 'all':
                    context['datahtml'] = df[selected_columns]
            df = context['datahtml']
            import plotly.express as px


            if selected_chart_key == 'Line_Plot':

    
                fig = px.line(df, x=selected_columns[0], y=selected_columns[1], markers=True, line_shape='linear',
                        labels={selected_columns[0]: selected_columns[0], selected_columns[1]: selected_columns[1]},
                        title=f'Line Plot ({selected_columns[0]} vs {selected_columns[1]})')



                plot_html = fig.to_html(full_html=False)
                
                context['image'] = plot_html


            if selected_chart_key == 'Scatter_Plot':
                print(selected_chart_key)

                # Create a Scatter Plot using Plotly Express
                fig = px.scatter(df, x=selected_columns[0], y=selected_columns[1], title='Scatter Plot')

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html

            if selected_chart_key == 'box_plot':
                # Create a Box Plot using Plotly Express
                fig = px.box(df, x=selected_columns[0], y=selected_columns[1], title=f'Box Plot - {selected_columns[0]} and {selected_columns[1]}')

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html

            if selected_chart_key == 'Histogram':
                # Create a Histogram using Plotly Express
                fig = px.histogram(df, x=selected_columns[0], title=f'Histogram - {selected_columns[0]}')

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html

            if selected_chart_key == 'Image':
                heatmap = go.Heatmap(x=df[selected_columns[1]], y=df[selected_columns[0]], z=[[1]*len(df)]*len(df),
                                colorscale='Viridis', showscale=False)

                # Create layout
                layout = go.Layout(title=f'Heatmap - {selected_columns[0]} vs {selected_columns[1]}')

                # Create figure
                fig = go.Figure(data=[heatmap], layout=layout)

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html




            if selected_chart_key == 'Kde_Plot':
                # Create a KDE Plot using Plotly Express
            
                fig = px.histogram(df, x=selected_columns[0], marginal='kde', title=f'KDE Plot - {selected_columns[0]}')

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html


            if selected_chart_key == 'Heatmap':
                # Create a Heatmap using Plotly Express
                fig = px.imshow(df.pivot_table(index=selected_columns[0], columns=selected_columns[1], aggfunc='size'),
                            title=f'Heatmap - {selected_columns[0]} vs {selected_columns[1]}')

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html

            if selected_chart_key == 'Violin_Plot':
                fig = px.violin(df, x=selected_columns[0], y=selected_columns[1], box=True, points="all",
                                title=f'Violin Plot - {selected_columns[0]} vs {selected_columns[1]} ')

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html

            if selected_chart_key == 'Pie_chart':
            
                # Create a pie chart using Plotly Express
                fig = px.pie(df, names=selected_columns[0], values=selected_columns[1],
                            title=f'Pie Chart - {selected_columns[0]} vs {selected_columns[1]}')

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html

            context['lendata'] = len(context['datahtml'])
    except pd.errors.EmptyDataError:
        context['error_message'] = "The uploaded file is empty."
        print(context['error_message'] )
    except ValueError as ve:
        context['error_message'] = f"Error: {ve}"
        print(context['error_message'] )
    except Exception as e:
        context['error_message'] = f"An unexpected error occurred: {e}"
        print(context['error_message'] )
        
    
    context['charts']= charts
    return render(request, 'visualisation.html',context )

