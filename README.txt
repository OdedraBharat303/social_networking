# Social Networking Application

Welcome to the Social Networking Application! This README provides an overview of the project and instructions for setting it up and using it.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Docker Setup](#docker-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Social Networking Application is a Django-based platform that enables users to create accounts, connect with friends, send/receive friend requests, and search for other users. This README provides details on how to set up and use the application.

## Features

- User registration and login with email and password (case-insensitive email).
- Sending, accepting, and rejecting friend requests.
- Listing friends (accepted friend requests).
- Listing pending friend requests (received friend requests).
- Search for users by email or name.
- Rate limiting for sending friend requests (3 per minute).

## Prerequisites

Make sure you have the following software and dependencies installed:

- Python (3.x)
- Django
- Django Rest Framework
- Docker (for optional containerization)
- SQLite (for optional database)

## Getting Started

Follow these steps to set up the project:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/social-networking-app.git
   cd social-networking-app

## Install Python dependencies:
    -pip install -r requirements.txt

Configuration
    Environment Variables:
        DJANGO_SECRET_KEY: Your Django secret key.
        DJANGO_DEBUG: Set to True for development, False for production.

##Docker Setup
    1 Build Docker containers:
        -docker-compose build
    2 Run the application in Docker:
        -Run the application in Docker:

###Running the Application:
    For development:
        -python manage.py runserver
    For production (Docker):
        -docker-compose build
        -docker-compose up

## API Documentation:
    ill share you postman collection.

    Note: each api except login and signup required authentication TOKEN which you get after user login , that token you can use to call every api.

