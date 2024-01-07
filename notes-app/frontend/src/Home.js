import React from "react";
import { useAuth } from "react-oidc-context";

const Home = () => {
  const auth = useAuth();
  return (
    <div className="home-container">
      <div className="home-content">
        <h1 className="home-heading">Welcome to Reminder App</h1>
        <p className="home-text">
          Never forget important tasks again. Manage your reminders effortlessly
          with Reminder App.
        </p>
        <button
          className="signin-btn"
          onClick={() => {
            console.log(process.env.REACT_APP_PROJECT_URL + "/dashboard");
            auth.signinRedirect({
              redirect_uri: process.env.REACT_APP_PROJECT_URL + "/dashboard",
            });
          }}
        >
          Sign In
        </button>
      </div>
    </div>
  );
};

export default Home;
