var axios = require('axios');

let emotion = "Calm";
let energy= 0.6;
let dancebility=0.5;
let loudness = -0.4;
var config = {

  method: 'get',
  url: `http://localhost:3004?emotion=${emotion}&energy=${energy}&loudness=${loudness}&dancebility=${dancebility}`,
  headers: { }
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});




