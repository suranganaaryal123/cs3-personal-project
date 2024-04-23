from flask import Flask, render_template, request
import phonenumbers
from phonenumbers import geocoder, carrier, PhoneNumberFormat
import pycountry

app = Flask(__name__)

def get_country_list():
    country_list = {}
    for country in pycountry.countries:
        country_list[country.alpha_2] = country.name
    return country_list

@app.route('/')  # Route to display the form
def display_form():
    country_list = get_country_list()
    return render_template('index.html', country_list=country_list)

@app.route('/validate', methods=['POST'])  # This route now handles only POST requests
def validate_number():
    country_list = get_country_list()
    result = None
    carrier_info = None

    country_code = request.form['country_code']
    phone_number = request.form['phone_number']
    try:
        parsed_number = phonenumbers.parse(phone_number, country_code)
        if phonenumbers.is_valid_number(parsed_number):
            if int(parsed_number.country_code) == phonenumbers.country_code_for_region(country_code):
                result = f"Valid phone number! Formatted: {phonenumbers.format_number(parsed_number, PhoneNumberFormat.INTERNATIONAL)}"
                carrier_info = carrier.name_for_number(parsed_number, 'en')
            else:
                result = "Phone number does not match the selected country."
        else:
            result = "Invalid phone number!"
    except phonenumbers.NumberParseException:
        result = "Invalid input! Please enter a valid phone number."

    return render_template('index.html', country_list=country_list, result=result, carrier_info=carrier_info)

if __name__ == '__main__':
    app.run(debug=True)
