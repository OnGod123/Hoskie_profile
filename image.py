from django.http import StreamingHttpResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import UserProfile

# List to store served images (LIFO)
served_images = []

@login_required
def serve_image(request, user_id):
    # Retrieve the UserProfile instance based on user_id
    user_profile = get_object_or_404(UserProfile, user_id=user_id)

    # Check if the user_profile has an image attribute and it's not None
    if user_profile.image:
        try:
            # Open the image file associated with the user_profile
            with open(user_profile.image.path, 'rb') as file:
                # Create a streaming response for the image file
                response = StreamingHttpResponse(file, content_type='image/jpeg')
                # Set the Content-Disposition header to inline with the image's filename
                response['Content-Disposition'] = f'inline; filename="{user_profile.image.name.split("/")[-1]}"'
                # Append the response to the served_images list (LIFO)
                served_images.append(response)
                # Limit the list to 50 items (adjust as needed)
                served_images = served_images[-50:]

                # Functionality to serve all images in served_images
                def stream_image_responses():
                    for img_response in reversed(served_images):
                        try:
                            with open(img_response.streaming_content.file.name, 'rb') as img_file:
                                img_name = img_response['Content-Disposition'].split('filename=')[1]
                                img_response_stream = StreamingHttpResponse(img_file.read(), content_type='image/jpeg')
                                img_response_stream['Content-Disposition'] = f'inline; filename="{img_name}"'
                                yield img_response_stream
                        except FileNotFoundError:
                            yield HttpResponse('Image not found', status=404)

                return stream_image_responses()

        except FileNotFoundError:
            return HttpResponse('Image not found', status=404)
    else:
        return HttpResponse('Image not found', status=404)


