const express = require("express");
const parse = require("csv-parse")
const fs  = require("fs");

const app = express();
const port = 3004

app.get('/', (req, res) => {
    let data = ''
    let emotionTag = req.query
    // console.log(emotionTag)
    if(emotionTag.emotion === 'Happy' || emotionTag.emotion === 'Calm' || emotionTag.emotion === 'Energetic' || emotionTag.emotion === 'Sad'){
      const musicList = fs.readFileSync('./data_moods.csv',
      { encoding: 'utf8', flag: 'r' });
      data = searchCSV(musicList,emotionTag.emotion,emotionTag.tempo)
      // console.log(parseCSV(musicList))
      data = JSON.stringify(data)

      fs.writeFileSync("musiclist.json", data)        
     
             
         
      res.send(data)
    }else{
      res.status(500).send('Emotion Tag is not defined')
    }

  })


app.listen(port, () => {
    console.log(`App listening port: ${port}`)
  })
  

     // Function to parse CSV data
function searchCSV(csvData,emotionTag,tempo) {
  let rows = csvData.split('\r\n'); // Split the CSV data into rows
  let headers = rows[0].split(','); // Extract headers
  const data = []; 
  let music = {};

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i].split(','); // Split each row into values
    if (row.length === headers.length) {
      const obj = {};
      for (let j = 0; j < headers.length; j++) {
        obj[headers[j]] = row[j]; // Create an object using header-value pairs
        // console.log(obj.mood)
        if(obj.mood===emotionTag){
          
          music = {
            "name": obj.name,
            "album": obj.album,
            "artist": obj.artist,
            "tempo": obj.tempo

          }
          data.push(music); // Push the object to the data array
        }
      }      
      if(tempo<100){
        data.sort((a, b) => a.tempo - b.tempo) // When the tempo is low we are listing musics low BPS to low BPS
      }else{
        data.sort((a, b) => -(a.tempo - b.tempo))
      }
      
    }
  }
  // console.log(data)
  return data;
}


// Data is from
// https://github.com/cristobalvch/Spotify-Machine-Learning/blob/master/data/data_moods.csv