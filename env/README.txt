Welcome to SChannel!

--PURPOSE--
Intended to automate mass-messages for small businesses, SChannel is currently a work-in-progress Flask-based app with limited functionality.
This project is built in Python and supported by Flask with WTForms, all while connected to a callable Firebase DB. 

--HOW TO RUN--
SChannel is built in a virtual environment with all the necessary libraries stored in env/lib/site-packages. 
Please create a virtual environment on your workspace by entering the directory on your computer where the \env folder is stored. 
In terminal on Windows, run this line: 
env\scripts\activate
to run the virtual environment. From there enter the \env folder, and run this line:
python app.py
You can now test the development server on your browser.

--STRUCTURE--
app.py 
    hosts the main body of the app - database initialization, account authentication, twilio API and messaging functions start here. 
    API routes render pages for the admin to use: some of these pages are linked to HTML, while others are still in REST API form. 
    
    There are 3 main routes at the end of this file. They render HTML templates and pass along objects to forms within those templates.
    admin: allows admin to create users and delete users from DB. create users is functional, deleting users is not. We wanted to created a dropdown box
           that would display all current users in the DB, admin chooses which to delete, and the user (as well as corresponding data) is removed from DB. 
           We were unable to implement this dropdown.
    groupgrid: the main page that displays all existing groups with their respective information. We did not use HTML grids as we found that iterating each group 
            in a blogpost-fashion gave the desired effect. Here we also render the button to create groups, which is fully functional (try it with Firebase open!)
    editgroup: once admin clicks on a group from <groupgrid>, they would be redirected to this page. The idea for editgroup is to populate the page with information
            on the selected group. the edit group modal should populate fields based on the group selected. we also tried to add the functionality to add/remove users 
            from a group, but were unable to implement. This would simply consist of querying the database for all users associated with the group's ID, and displaying 
            them in the modal (perhaps in a dropdown like mentioned in another route). We also kept the message button here, which we planned on being able to grab all
            phone numbers associated with all users in the group, then using the sendMessage function to both send and store the message in firebase.

forms.py
    imports WTForms and creates basic outline for all forms used in this project. Most have been implemented within html files in the templates folder.

static folder
    defaultImage.png - what we used as placeholder for group icons
    main.css - additional styles used by all HTML files

templates folder 
    home.html - lays style and form for individual pages. all other templates extend this file.
    admin.html - renders 2 important buttons that open bootstrap modals.
    editgroup.html - renders the buttons necessary to edit an individual group and also send messages
    groupgrid.html - renders an iterative grid that displays all existing groups with areas for group name, group description, image for a group,
                     and button to access the <editgroup.html> path for a particular group. also has the button to create a group.

--OVERVIEW OF WHAT'S LEFT--
Much of this project has yet to be finished. You may have noticed a trend with what's not done - it mainly has to do with querying Firebase through Flask and passing this info to templates.
For example - in order for admin to delete a user, we would have to query the DB for all existing users, then display the results of this query in a dropdown. We created the button/forms/routes:
all that is left is to implement the queries.