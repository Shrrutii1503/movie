from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    text = "<h1>Welcome To Adam's Movie Rental Store</h1>"
    return HttpResponse(text)


def all():
    items = []
    with open('./movies/customers.csv','r') as f:
        for line in f.readlines():
            item = {}
            info = (line.rstrip().split(','))
            item['id'] = info[0]
            item['name'] = info[1]
            item['age'] = info[2]
            item['pincode'] = info[3]
            if len(info) == 5:
                movie_str = "" 
                for i in info[4].split('-')[1:]:
                    movie_str += diary()[int(i)]['movie_name'] + ", "
                item['rented_cd'] = movie_str[:-2]
            items.append(item)
    return items

def all_movies():
    pass

def get_all(req):
    items = all()
    return render(req,'movies/welcome.html',{'cart':items})

def format_for_write(items):
    write_str = ''
    for item in items:
        write_str += item['id'] + ',' +item['name'] + ',' +item['age'] + ',' +item['pincode']+'\n'
    return(write_str.rstrip())

def delete_item(req,id):
    items = all()
    new_items = list(filter(lambda x:x['id']!= id,items))
    wformat = format_for_write(new_items)

    with open('./movies/customers.csv', 'w+') as f:
        f.write(wformat)
    return HttpResponse('Successfully Deleted')

def diary():
    registers = []
    with open('./movies/movies.csv','r') as f:
        for line in f.readlines():
            register = {}
            info = (line.rstrip().split(','))
            register['movie_id'] = info[0]
            register['movie_name'] = info[1]
            register['in_stock'] = info[2]
            registers.append(register)
    return registers

#def rent(req):
    #registers = diary()
    #return render(req, 'movies/movie.html',{'cart':registers})

def diary_for_write(registers):
    write_str = ''
    for register in registers:
        write_str += register['movie_id'] + ',' +register['movie_name'] + ',' +register['in_stock']+'\n'
    return(write_str.rstrip())
    
def rent_movie(req,id):
    registers = diary()
    return render(req,'movies/movies.html',{'cart':registers, 'id': id})

def rent(req,id,movie_id):
    user_id = id
    movie_id = movie_id

    # Getting all the movies
    registers = []
    with open('./movies/movies.csv','r') as f:
        for line in f.readlines():
            register = {}
            info = (line.rstrip().split(','))
            register['movie_id'] = info[0]
            register['movie_name'] = info[1]
            register['in_stock'] = info[2]
            registers.append(register)

    if(movie_id >= len(registers)):
        return render(req,'movies/movie.html',{'id':user_id, 'movie_id':movie_id, 'error':'Movie with this id doesnt exist', 'movie_name': registers[movie_id]})

    # Getting all customers
    customers = []
    with open('./movies/customers.csv','r') as f:
        for line in f.readlines():
            customer = {}
            info = (line.rstrip().split(','))
            customer['id'] = info[0]
            customer['name'] = info[1]
            customer['age'] = info[2]
            customer['pincode'] = info[3]
            if len(info) == 5:
                customer['rented_cd'] = info[4] 
            else:
                customer['rented_cd'] = "" 
            customers.append(customer)

    if(user_id >= len(customers)):
        return render(req,'movies/movie.html',{'id':user_id, 'movie_id':movie_id, 'error':'User with this id doesnt exist', 'movie_name': registers[movie_id]})


    # Checking if we have stock of selected movie
    if int(registers[movie_id]['in_stock']) > 0:
        registers[movie_id]['in_stock'] = str(int(registers[movie_id]['in_stock'])-1)
    else:
        return render(req,'movies/movie.html',{'id':user_id, 'movie_id':movie_id, 'cart':registers, 'error': registers[movie_id]['movie_name'] + ' is Out Of Stock', 'movie_name': registers[movie_id]})

    # Updating the .csv file decremented by 1
     
    # # Creating the CSV string id,name,stocl 
    write_str = ''
    for register in registers:
        write_str += register['movie_id'] + ',' +register['movie_name'] + ',' + register['in_stock'] + '\n'

    ## Writing the CSV String
    with open('./movies/movies.csv', 'w') as f:
        f.write(write_str)

    print('rented cd', customers[user_id]['rented_cd'])

    customers[user_id]['rented_cd'] += "-"+str(movie_id)

    # if customers[user_id].get('rented_cd'):
    #     customers[user_id]['rented_cd'] += "-"+str(movie_id)
    # else:
    #     print("bere")
    #     customers[user_id]['rented_cd'] = str(movie_id)

    print(customers[user_id])

    write_str = ''
    for customer in customers:
        if customer.get('rented_cd'):
            write_str += customer['id'] + ',' +customer['name'] + ',' + customer['age'] + ',' +  customer['pincode'] + ',' + customer['rented_cd'] + '\n'
        else:
            write_str += customer['id'] + ',' +customer['name'] + ',' + customer['age'] + ',' +  customer['pincode'] + '\n'

    with open('./movies/customers.csv', 'w') as f:
        f.write(write_str)


    print(write_str)
    
    return render(req,'movies/movie.html',{'id':user_id, 'movie_id':movie_id, 'cart':registers, 'movie': registers[movie_id]})

def add_movie(req):
    movie_id = req.GET.get('registers.movie_id')
    print(movie_id)
    movie_name = req.GET.get('registers.movie_name')
    return HttpResponse("successfully added")
    movie_avail = request.GET.get('data.available', 'n/a')
    with open('movies/movie.csv', 'a+') as f:
        f.write('\n' + "{}, {}, {}".format(movie_id, movie_name, movie_avail))
        return HttpResponse('Successfully Added! <a href="/movies/add_movie/add_movie?movie_id={{data.id}}&movie_name={{data.name}}&movie_avail={{data.available}}"> Back To movies </a>')
