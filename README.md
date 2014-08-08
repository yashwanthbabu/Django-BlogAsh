Checkout the application and use it at https://github.com/yashwanthbabu/DjangoBlog

# **To try it locally**

1) Clone the repository.
2) cd DjangoBlog
3) pip install -r requirements.txt
4) python manage.py syncdb
5) python manage.py runserver

You will be able to access http://127.0.0.1:8000/admin/ with this.

Blog entries exist at /blog/. Try accessing it. It will show the limited blog entries which will be controlled by BLOG_ENTRIES_PER_PAGE in settings.py In the /blog/, you can see the links of: 
HOME - which will redirects to the /blog/ page.
RECENT ARTICLES - shows the recent blog entries in the manner of recently added.
MONTHLY ARCHIVES - shows the blog entries of the particular month and 
USER LOGIN - user can login through social authentication. This one is not yet completed still working on it.

If you are a Admin user and you are already logged in, then the links of Admin, Add Post and Add Comment will be appeared at the Top-Left of the /blog/ page.By this you can directly redirect to the adming to add posts and comments.

To directly see the Monthly Archive blog entries, just click on the Month and will redirect to the /month/ page. Here it shows the blog entries of that particular month.

If you want to see the entire details of the blog, I mean the detail page of the blog entry, just click on more info.. or on the title of the blog. It will redirect to the /post/id/ page and here the user can see the blog, comment on the blog. After commenting, the user will get the mail of confirms the user. 

If you are a Admin user then you can delete either single or bulk comments.

# **To integrate into your application:**

1) Install the requirements.txt
2) Include `django_admin_bootstrapped.bootstrap3` , `django_admin_bootstrapped` , `south` in settings.INSTALLED_APPS.
3) Enable django admin. If not already enabled python manange.py syncdb 4) Check out your blog at /blog/

Enjoy the blogging application in django now.
