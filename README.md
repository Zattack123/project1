# Information System for Air Quality Web Application

This is a web application used to provide a forum for the discussion of air quality, air pollution, and other related topics, created by Zach Dilliha for CS 396 Intermediate Software Project.

## Requirements

This application requires familiarity with Django in order to run the server and access the website.

## Installation

To install, download the project1 folder and place it where you keep python files.

Follow these steps to activate the site
Steps:
1. Open a Command Terminal
2. Navigate to the Scripts folder (project3/Scripts)
3. Run .\activate in the Scripts folder to activate the virtual environment
4. Navigate to the mysite folder (project3/Scripts/mysite)
5. Run python manage.py runserver
6. Open http://127.0.0.1:8000/ in your web browser to access the site

## Usage

The interface is simple and easy to understand. When first opening the application, it will start you on the home page, where it lists out the different Boards the user can visit.

There is a general Admin account, with Username and Password both: Admin

When logged in, users have full access to the website, where they can navigate through the different Boards, and posts on those Boards, and can create a new Topic on each Board. They can also edit their own posts, and the Admin can edit anyone's posts. If a user is not logged in, and they try to create a new Topic or post on a Topic, they will be redirected to the Login page, and then, if successful, they will then be redirected to the page where they can reply/create a new Topic.

Users, logged in or not, can also view the files that were uploaded to the site via the top navigation Bar File Button. They will see a list of all the files uploaded and be able to download them from the Download button. If an unregistered user attempts to upload a file, they will have to login/signup, and then they will be redirected back to the Upload page. The admin can delete any files uploaded to the site.

Users can also view a database of pollution data divided into Cities, Vehicles, and Power Plants via the Database button on the top navigation bar, next to the Files button. This will take the user to a screen showing the 3 options for viewing data, Cities, Vehicles, and Powerplants, and they each have their own page. On each page, it will display the pollution information for each particular entry. There is a search bar at the top of each page that allows users to search based on a few arguments:
  Cities: Name, State, and Database
  Vehicles: Automaker and Trim
  Power Plants: Name and State

On the Database page, there are various buttons to display graphs that correspond to the data

Alongside the Files button, are two buttons that link to the World Health Organization main site, as well as their page for Air Pollution.
