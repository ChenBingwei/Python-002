from django.shortcuts import render
from django.db.models import Q

from .models import TheEightHundred


# Create your views here.

def movie_short(request):
    conditions = Q()
    conditions.add(('star__gte', 3), 'AND')
    # condtions = {'star__gte': 3}

    query = request.environ.get('QUERY_STRING')
    if query:
        temp = Q()
        q = query.split('=')[1]
        temp.connector = 'OR'
        temp.children.append(('comment__icontains', q))
        temp.children.append(('star__icontains', q))
        temp.children.append(('time__icontains', q))
        conditions.add(temp, 'AND')
    shorts_gte_3 = TheEightHundred.objects.filter(conditions)

    return render(request, 'index.html', locals())
