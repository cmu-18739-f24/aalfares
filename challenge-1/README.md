# Problem Dev 1
Abdulrahman Alfares (andrew id: aalfares)

## Challenge Info
**Name:** Markdown 3030
**Description:** In a world *polluted* by Del the Funkee Homosapien's virus,
one code editor endures: Markdown 3030, created and operated by Dan the
Automator. Although Del and Dan have partnered up in this post-apocalyptic
world, Del's virus does not differentiate between friend and foe. Can you
help Dan find the virus before it takes over his server?
**Category:** Web
**Points:** 303
**File Handout:** I intend on providing `app.js`'s contents to players.

**Note:** I've added a flickering effect on the editor because of the setting of
this apocalyptic futuristic world (setting taken from an album called Deltron
3030). Let me know if it's too annoying and that I should remove this effect.

## Files 

* `/public/` & `/views/`: dirs for holding templates and static files for the 
web app
* `app.js`: main node js app for this challenge
* `del-funkee.txt`: flag (will change with cmgr deployment)
* `Dockerfile`: dockefile to build the challenge
* `package*.json`: npm packages/dependencies for the challenge
* `README.md`: this file
  
## Running the Challenge
I unfortunately wasn't able to figure out how to setup cmgr for this challenge
as I was having trouble understanding how to set up new instances for every 
player. I've instead provided a Dockerfile that you can build as follows: 
```
docker build -t aalfares .
```
Port 3000 is exposed on the docker container to connect to the web app. To run
the challenge, run the container:
```
docker run -p 3000:3000 --rm aalfares
```
Then open a browser and navigate to `localhost:3000`.

I'll be figuring out and submitting the cmgr build for this with submission 2
as instructed on Piazza.

## Solution Walkthrough
**Goal:** Find the "virus" on the machine and read it to capture the flag.
**Intended method:** Pollute the global object prototype, resulting in RCE
where you either pop up a reverse shell and `cat` the flag (#1) or copy the 
flag file into a directory like `./public/` whose files can be accessed 
via the browser (#2).  
**Hints within the challenge:**
* Pollution referenced in challenge description
* Virus (flag) location is shown in `app.js` (line 28)
* Line 7 in `app.js` showing that files in the `./public` directory are
accessible via the browser (hint for soln. method #2).

**Full Walkthrough:**
Upon navigating to `localhost:3000` you see an online markdown editor, 
adapted from [Marked Demo](https://marked.js.org/demo/), that is glitchy as
it is corrupted by Del's virus that's taken over the world's computers. There's
an editor on the left and a preview of the markdown code on the right. Both 
are largely irrelevant to the solution. The vulnerability arises form the 
settings text area. The purpose of the settings text area is for the user of
this editor to modify the "look and feel" of the app. You can go ahead and 
modify font sizes, colors, etc. 

When new settings are submitted, a POST request is sent to the server which 
performes a recursive merge of these newly submitted settings with the 
default editor settings (if the json recieved is valid). Due to this 
recursive merge it is possible to pollute the global object and inject 
an attribute to all newly created objects. We get the following executed with
a recursive merge for an input setting that contains a `"__proto__": {...}`:
`target['__proto__'] = merge(target['__proto__'] || {}, source['__proto__'])`.

Dan, a linux novice, is running the `ls` command to look for the virus on his 
machine whenever a GET request is recieved by the server. The function that 
is called to do this is `ping()` in line 19 of `app.js`. The function creates
and object to hold the "execution context" for that "ping". If a path is 
provided as an argument to `ping`, then it will be used as the argument
for the `ls` command `exec`'ed. However, all calls to `ping` are made without
passing in any arguments. Dan intended for it to fall into the default case 
(lines 25-29) where the `exec` eventually just runs `ls ./del-funkee.txt`.

If the global object prototype is polluted with a `ping_path` attribute, then
the default case will never be taken as the check in line 25 
`!('ping_path' in exe_ctx)` evaluates to `false`. Thus, whatever is assigned
to that polluted prototype attribute is exected by `exec()` instead of the 
default case that Dan intended to execute. So, we can pass in the following
setting configuration:
```
{
  "backgroundColor": "#222",
  "textColor": "#ffffff",
  "fontSize": "1rem",
  "textAreaFont": "monospace",
  "font": "sans-serif",
  "__proto__": {"ping_path": "./ && cp ./del-funkee.txt ./public"}
}
```
This causes a call to `ping` to use `"./ && cp ./del-funkee.txt ./public"`
instad of `"./del-funkee.txt"` as the path and execute the following:
```
ls ./ && cp ./del-funkee.txt ./public
```
After we change the setting configuration, we submit a GET request
to the `/` path to trigger the RCE and then navigate to 
`localhost:3000/del-funkee.txt` to read the flag. 

You can also pass in a reverse shell command instead of 
`cp ./del-funkee.txt ./public` but the copy method is simpler because you'd
have to get around js's `exec()` not working with bash operators like `>` if
you want to set up a reverse shell (which is possible but more tedious). 

There could be other ways to solve this, I just haven't considered any.

**TLDR:**
1. Paste the following into settings text area & submit:
```
{
  "backgroundColor": "#222",
  "textColor": "#ffffff",
  "fontSize": "1rem",
  "textAreaFont": "monospace",
  "font": "sans-serif",
  "__proto__": {"ping_path": "./ && cp ./del-funkee.txt ./public"}
}
```
2. Send a GET request to the server by visiting `localhost:3000` to cause the
`ping()` function to be called and your injected code to run in `exec()`.
3. Read the flag by navigating to `localhost:3000/del-funkee.txt`.
