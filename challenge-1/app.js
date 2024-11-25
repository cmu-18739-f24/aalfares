const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const defaultSettings = {
    backgroundColor: "#222",
    textColor: "#ffffff",
    fontSize: "1rem",
    textAreaFont: "monospace",
    font: "sans-serif"
};

// "scan" filesystem for a file
function ping(ping_path) {
    let exe_ctx = {};

    if (ping_path !== undefined) {
        exe_ctx.ping_path = ping_path;
    }
    if (!('ping_path' in exe_ctx)){
        // by default, check if server is 
        // infected with Del's virus
        exe_ctx.ping_path = './del-funkee.txt';
    }
    if (typeof exe_ctx.ping_path !== 'string'){
        return;
    }

    exec(`ls ${exe_ctx.ping_path}`, (error, stdout, stderr) => {
        if (error) {
            console.log(`exec stderr: ${stderr}`);
        } else {
            console.log(`exec stdout: ${stdout}`);
        }
    });
}

// merge source object into target
function merge(target, source) {
    for (const key in source) {
        if (source[key] && typeof source[key] === 'object') {
            target[key] = merge(target[key] || {}, source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}

app.get('/', function (req, res) {
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');

    // check for Del's virus with every visit
    ping();
    
    res.render('index', merge({ 
            settingsText: JSON.stringify(defaultSettings, null, 2),
            errorMsg: null 
        }, defaultSettings));
});

app.post('/', function (req, res) {
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');

    // process user setting changes
    const settingsData = req.body.settingsData;

    if (settingsData === null || settingsData === undefined) {
        res.render('index', merge({ 
            settingsText: JSON.stringify(defaultSettings, null, 2),
            errorMsg: 'Invalid request.' 
        }, defaultSettings));
        return;
    }
    
    let settings;

    try {
        settings = JSON.parse(settingsData);
    } catch (err) {
        res.render('index', merge({ 
            settingsText: JSON.stringify(defaultSettings, null, 2),
            errorMsg: 'Invalid JSON. Please fix your input settings and try again.' 
        }, defaultSettings));
        return;
    }

    let userSettings = merge({}, defaultSettings);
    userSettings = merge(userSettings, settings);

    res.render('index', merge({ 
        settingsText: JSON.stringify(userSettings, null, 2),
        errorMsg: null 
    }, userSettings));
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
