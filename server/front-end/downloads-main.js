import React from "react";
import {createRoot} from "react-dom/client";

const container = document.getElementById('root');
const root = createRoot(container);
function DownloadList() {
    const ACTIVE_DEVICES = JSON.parse(document.getElementById('active-devices').textContent);

    return (
        <div className="container" style={{marginTop: "5px", marginBottom: "30px"}}>
            <div className="row row-cols-1 row-cols-md-4 g-4">
                {ACTIVE_DEVICES.map(device => {
                    let device_card_style = device.enabled ? "col" : "col disabled-device-card";
                    let device_photo_url = device.photo_url === "" ? "static/img/no_device_image.png" : device.photo_url;
                    let device_card_title_style = device.enabled ? "card-title" : "card-title text-reset text-decoration-line-through";
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


root.render(<DownloadList />);