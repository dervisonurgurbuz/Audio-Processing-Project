
var axios = require('axios');



var config = {
  method: 'get',
  url: 'http://localhost:3004?emotion=happy&energy=0.6&loudness=-5&dancebility=0.5',
  headers: { }
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});




