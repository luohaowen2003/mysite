from django.shortcuts import render
import json

from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


from django.http import HttpRequest, JsonResponse
from .models import *
from django.forms.models import model_to_dict

def question_detail(req: HttpRequest, qid: int):
    res = Question.objects.filter(id=qid).first()
    if res:
        return JsonResponse({
            "code": 0,
            "data": {
                **model_to_dict(res),
                "choices": [
                    model_to_dict(ch, exclude=["question"])
                    for ch in res.choice_set.all()
                ]
            }
        })
    else:
        return JsonResponse({
            "code": -1
        }, status=404)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def vote(req: HttpRequest):
    info = json.loads(req.body)
    try:
        qid = info["qid"]
        cid = info["cid"]
        ch = Choice.objects.get(pk=cid)
        if ch.question.id != qid:
            raise ValueError("Mismatched question and choice pair")
        ch.votes += 1
        ch.save()
        return JsonResponse({
            "code": 0,
            "choices": [
                model_to_dict(ch, exclude=["question"])
                for ch in Choice.objects.filter(question__id=qid)
            ]
        }) 
    except:
        raise
        return JsonResponse({
            "code": -1
        }, status=400)
