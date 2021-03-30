from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from tiaApp.models import OrderProductsF, ProductsF, DepartmentsF, OrdersF
import pandas as pd
import json

# Create your views here.

order_products = pd.DataFrame(list(OrderProductsF.objects.all().values()))
products = pd.DataFrame(list(ProductsF.objects.all().values()))
orders = pd.DataFrame(list(OrdersF.objects.all().values()))
departmentsPD = pd.DataFrame(list(DepartmentsF.objects.all().values()))
prodXorderProd = products.merge(order_products)
prodXorderProd['Gain'] = (prodXorderProd['quantity'] * prodXorderProd['price']) * prodXorderProd['margin']
prodXorderProd['Sales'] = (prodXorderProd['quantity'] * prodXorderProd['price'])
prodDepart = prodXorderProd.merge(departmentsPD)
generalDF = prodXorderProd.merge(orders)



def indicators(request):
    ticketPromedio = round(prodXorderProd['Sales'].sum() / prodXorderProd['order_id'].count(),2)
    margenPromedio = round(prodXorderProd['margin'].mean() * 100,2)
    cantProdMean = round(order_products['quantity'].mean(), 2)
    response = json.dumps({
        'ticketPromedio':ticketPromedio,
        'margenPromedio':margenPromedio,
        'cantProdMean':cantProdMean
    })
    # qs_json = serializers.serialize('json', qs)
    return HttpResponse(response, content_type ="application/json")

def getDepartments(request):
    departments =  departmentsPD.loc[:,['department']]
    departments_list = departments['department'].values.tolist()
    response = json.dumps({
        'departments':departments_list
    })

    return HttpResponse(response, content_type ="application/json")


def top5(request, depart='frozen'):
    top5 = (prodDepart.groupby(['department','product_name'])['quantity'].sum()).sort_values(ascending = False)
    # depa = request.query_params.get('department')
    top5 = top5[depart].head().to_frame().reset_index()
    list_aux = top5.values.tolist()
    top_5 = []
    for i in range (len(list_aux)):
        response = {
            'Product Name':list_aux[i][0],
            'Quantity Sold':list_aux[i][1],
        }
        top_5.append(response)
    data = json.dumps({
        'data':top_5
    })

    return HttpResponse(data,content_type ="application/json")

def departmentTotalEarnings(request):
    departmentTotalEarnings = (prodDepart.groupby('department')['Sales'].sum()).sort_values(ascending = False)
    departmentTotalEarnings = departmentTotalEarnings.to_frame().reset_index()

    productsTotalEarnings =  (prodDepart.groupby(['department','product_name'])['Sales'].sum()).sort_values(ascending = False)
    productsTotalEarnings = productsTotalEarnings.to_frame().reset_index()

    groupTable = productsTotalEarnings.merge(departmentTotalEarnings, on='department', how='inner')
    groupTable.columns=['Department','Product Name','Product Earning','Department Earning']
    groupTable = groupTable[['Department','Department Earning','Product Name','Product Earning']]
    groupTable = groupTable.values.tolist()
    list_response = []
    for i in range (len(groupTable)):
        response = {
            'Department':groupTable[i][0],
            'Department Earning':"${:,.2f}".format(round(groupTable[i][1],3)),
            'Product Name':groupTable[i][2],
            'Product Earning':"${:,.2f}".format(round(groupTable[i][3],3)),
        }
        list_response.append(response)
    data = json.dumps({
        'data':list_response
    })

    return HttpResponse(data, content_type ="application/json")

def timeLine(request):
    df = generalDF.groupby('order_hour_of_day').agg({'Sales':'sum','Gain':'sum'}).round(2)
    df = df.reset_index()
    response = json.dumps({
        'hours':df['order_hour_of_day'].tolist(),
        'sales':df['Sales'].tolist(),
        'gain':df['Gain'].tolist()
    })

    return HttpResponse(response, content_type ="application/json")
