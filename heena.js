const express=require('express');
const app = express();

app.get('/user', function (req, res) {
    console.log("Route-1:",req.query)
})
app.get('/user/:value', function (req, res) {
    console.log("Route-2:",req.params.value)
})
app.listen(3000)