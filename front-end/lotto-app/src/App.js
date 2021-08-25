import { Switch, Route } from 'react-router-dom';
import './App.css';

import Header from './components/header.component'
import HomePage from './pages/homepage.page'
import CreateRafflePage from './pages/create-raffle.page'

function App() {
  return (
    <div>
        <Header/>
        <Switch>
          <Route exact path='/' component={HomePage} />
          <Route exact path='/create-raffle' component={CreateRafflePage} />
        </Switch>

    </div>
  );
}

export default App;
