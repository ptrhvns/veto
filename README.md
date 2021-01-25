# Veto

This web app helps users in a group select from a list of mutually exclusive
choices while also helping to minimizing conflict. The following notes are
probably insufficient to completely understand the project, but they are
hopefully enough to get started.

## Architecture

* The web app is broken into a client and a server.
* The server is built with Python and Flask.
* The client is built with React (via create-react-app).
* Heroku is used for production deployments.
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
  $EDITOR .env
  ```

  You can generate a SECRET_KEY with:

  ```sh
  python -c 'import os; print(os.urandom(24).hex())'
  ```

- Start client and server apps. The client app will proxy API calls to the
  server. (In production, only the server will be started. The client will be
  built as a set of static assets, and served by the server when visiting the
  root route):

  ```sh
  honcho -f Procfile.development start
  ```

## Running Tests

### Server

- Install server package in editable mode:

  ```sh
  cd server
  pip install -e .
  ```

- Run tests (see the plugins in `requirements.development.txt` for more options):

  ```sh
  invoke -r ops/lib test:server
  ```

- View a detailed test coverage report:

  ```sh
  # Pick a path to output test coverage report.
  coverage html -d $PATH
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
  heroku config:set SENTRY_DSN=${SENTRY_DSN}

  # Use appropriate value.
  heroku config:set SENTRY_TRACES_SAMPLE_RATE=${SENTRY_TRACES_SAMPLE_RATE}
  ```

## Releasing to Production

- Build and deploy the production app to Heroku:

  ```sh
  invoke -r ops/lib release
  ```
