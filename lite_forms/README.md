# lite-forms

[![Maintainability](https://api.codeclimate.com/v1/badges/be60e1b5dde9baa88a92/maintainability)](https://codeclimate.com/github/uktrade/lite-forms/maintainability)

An easy to use Python library for building GOV.UK forms.

## Docs

[Getting Started](/docs/getting_started.md)

## Building a form

```
Form(title='Register an organisation',
	 description='Part 1 of 3',
	 questions=[
		 Question(title='What\'s the organisation\'s name?',
				  description='',
				  input_type=InputType.INPUT,
				  name='name'),
		 Question(title='European Union registration and identification number (EORI)',
				  description='',
				  input_type=InputType.INPUT,
				  name='eori_number'),
		 Question(title='Standard Industrial Classification Number (SIC)',
				  description='Classifies industries by a four-digit code.',
				  input_type=InputType.INPUT,
				  name='sic_number'),
		 Question(title='UK VAT number',
				  description='9 digits long, with the first two letters indicating the'
							  ' country code of the registered business.',
				  input_type=InputType.INPUT,
				  name='vat_number'),
		 Question(title='Company registration number (CRN)',
				  description='8 numbers, or 2 letters followed by 6 numbers.',
				  input_type=InputType.INPUT,
				  name='registration_number'),
	 ],
	 buttons=[
		 Button('Save and continue', '')
	 ],
),
```

## Requirements

* GOV.UK Design System 2.11.0
