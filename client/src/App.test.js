import App from './App';
import ReactDOM from 'react-dom';
import { MemoryRouter } from 'react-router';
import { render, screen } from '@testing-library/react';

function renderWithRouting(component, path) {
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
  renderWithRouting(<App />, '/');
  screen.getByTestId('welcome');
});

it('renders NotFound component for "/invalid" route', () => {
  renderWithRouting(<App />, '/invalid');
  screen.getByTestId('not-found');
});
