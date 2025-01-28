import React from "react";
import { createRoot } from "react-dom/client";

import DownloadList from "./components/DownloadList";
import SearchBar from "./components/SearchBar";
import OptionsBar from "./components/OptionsBar";

declare let BUILD_DATE: string;

const root = createRoot(document.getElementById("root"));

const ACTIVE_VISIBLE_DEVICES = JSON.parse(
  document.getElementById("active-visible-devices").textContent,
);

function App() {
  const [searchTerm, setSearchTerm] = React.useState("");
  const [showUnmaintained, setShowUnmaintained] = React.useState(false);

  return (
    <>
      <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
      <OptionsBar
        showUnmaintained={showUnmaintained}
        setShowUnmaintained={setShowUnmaintained}
      />
      <DownloadList
        filterBy={searchTerm}
        showUnmaintained={showUnmaintained}
        devices={ACTIVE_VISIBLE_DEVICES}
      />
    </>
  );
}

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

const build_date = `Built on ${BUILD_DATE}`;
console.log(build_date);
