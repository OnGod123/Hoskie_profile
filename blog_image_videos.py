from PIL import Image
import subprocess

def save_blog_post(self, title, content):
    # Generate slug for the blog post
    slug = slugify(title)

    # Save the blog post content to a file in a user-specific directory
    user_directory = os.path.join('blog_posts', str(self.user.username))
    os.makedirs(user_directory, exist_ok=True)
    filename = os.path.join(user_directory, f"{slug}.txt")

    with open(filename, 'w', encoding='utf-8') as text_file:
        text_file.write(content)

    # Optionally, you can save the blog post to a database model if needed
    # BlogPost.objects.create(
    #     author=self.user,
    #     title=title,
    #     content=content,
    #     slug=slug,
    #     file_path=filename
    # )
    self.tweet.save(f"{slug}.txt", ContentFile(content), save=True)

    return filename  # Return the file path for later use


def save_video(self, video_file, title):
    if video_file:
        # Generate slug for the video filename
        slug = slugify(title)

        # Save the video file to a user-specific directory
        user_directory = os.path.join('blog_posts', str(self.user.username))
        os.makedirs(user_directory, exist_ok=True)
        video_filename = os.path.join(user_directory, f"{slug}.mp4")

        with open(video_filename, 'wb') as video_dest:
            for chunk in video_file.chunks():
                video_dest.write(chunk)

        # Optional: Process the video using ffmpeg (e.g., compression, format conversion)
        try:
            # Example command to re-encode with ffmpeg without quality loss
            subprocess.run(['ffmpeg', '-i', video_filename, '-c:v', 'copy', '-c:a', 'copy', '-strict', 'experimental', f"{slug}_processed.mp4"], check=True)
            processed_video_filename = os.path.join(user_directory, f"{slug}_processed.mp4")
            self.video.save(f"{slug}.mp4", processed_video_filename, save=True)
            return processed_video_filename
        except subprocess.CalledProcessError as e:
            print(f"Error processing video: {e}")
            return None
    else:
        return None


def save_image(self, image_file, title):
    if image_file:
        # Generate slug for the image filename
        slug = slugify(title)

        # Save the image file to a user-specific directory
        user_directory = os.path.join('blog_posts', str(self.user.username))
        os.makedirs(user_directory, exist_ok=True)
        image_filename = os.path.join(user_directory, f"{slug}.jpg")

        with open(image_filename, 'wb') as image_dest:
            for chunk in image_file.chunks():
                image_dest.write(chunk)

        # Resize image to 300x300 pixels
        try:
            with Image.open(image_filename) as img:
                img.thumbnail((300, 300))
                img.save(image_filename)
        except Exception as e:
            # Handle errors in image processing (e.g., if PIL fails to open or save the image)
            print(f"Error processing image: {e}")
            return None
          self.image.save(f"{slug}.jpg", image_filename, save=True)

        return image_filename
    else:
        return None

