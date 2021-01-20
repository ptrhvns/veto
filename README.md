# Veto

This web app helps users in a group select from a list of mutually exclusive
choices while minimizing conflict. Setup and visit the web app itself to get a
better idea of its purpose.

This is a portfolio project built to help me demonstrate my web development
skills. It was developed in a Linux environment, and for deployment to Heroku.

The following notes are probably insufficient to completely understand the
project, but my hope is that there are at least enough clues for an experienced
developer to get things working. I welcome feedback.

## Architecture

* The server was built with Python and Flask.
* The client was built with React.
* Heroku is used for production deployment.
* Sentry is used to track errors and performance.

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

## Running Tests

### Server

- Install server package in *editable* mode:

  ```sh
  cd server
  pip install -e .
  ```

- Run tests (see the plugins in `requirements.development.txt` for more options):

  ```sh
  invoke -r ops/lib test:server
  ```

- View detailed test coverage report:

  ```sh
  # Pick a path to output test coverage report.
  coverage html -d ${PATH}
  # Open path with a browser.
  ```

## Setting Up a Production Environment

- Setup Heroku. See their documentation.

- Setup environment variables:

  ```sh
  heroku config:set FLASK_APP=server.app:app
  heroku config:set FLASK_ENV=production
  heroku config:set SENTRY_ENABLED=yes

  # Set a specific key, or generate a random one like this:
  heroku config:set SECRET_KEY=$(python -c 'import os; print(os.urandom(24).hex())')

  # Use appropriate value.
  heroku config:set SENTRY_DSN=...

  # Use appropriate value.
  heroku config:set SENTRY_TRACES_SAMPLE_RATE=...
  ```

## Releasing to Production

- Build and deploy the production app to Heroku:

  ```sh
  invoke -r ops/lib release
  ```
