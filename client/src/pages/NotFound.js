import { buildTitle } from '../lib/utils';
import { Helmet } from 'react-helmet-async';

function NotFound() {
  return (
    <>
      <Helmet>
        <title>{buildTitle('Not Found')}</title>
      </Helmet>

      <div data-testid="not-found">
        <p>The page you requested was not found.</p>
      </div>
    </>
  );
}

export default NotFound;
