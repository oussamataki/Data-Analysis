from django.shortcuts import render
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
import numpy as np
from pandass.models import UploadedFile
from scipy.stats import norm,bernoulli,binom,uniform,poisson,expon
import plotly.graph_objects as go
from scipy.stats import ttest_ind
from scipy.stats import ttest_1samp
from scipy.stats import chi2_contingency
# Create your views here.






def test(request):
    context = {}
    uploaded_files = UploadedFile.objects.all()
    context['uploaded_files'] = uploaded_files
    

    charts = {

              't_test':'T test',
              'z_test':'Z test',
              'chi_square_test':'KHI Carre test'

            
             }
    try:
        if request.method == 'POST':
            
            selected_chart_key = request.POST.get('selected_chart')
        

            print(selected_chart_key)
            # Accessing selected columns
            selected_columns = request.POST.getlist('selected_columns')
            print('Selected Columns:', selected_columns)
            
        
            if selected_chart_key == 't_test':
                loc1_str = request.POST.get('loc1t', '0')
                loc2_str = request.POST.get('loc2t', '0')

                scale1_str = request.POST.get('scale1t', '0')
                scale2_str = request.POST.get('scale2t', '0')

                nmbre1_str = request.POST.get('nmbre1t', '0')
                nmbre2_str = request.POST.get('nmbre2t', '0')

                # Convert to float, handling empty strings
                loc1 = float(loc1_str) if loc1_str != '' else 0
                loc2 = float(loc2_str) if loc2_str != '' else 0

                scale1 = float(scale1_str) if scale1_str != '' else 0
                scale2 = float(scale2_str) if scale2_str != '' else 0

                nmbre1 = int(nmbre1_str) if nmbre1_str != '' else 0
                nmbre2 = int(nmbre2_str) if nmbre2_str != '' else 0

                np.random.seed(42)
                data1 = np.random.normal(loc=loc1, scale=scale1, size=nmbre1)
                data2 = np.random.normal(loc=loc2, scale=scale2, size=nmbre2)

                # Perform independent two-sample t-test
                t_stat, p_value = ttest_ind(data1, data2)

                # Create box plot using Plotly
                fig = go.Figure()

                fig.add_trace(go.Box(y=data1, name='Group 1'))
                fig.add_trace(go.Box(y=data2, name='Group 2'))

                # Add annotation with t-test results
                fig.add_annotation(
                    x=1.2,
                    y=3,
                    text=f'T-Test Results\nT-Stat: {t_stat:.2f}\nP-Value: {p_value:.4f}',
                    showarrow=False,
                )

                # Customize layout
                fig.update_layout(
                    title='Box Plot with T-Test Results',
                    yaxis=dict(title='Values'),
                    boxmode='group',
                )

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html
            if selected_chart_key == 'z_test':

                loc1 = float(request.POST.get('loc1','0'))
                loc2 = float(request.POST.get('loc2','0'))

                scale1 = float(request.POST.get('scale1','0'))
                scale1 = float(request.POST.get('scale2','0'))

                nmbre1 = float(request.POST.get('nmbre1','0'))
                nmbre2 = float(request.POST.get('nmbre2','0'))

                np.random.seed(42)
                data1 = np.random.normal(loc=loc1, scale=scale1, size=nmbre1)
                data2 = np.random.normal(loc=loc2, scale=scale2, size=nmbre2)

                # Specify the null hypothesis mean and population standard deviation
                null_hypothesis_mean = 0
                population_std_dev = 1

                # Calculate the Z-statistic
                z_stat = (np.mean(data1) - np.mean(data2)) / (population_std_dev * np.sqrt(2 / len(data1)))

                # Calculate the p-value
                p_value = 2 * (1 - norm.cdf(np.abs(z_stat)))

                # Create box plot using Plotly
                fig = go.Figure()

                fig.add_trace(go.Box(y=data1, name='Group 1'))
                fig.add_trace(go.Box(y=data2, name='Group 2'))

                # Add annotation with Z-test results
                fig.add_annotation(
                    x=1.2,
                    y=3,
                    text=f'Z-Test Results\nZ-Stat: {z_stat:.2f}\nP-Value: {p_value:.4f}',
                    showarrow=False,
                )

                # Customize layout
                fig.update_layout(
                    title='Box Plot with Z-Test Results',
                    yaxis=dict(title='Values'),
                    boxmode='group',
                )

                # Convert the plot to HTML
                plot_html = fig.to_html(full_html=False)

                # Embed the HTML in the context
                context['image'] = plot_html


            if selected_chart_key == 'chi_square_test':

                # Assuming you have a contingency table provided through POST data
                contingency_table = [[int(request.POST.get('obs11', '0')), int(request.POST.get('obs12', '0'))],
                                    [int(request.POST.get('obs21', '0')), int(request.POST.get('obs22', '0'))]]

                # Perform the Chi-Square test
                chi2_stat, p_value, _, _ = chi2_contingency(contingency_table)

                # Create a table with observed values
                table = go.Figure(data=[go.Table(
                    header=dict(values=['Observed 1', 'Observed 2']),
                    cells=dict(values=[contingency_table[0], contingency_table[1]])
                )])

                # Add annotation with Chi-Square test results
                table.add_annotation(
                    x=1.2,
                    y=3,
                    text=f'Chi-Square Test Results\nChi2 Stat: {chi2_stat:.2f}\nP-Value: {p_value:.4f}',
                    showarrow=False,
                )

                # Create bar chart for visualizing observed and expected values
                bar_chart = go.Figure()

                bar_chart.add_trace(go.Bar(x=['Group 1', 'Group 2'], y=contingency_table[0], name='Observed 1'))
                bar_chart.add_trace(go.Bar(x=['Group 1', 'Group 2'], y=contingency_table[1], name='Observed 2'))

                # Customize layout for the bar chart
                bar_chart.update_layout(
                    title='Observed Values in Each Group',
                    yaxis=dict(title='Values'),
                    barmode='group',
                )

                # Convert the plots to HTML
                table_html = table.to_html(full_html=False)
                bar_chart_html = bar_chart.to_html(full_html=False)

                # Embed the HTML in the context
                context['table'] = table_html
                context['image'] = bar_chart_html
    except Exception as e:
        # Handle other exceptions if needed
        context['error_message'] = f"An error occurred: {e}"

    context['charts']= charts
    return render(request, 'test.html',context )

