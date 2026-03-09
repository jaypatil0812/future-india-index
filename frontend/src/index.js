import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import axios from "axios";

// Bypass localtunnel's phishing interstitial page
axios.defaults.headers.common['Bypass-Tunnel-Reminder'] = 'true';

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
