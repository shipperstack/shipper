import React from "react";

export default function SearchBar({ searchTerm, setSearchTerm }) {
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
