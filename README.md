# Online Auction System

The Online Auction System is a web-based platform that allows users to create auctions, place bids, and participate in buying and selling various items through an online auction format.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- User Registration and Authentication: Users can create an account, log in, and authenticate using their credentials.
- Auction Creation: Users can create new auction listings, providing details such as title, description, starting bid, and end date.
- Bidding: Users can place bids on active auctions and manage their bidding activity.
- Auction Search: Users can search for auctions based on various criteria such as title, category, and price range.
- User Profile: Users have access to their profile information and can update their details.
- Category Management: Users can view available auction categories and explore auctions by category.

## Technologies

- Backend Development:
  - Python: Programming language for backend development.
  - Flask: Lightweight web framework for building the backend.
  - SQLite or MySQL: Database options for storing auction data.
  - Flask-RESTful: API framework for creating RESTful APIs.
- Frontend Development:
  - HTML, CSS, JavaScript: Web technologies for building the frontend user interface.
  - CSS Frameworks: Bootstrap or Bulma for responsive design and styling.
- Authentication and Authorization:
  - Flask-JWT: Lightweight authentication library for securing API endpoints.

## Future Implementation
- Payment Integration: Integration with a payment gateway API to facilitate secure payment transactions for won auctions.
- Payment Gateway Integration:
  - Stripe or PayPal: Payment gateway API for secure payment processing.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nchimunya-joseph/auction-marketplace
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - If using SQLite: No additional setup is required as SQLite creates a database file automatically.
   - If using MySQL: Set up a MySQL database and update the database configuration in `config.py`.

4. Configure the environment variables:
   - Rename the `.env` file to `.env`.
   - Update the environment variables in the `.env` file with your specific configurations.

## Usage

1. Start the application:

   ```bash
   python app.py
   ```

2. Access the application in your web browser at [https://auction-marketplace-six.vercel.app/](https://auction-marketplace-six.vercel.app/).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please submit an issue or create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---
