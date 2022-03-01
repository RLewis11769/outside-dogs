# Angel's Twilight Bark Chat Room

![Angel](https://github.com/RLewis11769/outside-dogs/blob/main/TwilightBark/media/profile_images/angel.png)

## Project Info

Using all of the skills you've developed over the last two trimesters, you're going to create your very own API from start to finish. You'll develop a design, narrow down what should be in your MVP (minimum viable product), and work to bring your idea to life. You have a limited number of days to work on this project, so be sure to keep your scope reasonable.

There is one rule that must be followed... Your application must follow the theme, "What's Outside?" You are free to interpret that in any way you see fit!

Every great project starts with the design phase. You should expect to spend about a day designing your application before starting on the implementation.

Once you have a design in place, it is time to start implementing that design. Begin collecting the data you need, set up your database based on your design docs, and work on a process to populate the database. Even if you (and your users) are manually inputting data into your database instead of collecting data from other sources, you do need to set up a database for this project for your API to interact with.

Once your database is in place and populated with data, it will be time to consider how to build your API to interact with your data. In this project, your API must do the following:
- Authenticate users of your API
- Allow for pagination of data
- Allow for caching of data to reduce hits to your database when possible and improve responsiveness to your users

Your API must also implement one of the following features:
- Queuing systems (for long-running process on your server)
- Web sockets (two-way communication between client and server)

You can have multiple users for your application, but at minimum make sure that there is a test user available so that if you do not implement a user-creation process, you can test your API with this test user.

Finally, an API is only as good as the user's ability to use it. For this task, build a small, single-page application that utilizes your API and presents data to your user in a relevant way.

It does not need to be pretty, although that always improves any product. The most important thing is that it is able to use your API to authenticate users, retrieve data (including the use of pagination), and in retrieving data use a caching system when appropriate.

If you've created a process for users to be created via your API you may choose to add user registration as a part of this page. Regardless, this page will need a way for your user to authenticate themselves to be able to use the API.

## Description

In my defense... I misread the prompt. I instead (apparently) decided to write a chat room. I added user authorization, a database to store info, websockets, and technically pagination. Of course my website is also making API calls to link the frontend and backend.

A detailed explanation of design decisions can be found [here](https://github.com/RLewis11769/outside-dogs/blob/main/pitch.md). Some features are summarized below in the Features section.

This website integrates the following components:
- [Django](https://www.djangoproject.com/) Python web framework
	- Including:
		- User Authorization
		- Websocket Channels
		- Pagination
- [Tailwind](https://tailwindcss.com/) CSS framework
- [SQLite Database](https://www.sqlite.org/index.html)
- Vanilla JavaScript

While I can't say I created a single-page application and it certainly isn't based around a single API call, I'm very proud of the project I decided to make.

## Installation

1. Install

Clone the repository into your system with the command:
```
git clone git@github.com:RLewis11769/outside-dogs.git
```

2. Change Directory

Navigate into the root directory where the Django project is stored with:
```
cd TwilightBark/
```

3. Install dependencies

Install dependencies with:
```
pip3 install -r requirements.txt
```

4. Run

Run the backend server with the command:
```
python3 manage.py runserver
```

5. View

The frontend will be available to view in your web browser at:
```
localhost:8000/
```

## Superuser

The database in the repository contains a superuser (Angel). Her credentials are:
```
username: angel@angel.com
password: bestdogever
```

When logged in as the superuser, access is granted to Django's admin panel found at:
```
localhost:8000/admin
```

From this panel, all tables in the database are viewable. All entries are deletable while some fields are editable. Specifically, user profile pictures are only editable in the admin panel.

A new superuser can be creating by running a command through the SQLite interactive shell:
```
python3 manage.py createsuperuser
```

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
- Fully accessible (checked with [axe Dev Tools](https://www.deque.com/axe/devtools/) - issues are manual review for sufficient color contrast of text based on color gradient)
- Designed as a tribute to my dog Angel! She is a black Border Collie mix with gentle and intelligent brown eyes. She wears a collar with a peacock design in blue and green with yellow highlights and a bright pink tag. Lovely color scheme. Inspiring. A portrait of her is set as her profile pic as the superuser and she looks very artistic and brooding, not at all goofy and cuddly.

## Bugs

I'm unhappy with two areas in particular.

First, while it is possible to change user profile pics in the admin panel, the new profile picture is not saved to the database. Clearly I have an error in my frontend code, whether in the view/logic itself or in the way the form is submitted/saved. In order to change a user's profile picture, a user currently has to navigate to http://localhost:8000/admin/user/user/ as a superuser and manually change the profile picture. In the actual frontend, at http://localhost:8000/user/id/edit/ (where id is the user id) the profile picture changes locally but does not save to the database.

Secondly, I had originally planned for more extensive pagination than is currently available. I believe the functionality is mostly in place but I was unable to introduce pagination to my websocket requests. As it stands, if a user enters a chatroom with more than 5 messages, the websocket call will pull the last 5 entries from the database in order and display the page that they are on. However, no more calls for page data are ever made from the frontend.

I believe I could have fixed this by displaying previous page numbers and allowing click events to send a request for past messages (which are currently inaccessible on the frontend). I had originally wanted scrolling or some other automatic request-sending to the consumer in order to continue displaying only a certain number of messages. As it stands, if a user submits messages, the chat log just grows so that many more than 5 messages display and the page number never updates until a refresh.

Bugs include:
- Attempts at responsiveness were made but are not at a professional level
- Everything should be centered but it is not vertically aligned
- The "edit" button on the "account settings" page is all over the place
- At times, I've noticed redirection doesn't work as planned or errors don't come out red but did not take good notes on finding/resolving them
- I was unable to update the timezone. It remains UTC

If you find any additional bugs, please contact Rachel Lewis at 2708@holbertonschool.com.

There are several features I decided not to implement based on time considerations. These include:
- Chat room names should not include spaces. There is almost no limitation on the backend for acceptable room names, but spaces are an obvious no. The name entered into the "input" field will be the name in the URL - obviously "http:localhost:800/chat/room name" is not a valid URL and should be converted to "/chat/room%name" or similar but I did not check for this
- An unauthorized user who attempts to chat will recieve a message logged to the console but no error alert
- Most errors print to terminal or log to console
- My models could have been thinner for better efficiency. My planned fields and methods were not all used
- I'm not sure if this is supposed to work like this, but my users do not disconnect from their chat room groups when navigating elsewhere in the database. Meaning that if a user is in room "dogs" and then navigates to their user account, no disconnect message is sent/received and the group does not receive the "user left" message
- The Tailwind CDN should not be used in production. Because this is still a development environment, this should theoretically be fine
- While I made an attempt at using the pycodestyle Python linter, my JavaScript is a mess

## Credit

This webpage was designed and implemented by Rachel Lewis with her very special assitant Angel.

Special thanks to [Mitch Tabian](https://github.com/mitchtabian) for helping me design custom models and admin panel views for user auth and [Corey Schafer](https://github.com/CoreyMSchafer) for breaking down Django in general, especially static/media URLS and its custom password reset views.

The [Django documentation](https://docs.djangoproject.com/en/4.0/) was wildly helpful, especially when dealing with [Channels](https://channels.readthedocs.io/en/stable/index.html) and WebSocket protocols. 
