from django.urls import path
from.views import (PostAPIView, CommentAPIView, PostDeleteView, PostUpdateView,
                   CommentDeleteView, CommentUpdateView, LikeUnlikeView, UserPostReadView,
                   SearchView)

urlpatterns = [
    path('list/', UserPostReadView.as_view(), name='create-post'),
    path('search/', SearchView.as_view(), name='search'),
    path('createpost/', PostAPIView.as_view(), name='create-post'),
    path('createcomment/', CommentAPIView.as_view(), name='create-comment'),
    path('delpost/', PostDeleteView.as_view(), name='delete-post'),
    path('delcomment/', CommentDeleteView.as_view(), name='delete-comment'),
    path('updatepost/', PostUpdateView.as_view(), name='edit-post'),
    path('updatecomment/', CommentUpdateView.as_view(), name='edit-comment'),
    path('likeunlike/', LikeUnlikeView.as_view(), name='like-unlike'),

]