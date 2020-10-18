from django.shortcuts import render
from django.db.models import Q

from .models import SmzdmShampoo


# Create your views here.

def shampoo_short(request):
    conditions = Q()
    query = request.environ.get('QUERY_STRING')
    if query:
        q = query.split('=')[1]

        conditions.connector = 'OR'
        conditions.children.append(('id__icontains', q))
        conditions.children.append(('shampoo_rank__icontains', q))
        conditions.children.append(('shampoo_name__icontains', q))
        conditions.children.append(('shampoo_evaluate__icontains', q))
        conditions.children.append(('shampoo_comments__icontains', q))
        conditions.children.append(('created_time__icontains', q))

    shampoo_objects = SmzdmShampoo.objects.filter(conditions)

    return render(request, 'index.html', locals())
