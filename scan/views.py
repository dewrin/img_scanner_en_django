from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.files.storage import FileSystemStorage

from PIL import Image
from pytesseract import image_to_string
from django.shortcuts import render
from django.http import HttpResponse
import json
import time, urllib.request 

class OCR(View):
	def index(request): 
		response_data = {}
		response_data["success"] = True
		response_data["url"] = None
		response_data["code"] = None
		if request.method == "GET":
			try:
				url = request.GET["url"]
				response_data["url"] = url
				file = "%s"%time.time()
				urllib.request.urlretrieve(url, file)
				im = Image.open(file)
				text = image_to_string(im)
				response_data["code"] = text
				response_data["message"] = file
				os.remove(file)
			except Exception as e:
				response_data["message"]="%s"%e
		return HttpResponse(json.dumps(response_data),content_type="application/json")


class IMGView(View):
  template_name = "index.html"

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, {})
  
  def post(self, request, *args, **kwargs):
    if request.FILES:
      myimg = request.FILES['img']
      context = {}
      try:
        im = Image.open(myimg)
        text = image_to_string(im)
        if text == '':
          context['message'] = 'Sorry, This is an empty image :('
        else:
          fs = FileSystemStorage()
          filename = fs.save(myimg.name, myimg)
          uploaded_file_url = fs.url(filename)
          context['imgurl'] = uploaded_file_url
          context['alt'] = myimg.name
          context['content'] = text
      except Exception as ex:
        context['message'] = ex
      return render(request, self.template_name, context)
    else:
      return redirect('img')
