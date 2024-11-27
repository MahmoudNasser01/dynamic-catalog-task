import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import ProductList from "./components/ProductList";
import Filters from "./components/filters";
import "./css/app.css";
import { Typography, Button } from "@mui/material";
import { fetchProductsAPI, fetchCategoryAttributesAPI } from "./services/apiService";

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [categoryId, setCategoryId] = useState("");
  const [attributes, setAttributes] = useState([]);
  const [filters, setFilters] = useState({});
  const [error, setError] = useState("");
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/categories/");
        const data = await response.json();
        if (response.ok) {
          setCategories(data);
        } else {
          setError("Failed to fetch categories.");
        }
      } catch (error) {
        setError("An error occurred while fetching categories.");
      }
    };

    fetchCategories();

    if (localStorage.getItem("token")) {
      setIsLoggedIn(true);
      fetchProducts();
    }
  }, []);

  const fetchProducts = async (queryParams = "") => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Please log in to view products.");
      return;
    }

    try {
      const data = await fetchProductsAPI(token, queryParams);
      setProducts(data);
      setFilteredProducts(data);
      setError("");
    } catch (error) {
      setError("Failed to fetch products.");
    }
  };

  const fetchCategoryAttributes = async (categoryId) => {
    try {
      const data = await fetchCategoryAttributesAPI(categoryId);
      setAttributes(data);
      setFilters({});
      setError("");
    } catch (error) {
      setError("Failed to fetch category attributes.");
    }
  };

  const handleLogin = (loggedIn) => {
    setIsLoggedIn(loggedIn);
    if (loggedIn) {
      fetchProducts();
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    setProducts([]);
    setFilteredProducts([]);
    setError("");
  };

  const handleCategoryChange = (event) => {
    const selectedCategoryId = event.target.value;
    setCategoryId(selectedCategoryId);
    fetchCategoryAttributes(selectedCategoryId);
  };

  const handleFilterChange = (event, attributeId) => {
    const { name, value } = event.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  const handleSearch = () => {
    let queryParams = "";
    if (searchQuery) {
      queryParams = `search=${searchQuery}`;
    }
    if (categoryId) {
      queryParams += queryParams ? `&category=${categoryId}` : `category=${categoryId}`;
    }
    if (Object.keys(filters).length > 0) {
      const filterParams = Object.keys(filters)
        .map((filterKey) => `${filterKey}="${filters[filterKey]}"`)
        .join(",");
      queryParams += queryParams ? `&attributes=${filterParams}` : filterParams;
    }
    fetchProducts(queryParams);
  };

  return (
    <div className="app-container">
      {!isLoggedIn ? (
        <Login onLogin={handleLogin} />
      ) : (
        <div className="dashboard">
          <div className="header">
            <Typography variant="h5">Welcome! You are logged in.</Typography>
            <Button variant="outlined" onClick={handleLogout} color="primary">
              Logout
            </Button>
          </div>
          {error && <Typography color="error">{error}</Typography>}

          <Filters
            categories={categories}
            categoryId={categoryId}
            searchQuery={searchQuery}
            attributes={attributes}
            filters={filters}
            handleCategoryChange={handleCategoryChange}
            handleFilterChange={handleFilterChange}
            handleSearch={handleSearch}
            setSearchQuery={setSearchQuery}
          />

          <ProductList products={filteredProducts} />
        </div>
      )}
    </div>
  );
};

export default App;
