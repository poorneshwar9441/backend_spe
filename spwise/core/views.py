from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Expense, Group,amount
from decimal import Decimal

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
def simplify(request):
    pass


# format {'payer' : , 'group_id' : , 'participants' : , 'amount' , des : ''}
#{"payer" : "name" , "group_id" : "2" , "participants" : ["name", "pass"], "des" : "for fun", "amount": "250"}
@api_view(['POST'])
def create_expense(request):

    payer = request.data['payer']
    group_id = request.data['group_id']
    participants = request.data['participants']

    val = request.data['amount']
    des  = request.data['des']

    try:
        user = User.objects.filter(user_name = payer)
        group = Group.objects.filter(id = group_id)
        actual_amo = amount.objects.filter(group__id = group_id, user__id = user[0].id)
        if(len(actual_amo)):
            actual_amo[0].value += Decimal(val)
            actual_amo[0].save()
        else:
            new_amount = amount(user = user[0],group = group[0])
            new_amount.value = Decimal(val)
            new_amount.save()
            
        for p in participants:
            user = User.objects.filter(user_name = p)
            actual_amo = amount.objects.filter(group__id = group_id, user__id = user[0].id)
            if(len(actual_amo)):
                actual_amo[0].value -= Decimal(val)/len(participants)
            else:
                print("expense exists already")
                new_amount = amount(user = user[0],group = group[0])
                new_amount.value = -1*Decimal(val)/(len(participants))
                new_amount.save()

        e = Expense(description = des,amount = val,payer = user[0],group = group[0])
        e.save()
        for p in participants:
            user  = User.objects.filter(user_name = p)
            e.participants.add(user[0])
            e.save()

        return Response({"transaction created sucessfully" : {
            "id" : e.id
        }})

    except Exception as e:
        print(e)
        return Response({"error" : "Bad data requested"})

#{"group_id" : ""}
#example {"group_id" : "2"}
@api_view(['POST']) 
def return_expenses(request):
    group_id = request.data['group_id']
    try:
        dic = {} 
        groups_part_of = Expense.objects.filter(group__id = group_id)
        
        for i in groups_part_of:
            dic[i.id] = {
                'id' : f'{i.id}',
                'name': f'{i.description}'
            }
        return Response(dic) 
    
    except Exception as e:
        print(e)
        return Response({"error" : "bad data requested"})

def simplify_balances(net_balances):
    simplified_debts = []

    while net_balances:
        # Find non-zero balances
        non_zero_balances = {k: v for k, v in net_balances.items() if v != 0}

        if not non_zero_balances:
            break  # Exit the loop if all balances are zero

        payer = min(non_zero_balances, key=non_zero_balances.get)
        payee = max(non_zero_balances, key=non_zero_balances.get)

        amount_settled = min(abs(net_balances[payer]), abs(net_balances[payee]))

        # Ensure debtor and creditor are not the same
        if payer != payee:
            simplified_debts.append({"debtor": payer, "creditor": payee, "amount": amount_settled})

            net_balances[payer] += amount_settled
            net_balances[payee] -= amount_settled

            # Remove zero balances
            net_balances = {k: v for k, v in net_balances.items() if v != 0}
        else:
            break

    return simplified_debts





#example {group_id : 14}
@api_view(['POST'])
def simplify(request):
    print("Here")
    print(request.data)
    group_id = request.data['group_id']
    try:
        group =  Group.objects.filter(id = group_id)
        group_members = group[0].members.all()
        dic = {}

        for mem in group_members:

            a = amount.objects.filter(user__id = mem.id,group__id = group[0].id)
            if(len(a)):
                dic[mem.user_name] = a[0].value
            else:
                dic[mem.user_name] = 0

        result = simplify_balances(dic)


        count = 1
        json_dic = {}
        for val in result:
            json_dic[count] = val
            count += 1


        return Response(json_dic)


    except Exception as e:
        print(e)
        return Response({"Error" : "Bad data Requested"})