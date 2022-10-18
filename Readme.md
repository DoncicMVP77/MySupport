# SupportService django rest framework
Support service api with django-rest-framework.

Want to use this project?
1. Update the environment variables in the docker-compose.yml and .env files
2. Build the images and run the containers:

    ```
    $ docker-compose up -d --build
    ```
Test it out at [http://localhost:8000](http://localhost:8000).

# SUPPORT_API ENDPOINT
| Method |  ENDPOINT | DESCRIPTION |
|--------|----------|--------------|          
|  **GET**   | api/v1/support/tickets  | Return all tickets. 
|  **POST**  | api/v1/support/ticket/create  | Create a new ticket.
|  **GET**   | api/v1/support/ticket/{slug}  | Returns the details of a ticket instance.
|  **PUT**   | api/v1/support/ticket/{slug}  | Update an existing ticket. Returns updated ticket data.
|  **DELETE**  | api/v1/support/ticket/{slug}  | Delete an existing ticket.
|  **GET**   | api/v1/support/ticket/{slug}/messages | Returns the list of messages on a particular ticket.
|  **POST**  | api/v1/support/ticket/{slug}/message/create | Create a new message instance on particular ticket. Returns created post data.
|  **GET**   | api/v1/support/ticket/{slug}/message/{id}   | Returns the details of a message instance.
|  **PUT**   | api/v1/support/ticket/{slug}/message/{id}   | Update an existing message.
|  **DELETE** | api/v1/support/ticket/{slug}/message/{id}  | Delete an existing message.

# AUTHENTICATION_API ENDPOINT
| Method |  ENDPOINT | DESCRIPTION |
|--------|----------|--------------|          
|  **POST**   | api/v1/authentication/register  | Create a new user. Returns created post data. 
|  **PUT**  | api/v1/authentication/reset_password/{pk}/  | Calls Django Auth SetPassword save method.
|  **PUT**   | api/v1/authentication/update_profile/{pk}/ | Update an existing user main information.
|  **PUT**   | api/v1/authentication/change_image/{pk}/| Update an existing user image.
|  **POST**  | api/v1/authentication/logout  | Calls Django logout method and delete the Token object assigned to the current User object.
|  **POST**   | api/v1/authentication/delete_profile/{pk}/ | Delete an existing user.
|  **POST**  | api/v1/authentication/token | Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials.
|  **POST**   | api/v1/authentication/token/refresh   | Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid
| 
