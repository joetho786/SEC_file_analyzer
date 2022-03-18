from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import Company


def index(request):
    return HttpResponse(" ")
# Create your views here.


def upload(request):
    if request.method == 'POST':
        file = request.FILES['files']
        path = file.file
        dataFrame = pd.read_csv(path)
        for line in dataFrame.values.tolist():
            Company.objects.create(
                cik=line[0],
                ticker=line[1],
                company=line[2],
            )

    return render(request, 'import_csv.html')
