from django.urls import path
from .views import get_reviewers, get_submitted_papers, assign_reviewer, add_comment, get_submitted_paper_aid, finalize_paper, assigned_papers
urlpatterns = [
    path("reviewers/", get_reviewers, name="get_reviewers"),
    path("papers/", get_submitted_papers, name="get_submitted_papers"),
    path("assign-reviewer/", assign_reviewer, name="assign_reviewer"),
    path("add-comment/<int:paper_id>/",add_comment,name="add_comment"),
    path("submitted-papers/<int:author_id>/",get_submitted_paper_aid,name="get_submitted_papers_aid"),
    path("finalize-paper/<int:paper_id/>",finalize_paper,name="finalize_paper"),
    path('assigned-papers/<int:reviewer_id>/',assigned_papers,name='assigned_papers')
]