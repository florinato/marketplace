import React from 'react';
import ReactDOM from 'react-dom/client';
import ProductList from './components/ProductList';

function App() {
  return (
    <ProductList />
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
