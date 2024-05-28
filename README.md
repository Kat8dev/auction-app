# Auction Site

## Description

This project is a web-based auction site built using Django. Users can create auction listings, place bids, comment on listings, and manage their watchlist. The site also includes an administrative interface for managing the listings, bids, and comments.

## Features

- User authentication and authorization
- Create, view, and manage auction listings
- Place bids on listings
- Comment on listings
- Add and remove listings from a personal watchlist
- Category-based listing browsing

## Project Overview

Watch the demo video below:

<div align="center">
  <iframe width="560" height="315" src="https://www.youtube.com/watch?v=Bl4wHD_XAiU" frameborder="0" 
    allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

### Models

The application includes the following models in addition to the User model:

1. **AuctionListing**: Represents an auction listing with fields for title, description, starting bid, image URL, category, and status.
2. **Bid**: Represents a bid on an auction listing with fields for the bid amount, user, and listing.
3. **Comment**: Represents a comment on an auction listing with fields for the content, user, and listing.
4. **Category**: Represents a category for auction listings.
5. **Watchlist**: Represents a user's watchlist for auction listings.

### Functionalities

1. **Create Listing**: Users can create a new auction listing by specifying a title, description, starting bid, and optionally providing an image URL and selecting a category.

2. **Active Listings Page**: The default route of the application displays all active auction listings, showing the title, description, current price, and photo (if provided).

3. **Listing Page**: Clicking on a listing takes users to a detailed page showing all the details about the listing, including the current price. Logged-in users can:
   - Add the item to their watchlist or remove it.
   - Place a bid on the item if the bid meets the requirements.
   - Close the auction if they are the creator of the listing.
   - View if they have won the auction if the listing is closed.

4. **Bidding**: Users can place bids on active listings. The bid must be at least as large as the starting bid and higher than any other bids.

5. **Watchlist**: Logged-in users can view their watchlist, which shows all the listings they have added. Clicking on a listing in the watchlist takes the user to the detailed listing page.

6. **Comments**: Logged-in users can add comments to a listing, and all comments are displayed on the listing page.

7. **Categories**: Users can view all listing categories and see all active listings within a selected category.

8. **Django Admin Interface**: The admin interface allows site administrators to view, add, edit, and delete any listings, comments, and bids.


## Usage

- **Creating a Listing**: Log in and navigate to the "Create Listing" page. Fill out the form and submit to create a new auction listing.
- **Bidding**: Navigate to an active listing and place a bid if the bid requirements are met.
- **Managing Watchlist**: Add or remove listings from your watchlist.
- **Commenting**: Add comments to any listing.
- **Closing an Auction**: If you are the creator of a listing, you can close the auction.
- **Admin Interface**: Access the Django admin interface at `http://127.0.0.1:8000/admin/` to manage the site.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project is part of the CS50's Web Programming with Python and JavaScript course.
