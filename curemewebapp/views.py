import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import markdown
from django.views.decorators.csrf import csrf_exempt

from curemewebapp.SemanticAPIQuery import backendQuery  # You might need to install markdown with 'pip install markdown'

logger = logging.getLogger(__name__)  # __name__ is the name of the current module

@csrf_exempt
def search_view(request):
    logger.debug("Search view has been called")
    result = ""
    if request.method == "POST":
        search_param = request.POST.get('search_param', None)

        if search_param == "hello world":
            return JsonResponse({'result': 'hello world'})

        if search_param:
            # Your Python code that takes the search_param and returns markdown text
            try:             
                result = backendQuery(search_param)
                result = markdown.markdown(result)  # Convert markdown to HTML
            except Exception as error:
                # handle the exception
                result = str(error) 

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # For AJAX requests, return only the result part as JSON
                return JsonResponse({'result': result})

        # For non-AJAX requests, render the whole page as usual
        return render(request, 'search.html', {'result': result})

    # If it's not a POST request, just render the page without any result
    return render(request, 'search.html')