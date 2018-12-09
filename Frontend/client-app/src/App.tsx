import TabMenu from "./components/tab-menu/TabMenu";
import rootStore from "./store/root-store";
import BrowseRoute from "./components/provider/browse-jobs"
import HomeRoute from "./components/home";
import AddJobRoute from "./components/jobs/add-job-form";
import ClientListRoute from "./components/clients/client-list";
import User from "./components/user/User";
import EditProfileRoute from "./components/user/edit-profile";
import UserOffersRoute from "./components/user/offers";
import "./App.css";

import { Provider } from "mobx-react";
import * as React from "react";
import { Router } from "react-router-dom";
import { withCookies, Cookies } from 'react-cookie';
import { createBrowserHistory } from "history";
import {Register} from "./components/register/Register";
import {TabMenuProps} from "./components/tab-menu/TabMenuProps";
import {HeaderTabs} from "./view-models/header-tabs";


interface Props {
    cookies: Cookies
}

class App extends React.Component<Props> {
    constructor(props) {
        super(props);

    }

    public render() {
      // try to load the cookies
      const username = this.props.cookies.get("username");
      const userType = this.props.cookies.get("userType");
      const logged = username !== undefined && userType !== undefined;

      // this.props.cookies.set("username", "bob");
      // this.props.cookies.set("userType", "client");

      return (
      <div className="App">
          <Provider {...rootStore}>
              <React.Fragment>
                  {!logged ? ( // if not logged in, show the register screen
                      <React.Fragment>
                          <Register/>
                      </React.Fragment>
                  ) : null}


                  {userType === 'client' ? ( // client home page
                      <React.Fragment>
                          <Router history={createBrowserHistory()}>
                              <React.Fragment>
                                  <User />
                                  <header className="App-header">Student Jobs</header>

                                  <TabMenu
                                      viewStore={rootStore.viewStore}
                                      menuOptions={[
                                          new TabMenuProps(HeaderTabs.home, "/home", "Home"),
                                          new TabMenuProps(HeaderTabs.add, "/add", "Add a job"),
                                          new TabMenuProps(HeaderTabs.clients, "/clients", "Other clients")
                                      ]}
                                  />
                                  <HomeRoute />
                                  <AddJobRoute />
                                  <ClientListRoute />
                                  <EditProfileRoute />
                                  <UserOffersRoute />
                              </React.Fragment>
                          </Router>
                      </React.Fragment>
                  ) : null}


                  {userType === 'provider' ? (  // provider home page
                      <React.Fragment>
                          <Router history={createBrowserHistory()}>
                              <React.Fragment>
                                  <User />
                                  <header className="App-header">Provider screen</header>

                                  <TabMenu
                                      viewStore={rootStore.viewStore}
                                      menuOptions={[
                                          new TabMenuProps(HeaderTabs.home, "/home", "Home"),
                                          new TabMenuProps(HeaderTabs.browse, "/browse", "Browse"),
                                      ]}
                                  />
                                  <HomeRoute />
                                  <BrowseRoute />
                                  <EditProfileRoute />
                                  <UserOffersRoute />
                              </React.Fragment>
                          </Router>
                      </React.Fragment>
                  ) : null}
              </React.Fragment>
          </Provider>
      </div>
    );
  }
}
export default withCookies(App); // withCookies adds this.props.cookies
