from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Elevator,Request
from .serializers import ElevatorInitializationSerializer,RequestSerializer,ElevatorSerializer

# Create your views here.

class ElevatorInitializationViewSet(viewsets.ViewSet):
    """
    To create elevator system with given number of elevators
    """
    def create(self, request):
        serializer = ElevatorInitializationSerializer(data=request.data)
        if serializer.is_valid():
            number_of_elevators = serializer.validated_data['number_of_elevators']
            for elevator_id in range(1, number_of_elevators + 1):
                Elevator.objects.create(elevator_id=elevator_id)
            return Response({"message": f"{number_of_elevators} elevators created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    To get all the requests for a given elevator id
    """
    serializer_class = RequestSerializer
    def get_queryset(self):
        elevator_id = self.kwargs['elevator_id']
        return Request.objects.filter(elevator_id=elevator_id)


class RequestElevatorViewSet(viewsets.ModelViewSet):
    """
    request coming from user to go up or down in elevator .
    Saves user request to the list of requests for a elevator
    """
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def create(self, request):
        elevator_id = request.data.get('elevator_id')
        floor = int(request.data.get('floor'))
        direction = request.data.get('direction')

        try:
            elevator = Elevator.objects.get(elevator_id=elevator_id)
        except Elevator.DoesNotExist:
            return Response({"message": f"Elevator with ID {elevator_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Assuming the elevator has already reached the called point
        direction = direction.upper()
        if direction not in ['UP', 'DOWN']:
            return Response({"message": "Invalid direction. Use 'UP' or 'DOWN'."}, status=status.HTTP_400_BAD_REQUEST)

        if floor < elevator.current_floor:
            elevator.direction = 'DOWN'
        elif floor > elevator.current_floor:
            elevator.direction = 'UP'
        else:
            elevator.direction = 'STOP'

        elevator.destination_floor = floor
        elevator.save()

        request_obj = Request.objects.create(elevator=elevator, floor=floor, direction=direction)

        return Response(RequestSerializer(request_obj).data, status=status.HTTP_201_CREATED)
    

class ElevatorViewSet(viewsets.ModelViewSet):
    """
    Fetch if the elevator is moving up or down currently
    Fetch the next destination floor for a given elevator
    """
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer
    def retrieve(self, request, pk=None):
        elevator = self.get_object()
        status = elevator.get_current_status()
        return Response(status)

    def get_next_destination_floor(self, request, pk=None):
        print(self.get_object(),"self-----")
        elevator = self.get_object()
        next_destination_floor = elevator.get_next_destination_floor()
        return Response({"next_destination_floor": next_destination_floor})



class ElevatorMarkViewSet(viewsets.ModelViewSet):
    """
    To Mark a elevator as not working or in maintenance 
    """
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    def mark_elevator_maintenance(self, request, pk=None):
        try:
            elevator = self.get_object()
        except Elevator.DoesNotExist:
            return Response({"message": "Elevator not found."}, status=status.HTTP_404_NOT_FOUND)

        elevator.is_operational = False
        elevator.save()

        return Response({"message": f"Elevator {elevator.elevator_id} marked as not working/maintenance."}, status=status.HTTP_200_OK)
