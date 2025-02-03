module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        targets: {
          node: 'current', // Ensure Babel targets the current Node.js version
        },
      },
    ],
  ],
};