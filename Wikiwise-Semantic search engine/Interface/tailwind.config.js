/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        darkblue: "#0b0e17", 
        lightgrey: "#ccc",
      },
    },
  },
  plugins: [],
};
