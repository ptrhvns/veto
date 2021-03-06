# Veto

This website helps users make decisions faster. The following notes may not be
sufficient to completely understand the project, but they are hopefully enough
to get started.

## Architecture

* The website is split into a client and a server.
* The server is built with Python and Flask.
* The client is built with React (via create-react-app).
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
  pip -r requirements.dev.txt
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
  honcho -f Procfile.dev start
  ```

## Running Tests

### All

- Run all tests (see server test notes about editable mode first):

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

- Run server tests (see the `pytest` plugins in `requirements.dev.txt` for options):

  ```sh
  invoke -r ops/lib test:server
  ```

- View server test coverage report:

  ```sh
  invoke -r ops/lib test:server:coverage
  # Open server/coverage/index.html
  ```
