import { Route } from "react-router";
import * as React from "react";
import { MailValidation } from "./MailValidation";

export default () => {
  return (
    <React.Fragment>
      <Route path="/validation" component={MailValidation} />
    </React.Fragment>
  );
};
