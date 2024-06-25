const initSortBy = () => {
  const sortBy = document.getElementById("sort_by");
  const form = sortBy.form;
  sortBy.addEventListener("change", () => {
    form.submit();
  });
};

export default initSortBy;
