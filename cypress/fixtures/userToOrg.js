exports.userToOrg = (email) => {
  return {
    email,
    user_profile: {
      first_name: 'Test',
      last_name: 'Lite',
    },
    sites: {},
    role: '00000000-0000-0000-0000-000000000003'
  }
}
