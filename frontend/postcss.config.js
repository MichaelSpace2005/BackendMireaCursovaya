// Use CommonJS so PostCSS can load without ESM interop issues in Docker builds
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
