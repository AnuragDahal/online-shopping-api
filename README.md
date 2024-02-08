# Online Shopping Stores API

## Overview

This repository contains an API for online shopping stores, built using FastAPI. The API provides essential features for user authentication, order management, and administrative tasks for online shopping platforms or marts.

## Features

### FastAPI Framework

Developed on FastAPI, a modern and high-performance web framework for building APIs with Python 3.7+.

### User Authentication

- `POST /login`: Endpoint for user login.
- `POST /logout`: Endpoint for user logout.
- `POST /forgot-password`: Endpoint for user password recovery.
- `POST /reset-password`: Endpoint for resetting user password.

### User Management

- `POST /users/signup`: Endpoint for user registration.
- `GET /users/getallusers`: Endpoint to retrieve all users.
- `GET /users/getuser/{email}`: Endpoint to retrieve a user by email.
- `GET /users/getuserbyid/{user_id}`: Endpoint to retrieve a user by ID.

### Order Management

- `POST /createorder`: Endpoint to create a new order.
- `DELETE /cancel-order/{order_id}`: Endpoint to cancel a specific order.
- `GET /user/order/{user_id}`: Endpoint to retrieve orders for a specific user.
- `GET /order/status/{order_id}`: Endpoint to retrieve the status of a specific order.

### Admin Tasks

- `PUT /update-to-admin/{user_id}`: Endpoint to update a user to admin status.
- `GET /get-allorders/{admin_id}`: Endpoint to retrieve all orders for a specific admin.
- `PUT /order/update/status/{order_id}`: Endpoint to update the status of a specific order.
- `GET /getorders-bystatus`: Endpoint to retrieve orders by status.

### Authentication Mechanisms

- Cookie-based authentication for users to persist login sessions.
- JWT-based authentication for secure admin logins.

## Installation

To set up and run the API locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AnuragDahal/online-shopping-api.git
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the API:**

    ```bash
    uvicorn main:app --reload
    ```

The API will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Documentation

Explore the detailed API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for information on available endpoints, request parameters, and response formats.

## Contributing

Refer to the guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file if you wish to contribute to the development of this API.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code as per the terms of the license.

## Contact

For any inquiries or support, please contact [dahal.codecraft@gmail.com](mailto:dahal.codecraft@gmail.com).

Happy coding! 
