import React, { Component } from "react";
import { HashRouter } from "react-router-dom";
import Home from "./controllers/Home";
import DataUpload from "./controllers/DataUpload";
import { EDA } from "./controllers/EDA";
import { Predict }  from "./controllers/Predict";
import { Session } from "./controllers/Session";
import { ReactComponent as Logo} from './icons/epa-logo.svg';  // eslint-disable-next-line 
import './styles/App.css';
import './styles/base.css';

class App extends Component {
render() {
  return (
    <HashRouter>
      <Session />
      <div className="App">
      <link rel="{Logo}"/>
      <header class="header">
        <div class="header-img-wrapper">
          <h1>Environmental Performance Analyzer</h1>
        </div>
      </header>

      <nav class="sticky navbar fixed-top">
        <div class="brand  display__logo">
          <a href="#top" class="nav__link">
            <div class="logo-icon-menu logo"><Logo/></div>
          </a>
        </div>

        <input type="checkbox" id="nav" class="hidden" />
        <label for="nav" class="nav__open"><i></i><i></i><i></i></label>
        <div class="nav">
          <ul class="nav__items">
            <li class="nav__item"><a href="#upload" class="nav__link">Upload</a></li>
            <li class="nav__item"><a href="#analyze" class="nav__link">Analyze</a></li>
            <li class="nav__item"><a href="#predict" class="nav__link">Predict</a></li>
          </ul>
        </div>
      </nav>

      <main>
        <section>
          <div class="section-wrapper pt-5 mt-2" id="intro">
            <Home />
          </div>
        </section>
        <section>
          <div class="section-wrapper" id="upload">
            <h1>Upload data</h1>
            <DataUpload />
          </div>
        </section>
        <section>
          <div class="section-wrapper hidden" id="analyze">
            <h1>Exploratory Data Analysis</h1>
            <EDA />
          </div>
        </section>
        <section>
          <div class="section-wrapper hidden" id="predict">
            <h1>Predict</h1>
            <Predict />
          </div>
        </section>
      </main>

      <footer class="footer">
        <h1>Footer</h1>
      </footer>
      </div>
    </HashRouter>
  );
}
}
export default App;
