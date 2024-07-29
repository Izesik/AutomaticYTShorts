import moviepy.editor as mp
import textwrap
import pandas as pd
import random
import os

## Let's load the quotes
def load_quotes(quotesFile):
    quotes = pd.read_csv(quotesFile, header=None)
    return quotes[0].tolist()

## Selects a quote from the list randomly
def selectRandomQuote(quotes):
    return random.choice(quotes)

## Selects a video from the folder randomly
def selectRandomVideo(videoDir):
    videos = [os.path.join(videoDir, vid) for vid in os.listdir(videoDir)]
    return random.choice(videos)

## Create a video clip with text overlay
def create_text_clip(quote, video_duration, video_width, video_height):
    font_size = 70  ## Starting font size
    while True:
        test_clip = mp.TextClip(quote, fontsize=font_size, color='white', font='minecraft_font.ttf', method='caption', size=(video_width-50, None), stroke_width=3, stroke_color='black')
        if test_clip.size[1] < video_height - 100:
            break
        font_size -= 5  ## Decrease font size and try again

    fade_duration = 1  # Duration of the fade effect in seconds

    # Create text clip
    text_clip = mp.TextClip(quote, fontsize=font_size, color='white', font='minecraft_font.ttf', stroke_width=3, stroke_color='black', method='caption', size=(video_width-50, None))
    text_clip = text_clip.set_position(('center', 'center'))
    text_clip = text_clip.set_duration(video_duration).fadein(fade_duration).fadeout(fade_duration)
    
    # Create text shadow
    text_shadow = mp.TextClip(quote, fontsize=font_size, color='black', font='minecraft_font.ttf', stroke_width=2, stroke_color='black', method='caption', size=(video_width-50, None)).set_opacity(0.6)
    text_shadow = text_shadow.set_position(('center', 'center')).set_duration(video_duration).fadein(fade_duration).fadeout(fade_duration)
    
    text_clip_combined = mp.CompositeVideoClip([text_shadow, text_clip]).set_duration(video_duration)
    
    return text_clip_combined

## Put it all together
def create_motivational_short(video_paths, quotes, output_path):
    subclip_duration = 60 / len(quotes)  ## Each quote will have equal time
    video_clips = []
    
    for i, (video_path, quote) in enumerate(zip(video_paths, quotes)):
        video = mp.VideoFileClip(video_path).subclip(0, subclip_duration)
        video = video.resize(height=1920)
        video = video.crop(x_center=video.w / 2, y_center=video.h / 2, width=1080, height=1920)
        
        video_width, video_height = video.size
        text_clip_combined = create_text_clip(quote, subclip_duration, video_width, video_height)
        
        video_with_text = mp.CompositeVideoClip([video, text_clip_combined])
        video_clips.append(video_with_text)
    
    final_video = mp.concatenate_videoclips(video_clips)
    final_video.write_videofile(output_path, codec='mpeg4', audio_codec='aac', bitrate="8000k", fps=24, preset='slow', ffmpeg_params=['-crf', '18'])

def main():
    quotes = load_quotes('quotes.csv')
    video_dir = './videos/'
    output_dir = './output/'

    for i in range(3):
        selected_quotes = random.sample(quotes, 8)  ## Assuming 5 quotes per minute
        selected_videos = [selectRandomVideo(video_dir) for _ in range(5)]
        
        output_path = os.path.join(output_dir, f'motivational_short_{i+1}.mp4')
        create_motivational_short(selected_videos, selected_quotes, output_path)
        print(f'Created: {output_path}')

if __name__ == "__main__":
    main()
