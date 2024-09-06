const initSortBy = () => {
  const sortBy = document.getElementById("id_sort_by");
  if (!sortBy) {
    return;
  }
  const form = sortBy.form;
  sortBy.addEventListener("change", () => {
    form.submit();
  });
};

export default initSortBy;
