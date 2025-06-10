from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from .models import ChitFund
from .serializers import ChitFundSerializer, ChitFundSummarySerializer


class ChitFundCreateView(generics.CreateAPIView):
    queryset = ChitFund.objects.all()
    serializer_class = ChitFundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chitfund = serializer.save(host=self.request.user)
        chitfund.members.add(self.request.user)  # Automatically add host to members


# Hosted
class HostedFundsView(generics.ListAPIView):
    serializer_class = ChitFundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChitFund.objects.filter(host=self.request.user)

# Joined
class JoinedFundsView(generics.ListAPIView):
    serializer_class = ChitFundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.funds_joined.all()


class StartChitFundView(generics.UpdateAPIView):
    queryset = ChitFund.objects.all()
    serializer_class = ChitFundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(is_active=True)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import ChitFund

class JoinChitFundView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get("invite_token")
        try:
            fund = ChitFund.objects.get(invite_token=token)
        except ChitFund.DoesNotExist:
            return Response({"error": "Invalid invite token"}, status=status.HTTP_404_NOT_FOUND)

        if fund.is_active:
            return Response({"error": "Fund has already started"}, status=status.HTTP_400_BAD_REQUEST)

        if fund.has_reached_capacity():
            return Response({"error": "Fund is full"}, status=status.HTTP_400_BAD_REQUEST)

        fund.members.add(request.user)
        return Response({"message": "Successfully joined the chit fund"}, status=status.HTTP_200_OK)


class UserHomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Funds hosted by this user
        funds_hosted = ChitFund.objects.filter(host=user)
        hosted_serializer = ChitFundSummarySerializer(funds_hosted, many=True)

        # Funds joined by user but not hosted by them
        funds_joined = ChitFund.objects.filter(members=user).exclude(host=user)
        joined_serializer = ChitFundSummarySerializer(funds_joined, many=True)

        return Response({
            "funds_hosted": hosted_serializer.data,
            "funds_joined": joined_serializer.data
        })