/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: "#05070a",
          card: "#0d1117",
          border: "#30363d",
          primary: "#00f2ff", // Neon Cyan
          secondary: "#7000ff", // Neon Purple
          danger: "#ff003c", // Cyber Red
          success: "#00ff88", // Neon Green
          warning: "#ffcc00",
        }
      },
      backgroundImage: {
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%)',
      },
      boxShadow: {
        'cyber-glow': '0 0 15px rgba(0, 242, 255, 0.3)',
        'danger-glow': '0 0 15px rgba(255, 0, 60, 0.3)',
      }
    },
  },
  plugins: [],
}
