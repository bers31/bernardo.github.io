module.exports = {
  content: [
      './vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php',
      './vendor/laravel/jetstream/**/*.blade.php',
      './storage/framework/views/*.php',
      './resources/views/**/*.blade.php',
      './resources/views/*.blade.php',
      "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        red: 'red',
      },
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
  darkMode: 'class'

}
