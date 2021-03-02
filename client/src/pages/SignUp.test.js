import ReactDOM from 'react-dom';
import SignUp from './SignUp';
import { HelmetProvider } from 'react-helmet-async';

it('renders successfully', () => {
  const div = document.createElement('div');
  ReactDOM.render(
    <HelmetProvider>
      <SignUp />
    </HelmetProvider>,
    div
  );
});
