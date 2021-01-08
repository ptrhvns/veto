import { buildTitle } from './utils';
import { Helmet } from 'react-helmet';

function App() {
  return (
    <>
      <Helmet>
        <title>{buildTitle()}</title>
      </Helmet>
      <div>App</div>
    </>
  );
}

export default App;
