# roadtaxTracker
CRUD operation for a fleet of vehicle in Singapore to ease roadtax renewal

A simple personal project to monitor a fleet of vehicles' road-tax related operations. Such as keeping track if driver of the vehicle is informed about the soon to be due road-tax, check if inspection is done and if the above were completed, to monitor if the individual road-tax is renewed with Land Transport Authority of Singapore.

## Setting up / Using instruction
1. First you will need to upload the whole fleet of vehicles.
2. When you open this App it will automatically generate any vehicles that will be due in 30 days or already expired as of the day you open this App.
3. Day in advance can be changed via the input and click update to change.
4. When you first batch upload your fleet, inform, inspect and renew will mark as false. So make sure your data is up-to-day before batch uploading it to the App.
5. To change the status of the vehicle, select it and check the respective check boxes. Then click update.
6. Once updated, vehicles expiry date will automatically updated to the next 6 months or (182.5 days).
7. Add, remove or edit of vehicles can be done using the edit button.
8. For changing of expiry date of a vehicle, or misclicking three checkboxes, keying in the existing vehicle number will update the record.
9. Please note that all changes is saved via the update button. So please remember to click update to save any changes.

## Questions, issues, feature requests, and contributions
If you encounter any issue with the App, or would like to report on a bug, please open an issue in this repository.

feel free to ask for feature requests or improvement to this App. Any contribution is welcomed!

## Development
```
>> python3 -m venv env
>> source env/bin/activate
>> pip install -r requirements.txt
>> python -m unittest test/*.py
>> deactivate
```
