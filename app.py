from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    video_resolution = request.form['resolution']

    try:
        youtube_object = YouTube(video_url)
        if video_resolution == "Lowest Quality":
            video = youtube_object.streams.get_lowest_resolution()
        else:
            video = youtube_object.streams.get_highest_resolution()

        # Get the video filename
        video_filename = f"{youtube_object.title}.mp4"

        # Download the video to a temporary location
        video_path = video.download("downloads/", filename=video_filename)

        # Serve the downloaded file as an attachment
        return send_file(video_path, as_attachment=True)
    except Exception:
        return "Download Error"


if __name__ == '__main__':
    app.run(debug=True)
