from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import UserProfile

# List to store served blog images (LIFO)
served_blog_images = []

def serve_blog(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    
    if user_profile.blog:
        with open(user_profile.blog.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='image/jpeg')
            response['Content-Disposition'] = 'inline; filename=' + user_profile.blog.name.split('/')[-1]
            served_blog_images.append(response)  # Append the served blog image to the list
            return response
    else:
        return HttpResponse('Blog image not found', status=404)

