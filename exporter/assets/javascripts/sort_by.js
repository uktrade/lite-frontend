const initSortBy = () => {
  const sortBy = document.getElementById("sort");
  const form = sortBy.form;
  sortBy.addEventListener("change", () => {
    form.submit();
  });
};

export default initSortBy;
