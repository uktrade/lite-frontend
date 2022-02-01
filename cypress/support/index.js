import './commands'

Cypress.Cookies.defaults({
  preserve: ['sessionid', 'csrftoken', 'seen_cookie_message'],
})
