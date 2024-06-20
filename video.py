from django.http import StreamingHttpResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import UserProfile

# List to store served videos (LIFO)
served_videos = []

@login_required
def serve_video(request, user_id):
    # Retrieve the UserProfile instance based on user_id
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    
    # Check if the user_profile has a video attribute and it's not None
    if user_profile.video:
        try:
            # Open the video file associated with the user_profile
            with open(user_profile.video.path, 'rb') as file:
                # Create a streaming response for the video file
                response = StreamingHttpResponse(file, content_type='video/mp4')
                # Set the Content-Disposition header to inline with the video's filename
                response['Content-Disposition'] = f'inline; filename="{user_profile.video.name.split("/")[-1]}"'
                # Append the response to the served_videos list (LIFO)
                served_videos.append(response)
                # Limit the list to 50 items (adjust as needed)
                served_videos = served_videos[-50:]
                
                # Functionality to serve all videos in served_videos
                def stream_video_responses():
                    chunk_size = 8192  # Chunk size for streaming responses (adjust as needed)
                    for response in reversed(served_videos):
                        try:
                            with open(response.streaming_content.file.name, 'rb') as file:
                                video_name = response['Content-Disposition'].split('filename=')[1]
                                streaming_response = StreamingHttpResponse(file.read(chunk_size), content_type='video/mp4')
                                streaming_response['Content-Disposition'] = f'inline; filename="{video_name}"'
                                yield streaming_response
                        except FileNotFoundError:
                            yield HttpResponse('Video not found', status=404)
                
                return stream_video_responses()
        
        except FileNotFoundError:
            return HttpResponse('Video not found', status=404)
    else:
        return HttpResponse('Video not found', status=404)

