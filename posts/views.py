from .models import Post, Comment, Like
from .forms import PostModelForm, CommentModelForm
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import PostSerializer, CommentSerializer

from django.http import JsonResponse


# Create your views here.

class PostAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = PostSerializer

    def post(self, request):
        p_form = PostModelForm(request.POST, request.FILES)
        # print(request.POST)
        # print(request.user)
        output = {}
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = request.user
            instance.save()
            output['result'] = "Success"
            output['likes'] = instance.num_likes()
            output['author'] = instance.author.username
            output.update((self.get_serializer(instance)).data)
        return Response(output)


class CommentAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = CommentSerializer

    def post(self, request):
        print(request.POST)
        print(request.user)
        output = {}
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            output['result'] = "Success"
            output.update((self.get_serializer(instance)).data)
        return Response(output)

class LikeUnlikeView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):

        user = request.user
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        else:
            like.value = 'Like'
        post_obj.save()
        like.save()
        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)


class PostDeleteView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    success_url = '/posts/list/'


    def delete(self, request):
        try:
            output = self.get_object()
        except Exception as e:
            return Response({'error': e})
        msg = ''
        if output.author != self.request.user:
            msg = "Only author can remove their posts"
        else:
            output.delete()
            msg = 'Success'
        return Response({'message': msg})

    def get_object(self, *args, **kwargs):
        pk = self.request.POST.get('post_id')
        obj = Post.objects.get(id=pk)
        return obj


class CommentDeleteView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    # success_url = '/posts/list/'

    def delete(self, request):
        try:
            output = self.get_object()
        except Exception as e:
            return Response({'error': e})
        msg = ''
        if output.user != self.request.user or output.post.author != self.request.user:
            msg = "Only author of post or comment can remove the comment"
        else:
            output.delete()
            msg = 'Success'
        return Response({'message': msg})

    def get_object(self, *args, **kwargs):
        pk = self.request.POST.get('cmt_id')
        obj = Comment.objects.get(id=pk)
        return obj


class PostUpdateView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def put(self, request):

        pid = request.POST.get('post_id')
        content = request.POST.get('content')
        img = request.POST.get('image')
        try:
            postobj = Post.objects.get(id=pid)
        except Exception as e:
            return Response({"error": "Post not available"})
        if request.user == postobj.author:
            if content or img:
                postobj.content = content
                postobj.image = img
                postobj.save()
            return Response({'status':'Success', 'message': 'post updated'})
        else:
            return Response({"error": "Only post owner can edit post"})


class CommentUpdateView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def put(self, request):

        pid = request.POST.get('cmt_id')
        content = request.POST.get('body')
        try:
            cmtobj = Comment.objects.get(id=pid)
        except Exception as e:
            return Response({"error": "Comment not available"})
        if request.user == cmtobj.user:
            if content:
                cmtobj.body = content
                cmtobj.save()
            return Response({'status':'Success', 'message': 'post updated'})
        else:
            return Response({"error": "Only cmt owner can edit comment"})


class SearchView(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('content', 'author__username')


class UserPostReadView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        posts = Post.objects.order_by('-created')
        p = []
        for post in posts:
            pd={}
            postdata = PostSerializer(post)
            pd['likes'] = post.num_likes()
            pd['comments_no'] = post.num_comments()
            pd.update(postdata.data)
            cmts = post.get_comments()
            comm = []
            for cmt in cmts:
                cmtdata = CommentSerializer(cmt)
                comm.append(cmtdata.data)
            pd['comments'] = comm
            p.append(pd)
        return Response(p)