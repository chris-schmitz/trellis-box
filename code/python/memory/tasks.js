const path = require("path")
const fs = require("fs")

const trinketPath = path.join("/", "Volumes", "CIRCUITPY", "main.py")
const mainPyPath = path.join(__dirname, "main.py")

fs.createReadStream(mainPyPath).pipe(fs.createWriteStream(trinketPath))
