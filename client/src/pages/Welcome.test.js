import ReactDOM from 'react-dom';
import Welcome from './Welcome';
import { buildTitle } from '../lib/utils';
import { HelmetProvider } from 'react-helmet-async';
import { MemoryRouter } from 'react-router';
import { render, waitFor } from '@testing-library/react';

function renderCustom(component) {
  render(
    <HelmetProvider>
      <MemoryRouter>{component}</MemoryRouter>
    </HelmetProvider>
  );
}

it('renders successfully', () => {
  const div = document.createElement('div');
  ReactDOM.render(
    <HelmetProvider>
      <MemoryRouter>
        <Welcome />
      </MemoryRouter>
    </HelmetProvider>,
    div
  );
});

it('renders <title>', async () => {
  renderCustom(<Welcome />);
  await waitFor(() => {
    const titles = document.getElementsByTagName('title');
    expect(titles.item(0).textContent).toEqual(buildTitle('Welcome'));
  });
});
