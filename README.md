# US VISA Appointment Checker
---
## Guide 
1. Create a file name `config.ini` following the existing `config.ini.example` file format to reconfigure your `country code`, `schedule id`, `city`, `session` and `user_agent` 
2. Run the following command `./entry.sh` in your terminal.

## How to find values for config file
### Country Code
When you login to https://ais.usvisa-info.com/{country_code}/niv. The url should contain your country code automatically.

### Schedule Id 
When you login to https://ais.usvisa-info.com/en-gb/niv/schedule/{schedule_id}. The url shoul have your schedule id.

### City
Write down the visa center's city location that you want to make your appointment.

### Session and user agent
After login. 
- Create one appointment without payment. 
- `Inspect` the browser 
- Refresh and check`Network` 
- Find the `payment`
- Check `request headers`
- Find `Cookie`
- Copy `_yatri_session`'s value
- Paste in config.ini
- Find `user_agent` and copy paste in config.ini
