# User Authentication System

This project is a user authentication system built with FastAPI and PostgreSQL. It provides functionalities for user registration, email verification, user login, and user logout.

## Features

### User Registration

The `create_user` function is used to register a new user. It checks if the email already exists in the database. If not, it creates a new user with the provided details. The first registered user is assigned the role of "admin", and all subsequent users are assigned the role of "user". A verification token is generated and sent to the user's email for account verification.

### Email Verification

The `verify_user_email` function is used to verify a user's email. It checks if the user exists in the database and if the provided verification token matches the one in the database. If the verification is successful, the user's account is marked as verified.

### User Login

The `login_user` function is used for user login. It checks if the user exists in the database and if the provided password matches the one in the database. If the user is verified and the password is correct, a JWT token is generated and sent to the user. The JWT token is also attached to the response as a cookie.

### User Logout

The `logout_user` function is used for user logout. It deletes the user's token from the database and removes the cookies from the response.

## Setup

### Environment Variables

The following environment variables are required:

- `DATABASE_USER`: The username for the PostgreSQL database.
- `DATABASE_PASSWORD`: The password for the PostgreSQL database.
- `DATABASE_HOST`: The host of the PostgreSQL database.
- `DATABASE_PORT`: The port of the PostgreSQL database.
- `DATABASE_NAME`: The name of the PostgreSQL database.
- `SECRET_KEY`: The secret key for JWT token generation.
- `ALGORITHM`: The algorithm for JWT token generation.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The expiration time for the access token.
- `EMAIL_PASSWORD`: The password for the email account used to send verification emails.
- `EMAIL_USERNAME`: The username for the email account used to send verification emails.
- `EMAIL_SERVER`: The server for the email account used to send verification emails.
- `EMAIL_PORT`: The port for the email account used to send verification emails.

### Docker

This project uses Docker for easy setup and deployment. The `docker-compose.yml` file is used to create a Docker container for the FastAPI application and a Docker container for the PostgreSQL database.

To build and run the Docker containers, use the following command:

```bash
docker-compose up --build


The FastAPI application will be available at `http://localhost:8000`.

## Testing

To run the tests, use the following command:

```bash
pytest

Here is the text you provided, formatted with Markdown:

```markdown
The FastAPI application will be available at `http://localhost:8000`.

## Testing

To run the tests, use the following command:

```bash
pytest
```

Make sure to install the required packages listed in the `requirements.txt` file before running the tests:

```bash
pip install -r requirements.txt
```

## Deployment

To deploy the application, you can use any cloud service that supports Docker, such as AWS, Google Cloud, or Heroku. Make sure to set the environment variables as described in the "Environment Variables" section.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```