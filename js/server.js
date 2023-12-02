const express = require("express");
const parse = require("csv-parse")
const fs  = require("fs");

const app = express();
const port = 3004

app.get('/', (req, res) => {
   
    let emotionTag = req.query
    // console.log(emotionTag)
    const musicList = fs.readFileSync('./data_moods.csv',
    { encoding: 'utf8', flag: 'r' });
    searchCSV(musicList,emotionTag.emotion)
    // console.log(parseCSV(musicList))

 
    res.send('Request have been received :) ')

  })


app.listen(port, () => {
    console.log(`App listening port: ${port}`)
  })
  

     // Function to parse CSV data
function searchCSV(csvData,emotionTag) {
  const rows = csvData.split('\r\n'); // Split the CSV data into rows
  const headers = rows[0].split(','); // Extract headers
  const data = [];

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i].split(','); // Split each row into values
    if (row.length === headers.length) {
      const obj = {};
      for (let j = 0; j < headers.length; j++) {
        obj[headers[j]] = row[j]; // Create an object using header-value pairs
        // console.log(obj.mood)
        if(obj.mood===emotionTag){
        console.log(obj.name)
        console.log(obj.mood)
        }
      }
    


      data.push(obj); // Push the object to the data array
    }
  }
  // console.log(data)
  return data;
}