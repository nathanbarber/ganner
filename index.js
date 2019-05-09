const http = require("http");
var server = http.createServer();

server.on("clientError", (err, socket) => {
    socket.end('HTTP/1.1 400 Bad Request\r\n\r\n');
});

server.on("request", router);

server.listen(8080);

function router(req, resp) {
    let url = req.url,
        path = url.split("?")[0],
        method = req.method;
    log(method + " request from " + path);
    // router
    switch(`${method} ${path}`) {
        case "GET /":
            respond(resp, {
                "message": "Hello, this is the GANNER server. We are still under development, please check back at the /upload endpoint later!"
            });
            break;
        default:
            respond(resp, "Bad request\n", 400);
            log("Bad request from client");
            break;
    }
}

function respond(resp, data, statusCode, headers, cb) {
    let body = (() => {
        if(typeof data == "object") return JSON.stringify(data);
        return data;
    })();
    log("Sending " + body);
    resp
        .writeHead(statusCode || 200, headers || {"Content-Type": "text/plain"})
        .end(body, null, cb || (() => {
            log("Sent response");
        }));
    return body;
}

function log(data) {
    console.log("SERVER ==> " + data);
}