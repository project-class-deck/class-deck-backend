from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Board, BoardMembershipRequest
from .serializers import BoardMembershipRequestSerializer
from .serializers import BoardSerializer


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardMembershipRequestViewSet(viewsets.ViewSet):
    """
    보드 가입 신청과 승인을 처리하는 ViewSet
    """

    def create(self, request):
        serializer = BoardMembershipRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_membership(self, request, pk=None):
        membership_request = BoardMembershipRequest.objects.get(pk=pk)
        board = membership_request.board

        if request.user != board.owner:
            return Response({'error': 'You are not the owner of this board.'}, status=status.HTTP_403_FORBIDDEN)

        membership_request.is_approved = True
        membership_request.save()
        board.members.add(membership_request.user)
        return Response({'status': 'membership approved'})