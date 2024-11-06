from django.urls import path

from app.apis.apis import GetAddNotesApi, LoginAPIView, LogoutApi, RefreshTokenApiview, RetrievePatchDeleteNotesApi, UserRegistrationApiView

urlpatterns = [
    path('register/', UserRegistrationApiView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/', RefreshTokenApiview.as_view()),
    path('logout/', LogoutApi.as_view()),
    path("notes/", GetAddNotesApi.as_view()),
    path("notesedit/", RetrievePatchDeleteNotesApi.as_view())
]