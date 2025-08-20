import React from "react";
import Fuse, { type FuseResult } from "fuse.js";

import DeviceCard from "./DeviceCard";

export interface Device {
  enabled: boolean;
  photo_url: string;
  photo_thumbhash: string;
  codename: string;
  url: string;
  name: string;
}

export default function DownloadList({
  filterBy,
  showUnmaintained,
  devices,
}: {
  filterBy: string;
  showUnmaintained: boolean;
  devices: Device[];
}) {
  let filtered_devices = devices;

  if (!showUnmaintained) {
    filtered_devices = filtered_devices.filter(
      (device: Device) => device.enabled,
    );
  }

  if (filterBy) {
    // Fuzzy search through all devices
    filtered_devices = new Fuse(filtered_devices, { keys: ["name"] }).search(
      filterBy,
    ).map((result: FuseResult<Device>) => result.item);
  }

  function sortActive(a: Device, b: Device): number {
    return a.enabled === b.enabled ? 0 : a.enabled ? -1 : 1;
  }

  function sortName(a: Device, b: Device): number {
    if (a.name > b.name) {
      return -1;
    }
    if (a.name > b.name) {
      return 1;
    }
    return 0;
  }

  filtered_devices = filtered_devices.sort(sortName).sort(sortActive);

  return (
    <div
      className="container"
      style={{ marginTop: "5px", marginBottom: "30px" }}
    >
      {filtered_devices?.length ? (
        <div className="row row-cols-1 row-cols-md-4 g-4">
          {filtered_devices.map((device: Device) => {
            return <DeviceCard device={device} key={device.codename} />;
          })}
        </div>
      ) : (
        <p>There are no devices matching the search criteria.</p>
      )}
    </div>
  );
}
