import React from "react";
import { createRoot } from "react-dom/client";
import Fuse from "fuse.js";

const root = createRoot(document.getElementById("root"));

const ACTIVE_DEVICES = JSON.parse(
  document.getElementById("active-devices").textContent,
);

function App() {
  let [searchTerm, setSearchTerm] = React.useState("");
  return (
    <>
      <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
      <DownloadList filter={searchTerm} />
    </>
  );
}

function SearchBar({ searchTerm, setSearchTerm }) {
  function changedInput(event) {
    setSearchTerm(event.target.value);
  }

  return (
    <input
      className="form-control"
      type="text"
      placeholder="Search for devices"
      value={searchTerm}
      onChange={changedInput}
    />
  );
}

function DownloadList({ filter }) {
  let filtered_devices;

  if (filter) {
    // Fuzzy search through all devices
    filtered_devices = new Fuse(ACTIVE_DEVICES, {keys: ['name']}).search(filter);

    // Map results returned from Fuse.js to remove item enclosing
    filtered_devices = filtered_devices.map((result) => result.item)
  } else {
    filtered_devices = ACTIVE_DEVICES;
  }

  return (
    <div
      className="container"
      style={{ marginTop: "5px", marginBottom: "30px" }}
    >
      <div className="row row-cols-1 row-cols-md-4 g-4">
        {filtered_devices.map((device) => {
          let device_card_style = device.enabled
            ? "col"
            : "col disabled-device-card";
          let device_photo_url =
            device.photo_url === ""
              ? "static/img/no_device_image.png"
              : device.photo_url;
          let device_card_title_style = device.enabled
            ? "card-title"
            : "card-title text-reset text-decoration-line-through";
          return (
            <div className={device_card_style} key={device.codename}>
              <a className="card-url" href={device.url}>
                <div className="card h-100">
                  <img src={device_photo_url} className="card-img-top"></img>
                  <div className="card-body">
                    <h5 className={device_card_title_style}>{device.name}</h5>
                  </div>
                </div>
              </a>
            </div>
          );
        })}
      </div>
    </div>
  );
}

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

const commit_version = `Running commit ${COMMIT_VERSION}`;
console.log(commit_version);