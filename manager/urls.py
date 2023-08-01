from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ElevatorInitializationViewSet,RequestViewSet,RequestElevatorViewSet,ElevatorViewSet,ElevatorMarkViewSet

router = DefaultRouter()
router.register(r'initialize', ElevatorInitializationViewSet, basename='initialize-elevators')
router.register(r'requests/(?P<elevator_id>\d+)', RequestViewSet, basename='elevator-requests')
router.register(r'request-elevator', RequestElevatorViewSet, basename='request-elevator')
router.register(r'elevatormark/(?P<elevator_id>\d+)', ElevatorMarkViewSet)
urlpatterns = [ 
    path('elevators/<int:pk>/current-status/', ElevatorViewSet.as_view({'get': 'retrieve'}), name='get-current-status'),
    path('elevators/<int:pk>/next-destination/', ElevatorViewSet.as_view({'get': 'get_next_destination_floor'}), name='next-destination'),
    path('elevators/<int:pk>/mark-maintenance/', ElevatorMarkViewSet.as_view({'post': 'mark_elevator_maintenance'}), name='mark-maintenance'),
]
# router.register(r'elevators/(?P<elevator_id>\d+)', ElevatorViewSet, basename='next-destination')
urlpatterns += router.urls
