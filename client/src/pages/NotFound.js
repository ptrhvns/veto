import { buildTitle } from '../lib/utils';
import { Helmet } from 'react-helmet-async';

function NotFound() {
  return (
    <>
      <Helmet>
        <title>{buildTitle('Not Found')}</title>
      </Helmet>

      <p>The page you requested was not found.</p>
    </>
  );
}

export default NotFound;
