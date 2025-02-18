from django.db import models
from users.models import User

# Create your models here.
class ResearchPaper(models.Model):
    STATE_CHOICES = [
        ('submitted','Submitted'),
        ('assigned','Assigned'),
        ('in review','In Review'),
        ('finalized','Finalized')
    ]
    title = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='papers/')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='papers')
    state = models.CharField(max_length=20,choices=STATE_CHOICES,default='submitted')
    reviewer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='reviews')

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    paper = models.ForeignKey(ResearchPaper,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.paper.title}"
    