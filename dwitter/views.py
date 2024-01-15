from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Dweet, Profile
from .permissions import IsOwnerOrReadOnly
from .serializers import DweetSerializer, ProfileSerializer, RegisterSerializer


@api_view(['POST'])
def register(request):
    """Allows for the creation of new users."""
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.POST or None)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        """Returns a list of all users."""
        users = Profile.objects.all()
        serializer = ProfileSerializer(users, many=True)
        return Response({"data": serializer.data, "results": len(serializer.data)}, status=200)

    @action(detail=True)
    def dweets(self, request, pk=None):
        """Returns a list of all dweets created by the user specified in the path."""
        try:
            profile = Profile.objects.get(id=pk)
            dweets = Dweet.objects.filter(user=pk)
            serializer = DweetSerializer(dweets, many=True)
            return Response({"data": serializer.data, "results": len(serializer.data)}, status=200)
        except Profile.DoesNotExist:
            return Response({"Error": "The profile does not exist"}, status=404)

    @action(detail=False)
    def all_followed(self, request, *args, **kwargs):
        """Returns a list of all dweets from users followed by the current user."""
        if request.user.is_authenticated is False:
            return Response({"Error": "Unauthorized"}, status=401)
        dweets = Dweet.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by('-created_at')
        serializer = DweetSerializer(dweets, many=True)
        return Response({"data": serializer.data, "results": len(serializer.data)}, status=200)

    @action(detail=True)
    def followers(self, request, pk=None):
        """Returns a list of users the specified user ID is followed by."""
        try:
            follower_ids = Profile.objects.filter(id=pk).values_list('followed_by', flat=True)
            followers = Profile.objects.filter(pk__in=follower_ids)
            serializer = ProfileSerializer(followers, many=True)
            return Response({"data": serializer.data, "results": len(serializer.data)}, status=200)
        except Profile.DoesNotExist:
            return Response({"Error": "The profile does not exist"}, status=404)

    @action(detail=True)
    def following(self, request, pk):
        """Returns a list of users the specified user ID is following."""
        try:
            following_ids = Profile.objects.filter(id=pk).values_list('follows', flat=True)
            following = Profile.objects.filter(pk__in=following_ids)
            serializer = ProfileSerializer(following, many=True)
            return Response({"data": serializer.data, "results": len(serializer.data)}, status=200)
        except Profile.DoesNotExist:
            return Response({"Error": "The profile does not exist"}, status=404)

    @following.mapping.post
    def post_following(self, request, pk=None):
        """Allows the requesting user to follow the user specified in the path."""
        try:
            profile_to_follow = Profile.objects.get(id=pk)
            current_user_profile = request.user.profile
            current_user_profile.follows.add(profile_to_follow)
            current_user_profile.save()
            return Response({"data": {"following": True}}, status=200)
        except Profile.DoesNotExist:
            return Response({"Error": "The profile does not exist"}, status=404)

    @following.mapping.delete
    def delete_following(self, request, pk=None):
        """Allows the requesting user to unfollow the user specified in the path."""
        try:
            profile_to_follow = Profile.objects.get(id=pk)
            current_user_profile = request.user.profile
            current_user_profile.follows.remove(profile_to_follow)
            current_user_profile.save()
            return Response({"data": {"following": False}}, status=200)
        except Profile.DoesNotExist:
            return Response({"Error": "The profile does not exist"}, status=404)


class DweetViewSet(viewsets.ModelViewSet):
    queryset = Dweet.objects.all()
    serializer_class = DweetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        """Creates a new dweet for the current user."""
        serializer = DweetSerializer(data={'user': request.user.id, 'body': request.data.get('body')})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Updates the body of the dweet corresponding to the id specified in the path,
        if the requesting user is the dweet's creator."""
        try:
            dweet = Dweet.objects.get(id=pk)
            body = request.data.get('body')
            if dweet.user == request.user:
                dweet.body = body
                if dweet.body is None:
                    return Response({"Error": "body: [This field may not be null.]"}, status=400)
                dweet.save()
                return Response({"Success": "The post was successfully updated"}, status=200)
            else:
                return Response({"Error": "Unauthorized"}, status=401)
        except Dweet.DoesNotExist:
            return Response({"Error": "The dweet does not exist"}, status=404)

    def destroy(self, request, pk=None):
        """Deletes the dweet corresponding to the id specified in the path,
        if the requesting user is the dweet's creator."""
        try:
            dweet = Dweet.objects.get(id=pk)
            if dweet.user == request.user:
                dweet.delete()
                return Response(status=204)
            else:
                return Response({"Error": "Unauthorized"}, status=401)
        except Dweet.DoesNotExist:
            return Response({"Error": "The dweet does not exist"}, status=404)
