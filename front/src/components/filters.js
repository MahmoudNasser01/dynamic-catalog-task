// components/Filters.js
import React from "react";
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
} from "@mui/material";

const Filters = ({
  categories,
  categoryId,
  searchQuery,
  attributes,
  filters,
  handleCategoryChange,
  handleFilterChange,
  handleSearch,
  setSearchQuery,
}) => {
  return (
    <div className="filters">
      <FormControl fullWidth>
        <InputLabel id="category-label">Select Category</InputLabel>
        <Select
          labelId="category-label"
          value={categoryId}
          onChange={handleCategoryChange}
          label="Select Category"
          fullWidth
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          {categories.map((category) => (
            <MenuItem key={category.id} value={category.id}>
              {category.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <TextField
        label="Search products..."
        variant="outlined"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        fullWidth
      />

      <Button
        onClick={handleSearch}
        variant="contained"
        color="primary"
        disabled={!categoryId}
      >
        Search
      </Button>

      {attributes.length > 0 && (
        <div className="filter-fields">
          {attributes.map((attribute) => (
            <TextField
              key={attribute.id}
              label={attribute.name}
              variant="outlined"
              name={attribute.name}
              value={filters[attribute.name] || ""}
              onChange={(e) => handleFilterChange(e, attribute.id)}
              fullWidth
              margin="normal"
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Filters;
