from django.contrib import admin
from django.urls import path, include
from social_users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/search_users/<str:search_keyword>/', UserSearchView.as_view(), name='user-search'),
    path('api/send_friend_request/<int:to_user_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('api/accept_friend_request/<int:from_user_id>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('api/reject_friend_request/<int:from_user_id>/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('api/list_friends/', ListFriendsView.as_view(), name='list-friends'),
    path('api/list_pending_friend_requests/', ListPendingFriendRequestsView.as_view(), name='list-pending-friend-requests'),
]
