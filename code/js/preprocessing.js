const fs = require('fs');

// List all the filenames before renaming 
// getCurrentFilenames(); 

// Function to get current filenames and rename the files to perpare for Model

let dataDirectory = 'Crema'
let i = 1 // File counter

fs.readdirSync(dataDirectory).forEach(file => {

  i = i + 1;

  let emotionTag = file.slice(-10, -7);

  fs.rename(`Crema/${file}`, `Crema Version3/${emotionTag}/${i}_${file.slice(-10)}`, () => {
    console.log(`\nFile Renamed: ${file}\n  `);

  });

}); 