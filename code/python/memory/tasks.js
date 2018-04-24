const path = require("path")
const fs = require("fs")

const trinketPath = path.join("/", "Volumes", "CIRCUITPY")
const projectPath = path.join(__dirname)

const toCopy = [
    {
        from: path.join(projectPath, "main.py"),
        to: path.join(trinketPath, "main.py")
    },
    {
        from: path.join(projectPath, "lib", "pitches.py"),
        to: path.join(trinketPath, "lib", "pitches.py")
    },
    {
        from: path.join(projectPath, "lib", "MatchingGame.py"),
        to: path.join(trinketPath, "lib", "MatchingGame.py")
    }
]

toCopy.forEach(pathData => {
    console.log(`Copying: ${pathData.from}`)
    console.log(`to: ${pathData.to}`)
    fs.createReadStream(pathData.from).pipe(fs.createWriteStream(pathData.to))
})
