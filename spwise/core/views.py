from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Expense, Group

@api_view(['POST'])
def create_user_profile(request):
    print("HERE")
    print(request.data)
    user_name = request.data['user_name']
    email = request.data['email']
    password = request.data['password']
    
    print(user_name,email,password)
    try:
        user = User(user_name = user_name,email = email,password = password)
        user.save()
        print("here")
        return Response({ "id" : user.id, "name" : user.user_name, "amount" :user.amount,"email":user.email})
    except Exception as e:
        print(e)
        return Response({"error":"Bad data"})

@api_view(['POST'])    
def get_user(request):
    id = request.data['user_id']
    try:
        user = User.objects.filter(id = id)
        return Response({ "id" : user[0].id, "name" : user[0].user_name, "amount" :user[0].amount,"email":user[0].email})
    except Exception as e: 
        print(e)
        return Response({"error" : "Bad data requested"})

@api_view(['POST'])
def login_user(request):
    user_name = request.data['user_name']
    password = request.data['password']

    try:
        user = User.objects.filter(user_name = user_name,password = password)
        if(len(user)):
            return Response({"id" : user[0].id,"name" : user[0].user_name,"balance":user[0].amount})
        else:
            return Response({"id" : "-1"})

    except Exception as e:
        print(e)
        return Response({"error" : "Bad data requested"})

@api_view(['POST'])
def api_login(request):
    user_name = request.data['user_name']
    #password = request.data['password']

    try:
        user = User.objects.filter(user_name = user_name)
        if(len(user)):
            return Response({"id" : user[0].id,"name" : user[0].user_name,"balance":user[0].amount})

        else:
            us = User(user_name = user_name,password = "OAUTH2.0")
            us.save()

            return Response({ "id" : us.id, "name" : us.user_name, "amount" :us.amount,"email":us.email})


    except Exception as e:
        print(e)
        return Response({"error" : "Bad data requested"})


@api_view(['POST'])
def return_groups(request):
    user_name = request.data['user_name']

    try:
        user = User.objects.filter(user_name = user_name)
        groups = groups.objects.filter(user_name = user_name)

        return Response({id:,group.id});

    except Exception as e:
        print(e)


@api_view(['POST'])
def create_expense(request):
    des = request.data['desc']
    amount = request.data['amount']
    payer_name = request.data['payer']
    participants = request.data['participants']

@api_view(['POST'])
def simplify(request):
    user_id = request.data['user_id']
    group_id = request.data['group_id']

    am = []
 
    for u in user.objects.get(id = user_id):
        am.append(u.balance)


    return Response({100:ok})

    
   

@api_view(['POST'])
def create_group(request):
    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)