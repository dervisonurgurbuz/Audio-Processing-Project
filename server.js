const express = require("express");

const fs  = require("fs");

const app = express();
const port = 3004

app.get('/', (req, res) => {
   
    let emotionTag = req.query
    console.log(emotionTag)

    res.send('Request have been received :) ')

  })


app.listen(port, () => {

    console.log(`App listening port: ${port}`)
  })
  