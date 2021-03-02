import App from './App';
import ReactDOM from 'react-dom';
import { MemoryRouter } from 'react-router';
import { render, screen } from '@testing-library/react';

function renderCustom(component, path) {
  render(
    <MemoryRouter initialEntries={[path]} initialIndex={0}>
      {component}
    </MemoryRouter>
  );
}

it('renders successfully', () => {
  const div = document.createElement('div');
  ReactDOM.render(
    <MemoryRouter>
      <App />
    </MemoryRouter>,
    div
  );
});

it('renders Welcome component for "/" route', () => {
  renderCustom(<App />, '/');
  screen.getByTestId('welcome');
});

it('renders SignUp component for "/sign-up" route', () => {
  renderCustom(<App />, '/sign-up');
  screen.getByTestId('sign-up');
});

it('renders NotFound component for "/invalid" route', () => {
  renderCustom(<App />, '/invalid');
  screen.getByTestId('not-found');
});
