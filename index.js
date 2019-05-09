const http = require("http"),
    fs = require("fs"),
    spawn = require("child_process").spawnSync,
    crypto = require("crypto"),
    formidable = require("formidable");
var server = http.createServer();

server.on("clientError", (err, socket) => {
    socket.end('HTTP/1.1 400 Bad Request\r\n\r\n');
});

server.on("request", router);

server.listen(8080);

async function router(req, resp) {
    let { method, url, headers } = req,
        path = url.split("?")[0];

    log(method + " request from " + path);
    // router
    try {
        var body = undefined;
        switch(`${method} ${path}`) {
            case "GET /":
                respond(resp, {
                    "message": "Hello, this is the GANNER server. We are still under development, please check back at the /upload endpoint later!"
                });
                break;
            case "GET /greet":
                body = await request(req);
                respond(resp, {
                    "message": "Hello there client!"
                });
                break;
            case "POST /process":
                body = await multipart(req);

                respond(resp, {
                    "success": true
                });
                break;
            default:
                respond(resp, "Bad request\n", 400);
                log("Bad request from client");
                break;
        }
    } catch(err) {
        log(err);
        if(!resp.finished) resp.end("HTTP/1.1 500 Internal Server Error\r\n\r\n");
    }
}

function request(req) {
    return new Promise((resolve, reject) => {
        if(["POST", "PUT"].includes(req.method)) {
            let body = [];
            req
                .resume()
                .on("data", (chunk) => {
                    body.push(chunk);
                })
                .on("end", () => {
                    if(!req.complete) {
                        log("ERROR - Connection terminated while reading request");
                        reject("Connection interrupted");
                    } else {
                        body = Buffer.concat(body).toString();
                        log("Received request -> " + body);
                        resolve(body);
                    }
                });
        } else if(req.method == "GET") {
            let url = req.url,
                query = req.url.substring(req.url.indexOf("?") + 1),
                decouple = query.split("&"),
                json = {};
            for(let pair of decouple) {
                json[pair.split("=")[0]] = pair.split("=")[1];
            }
            log("Received request -> " + query);
            log("Decoupled to get -> " + JSON.stringify(json));
            resolve(json);
        }
    });
}

function multipart(req, path) {
    return new Promise((resolve, reject) => {
        let form = new formidable.IncomingForm(),
            tag = crypto.randomBytes(16).toString("hex");
        form.on("fileBegin", (name, file) => {
            fs.mkdirSync(`${__dirname}/uploaded/${tag}`);
            file.path = `${__dirname}/uploaded/${tag}/${file.name}`;
        });
        form.parse(req, (err, fields, files) => {
            if(err) return reject(err);
            for(let file in files) {
                files[file]["tag"] = tag;
            }
            log("MULTIPART -> " + JSON.stringify(fields) + JSON.stringify(files))
            resolve(fields, files);
        });
    });
}

function respond(resp, data, statusCode, headers, cb) {
    let body = (() => {
        if(typeof data == "object") return JSON.stringify(data);
        return data;
    })();
    log("Sending response -> " + body);
    resp
        .writeHead(statusCode || 200, headers || {"Content-Type": "text/plain"})
        .end(body, null, cb || (() => {
            log("Sent response");
        }));
    return body;
}

function log(data) {
    console.log("SERVER ==> " + data);
    return data;
}