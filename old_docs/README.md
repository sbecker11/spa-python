# Python GUI Application

This project is a Python GUI application with the following features:

- A home page with a "Hello World" message that stays centered within the window when resized.
- A horizontal menu bar at the top with links: Home, About, Register, Login, Profile, and Quit.
- Each link displays controls and content appropriate for the link name.

## Features

### Home
- Displays the home page content with a "Hello World" message centered in the window.

### About
- Displays an about page with an image of an attractive couple.

### Register
- Displays a form with "Email" and "Password" fields and a "Register" button.
- Fields are validated as needed.
- The "Register" button submits the email and password to create a unique account.
- Accounts are stored in a local file-based data store that retains values after the app is terminated.

### Login
- Displays a form with "Email" and "Password" fields and a "Login" button.
- If login is unsuccessful, a message is displayed informing if the email and/or password is not valid or does not match a stored account.
- If both email and password match a stored account, the "Profile" page is shown.

### Profile
- Displays a form with "Email" and "Password" fields and a "Save Profile" button.
- Fields are editable and subject to validation rules.
- Accounts are indexed by a non-changeable primary key, so email and password can be modified at any time.
- An error is reported if the new email address is not unique.

### Quit
- Closes the application.

## Packaging

- The application is packaged as a single standalone application.
- An installer can be downloaded from the web.
- The installer installs an executable package in the user's "Downloads" folder.
- The installer informs the user that the application package can be moved or copied to the user's Applications folder.
- Deleting the app package from the system's File Explorer deletes all code and data files without fanfare.

## Approximate Time for Development

The approximate time to create this packaged app and make it ready for testing is not provided.
