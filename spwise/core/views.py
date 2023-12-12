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
        return Response({ "id" : user.id, "name" : user.user_name,"email":user.email})
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


#{'user_id' : '', group_name : ''}; 
@api_view(['POST'])
def create_group(request):
    user_id = request.data['user_id']
    group_name = request.data['group_name']
    
    try:
        user = User.objects.filter(id = user_id); 
        group = Group(name = group_name); 
        group.save(); 
        group.members.add(user[0]); 
        
        return Response({'Group creation scucees' : f'Group id {group.id}'})
        
        
    except Exception as e:
        print(e)
        return Response({"error" : "Bad data requested"})

@api_view(['POST'])
def return_groups(request):
    user_id = request.data['user_id']
    
    try:
        dic = {} 
        groups_part_of = Group.objects.filter(members__id = user_id)
        
        for i in groups_part_of:
            dic[i.id] = {
                'id' : f'{i.id}',
                'name': f'{i.name}'
            }
            
        
        return Response(dic) 
    
    except Exception as e:
        print(e)
        return Response({"error" : "bad data requested"})

#update the group with new user
@api_view(['POST'])  
def update_group(request):
    user_name = request.data['user_name']
    group_id = request.data['group_id']

    try:
        group = Group.objects.filter(id = group_id)
        user = User.objects.filter(user_name = user_name)
        
        group[0].members.add(user[0])
        
        return Response({"success" : "user added sucessfully"})
        
    except Exception as e:
        print(e)
        return Response({"error" : "bad data requested"})
        
    
@api_view(['POST'])
def create_expense(request):
    payer = request.data['payer_name']
    
def update_expense(request):
    pass
@api_view(['POST'])
def return_expense(request):
    pass
    

    

    
    
    
