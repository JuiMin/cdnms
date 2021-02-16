import React from "react";
import ReactDOM from "react-dom";
import Codenames from "./Codenames";
ReactDOM.render(
  <Codenames baseURL={window.baseURL} />,
  document.getElementById("content")
);
