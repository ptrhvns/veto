import { buildTitle } from './utils';
import { Helmet, HelmetProvider } from 'react-helmet-async';

function App() {
  return (
    <>
      <HelmetProvider>
        <Helmet>
          <title>{buildTitle()}</title>
        </Helmet>
        <div>App</div>
      </HelmetProvider>
    </>
  );
}

export default App;
