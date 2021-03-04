# Veto

This website helps users make decisions faster. The following notes may not be
sufficient to completely understand the project, but they are hopefully enough
to get started.

## Architecture

* The website is split into a client and a server.
* The server is built with Python and Flask.
* The client is built with React (via create-react-app).
* Heroku is used for production deployments.
* Sentry is used to track errors.

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
  (cd client; npm install)
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

- Start client and server. The client will proxy API calls to the server. (In
  production, only the server will be started. The client will be built as a
  set of static assets, and served by the server when visiting the root route):

  ```sh
  honcho -f Procfile.development start
  ```

## Running Tests

### All

- Run all tests:

  ```sh
  invoke -r ops/lib test:all
  ```

### Client

- Run client tests:

  ```sh
  invoke -r ops/lib test:client
  ```

- View client test coverage report:

  ```sh
  invoke -r ops/lib test:client:coverage
  ```

### Server

- Install server package in editable mode:

  ```sh
  (cd server; pip install -e .)
  ```

- Run server tests (see the `pytest` plugins in `requirements.development.txt` for options):

  ```sh
  invoke -r ops/lib test:server
  ```

- View server test coverage report:

  ```sh
  invoke -r ops/lib test:server:coverage
  # Open server/coverage/index.html
  ```

## Setting Up a Production Environment

- Setup Heroku. See their documentation.

- Setup environment variables:

  ```sh
  # Use an appropriate value. Assumes only one domain and HTTPS.
  # For example: https://$(heroku domains --json | jq -r '.[0].hostname')
  heroku config:set CSRF_TARGET_ORIGIN=${CSRF_TARGET_ORIGIN}

  heroku config:set FLASK_APP=server.app:app
  heroku config:set FLASK_ENV=production
  heroku config:set SENTRY_ENABLED=yes

  # Use an appropriate value.
  # For example: python -c 'import os; print(os.urandom(24).hex())'
  heroku config:set SECRET_KEY=${SECRET_KEY}

  # Use an appropriate value.
  heroku config:set SENTRY_DSN=${SENTRY_DSN}

  # Use an appropriate value.
  heroku config:set SENTRY_TRACES_SAMPLE_RATE=${SENTRY_TRACES_SAMPLE_RATE}
  ```

## Releasing to Production

- Manually test that website works locally using Heroku tools:

  ```sh
  heroku local
  ```

- Build project and deploy it to production on Heroku:

  ```sh
  # Assumes git remotes origin and heroku exist.
  invoke -r ops/lib release
  ```

- Verify that production website is up and running:

  ```sh
  heroku logs
  heroku open
  ```
