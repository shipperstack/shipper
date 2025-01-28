import React from "react";

export default function SearchBar({
  searchTerm,
  setSearchTerm,
}: {
  searchTerm: string;
  setSearchTerm: React.Dispatch<React.SetStateAction<string>>;
}) {
  function changedInput(event: React.ChangeEvent<HTMLInputElement>) {
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
