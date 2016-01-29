import ast

from itertools import izip

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mlapi.DatumBox import DatumBox
from monkeylearn import MonkeyLearn


# Create your views here.
def index(request):
    return render(request, 'core/index.html')


@api_view(['GET', 'POST'])
def classify(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        text = request.POST.get('text')
        newtext = text.encode('ascii', 'ignore')
        data = {}
        classifier = DatumBox(settings.API_KEY)
        data.update({"result": classifier.sentiment_analysis(newtext)})
        return Response(data)

    else:
        data = {}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def entities(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'POST':
        text = request.POST.get('text')
        data = []
        ml = MonkeyLearn(settings.MONKEYLEARN_API_KEY)
        text_list = [text]
        module_id = settings.MONKEYLEARN_MODULE_ID
        res = ml.extractors.extract(module_id, text_list)
        print(res.result)
        for i in range(len(res.result[0])):
            data.append(convert(res.result[0][i]))
        # data.append({'count': 1, 'tag': 'ORGANIZATION', 'entity': 'About Data Respons Data Respons'})
        # data.append({'count': 1, 'tag': 'ORGANIZATION', 'entity': 'Oslo Stock Exchange'})
        # data.append({'count': 3, 'tag': 'PERSON', 'entity': 'Ragnvaldsen'})
        data.append({"message":text})
        return Response(data)

    else:
        data = {}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input