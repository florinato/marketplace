import React, { useEffect, useState } from 'react';

function ProductList() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/products/api/products/')
      .then(response => response.json())
      .then(data => {
        setProducts(data.products);
      });
  }, []);

  return (
    <div>
      <h2>Product List Component</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
        {products.map(product => (
          <div key={product.pk} className="bg-white rounded-lg shadow-md overflow-hidden">
            <img src={product.fields.main_image} alt={product.fields.title} className="w-full object-contain rounded-md" />
            <div className="p-4">
              <h3 className="text-lg font-bold text-gray-800 truncate">{product.fields.title}</h3>
              <p className="text-green-600 font-semibold text-xl">{product.fields.price}€</p>
              <p className="text-gray-500 text-sm flex items-center">Publicado por: <strong>{product.fields.user}</strong></p>
              <a href={`/products/${product.pk}/`} className="text-blue-500 mt-4 block">Ver Detalles</a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProductList;
