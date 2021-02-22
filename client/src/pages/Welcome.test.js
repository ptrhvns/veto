import ReactDOM from 'react-dom';
import Welcome from './Welcome';
import { buildTitle } from '../lib/utils';
import { HelmetProvider } from 'react-helmet-async';
import { render, waitFor } from '@testing-library/react';

function renderWithProviders(component) {
  render(<HelmetProvider>{component}</HelmetProvider>);
}

it('renders successfully', () => {
  const div = document.createElement('div');
  ReactDOM.render(
    <HelmetProvider>
      <Welcome />
    </HelmetProvider>,
    div
  );
});

it('renders <title>', async () => {
  renderWithProviders(<Welcome />);
  await waitFor(() => {
    const titles = document.getElementsByTagName('title');
    expect(titles.item(0).textContent).toEqual(buildTitle('Welcome'));
  });
});
