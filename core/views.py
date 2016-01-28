from itertools import izip

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
        data = {}
        classifier = DatumBox(settings.API_KEY)
        data.update({"result": classifier.sentiment_analysis(text)})
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
        for i in range(len(res.result[0])):
            print res.result[0][i]
            data.append(res.result[0][i])
        return Response(data)

    else:
        data = {}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

