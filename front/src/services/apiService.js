// services/apiService.js
export const fetchProductsAPI = async (token, queryParams = "") => {
    const response = await fetch(
      `http://127.0.0.1:8000/api/products/search/?${queryParams}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.json();
  };
  
  export const fetchCategoryAttributesAPI = async (categoryId) => {
    const response = await fetch(
      `http://127.0.0.1:8000/api/categories/${categoryId}/attributes/`
    );
    return response.json();
  };
  
  export const fetchCategoriesAPI = async () => {
    const response = await fetch("http://127.0.0.1:8000/api/categories/");
    return response.json();
  };
  