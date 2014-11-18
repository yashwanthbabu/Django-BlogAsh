Checkout the application and use it at https://github.com/yashwanthbabu/DjangoBlog

[MIT License](https://github.com/yashwanthbabu/Django-BlogAsh/blob/master/license.md)

# **To try it locally**

* `Clone the repository.`
* `cd DjangoBlog`
* `pip install -r requirements.txt`
* `python manage.py syncdb`
* `python manage.py runserver`

You will be able to access http://127.0.0.1:8000/admin/ with this.

Blog entries exist at /blog/. Try accessing it. It will show the limited blog entries which will be controlled by BLOG_ENTRIES_PER_PAGE in settings.py In the /blog/, you can see the links of: 
* HOME - Home page of me.
* BLOG - shows the blog page of me named BlogAsh.
* RECENT ARTICLES - shows the recent blog entries in the manner of recently added.
* CONTACT ME - shows the contact details of me.
* FEEDBACK - is the form to get the feedback from the users.
* MONTHLY ARCHIVES - shows the blog entries of the particular month.
* TAGS - shows the tags used for all the posts. If you click on any one the tag, it shows the posts for that tag.
* TWITTER FEEDS - shows the last 10 tweets of me.
* FOLLOW ME - shows the social account links.
* PROJECTS - shows the github link redirects to my github account.
* USER LOGIN - user can login through social authentication. The user can login using Facebook, Twitter and google+. If you want more, you can add according to your requirement.

    - After clicking USER LOGIN, you will see the Login form with username and password. If you are already a member you can login here. 
    - For the forgot password., the user should provide an email address to sent an password_reset_email for the user. so that the user can reset his password and can enter the new password. Added this functionality for the application.
    - If not a member, then JOIN US button will provide the registration form. By this the user can register and here. After the registration has been done, it will ask for the login. Again you should login. If the particulars are correct then it will login.

If you are a Admin user and you are already logged in, then the links of Admin, Add Post and Add Comment will be appeared at the Top-Left of the /blog/ page.By this you can directly redirect to the adming to add posts and comments.

To directly see the Monthly Archive blog entries, just click on the Month and will redirect to the /month/ page. Here it shows the blog entries of that particular month.

If you want to see the entire details of the blog, I mean the detail page of the blog entry, just click on more info.. or on the title of the blog. It will redirect to the /post/id/ page and here the user can see the blog, comment on the blog. After commenting, the user will get the mail of confirms the user. 

If you are a Admin user then you can delete either single or bulk comments.

# **To integrate into your application:**

* Install the requirements.txt
* Include `django_admin_bootstrapped.bootstrap3` , `django_admin_bootstrapped` , `south` , `registration` in settings.INSTALLED_APPS.
* Enable django admin. If not already enabled python manange.py syncdb 
* Check out your blog at /blog/

Enjoy the blogging application in django now.

# **DEMO**
https://blogash.herokuapp.com/

# **LIVE**
www.yashwanthbabu.in