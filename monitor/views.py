from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from .MobileNetSSD.videoCamera import gen, VideoCamera
from django.views.decorators import gzip

# Create your views here.
def index(request):
    user_cookie = request.COOKIES.get('username', '')
    if user_cookie:
        return render(request, 'monitor/index.html', { 'username': user_cookie })
    else:
        return HttpResponseRedirect('/web/')

def start(request):
    global vc
    vc = VideoCamera('./monitor/MobileNetSSD/deploy.prototxt', './monitor/MobileNetSSD/MobileNetSSD_deploy.caffemodel')
    return HttpResponse()

def stop(request):
    global vc
    del vc
    return HttpResponse()

def stream(request):
    global vc
    try:
        return StreamingHttpResponse(gen(vc),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")
