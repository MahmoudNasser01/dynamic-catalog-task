// components/ProductItem.js
import React from "react";
import { Card, CardContent, CardMedia, Typography, Box } from "@mui/material";

const ProductItem = ({ product }) => {
  return (
    <Box sx={{ boxShadow: 3, borderRadius: 2, overflow: "hidden" }}>
      <Card>
        <CardMedia
          component="img"
          height="200"
          image={product.images[0]}
          alt={product.name}
          sx={{ objectFit: "cover" }}
        />
        <CardContent>
          <Typography variant="h6" component="div" gutterBottom>
            {product.name}
          </Typography>
          <Typography variant="body2" color="text.secondary" noWrap>
            {product.description}
          </Typography>
          <Typography variant="h6" sx={{ marginTop: 1 }}>
            Price: ${product.price}
          </Typography>
          {product.attributes.map((attribute) => (
            <Typography
              key={attribute.attribute_name}
              variant="body2"
              color="text.secondary"
            >
              <strong>{attribute.attribute_name}:</strong> {attribute.value}
            </Typography>
          ))}
        </CardContent>
      </Card>
    </Box>
  );
};

export default ProductItem;
