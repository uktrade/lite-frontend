require('dotenv').config({ path: './caseworker.env' })

module.exports = (on, config) => {
  config.env.sso_user = process.env.CYPRESS_SSO_USER
  config.env.sso_password = process.env.CYPRESS_SSO_PASSWORD
  return config
}
