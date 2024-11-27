// components/ProductList.js
import React from "react";
import { Grid, Typography } from "@mui/material";
import ProductItem from "./ProductItem";

const ProductList = ({ products }) => {
  return (
    <Grid container spacing={3}>
      {products.length > 0 ? (
        products.map((product) => (
          <Grid key={product.id} item xs={12} sm={6} md={4}>
            <ProductItem product={product} />
          </Grid>
        ))
      ) : (
        <Grid item xs={12}>
          <Typography>No products found.</Typography>
        </Grid>
      )}
    </Grid>
  );
};

export default ProductList;
