from django.shortcuts import render


# Create your views here.
def noticia(request):
    ctx = {

    }
    # return render_to_response('index/index.html', ctx, context_instance=RequestContext(request))
    return render_to_response('', ctx, context_instance=RequestContext(request))