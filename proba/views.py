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
# Create your views here.






def lois(request):
    context = {}
    uploaded_files = UploadedFile.objects.all()
    context['uploaded_files'] = uploaded_files
    

    charts = {

              'densite':'densité de probabilité',
              'Bernoulli':'Bernoulli',
              'Binomial':'Binomial',
              'Uniforme':'Uniforme',
              'Poisson':'Poisson',
              'Loi_Normale':'Loi Normale',
              'Loi_exponentielle':'Loi exponentielle',
              't_test':'T test',
              'z_test':'Z test'

            
             }
    try:
        if request.method == 'POST':
            
            selected_chart_key = request.POST.get('selected_chart')
            print(selected_chart_key)
            # Accessing selected columns
            selected_columns = request.POST.getlist('selected_columns')
            print('Selected Columns:', selected_columns)
            
            if selected_chart_key == 'densite':
                a=0
                b=0
                print(selected_chart_key)
                print(request.POST.get('densite',''))
                # Accessing line1 and line2 inputs
                line1_value = request.POST.get('line1', 0)
                if line1_value != '':
                    line1_value = int(line1_value)
                else:
                    line1_value = 0

                line2_value = request.POST.get('line2', 0)
                if line2_value != '':
                    line2_value = int(line2_value)
                else:
                    line2_value = 0

                sigma = request.POST.get('sigma', 0)
                if sigma != '':
                    sigma = int(sigma)
                else:
                    sigma = 0

                mu = request.POST.get('mu', 0)
                if mu != '':
                    mu = int(mu)
                else:
                    mu = 0

        

                if line2_value != 0 and line1_value != 0:
                    print(line1_value)
                    a = int(line1_value) # borne inférieure
                    b = int(line2_value)
            


                print('Line 1 Value:', line1_value)
                print('Line 2 Value:', line2_value)
                
                x = np.linspace(-5, 5, 1000)
                pdf = norm.pdf(x, loc=mu, scale=sigma) #loc=moyenne, scale=écart-type
                # borne supérieure
                prob = norm.cdf(b, loc=mu, scale=sigma)- norm.cdf(a, loc=mu, scale=sigma)

                plt.plot(x, pdf, c='r', ls='-', lw=2, label='DDP')
                plt.fill_between(x, pdf, where=(x >= a) & (x <= b), alpha=0.2,
                color='blue', label=f'Probability: {prob:.4f}')
                plt.xlabel('X')
                plt.ylabel('Densité de probabilité')
                plt.legend()
                plt.grid()

                plt.show()
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                plt.close()
                buffer.close()
                

                # Encode the image as base64
                graph = base64.b64encode(image_png).decode()
                context['image'] = graph

            if selected_chart_key == 'Bernoulli':
                
                print(request.POST)
                
                size = request.POST.get('sizeb', 0)
                print(size)
                if size != '':
                    size = int(size)
                    print("hello")
                else:
                    size = 0

                pro = request.POST.get('prob', 0)
                print(pro)
                if pro != '':
                    pro = float(pro)
                else:
                    pro = 0

                # figX = request.POST.get('figX', 0)
                # if figX != '':
                #     figX = int(figX)
                # else:
                #     figX = 0

                # figY = request.POST.get('figY', 0)
                # if figY != '':
                #     figY = int(figY)
                # else:
                #     figY = 0

                data_bern = bernoulli.rvs(size=size, p=pro) #p=0.6 --> donc 1-p = 0.4
                plt.figure(figsize=(6,4))
                ax = sb.histplot(data_bern, kde=True, stat='probability')

                ax.set(xlabel='Bernoulli', ylabel='Probabilité')
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                plt.close()
                buffer.close()
                

                # Encode the image as base64
                graph = base64.b64encode(image_png).decode()
                context['image'] = graph

            if selected_chart_key == 'Binomial':
            
            
                size = request.POST.get('sizebi', 0)
                if size != '':
                    size = int(size)
                else:
                    size = 0

                pro = request.POST.get('probi', 0)
                if pro != '':
                    pro = float(pro)
                else:
                    pro = 0
                
                essais = request.POST.get('essais', 0)
                if essais != '':
                    essais = int(essais)
                else:
                    essais = 0
                
                position = request.POST.get('position', 0)
                if position != '':
                    position = int(position)
                else:
                    position = 0

            

                plt.figure(figsize=(6,4))
                data_binom = binom.rvs(n=essais,p=pro,loc=position,size=size)
                ax = sb.histplot(data_binom, kde=True, stat='probability')
                ax.set(xlabel='Binomial', ylabel='Probabilité')
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                plt.close()
                buffer.close()
                

                # Encode the image as base64
                graph = base64.b64encode(image_png).decode()
                context['image'] = graph

            if selected_chart_key == 'Uniforme':

            
                size = request.POST.get('sizeuni', 0)
                if size != '':
                    size = int(size)
                else:
                    size = 0

            
                scale = request.POST.get('scaleuni', 0)
                if scale != '':
                    scale = float(scale)
                else:
                    scale = 0
                
                position = request.POST.get('positionuni', 0)
                if position != '':
                    position = float(position)
                else:
                    position = 0

            

                data_unif = uniform.rvs(loc=position, scale=scale, size=size) ## loc=a, b=loc+scale
                plt.figure(figsize=(6,4))
                ax = sb.histplot(data_unif, kde=True, stat='probability')
                ax.set(xlabel='Uniforme', ylabel='Probabilité')
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                plt.close()
                buffer.close()
                

                # Encode the image as base64
                graph = base64.b64encode(image_png).decode()
                context['image'] = graph

            if selected_chart_key == 'Poisson':

            
                size = request.POST.get('sizepo', 0)
                if size != '':
                    size = int(size)
                else:
                    size = 0

            
                mu = request.POST.get('mupo', 0)
                if mu != '':
                    mu = float(mu)
                else:
                    mu = 0
                
                data_binom = poisson.rvs(mu=mu, size=size)
                plt.figure(figsize=(6,4))
                ax = sb.histplot(data_binom, kde=True, stat='probability')
                ax.set(xlabel='Poisson', ylabel='Probabilité')

                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                plt.close()
                buffer.close()
                

                # Encode the image as base64
                graph = base64.b64encode(image_png).decode()
                context['image'] = graph

            if selected_chart_key == 'Loi_exponentielle':

            
                size = request.POST.get('sizeex', '')
                if size != '':
                    size = int(size)
                    print(size)


                else:
                    size = 0

            
                scale = request.POST.get('scaleex', '')
                if scale != '':
                    scale = int(scale)
                    print(scale)
                else:
                    scale = 0
                    print(scale)

                
        

            
                data = expon.rvs(scale=scale, size=size)
                sb.histplot(data, kde=True)
                sb.kdeplot(data, fill=True)



                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                plt.close()
                buffer.close()
                

                # Encode the image as base64
                graph = base64.b64encode(image_png).decode()
                context['image'] = graph

            if selected_chart_key == 'Loi_Normale':

            
                size = request.POST.get('sizeno', 0)
                if size != '':
                    size = int(size)
                else:
                    size = 0

            
                scale = request.POST.get('scaleno', 0)
                if scale != '':
                    scale = float(scale)
                else:
                    scale = 0
                
        
                mu = request.POST.get('muno', 0)
                if mu != '':
                    mu = float(mu)
                else:
                    mu = 0
                
            

                data = norm.rvs(loc=mu,scale=scale, size=size)
                sb.histplot(data, kde=True)
                sb.kdeplot(data, fill=True)



                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                plt.close()
                buffer.close()
                

                # Encode the image as base64
                graph = base64.b64encode(image_png).decode()
                context['image'] = graph

            if selected_chart_key == 't_test':
                print("hellllllllllo")
                np.random.seed(42)
                data1 = np.random.normal(loc=0, scale=1, size=100)
                data2 = np.random.normal(loc=0.5, scale=1, size=100)

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

                np.random.seed(42)
                data1 = np.random.normal(loc=0, scale=1, size=100)
                data2 = np.random.normal(loc=0.5, scale=1, size=100)

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
    except Exception as e:
        # Handle other exceptions if needed
        context['error_message'] = f"An error occurred: {e}"

    context['charts']= charts
    return render(request, 'lois.html',context )

