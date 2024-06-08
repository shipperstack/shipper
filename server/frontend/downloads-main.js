import React from "react";
import {createRoot} from "react-dom/client";
import Fuse from "fuse.js";

const root = createRoot(document.getElementById("root"));

const ACTIVE_VISIBLE_DEVICES = JSON.parse(
    document.getElementById("active-visible-devices").textContent,
);

function App() {
    let [searchTerm, setSearchTerm] = React.useState("");
    let [showUnmaintained, setShowUnmaintained] = React.useState(false);

    return (
        <>
            <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm}/>
            <OptionsBar showUnmaintained={showUnmaintained} setShowUnmaintained={setShowUnmaintained}/>
            <DownloadList filter={searchTerm} showUnmaintained={showUnmaintained}/>
        </>
    );
}

function SearchBar({searchTerm, setSearchTerm}) {
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

function OptionsBar({showUnmaintained, setShowUnmaintained}) {
    return (
        <label>
            <input
                type="checkbox"
                checked={showUnmaintained}
                onChange={e => setShowUnmaintained(e.target.checked)}
            /> Show unmaintained devices
        </label>
    )
}

function DownloadList({filter, showUnmaintained}) {
    let filtered_devices = ACTIVE_VISIBLE_DEVICES;

    if (!showUnmaintained) {
        filtered_devices = filtered_devices.filter(device => device["enabled"]);
    }

    if (filter) {
        // Fuzzy search through all devices
        filtered_devices = new Fuse(filtered_devices, {keys: ['name']}).search(filter);

        // Map results returned from Fuse.js to remove item enclosing
        filtered_devices = filtered_devices.map((result) => result.item)
    }

    function sortActive(a, b) {
        return (a["enabled"] === b["enabled"]) ? 0 : a["enabled"] ? -1 : 1;
    }

    function sortName(a, b) {
        return a["name"] > b["name"];
    }

    filtered_devices = filtered_devices.sort(sortName).sort(sortActive);

    return (
        <div
            className="container"
            style={{marginTop: "5px", marginBottom: "30px"}}
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
                })}
            </div>
        </div>
    );
}

root.render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>,
);

const build_date = `Built on ${BUILD_DATE}`;
console.log(build_date);