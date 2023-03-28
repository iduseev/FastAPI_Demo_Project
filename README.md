# FastAPI Demo Project

This is a demo project built with FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. 

The project includes several endpoints for performing CRUD operations on a fake database.

The project imitates a digital book shelf with the books already in. You can add or delete books from the shelf or request to show all the books available at the moment.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)


## Installation

To install and set up the project, follow these steps:

1. Clone the repository:

```git clone https://github.com/iduseev/FastAPI_Demo_Project.git```


2. Create & activate python venv

```python -m venv .venv```

```source .venv/bin/activate```


3. Install the project dependencies:

```python -m pip install -r requirements.in```


4. Run the uvicorn web-server in terminal while in the project's root directory using the following command:

```uvicorn backend.endpoints:app --reload```

This will start the FastAPI server on `http://localhost:8000`.


## Usage

To use the project, you need to authorize first using the username/password pair for the existing user.

JWT token is assigned to the current user by sending a `POST` request to `/token` endpoint.

After that, you are able to send HTTP requests to the various endpoints using a tool like `curl` or a web browser extension like Postman. 

For example, to add a new book, send a `POST` request to the `/books/add_book` endpoint:

```curl -X POST -H "Content-Type: application/json" -d '{"book_name": "The Adventures of Tom Sawyer", "author": "Mark Twain", "description": "An 1876 novel about a boy growing up along the Mississippi River"}' http://localhost:8000/books/add_book```

Such endpoints as `/` or `/about` are available for non-authorized users as well.


## API Documentation

The API documentation is generated automatically by FastAPI.

THe documentation compatible with OpenAPI (former Swagger) schema can be accessed at `http://localhost:8000/docs`.
Alternative documentation (ReDoc) is available via `http://localhost:8000/redoc`. 
The documentation includes detailed information on each endpoint, including request and response schemas, example requests and responses, and possible status codes.


## Contributing

If you'd like to contribute to this project, please fork the repository and create a new branch for your changes. Then, submit a pull request with a detailed description of your changes.


## Credits

Thanks to the FastAPI team for creating such a powerful and easy-to-use web framework.


## License

This project is licensed under the MIT License.
