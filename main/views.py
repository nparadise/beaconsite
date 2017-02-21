from django.shortcuts import render, render_to_response

# Create your views here.
def main_view(request):
	return render(request, 'main/index.html', {})