# Django Number to Text API

This is a challenge completed for a job interview. You can see the assessment description on the following link:

```
https://docs.google.com/document/d/1ib6iuXJTWnvY1i-9DuRk1AaFmKvEDz0otAc1uK5bm-U/edit?usp=sharing
```

## Python version

This has been developed and tested with `Python 3.10`. Other Python versions may work but it is not guaranteed.

## Implementation

When the `num_to_english` endpoint is hit, it validates the input and calls the `number2english` function. This function does the following:

1. Calls the Lexer to tokenize the received number.
2. Calls the Parser to validate the token list.
3. Create a small binary tree with the tokens before and after the decimal point.
4. Calls the Translator function and return its result.

> NOTE: The `num_to_english` endpoint is protected with JWT.

## Features

1. Easily extensible to other languages (just need to create a translator for the desired language).
2. Support integers and float
3. Support numbers with a maximum length of 36 digits on each side of the point.
4. The maximum length can be easily extended. I think 36 digits is fine, don't you?

## Installation and Usage

1. Clone the repository.
2. Get into the directory.
3. Create a virtual environment.
4. Activate the virtual environment.
5. Install the dependencies on the `requirements.txt` file.
6. Make the migrations.
7. Run the development server.
8. Create a root user.
9. Get an Access Token (fetch `/token` with the username and password of your user).
10. Fetch the `/num_to_english` as explained in the document link on the first part of this README file. Don't forget to send the `access` token as a bearer token.