## Get this shit running
- Copy `login_copy.json` to `login.json`
- Run `python3 generate_login_string.py`
- Copy the generated login string.
- Open `login.json`
- Change the `"telegram_login_string" : ""` field to `"telegram_login_string" : "that_generated_login_string"`
- Put your discord bot token in the relevant field as well, inside quotes
- Make sure you put a comma after the value string of `telegram_channel_id` field.
- Change `telegram_channel_id` and `discord_channel_id` fields as well. 
Note that telegram id is in `"` string while discord id is an integer.
- After you have generated a functional `login.json`, simply run `main.py`
- `python3 main.py`