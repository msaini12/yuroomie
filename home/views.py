from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RoomPostForm
from .models import Room, RoomImage
from django.contrib.auth.decorators import login_required

def index(request):
    latest_posts_list = Room.objects.order_by('-last_updated')[:4]
    return render(request, 'home/index.html', {'latest_posts_list': latest_posts_list,})

def browse_rooms(request):
    rooms_list = Room.objects.all()
    paginator = Paginator(rooms_list, 2)
    page = request.GET.get('page')
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'home/browse.html', {'page': page, 'rooms': rooms})

def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    roomImages = list(room.roomimage_set.all())
    return render(request, 'home/detail.html', {'room': room, 'roomImages': roomImages})

def search(request):
    RESULTS_PER_PAGE = 2

    result_list = Room.objects.all()
    query_dict = request.GET
    context = {}
    search = True

    if 'q' in query_dict and query_dict['q'] is not "":
        query_q = context['query'] = query_dict['q']

        result_list = result_list.filter(
            Q(property_name__icontains=query_q) |
            Q(host_name__icontains=query_q) |
            Q(address__icontains=query_q) |
            Q(description__icontains=query_q)
        )
    else:
        search = False


    if 'filter' in query_dict:
        filters = context['filters'] = query_dict['filter']
        try:
            filter_dict = dict(item.split("=") for item in filters.split("~"))
            #price range high
            if 'prh' in filter_dict:
                context['prh'] = filter_dict['prh']
                result_list = result_list.filter(cost__lte=context['prh'])
            else:
                context['prh'] = 99999

            #price range low
            if 'prl' in filter_dict:
                context['prl'] = filter_dict['prl']
                result_list = result_list.filter(cost__gte=context['prl'])
            else:
                context['prl'] = 0
            
            ## uncomment when gender is added to room ##
            context['gen'] = 0
        #     #gender
        #    if 'gen' in filter_dict:
        #         context['gen'] = filter_dict['gen']
        #         result_list = result_list.filter(gender__iexact=context['gen'])
        #     else:
        #         context['gen'] = 0

            #number of garages
            if 'par' in filter_dict:
                context['par'] = filter_dict['par']
                result_list = result_list.filter(garages__exact=context['par'])
            else:
                context['par'] = 0

            #number of rooms
            if 'rms' in filter_dict:
                context['rms'] = filter_dict['rms']
                result_list = result_list.filter(number_of_rooms__exact=context['rms'])
            else:
                context['rms'] = 0

            #property type
            if 'type' in filter_dict:
                context['type'] = filter_dict['type']
                result_list = result_list.filter(property_type__exact=context['type'])
            else:
                context['type'] = 0 
            
        except ValueError:
            # do not filter, no value for all keys
            filters = None    
    else:
        context['prh'] = 99999
        context['prl'] = 0
        context['gen'] = 0
        context['par'] = 0
        context['rms'] = 0
        context['type'] = 0
        filters = None

    paginator = Paginator(result_list, RESULTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context['sf'] = 's' if search == True else ''
    context['sf'] += 'f' if filters is not None else ''
    
    context['rooms'] = rooms
    context['num_results'] = len(result_list)

    return render(request, 'home/search.html', context)

@login_required()
def create(request):
    if request.method == 'POST':
        form = RoomPostForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            # if the user added more than 4 (to be changed to 6) or no images, return the form again
            if len(request.FILES.getlist('images')) > 4 or len(request.FILES.getlist('images')) == 0:
                return render(request, 'home/create.html', {'form': form})
            
            new_room = form.save(commit=False)
            new_room.host_name = (request.user.first_name + ' ' + request.user.last_name[:1])
            # concatenate all form address inputs into one consistentLy formatted address
            address = (request.POST['address1'] + ', ')
            address += (request.POST['city'] + ', ON, ' + request.POST['postalCode'])
            new_room.address = address
            new_room.creator_id = request.user.pk
            new_room.save()
            # for each image uploaded, save it with it's parent room being the room we just created
            for i in request.FILES.getlist('images'):
                image = RoomImage(room=new_room, image=i)
                image.save()
            return HttpResponseRedirect(reverse(detail, args=(new_room.pk,)))
        else:
            print('invalid')
    else:
        form = RoomPostForm()
    return render(request, 'home/create.html', {'form': form})
