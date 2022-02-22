require('dotenv').config({ path: './caseworker.env' })

module.exports = (on, config) => {
  config.env.sso_user = process.env.CYPRESS_SSO_USER
  config.env.export_sso_user = process.env.CYPRESS_EXPORT_SSO_USER
  config.env.sso_password = process.env.CYPRESS_SSO_PASSWORD
  config.env.sso_url = process.env.CYPRESS_SSO_URL
  config.env.api_url = process.env.CYPRESS_API_URL
  return config
}
