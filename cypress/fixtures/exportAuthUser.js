exports.exportAuthUser = (email) => {
  const data = {
    email,
    user_profile: {
      first_name: 'Automated',
      last_name: 'Test',
    },
    sites: {},
    role: '00000000-0000-0000-0000-000000000003',
  }
  return data
}
