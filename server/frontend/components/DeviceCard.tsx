import React from "react";

import type { Device } from "./DownloadList";

export default function DeviceCard({ device }: { device: Device }) {
  const device_card_style = device.enabled ? "col" : "col disabled-device-card";
  const device_photo_url =
    device.photo_url === ""
      ? "static/img/no_device_image.png"
      : device.photo_url;

  return (
    <div className={device_card_style} key={device.codename}>
      <a className="card-url" href={device.url}>
        <div className="card h-100">
          <img src={device_photo_url} className="card-img-top"></img>
          <div className="card-body">
            <h5 className="card-title">{device.name}</h5>
          </div>
        </div>
      </a>
    </div>
  );
}
