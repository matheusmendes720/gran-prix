/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontSize: {
        // Base font-size is now 20px (set in globals.css), so rem values scale accordingly
        // These maintain proportional scaling from the new base
        'xs': ['0.75rem', { lineHeight: '1rem' }],      // 15px (was 12px)
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],  // 17.5px (was 14px)
        'base': ['1rem', { lineHeight: '1.5rem' }],     // 20px (was 16px) - base size
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],  // 22.5px (was 18px)
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],   // 25px (was 20px)
        '2xl': ['1.5rem', { lineHeight: '2rem' }],      // 30px (was 24px)
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }], // 37.5px (was 30px)
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],   // 45px (was 36px)
        '5xl': ['3rem', { lineHeight: '1' }],           // 60px (was 48px)
        '6xl': ['3.75rem', { lineHeight: '1' }],        // 75px (was 60px)
        '7xl': ['4.5rem', { lineHeight: '1' }],         // 90px (was 72px)
        '8xl': ['6rem', { lineHeight: '1' }],           // 120px (was 96px)
        '9xl': ['8rem', { lineHeight: '1' }],           // 160px (was 128px)
      },
      colors: {
        'brand-blue': '#0a192f',
        'brand-light-navy': '#172a45',
        'brand-navy': '#112240',
        'brand-lightest-slate': '#ccd6f6',
        'brand-light-slate': '#a8b2d1',
        'brand-slate': '#8892b0',
        'brand-cyan': '#64ffda',
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
    },
  },
  plugins: [],
};

