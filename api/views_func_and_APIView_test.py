from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView


@api_view(['GET', 'POST'])
@throttle_classes([UserRateThrottle])
def hello(request):
    if request.method == 'POST':
        return Response({'message': f'Привет {request.data}'})
    return Response({'message': 'Привет, мир!'})


class ExampleView(APIView):
    #  класс UserRateThrottle; и для этого view-класса сработает лимит "10000/day" для залогиненных пользователей,
    #  объявленный в settings.py
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        text = {
            'hello': 'world'
        }
        return Response(text)
