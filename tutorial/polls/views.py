from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic # For generic views
from django.utils import timezone


# Create your views here.
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    # ListView generic view uses a default template called <app name>/<model name>_list.html.
    # For ListView, the automatically generated context variable is question_list
    # To override this we provide the context_object_name attribute, specifying that we want to use latest_question_list instead.

    def get_queryset(self):
        # Return the last five published questions.
        # (not including those set to be published in the future).
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # DetailView generic view uses a default emplate called <app name>/<model name>_detail.html.
    def get_queryset(self):
        # Excludes any questions that aren't published yet.
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # request.POST is a dictionary-like object that lets you access submitted data by key name.
        # In this case, request.POST['choice'] returns the ID of the selected choice, as a string.
        # request.POST values are always strings.
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # reverse function helps avoid having to hardcode a URL in the view function.
        # It is given the name of the view that we want to pass control to and
        # the variable portion of the URL pattern that points to that view.
