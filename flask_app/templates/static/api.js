
const url = 'http://127.0.0.1:5000/api/'
const endpoint = `price/${ticker}`

function getPx(ticker) {
    let creds = {
                method: 'post',
                headers: {'Content-type': 'application/json'},
                mode: 'CORS',
                body: JSON.stringify({'ticker' : ticker.value})             
                };
    const promise = fetch(url + endpoint, creds)
    promise.then(response => response.json()).then(data => console.log(data))
        }

export default getPx