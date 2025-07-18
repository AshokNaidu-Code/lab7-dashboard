/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        lab: {
          glow: '#22ff77',
          dim: '#0a0f0a',
          panel: '#0f1911',
          accent: '#8affcc',
          warning: '#ff4d4d'
        }
      },
      fontFamily: {
        mono: ['"Fira Code"', 'monospace']
      },
      boxShadow: {
        glow: '0 0 15px #22ff77',
        pulse: '0 0 5px 2px rgba(34, 255, 119, 0.6)'
      },
      animation: {
        flicker: 'flicker 2s infinite ease-in-out',
        fadeIn: 'fadeIn 0.5s ease-out forwards'
      },
      keyframes: {
        flicker: {
          '0%, 100%': { opacity: '1' },
          '45%': { opacity: '0.6' },
          '55%': { opacity: '1' }
        },
        fadeIn: {
          from: { opacity: '0' },
          to: { opacity: '1' }
        }
      }
    }
  },
  plugins: []
};