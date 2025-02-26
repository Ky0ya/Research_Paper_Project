from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from users.models import User
from .models import ResearchPaper, Comment
import json

def get_reviewers(request):
    if request.method == 'GET':
        reviewers = User.objects.filter(role="reviewer").values("id","username")
        return JsonResponse(list(reviewers),safe=False)
    

def get_submitted_papers(request):
    if request.method == 'GET':
        papers = ResearchPaper.objects.filter(state="submitted").values("id","title","state")
        return JsonResponse(list(papers),safe=False)
    
def get_submitted_paper_aid(request,author_id):
    try:
        submitted_papers = ResearchPaper.objects.filter(author_id=author_id).values("id","title","state")
        return JsonResponse(list(submitted_papers),safe=False)
    except Exception as e:
        return JsonResponse({"message":f"Failed to fetch submitted papers: {str(e)}"},status = 500)

def assigned_papers(request,reviewer_id):
    try:
        papers = ResearchPaper.objects.filter(reviewer_id=reviewer_id, state="assigned")
        papers_list = list(papers.values("id","title","file","author","state"))
        return JsonResponse(papers_list,safe=False)
    except Exception as e:
        return JsonResponse({"message":"Failed to fetch assigned papers","error":str(e)},status=500)

@csrf_exempt
def assign_reviewer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            paper_id = data.get("paperId")
            reviewer_id = data.get("reviewerId")

            if not paper_id or not reviewer_id:
                return JsonResponse({"message":"Paper ID and Reviewer ID are required"},status=400)
            
            paper = get_object_or_404(ResearchPaper,id=paper_id)
            reviewer = get_object_or_404(User,id=reviewer_id)
            paper.state = "assigned"
            paper.save()
            return JsonResponse({"message": "Reviewer assigned successfully", "paper_id": paper.id})
        except Exception as e:
            return JsonResponse({"message": "Reviewer assigned successfully", "paper_id": paper.id} )
        
@csrf_exempt
def add_comment(request,paper_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get("UserID")
            comment_text = data.get("commentText")
            if not user_id or not comment_text:
                return JsonResponse({"message": "User ID and comment text are required"}, status=400)
            paper = get_object_or_404(ResearchPaper,id=paper_id)
            user = get_object_or_404(User,id=user_id)
            comment = Comment.objects.create(paper=paper,user=user,comment_text=comment_text)
            return JsonResponse({"message": "Comment added successfully", "comment_id": comment.id}, status=200)
        except Exception as e:
            return JsonResponse({"message": f"Error adding comment: {str(e)}"}, status=500)

@csrf_exempt
def finalize_paper(request,paper_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reviewer_user_id = data.get("reviewerUserID")

            if not reviewer_user_id:
                 return JsonResponse({"message": "Reviewer ID is required"}, status=400)
            paper = get_object_or_404(ResearchPaper,id=paper_id)
            reviewer = get_object_or_404(User, id=reviewer_user_id)
            paper.state = "finalized"
            paper.save()
            Comment.objects.create(
                paper=paper,
                user=reviewer,
                comment_text="Paper finalized."
            )
            return JsonResponse({"message": "Paper finalized successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"message": f"Error finalizing paper: {str(e)}"}, status=500)

        
pappu = 5