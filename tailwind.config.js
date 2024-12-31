/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
    './static/**/*.css',
    './accounts/templates/accounts/**/*.html',
    './chat/templates/chat/**/*.html',
    './products/templates/products/**/*.html',
    // Añade aquí cualquier otra ruta donde uses clases de Tailwind
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
