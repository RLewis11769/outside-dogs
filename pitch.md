# What's Outside

One could argue that a website containing an infinite number of chat rooms does not utilize a custom API. One could argue that a number of interconnected templates at calls to nearly a dozen URL patterns does not compose a single-page application.

But consider this: I wanted to write a chat room system. I saw "web sockets" and decided this would be a great opportunity to learn something new.

Moreover, I'd recently completed the [Joy of Painting project](https://github.com/RLewis11769/the-joy-of-painting-api) and the project requirements for hosting a custom API for this project sounded similar. I wasn't interested in essentially adding user authorization, pagination, and a frontend to the same project I'd just finished. In actuality, it's not a bad idea to know how to add a frontend to a backend but directly after the Bob Ross project, I just didn't have any interest in it.

Instead, a series of chat rooms! A discussion board! An internet forum! Sockets!!!

## Structure

The structure of my project largely depended on Django. I'd played around with it in the past and was glad to have the opportunity to explore more. I like that it forces organization and I like its built-in functionality. For example, by using form.is_valid() I didn't have to worry about adding custom errors.

I copy-pasted the code in Django's documentation for channels into my routing.py file, frontend, and backend, and I immediately had a working chat room that I could modify to my preferences.

For my frontend, I briefly considered using something like Vue to ensure that my site was in fact a single-page application. However, it seemed a waste not to use Django's templates. Instead, I added Tailwind classes to my project.

### Project

Inside TwilightBark/ there are 6 primary directories, also known as apps.

The inner TwilightBark/ is the root directory of the project. This is where all of the other apps combine. The settings.py file is for overall project configuration while routing.py is where I configured channel settings for the ASGI websocket. In addition to A LOT of configuration in both settings.py and routing.py, this directory holds the urls.py file which defines URLs and routes to other directories. TwilightBark/ only contains one endpoint of its own -- the homepage.

user/ is the directory that holds all user data-- models, forms, views, templates, and routes. Because I used a custom User class to define my user table in the database, I had to include custom forms, admin info, and even a "backend" model. I prefer users logging in with email address and all of this configuration was necessary to override Django's default username-based login. user/ also includes HTML templates for user registration, logging in, account viewing, and account updating, as well as several templates for user password reset/change. However, password views must be in the root-level directory for Django to handle them properly, so only the password templates are included, while every other view/route in the directory maps to localhost:800/user and its related URLs.

chat/ is the directory that holds chat data, more websocket configuration, and the backend socket/channel consumer. I define two tables in my database: ChatRoom and ChatMessage, as described below. However, the most important file in this directory is consumers.py, which receives and handles messages from the frontend. A signal is sent when a user connects or disconnects, and also when a user sends a message. When a user connects, the consumer creates or links to a ChatRoom instance as well as adds the user to the ChatRoom's group. Once the user is added to the group, messages from the frontend can be directed to all members of the group, which happens in receive(). When a user disconnects from the server, that user is removed from both the ChatRoom database and the group.

Almost all actual functionality for the project is found in the three directories listed above.

The only other functionality for the project is found in static/ where I stored my CSS and JavaScript. This was a decision I made early in the project and do regret to some extent. I don't have any project-scope JS and I'm not sure styles.css is helpful in the least. Because I'm using Tailwind, I didn't really have a need for custom CSS. As mentioned, however, I am using custom JavaScript on a page-by-page basis. index.js holds the event listener for creating a new URL which routes to the websocket. room.js holds frontend socket configuration and the functions that handle receiving messages from the backend. account_edit.js holds the JavaScript for changing a user's profile pic which does not actually work except for looking good. If I were to restructure this project, I would include each .js file in the directory that includes the template for that file. room.js would be in chat/ for example so the frontend and backend socket information would not be broken up into different directories. I think the STATIC configuration I did in settings.py allows files to be linked across directories and is therefore only necessary because I did it this way.

settings.py also contains configuration for the media/ directory. When a user is created, a profile picture is added to the database. This is media/default_pic.png. The User model in user/ demonstrates how the image is defaulted and where a new picture is uploaded if a user selects a new profile picture. MEDIA_ROOT and MEDIA_URL are Django file access APIs for uploading pictures. I would have liked media/ to be inside of static/ but was unable to configure it properly. In addition, I attempted to override User's default save class in order to save smaller image files but was unsuccessful. My attempt remains commented out inside user/models.py for reference. While I successfully shrank default_pic.py, including this method messed up the admin panel and of course was useless for the new uploaded profile pic that wasn't ever uploaded/saved to the database.

The last directory inside TwilightBark/ is templates. I think this directory could have been inside TwilightBark/TwilightBark/ but I wasn't able to reference these templates properly. In any case, this directory holds 4 HTML templates. base.html is the base template that most other templates extend from. It itself extends from header.html and footer.html which define the header and footer respectively. index.html is the file that defines Angel's Twilight Bark homepage as referenced in TwilightBark/. I wasn't interested in creating a new templates/TwilightBark/ directory inside of TwilightBark/ for one file so it's hanging out at root level for no reason in particular.

In addition to these 6 directories, the project controller for the top-level TwilightBark is manage.py. This file came as-is with the Django install and is constantly referenced, whether with "python3 manage.py runserver" or "python3 manage.py createsuperuser" or "python3 manage.py shell".

The project structure is:
```
outside-dogs/
	TwilightBark/
		TwilightBark/
		user/
		chat/
		static/
		media/
		templates/
		manage.py
```

### Database

This project has 3 models and 2 managers.

In user/ there is one model that defines a table in my database: User. While [User](https://docs.djangoproject.com/en/4.0/ref/contrib/auth/) is a default Django model out of the box, I wrote a custom User instead. This is because I want different fields in my model and specifically want to override the optional email field to be the controlling USERNAME_FIELD.

I have a custom manager which interfaces with database query operations. There is a default manager for every model but I wanted to specifically customize how users are added. When running "python3 manage.py createsuperuser" or User.objects.create_user() specific class methods are called and I want to customize them in order to link them to my new custom User model.

In chat/ there are two models: ChatRoom and ChatMessage. ChatRoom is linked to User in a many-to-many relationship while ChatMessage includes foreign keys to both ChatRoom and User. What this means is that a user can be in as many rooms as they would like at once. When they send a message, however, that message instance is linked specifically to both the user and room. A User does not need to be linked to any rooms or messages and a ChatRoom does not need any users or messages, but a ChatMessage requires both a user and room to exist.

The manager in chat/ contains one custom method which allows for querying on ChatMessage based on the ChatRoom passed in. The query returns all ChatMessage instances that are linked to the ChatRoom.

I do not have a design document drawing out the links between tables but hope this description outlines the database structure.

## Design

When asked about "design" on an API project, I'm willing to bet it means project architecture rather than frontend design but I'll touch on each.

### Backend 
In general, a backend's design process should probably include thoughts on:
- Language/framework
- Authentication/authorization
- Notifications
- Error logging
- Security
- Efficiency
- Production/Deployment
- Environment specifications

As mentioned, I chose Django for my web framework and a lot of things fell into place after that. For authorization, for example, I used Django's built-in user auth rather than JSON Web Tokens or OAUTH.

I had originally planned on including notifications so that users would be alerted when new messages come in to their chat rooms but had to give up on that idea pretty early. My only other notification service is when a user changes or resets their password, in which case I wanted to play around with Django's [mail interface](https://docs.djangoproject.com/en/4.0/topics/email/) rather than actually sending an email, since I've done that before.

I did not add enough error handling to my project. Errors are most likely going to show the basic development version of a 404 or 500 page. I logged or printed errors to the terminal but much more would be necessary in a production environment.

I believe I added basic security in the form of requiring the user to be authorized before certain requests and not allowing them to update someone else's profile. Again, I suspect I have neglected my 403 errors. I also forgot to save my security key in an environment variable.

I'm sure my project is not very efficient. For example, adding caching to save room group members in [MongoDB](https://www.mongodb.com/) rather than continuously hitting the database to add or count them would have been nice. I'm not sure if Django's RedisChannel layer has actual caching. At one point, I've realized in hindsight, I update pictures in the chat log, but there's a possibility that the picture doesn't change from default_pic.png and I never check if the update is necessary. I'm not impressed with my models considering how little of the fields and methods included in them I used.

I made a few production considerations. For example, my websocket endpoint would change from ws:// to wss:// change based on an http vs https request and I did set that up. I added an "if settings.DEBUG" check in my TwilightBark/urls.py file as well although I've since learned it's not necessary. An easy production vs development consideration would have been to send an actual email rather than using Django's built-in terminal email emulator. However, that was about the extent of my thoughts on actual deployment of my page considering that I don't have any interest in moving this project out of development.

I tried to set up a venv virtual environment in my code editor and broke something. Because of this, my requirements.txt file is kind of handmade. But I did push it and my actual dependencies should be available.

### Frontend

As far as my frontend design goes, I combined Django templates with Tailwind classes and vanilla JavaScript. The templates gave me a clear theme based on extending other HTML pages, as well as allowed for easy creation of entire  pages with similar endpoints. I used Tailwind CSS to customize the look/feel of my static design. I very much prefer Tailwind to Bootstrap. Whenever I needed to change something on the DOM, I used vanilla JavaScript to reference it as well as style/classList attributes.

I specifically chose a dark theme first because I prefer it and second because the design is dedicated to my beautiful black dog. I also wanted to unify my page with a header including a navbar and a footer. My navbar changes based on whether a user is logged in or not.

This project was designed as a tribute to my dog Angel. She is a black Border Collie mix with gentle and intelligent brown eyes. She wears a collar with a peacock design in blue and green with yellow highlights and a bright pink tag, which is where I came up with the color scheme.

I don't think I did anything especially interesting with the design so it's a pretty simple-looking group of pages. I do like the very simple hover and focus effects I added, however. While my goal was accessability, I like how it ended up looking.

## Features

- Full user authentication
	- Entries added to database based on form input
	- Custom user model based on email rather than default name
	- Restrictions on duplicate usernames, user emails, and password strength displayed upon incorrect input in registration form
	- Some site functionality/access restricted based on user registration/login
	- Custom user account pages - different for viewing own account and other user accounts
	- Users have ability to update username and email
	- Users have ability to change or reset password (via terminal-based "email" in production)
- Asynchronous websocket integration
	- Chatroom is created on submit based on name
	- Chat page is updated in real-time with chat messages and number of registered users
	- All users (authenticated and non-authenticated) are accepted into channel group and granted read access
	- Authenticated users are granted read-write access - messages are displayed when entering and leaving a room
	- Chat messages are displayed including user name, user profile pic, and date/time of message
	- When entering a chat room for the first time, backlog of last 5 chat messages and current page number are loaded (if applicable)
- Custom Django templates including context rendering

## Challenges

The biggest challenge was implementing the user auth. I was attempting to more-or-less follow a tutorial and I honestly found it super boring. Of the 12-day project, I spent probably 5 days on the user/ app, which in addition to the 3+ days I took off for various reasons, left very little time for the actual goal of the project in chat/ and the websocket implementation. It wasn't that the user authorization was difficult. I just didn't have the motivation when I just wanted to get through to the interesting parts.

My second challenge was in the implementation and routing of the channel. I originally found a great example of a consumer inheriting from AsyncJsonWebsocketConsumer that I thought would be perfect for both implementing pagination and directing to other methods based on receive_json()'s content type. As it is, the AsyncWebsocketConsumer I'm using has only 3 default methods and I was unable to pass data from receive() to a different method. I experimented a little and an if check sent to a different method would just continue down receive() and run into errors. Instead, I think I would have had to continue the if check within receive() when I was already unhappy with the length of my functions.

In any case, my original AsyncJsonWebsocketConsumer consumer was correctly passing messages to everyone in the group but not updating on the pages until refreshing. I solved this issue by creating a test app and copy-pasting from the [Channels](https://channels.readthedocs.io/en/stable/index.html) documentation, which got me a working open socket in about 5 minutes. I tried to duplicate the routing steps I'd missed into my existing consumers.py and routing.py files but it still didn't work. I had to delete my original consumers.py and room.js files and start from scratch. Once I finally figured it out though, I got into a nice rhythm and wrote most of the chat functionality in about 5 hours. I was missing a few key pieces and wasn't including pictures, but those were easy enough to figure out.

My next challenge lay in receiving messages from the database and sending them to the frontend. I believe I set up my by_room() method in my MessageManager class in a goofy way, because the queryset came back in a format I didn't like. I found a good resource on how to include pagination within the async get_room_chat_messages() database call but had a difficult time figuring out how to serialize the payload I received from the database. I've never been confident in my understanding of why or how to serialize but I finally found a useful resource and was able to implement the PayloadSerializer helper class to create an object containing the exact values I wanted to return.

I had struggled with adding user profile pics to the HTML early in the user auth process and hardcoded in the default pic as a stand-in. When I went to add pictures to the chat log, I decided to go back and actually figure it out. I was actually missing the MEDIA configuration. With that in place, everything went smoothly until a runthrough of my project on the last day, when I realized that updating a picture in my frontend didn't actually update it in my database or even save it anywhere. I spent an insane amount of time on this and still came up with nothing in the end.

Finally, and this is potentially related to the above point, Django adds a lot of built-in functionality and I really like a lot of it. However, forms in particular require such specific names/ids that I struggled differentiating between preferences and requirements. For example, at one point, I wanted to change the names of "password1" and "password2" in my registratin form, but even though I changed it everywhere in my code, it threw an error because the source files reference the names. The [documentation](https://docs.djangoproject.com/en/4.0/topics/forms/) helped, but most examples I found just passed forms as {{form}} or [crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) and I wanted a more custom appearance.

## Conclusion

Most of my issues stemmed from two sources:

1. My poor time management
2. My insistence on customization

My skimming of project requirements until 4 days in likely contributed, but I'm actually glad I chose this project and got familiar with websockets. I'm not sure how I would have implemented them in a project that met more of the "Custom API" requirements so it's likely that my project decision wouldn't have changed regardless, as forcing websockets into the project was my entire goal.

I am frustrated that I didn't plan out my schedule in more detail or even stick to the rough schedule I'd planned. I also spent way more time trying to change the profile picture on the frontend on the last day when I could have been wrapping up other areas that deserved more time. I also had no interest in putting together a proper project proposal, which makes my accomplishments harder to describe.

Much of my time was spent on customizing models and forms. I'm glad for it as far as the final product goes, but there's no doubt that I put in way more work than necessary.

Most of my satisfaction in what I completed stemmed from a few sources:

1. My entire goal was to learn about websockets. Goal accomplished! When I finally added pictures to the chat log, it took about 10 minutes in the backend and 15 minutes in the frontend. Then I copy-pasted in a helper function so I could load in filler images and update them, since I liked that idea, and that took another 10 minutes total, including figuring out how to pass in and add the id
2. I've never considered myself good at configuration but this project had SO much configuration of SO many moving parts that I have to consider it a win to set up everything correctly
3. I've experimented with Django before but didn't fully realize how expansive it was. I've never touched Tailwind. I've primarily stuck to jQuery rather than using vanilla JS to affect the DOM. Considering that I wasn't comfortable with any of the tools or frameworks when I started, I learned a TON and feel good with what I accomplished
4. Even the areas where I can see definite room for improvement tell me how much I learned. I'm really happy with the overall result of this project
5. I love my dog <3
