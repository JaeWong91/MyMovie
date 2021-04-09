# [MyMovie](http://my-movie-project-jason.herokuapp.com/home)

![](/static/readme-images/readme-header.PNG)

This is a movie review website for all movie fans. Visitors of the site can search and view reviews and ratings for all kinds of movies, even without a registered account. If a user would like to write a review of their own, a registered account is required. Once registered, the user is able to write reviews and see their written reviews on their profile page. They will also have the ability to edit existing reviews, or remove them.

The Live website can be found [here](http://my-movie-project-jason.herokuapp.com/home).

# User Experience (UX)

## User Stories
- As a New Visiter:

    - I would like to browse the content of the website without registering or signing up.
    - I would like to see the director and the main cast of a movie.
    - I would like to view reviews for any particular movie which were written by other users.
    - I would like to register an account for the website.

- As a Registered User:

    - I would like to log in to the website.
    - I would like to add a rating and a review for a movie.
    - I would like to see when I wrote a review.
    - I would like to edit the review to add, remove or adjust parts of my description.
    - I would like to see when I edited a movie review.
    - I would like to change my rating score for a movie.
    - I would like to view all the reviews I have written.
    - I would like to remove my existing review.

- As an Administrative User:

    - I would like to add a movie to the database.
    - I would like to edit an existing movie such as the title, year of release, genre, director, cast and image.
    - I would like to delete or edit an existing review written by all users, in case the contents are inappropriate. 

## Design
### Colour Scheme
- The colours used for the project were taken from materialize.css. The site has a range of colours which I chose to mainly use the dark-grey pallete for the backgrounds. Having a dark background gave the site a feeling of a cinema experience. For the headings, navigation and footer I used a deep orange which compliments the dark background. For the text, I used the colour white for readability. 
The buttons were also from materialize.css which were recoloured as appropriate. Red for Delete, and blue for Submit/Edit. 

### Typography
- The font-family used for headings, movie titles and navigation bar is "Squada One". This gave a unique look to the site and inline to the topic.
The general body font used is "Encode". "Sans-Serif" is used as the fallback for situations where the initial fonts were failing to process.



### Wireframes and Mockups
- The design for the wireframes were created using Balsamiq. These can be viewed [here](./static/readme-images/wireframes.pdf).

# Features

## Navigation Bar and footer
- The navigation bar is fixed at the top of all pages for easy navigation. On small devices, the nav bar will be compressed into a side menu which will open upon pressing the burger menu icon.

- The footer contains icons for social media links. The landing page for these will be the home page per social media site. No actual account was created for the website as this is for educational purposes.

## Home page
- There is a welcome message and a brief description of the website.

- There will be two panels showing at all times:
    - The first panel is dependant of the visitor being a registered user. If the visitor is not logged in, the panel will show links to the Log In page, or the Register page. If a user is logged in, the panel will show a Profile button, to redirect the user to the profile page.
    - The second panel is a link to redirect the all users to the Movies page.

## Movies page (List of Movies)

- The full list of movies can be found here. A search bar can be used to find particular movies. The search queries includes the movie title, movie genre, director and cast members.

- Each movie here will redirect to the individual movie page.

## Movie page (Individual Movie)
- Visitors can read reviews submitted by registered users.

- Registered users have the ability to rate and write a review. They will also be able to delete or edit their existing review. Each registered user is limited to one review per movie.

- Where a registered user is logged in and has already placed a review, a message will show that they have already reviewed that particular movie.

- Each review will have a time stamp for when the review was created. A seperate time stamp will be present if a review has been edited.

- The Administrator is able to remove or edit all reviews.

- The Administrator is able to remove the Movie from the database or edit the Movie information.

- If the user wishes to delete a review, a warning popup will appear for confirmation.

- If the Administrator wishes to delete the Movie from the database, a warning popup will appear for confirmation.

## Future Features
- User password reset function where a user may have forgotten their password.

- A welcome email for when the user first registers.

- An advanced search option for movies such as selection boxes for genres and movie list sorting.

- Display an overall rating for a movie based on the total reviews.

- Embedded movie trailers from video sites such as youtube for each movie.

- A section on the home page to show popular and new movies. This could be housed in a carousel.

# Database

### MongoDB
MongoDB is the database used to store my collection of data. There are three collections of data - Movies, Reviews and Users. 
Each of the collections have a simple key-value format. 

- Movies 
    - This contains the movie's name, year of release, genre, director, cast and image url. All are text inputs.
    - Movies can only be added or edited by the admin.
    - The movie ID is the reference point for the Reviews collection.
    - The admin cannot add duplicate movies. This is based on the movie_name such that the application will advise the admin that the movie already exists in the database.
    - The image url is taken from IMDB poster images.

- Reviews
    - When a review is posted, the movie ID and movie name is set based on the movie being reviewed. 
    - The review description is a text input by the user.
    - The username refers to the creater or writer of the review.
    - Date created is time stamped automatically.
    - If a user edits a review, this is also automaticlly added.
    - Only one review can be written per movie for each user.

- Username
    - This contains the user's username and password.
    - Upon registration, the application will advise if a username is already taken to ensure no duplicate usernames are created.


### Database Relationship

![](./static/readme-images/data-collections.png)

### MongoDB Setup 
The following steps were used to set up the database for the project.



# Credits

### Code credits
- Code institute Flask mini project video tutorials - This has assisted greatly for my project.

- Confirmation Modals - The code for creating warning modals for confirmation of deleting seperate movies or reviews - [Stack Overflow](https://stackoverflow.com/questions/28556370/confirmation-modal-for-flask-not-working-in-a-loop)

- Time stamps to show when a review was added and edited - [codegrepper.com](https://www.codegrepper.com/code-examples/python/datetime+today)

### Content
- All Movie information were obtained from [IMDB](https://www.imdb.com/?ref_=nv_home), arguably the most popular movie website.
- The Home page background image was taken from by a user named "Felix Mooneeram" on [unsplash.com](https://unsplash.com/s/photos/movie).

