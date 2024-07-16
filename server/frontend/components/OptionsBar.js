import React from "react";

export default function OptionsBar({ showUnmaintained, setShowUnmaintained }) {
  return (
    <label>
      <input
        type="checkbox"
        checked={showUnmaintained}
        onChange={(e) => setShowUnmaintained(e.target.checked)}
      />{" "}
      Show unmaintained devices
    </label>
  );
}
