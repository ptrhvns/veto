# Veto

This app helps users in a group select from a list of choices. It was developed
on a Linux operating system for deployment to Heroku. The following notes may
only be useful once someone has already setup the Heroku infrastructure.

## Setting Up a Development Environment

- Install programming language version managers:

  - https://github.com/pyenv/pyenv
  - https://github.com/pyenv/pyenv-virtualenv
  - https://github.com/nodenv/nodenv

- Install Python and a virtual environment:

  ```sh
  pyenv install $(cat runtime.txt)
  pyenv virtualenv $(cat runtime.txt) veto
  pyenv local "$(cat runtime.txt)/envs/veto"
  pyenv shell "$(cat runtime.txt)/envs/veto"
  ```

- Install server dependencies for development:

  ```sh
  pip -r requirements.development.txt
  ```

- Install Node.js:

  ```sh
  nodenv install $(cat client/.node-version)
  nodenv shell $(cat client/.node-version)
  ```

- Install client dependencies:

  ```sh
  cd client
  npm install
  ```

- Setup environment variables:

  ```sh
  cp .env.example .env
  # Edit values in .env.
  # SECRET_KEY=$(python -c 'import os; print(os.urandom(24).hex())')
  ```

- When working in development, start both the client app and the server app.
  The client app will proxy API calls to the server. (In production, only the
  server will be started. The client will be built as a set of static assets,
  and served by the server when visiting the root route):

  ```sh
  # In one terminal.
  cd client
  npm start

  # In another terminal.
  flask run
  ```

## Setting Up a Production Environment

- Setup environment variables:

  ```sh
  heroku config:set FLASK_APP=server.app:app
  heroku config:set FLASK_ENV=production
  # Set a specific key, or generate a random one like this:
  heroku config:set SECRET_KEY=$(python -c 'import os; print(os.urandom(24).hex())')
  ```

## Releasing to Production

- Build and deploy the production app to Heroku:

  ```sh
  invoke -r ops/lib release
  ```
