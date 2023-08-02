from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ElevatorInitializationViewSet,RequestViewSet,RequestElevatorViewSet,ElevatorViewSet,ElevatorMarkViewSet,ElevatorDoorStatusViewSet
router = DefaultRouter()
router.register(r'initialize', ElevatorInitializationViewSet, basename='initialize-elevators')
router.register(r'requests/(?P<elevator_id>\d+)', RequestViewSet, basename='elevator-requests')
router.register(r'request-elevator', RequestElevatorViewSet, basename='request-elevator')

urlpatterns = [ 
    path('elevators/current-status/', ElevatorViewSet.as_view({'get': 'retrieve'}), name='get-current-status'),
    path('elevators/next-destination/', ElevatorViewSet.as_view({'get': 'get_next_destination_floor'}), name='next-destination'),
    path('elevators/mark-maintenance/', ElevatorMarkViewSet.as_view({'post': 'mark_elevator_maintenance'}), name='mark-maintenance'),
    path('elevators/door-status/', ElevatorDoorStatusViewSet.as_view({'post': 'door_status'}), name='door-status'),
]

urlpatterns += router.urls
