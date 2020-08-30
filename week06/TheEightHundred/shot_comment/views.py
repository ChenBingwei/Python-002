from django.shortcuts import render
from django.db.models import Q

from .models import TheEightHundred


# Create your views here.

def movie_short(request):
    conditions = Q()
    conditions.add(('star__gte', 3), 'AND')

    query = request.environ.get('QUERY_STRING')
    if query:
        q = query.split('=')[1]

        temp = Q()
        temp.connector = 'OR'
        temp.children.append(('id__icontains', q))
        temp.children.append(('comment__icontains', q))
        temp.children.append(('star__icontains', q))
        temp.children.append(('time__icontains', q))

        conditions.add(temp, 'AND')
    shorts_gte_3 = TheEightHundred.objects.filter(conditions)

    return render(request, 'index.html', locals())
