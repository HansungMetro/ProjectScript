const express = require('express');
const app = express();
const spawn = require('child_process').spawn;
app.use(express.urlencoded({extended : true}));
const iconv = require('iconv-lite');
app.set('view engine', 'ejs')


app.listen(8080, function () {
    console.log('listening on 8080')
  });   
  
  app.get('/', function(요청, 응답){
    응답.sendFile(__dirname + '/index.html')
});

app.get('/lines', function(요청, 응답){
    응답.sendFile(__dirname + '/lines.html')
});


app.post('/lines/result', function(요청, 응답){
    console.log(요청.body)
    const result_02 = spawn('python', ['TrainTrace.py', 요청.body.SubwayID, 요청.body.start, 요청.body.end, 요청.body.trainNum]);
    let rs
    result_02.stdout.on('data', (result)=>{
        rs = iconv.decode(result, 'euc-kr');
        list = rs.split(';')
        console.log(list);
        응답.render('lines.ejs', { Data : list });
    });
    result_02.stderr.on('data', function (result) {
        rs = iconv.decode(result, 'euc-kr');
        console.log(rs)
    });

});