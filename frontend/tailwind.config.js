/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    safelist: [
        {
            pattern: /bg-(slate|stone|orange|rose|red|amber|blue|green|purple|pink)-(100|200|300|400|500)/,
        }
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}
