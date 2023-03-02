# Welcome to Earworm!

Earworm is a BEW project that enabled me to learn how to build a database, create models, set up authentication and routes, then pass information from my database through to a web application.

## How to run
```
pip3 install -r requirements.txt
python3 app.py
```

## Hosting
A version of earworm is currently hosted online at https://earworm.onrender.com. This is a free hosting solution so loading may take some time.

## Note about content and images
This is a school project, not a profitable venture or real app. I've used images and texts from online sources but they are only used for educational purposes. No copyright infringement is intended.

## Routes and use
Earworm is intended to be a music recommendation platform. Users can create an account, follow artists, add artists and albums, then provide reviews for those albums (including a star rating). All users' reviews are visible but a user can have a private profile which will show their name as 'Anonymous' and will not include an avatar.

Only logged in users can perform CRUD functions, which was part of the assignment. Utilising Jinja2, users who created a specific review can see options to edit / delete the review but logged in users can only read it.

The user profile pulls through a list of artists the user has liked, and a summary of reviews they have contributed, along with an avatar (or a site wide avatar if one is not provided) and a short bio.

### Routes created:
AUTH:
- login
- signup
- profile
- edit_profile
- delete_profile

MAIN:
- homepage
- search
- search_results
- about
- contact
- all_earworms (presented to user as browse)
- add_artist
- edit_artist
- artist_detail
- add_album
- edit_album
- album_detail
- all_albums
- all_artists
- all_users
- create_review
- edit_review
- delete_review
- like_artist
- unlike_artist

## What I've learned from this project
- How to set up a SQLite / PostGres database
- Designing models and ERDs
- Setting up authentication routes
- Setting up general navigation routes
- GET and POST requests
- Implemented db and forms using SQLAlchemy, Flask and WTForms
- Built html templates and rendered in the backend, using Jinja2

Particularly pleased about the design and usability of the site - a lot of hours went into the user flow and experience.
I enjoyed figuring out Mixins for the forms and partials in the templates to make my code more DRY.

## Future development ideas
- API integration with Spotify
- There's a CSRF form token error on edit profile
- Would like to set up admin authorization so not all users can create albums/artists
- Probably need to rebuild the Artist / Album model to have a relational table bridging the two
- More javascript to add character count to user inputs of larger text (reviews etc)
- Real user testing and genuine data would be great

## Resources
- Rating Stars were styled thanks to really helpful codepen: https://codepen.io/nnoy01/pen/VwPdeNo
- Form element styling implemented thanks to googling this from SO: https://stackoverflow.com/questions/9599551/wtforms-support-for-input-readonly-attribute
- Read-only attritbute figured out thanks to: https://stackoverflow.com/questions/9599551/wtforms-support-for-input-readonly-attribute

# Screenshots
## Homepage - Splash
![image](https://user-images.githubusercontent.com/33559193/222305078-fda33120-6428-4db7-9800-2790369022a3.png)
## Browse - all
<img width="2513" alt="Screenshot 2023-03-01 at 5 12 17 PM" src="https://user-images.githubusercontent.com/33559193/222305166-637e1b50-6a28-4023-8b42-249de68680c1.png">
## Artist detail
<img width="1558" alt="Screenshot 2023-03-01 at 5 20 08 PM" src="https://user-images.githubusercontent.com/33559193/222306198-993af639-bbe9-4b73-96f6-12db9f367bd7.png">
## Album detail
<img width="1483" alt="Screenshot 2023-03-01 at 5 20 51 PM" src="https://user-images.githubusercontent.com/33559193/222306280-03dd8458-61ab-4c6a-b9cc-d92f0b44b9f0.png">
## Review detail
<img width="1414" alt="Screenshot 2023-03-01 at 5 22 54 PM" src="https://user-images.githubusercontent.com/33559193/222306570-029974ef-2582-46cf-92a6-45d22f76407b.png">
## All users
<img width="1523" alt="Screenshot 2023-03-01 at 5 24 06 PM" src="https://user-images.githubusercontent.com/33559193/222306678-1adac88c-2f80-4372-9efb-57d5f70be028.png">



