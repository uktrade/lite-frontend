const create = {
  name: 'application',
  application_type: 'siel',
  export_type: 'permanent',
  have_you_been_informed: 'yes',
  reference_number_on_information_form: '42693635'
}

const submit = {
  submit_declaration: true,
  agreed_to_foi: true,
  agreed_to_declaration: true,
  foi_reason: 'No objection',
  agreed_to_declaration_text: 'I AGREE'
}

const status = (status) => {
  return { status }
}

module.exports = { status, create, submit }
