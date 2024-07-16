import React from "react";
import Fuse from "fuse.js";

import DeviceCard from "./DeviceCard";

export default function DownloadList({ filter, showUnmaintained, devices }) {
  let filtered_devices = devices;

  if (!showUnmaintained) {
    filtered_devices = filtered_devices.filter((device) => device["enabled"]);
  }

  if (filter) {
    // Fuzzy search through all devices
    filtered_devices = new Fuse(filtered_devices, { keys: ["name"] }).search(
      filter,
    );

    // Map results returned from Fuse.js to remove item enclosing
    filtered_devices = filtered_devices.map((result) => result.item);
  }

  function sortActive(a, b) {
    return a["enabled"] === b["enabled"] ? 0 : a["enabled"] ? -1 : 1;
  }

  function sortName(a, b) {
    return a["name"] > b["name"];
  }

  filtered_devices = filtered_devices.sort(sortName).sort(sortActive);

  return (
    <div
      className="container"
      style={{ marginTop: "5px", marginBottom: "30px" }}
    >
      {filtered_devices && filtered_devices.length ? (
        <div className="row row-cols-1 row-cols-md-4 g-4">
          {filtered_devices.map((device) => {
            console.log(device);
            return <DeviceCard device={device} key={device.codename} />;
          })}
        </div>
      ) : (
        <p>There are no devices matching the search criteria.</p>
      )}
    </div>
  );
}
