from django.http import HttpResponse, JsonResponse
import yt_dlp
import assemblyai as aai
import os 

aai.settings.api_key = "85dfd1af7ea047f1abf886314afcbd7d"

ydl_opts = {
    'format': 'm4a/bestaudio/best',  # The best audio version in m4a format
    'outtmpl': 'sameAudio.%(ext)s',  # The output name should be the id followed by the extension
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}


def getEnglishTranscript(request):
    videolink = request.GET.get('videolink', 'nolink')
    print("\n video is : ")
    print(videolink)
    print("\n")


    if(videolink=='nolink'): 
        return HttpResponse("No video link found the URL")
    
    Friends = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        URLS = [videolink]

        print("audio starting to download\n")

        error_code = ydl.download(URLS)

        print("audio download finished\n")
        print("\n")
        print("intialising Transcriber...\n")


        transcriber = aai.Transcriber()

        print("feeding audio to transcriber\n")
        print("\n")

        transcript = transcriber.transcribe("sameAudio.mp3")    

        print("transcription finished 🔥\n")

        Friends = [transcript.text]
        # transcript = transcriber.transcribe("sameAudio.m4a")
        # print(transcript.text)
        # print("transcript complete")

    # return HttpResponse(videolink)

    videolink = ''
    
    os.remove("./sameAudio.mp3")
    return JsonResponse(Friends, safe=False)