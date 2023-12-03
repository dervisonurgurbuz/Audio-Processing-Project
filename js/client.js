var axios = require('axios');

let emotion = "Calm"; // Important: This needs to be Calm, Happy, Energetic or Sad
let tempo = 101;

var config = {

  method: 'get',
  url: `http://localhost:3004?emotion=${emotion}&tempo=${tempo}`,
  headers: { }
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});




