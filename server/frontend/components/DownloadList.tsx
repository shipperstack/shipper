import React from "react";
import Fuse from "fuse.js";

import DeviceCard from "./DeviceCard";

export default function DownloadList({
  filterBy,
  showUnmaintained,
  devices,
}: {
  filterBy: string;
  showUnmaintained: boolean;
  devices: any;
}) {
  let filtered_devices = devices;

  if (!showUnmaintained) {
    filtered_devices = filtered_devices.filter(
      (device: any) => device["enabled"],
    );
  }

  if (filterBy) {
    // Fuzzy search through all devices
    filtered_devices = new Fuse(filtered_devices, { keys: ["name"] }).search(
      filterBy,
    );

    // Map results returned from Fuse.js to remove item enclosing
    filtered_devices = filtered_devices.map((result: any) => result.item);
  }

  function sortActive(a: any, b: any) {
    return a["enabled"] === b["enabled"] ? 0 : a["enabled"] ? -1 : 1;
  }

  function sortName(a: any, b: any) {
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
          {filtered_devices.map((device: any) => {
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
