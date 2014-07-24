class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
