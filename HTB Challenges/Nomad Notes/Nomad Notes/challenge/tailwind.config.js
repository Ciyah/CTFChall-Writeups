
module.exports = {
    content: ["./challenge/views/**/*.{html,ejs}", "./challenge/**/*.js"],
    theme: {
      extend: {
        colors: {
          gold:    '#eab308',
          void:    '#0f172a',
          accent:  '#6366f1',
          slate:   '#f8fafc',
          white:   '#ffffff',
        },
        fontFamily: {
          sans:  ["Inter", "system-ui", "sans-serif"],
          hand:  ["Caveat", "cursive"],
        },
        boxShadow: {
            bento: '0 8px 30px rgba(0,0,0,0.04)',
            postcard: '0 25px 50px -12px rgba(0,0,0,0.25)',
        },
      },
    },
    plugins: [require('@tailwindcss/typography')],
  };


  