from django import forms

from api.models import Comment


class CommentForm(forms.ModelForm):

    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Add a review...',
                'rows': 4,
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['body', 'content_id', 'user']
