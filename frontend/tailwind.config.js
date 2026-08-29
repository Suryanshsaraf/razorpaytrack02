/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        razorpay: {
          blue: "#0C2340",
          accent: "#3395FF",
          light: "#EBF4FE",
          dark: "#081627"
        }
      }
    },
  },
  plugins: [],
}
