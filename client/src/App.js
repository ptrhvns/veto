import NotFound from './pages/NotFound';
import Welcome from './pages/Welcome';
import { HelmetProvider } from 'react-helmet-async';
import { Route, Switch } from 'react-router-dom';

function App() {
  return (
    <>
      <HelmetProvider>
        <Switch>
          <Route exact path="/">
            <Welcome />
          </Route>
          <Route path="*">
            <NotFound />
          </Route>
        </Switch>
      </HelmetProvider>
    </>
  );
}

export default App;
