# Ian's Password Program
## For CYB3038: HCI/Usable Security

## Installation Guide:
* Install Python 3
* Run the command
    > pip install -r requirements.txt
* Start the Flask server with
    > python main.py
* Go to http://127.0.0.1:5000 in any web browser

## Pages
*/login* - Log in to a created account

*/create-account* - Account creation page

*/change-password* - Change the password of an already created account

## Debug:
* To change password multiple times in a day:
    * Change "lastchanged" for the user account in *userdb.json*
* To unlock an account
    * Change "locked" to **false** for the user account in *userdb.json*
* To give users more attempts, either:
    * Change the first value in num attempts to a value less than 10
    * Change the date in numattemtps to a date that is not today
