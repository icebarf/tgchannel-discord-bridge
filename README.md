## Get this shit running
- Copy `login_copy.json` to `login.json`
- Run `python3 generate_login_string.py`
- Copy the generated login string.
- Open `login.json`
- Change the `"telegram_login_string" : nill` field to `"telegram_login_string" : "that_generated_login_string"`
- Make sure you put a comma after the value string of `channel_id` field.
- After you have generated a functional `login.json`, simply run `main.py`
- `python3 main.py`