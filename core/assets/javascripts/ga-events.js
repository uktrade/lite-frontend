export function getUserID() {
  const element = document.getElementById("user_id");
  if (element) {
    return element.value;
  }
  return null;
}

export function gaPushUserID() {
  const userID = getUserID();
  if (!userID || !window.dataLayer) {
    return;
  }
  // eslint-disable-next-line camelcase
  window.dataLayer.push({ user_id: userID });
}
