<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&appId=559235774199929&version=v2.0";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>

<script type="text/javascript">
$(document).ready(function(){
$('#share_button').click(function(e){
e.preventDefault();
FB.ui(
{
method: 'feed',
name: 'This is the content of the "name" field.',
link: ' http://www.hyperarts.com/',
picture: 'http://www.hyperarts.com/external-xfbml/share-image.gif',
caption: 'This is the content of the "caption" field.',
description: 'This is the content of the "description" field, below the caption.',
message: ''
});
});
});
</script>