from django.shortcuts import render
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import urllib, base64
from django.contrib import messages

# Create your views here.

share = ''
numofdays = 0

def index(request):
    #share = request.POST.get('share_name')
    #numofdays = request.POST.get('numberofdays')
    #if share is not None:
     #   getgraph(request, share, numofdays)
    response = render(request, 'index.html')
    return response

def getgraph(request):
    share = request.POST.get('share_name')
    numofdays = int(request.POST.get('numberofdays'))
    if numofdays < 2:
        messages.error(request, 'Number of days should be greater than 1')
        return render(request, 'index.html')
    end_date = datetime.today()
    start_date = end_date - timedelta(days=numofdays)
    data = yf.download(share, start_date , end_date)
    if data.empty:
        messages.error(request, 'Please enter a valid ticker.')
        return render(request, 'index.html')
    plt.plot(data['Close'], color = "black", label=f"Share Price")
    plt.title(f"{share} Share Price")
    plt.xlabel("Time")
    plt.ylabel(f"{share} Share Price")
    plt.legend()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    html = '<img src = "%s"/>' % uri
    content = {'graph': html}
    plt.close()
    return render(request, 'displayplot.html', content)