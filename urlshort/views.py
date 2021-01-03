from django.shortcuts import render
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect

from django.views import View
from urlshort.models import UrlData
from django.http import JsonResponse
from django.shortcuts import redirect

# Create your views here.

def main(request):
  return render(request, 'urlshort/index.html')

class Shorten(View):
    def get(self, request, url):
        url_already_exist = UrlData.objects.filter(shortened_url=url).exists()
        if not url_already_exist: return redirect('main')

        get_old_user_url = UrlData.objects.get(shortened_url=url)
        return redirect('http://{}'.format(get_old_user_url.original_url))
     

    def post(self, request):
        #FOR JAVASCRIPT(JSON) IN PAGE
        if 'url' not in request.POST: return 

        get_user_url = request.POST['url']
        url_already_exist = UrlData.objects.filter(original_url=get_user_url).exists()
        if url_already_exist:
            get_old_user_url = UrlData.objects.get(original_url=get_user_url)
            return JsonResponse({'old': "{}/{}".format(get_current_site(request),get_old_user_url.shortened_url)}, status=200)

        unique_id = get_random_string(length=5)
        new_user_url=UrlData.objects.create(original_url=get_user_url, shortened_url=unique_id)
        new_user_url.save()
        return JsonResponse({'new': "{}/{}".format(get_current_site(request),new_user_url.shortened_url)})


        

