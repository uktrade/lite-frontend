# lite-forms

[![Maintainability](https://api.codeclimate.com/v1/badges/be60e1b5dde9baa88a92/maintainability)](https://codeclimate.com/github/uktrade/lite-forms/maintainability)
[![GitHub license](https://img.shields.io/github/license/uktrade/lite-forms.svg)](https://github.com/uktrade/lite-forms/blob/master/LICENSE)

An easy to use Python library for building GOV.UK forms.

## Docs

[Getting Started](/docs/getting_started.md)

## Building a form

```
Form(title='Register an organisation',
     description='Part 1 of 3',
     questions=[
		 TextInput(title='What\'s the organisation\'s name?',
				  name='name'),
		 TextInput(title='European Union registration and identification number (EORI)',
				  name='eori_number'),
		 TextInput(title='Standard Industrial Classification Number (SIC)',
				  description='Classifies industries by a four-digit code.',
				  name='sic_number'),
		 TextInput(title='UK VAT number',
				  description='9 digits long, with the first two letters indicating the'
							  ' country code of the registered business.',
				  name='vat_number'),
		 TextInput(title='Company registration number (CRN)',
				  description='8 numbers, or 2 letters followed by 6 numbers.',
				  name='registration_number'),
	 ],
	 buttons=[
		 Button('Save and continue', '')
	 ],
),
```

## Installing

```pipenv install lite-forms```

## Requirements

* GOV.UK Design System 3.0 >

## Deploying to PyPI:

* ```python setup.py sdist```
* ```twine upload dist/*```
