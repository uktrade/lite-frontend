exports.userToOrg = (email = '') => {
  return {
    'email': email || Cypress.env('sso_email'),
    'user_profile': {'first_name': 'Automated', 'last_name': 'Test'},
    'sites': {},
    'role': '00000000-0000-0000-0000-000000000003'
  }
}
