from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        return Response({
            'user_id': user.pk,
            'username': user.username,
            'authenticated': user.is_authenticated,
            'customer_id': user.customer_id,
        })

