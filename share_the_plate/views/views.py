from django.shortcuts import render


# Create your views here.
def home_page(request):
    """
    Display the home page.

    :param request: HTTP request
    :return: Rendered home page
    """
    return render(request, "share_the_plate/index.html")
