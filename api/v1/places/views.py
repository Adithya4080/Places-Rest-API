from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.v1.places.serializers import PlaceSerializer, PlaceDetailSerializer
from places.models import Place
from django.db.models import Q

from api.v1.places.pagination import StandardResultSetPagination


@api_view(["GET"])
@permission_classes([AllowAny])
def places(request):
    instances = Place.objects.filter(is_deleted=False)

    q = request.GET.get("q")
    if q:
        ids = q.split(",")
        instances = instances.filter(category__in=ids)

        # instances = instances.filter(Q(name__icontains=q) | Q(place__icontains=q) , is_deleted=False)
        # instances = instances.filter(category__name__icontains=q)

    paginator = StandardResultSetPagination()
    paginated_result = paginator.paginate_queryset(instances, request)

    context = {
        "request":request
    }
    # serializer = PlaceSerializer(instances, many=True, context=context)
    serializer = PlaceSerializer(paginated_result, many=True, context=context)
    response_data = {
        "status_code": 6000,
        "count" : paginator.page.paginator.count,
        "links" : {
            "next" : paginator.get_next_link(),
            "previous" : paginator.get_previous_link()
        },
        "data": serializer.data
    }

    return Response(response_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def place(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instance = Place.objects.get(pk=pk)

        context = {
            "request":request
        }
        serializer = PlaceDetailSerializer(instance, context=context)
        response_data = {
            "status_code": 6000,
            "data": serializer.data
        }

        return Response(response_data)  
      
    else:    
        response_data = {
            "status_code": 6001,
            "message": "Place not exist"
        }

        return Response(response_data)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instance = Place.objects.get(pk=pk)

        context = {
            "request":request
        }
        serializer = PlaceDetailSerializer(instance, context=context)
        response_data = {
            "status_code": 6000,
            "data": serializer.data
        }

        return Response(response_data)  
      
    else:    
        response_data = {
            "status_code": 6001,
            "message": "Place not exist"
        }

        return Response(response_data)