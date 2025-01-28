import React from "react";

export default function OptionsBar({
  showUnmaintained,
  setShowUnmaintained,
}: {
  showUnmaintained: boolean;
  setShowUnmaintained: (value: boolean) => void;
}) {
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
