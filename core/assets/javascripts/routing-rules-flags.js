(function () {
    var flagsConditions = [];
    var editing = false;
    var flagGroups = { "flags_to_include": [], "flags_to_exclude": [] };

    function renderTable(conditions) {
        if (conditions && conditions.flags_to_include.length === 0 && conditions.flags_to_exclude.length === 0) {
            $("#routing-rules-flags-details").hide();
            return;
        }
        edit_column_header = editing ? '<th class="govuk-table__header" scope="col"></th>' : ""
        var header = `
            <thead class="govuk-table__head">
            <tr class="govuk-table__row">
                <th class="govuk-table__header" scope="col">Condition</th>
                <th class="govuk-table__header" scope="col">Flags</th>
                ${edit_column_header}
                <th class="govuk-table__header" scope="col"></th>
            </tr>
        </thead>`

        var rows = [];
        if (conditions.flags_to_include.length) {
            var flags = conditions.flags_to_include.map(function (flag, index) {
                return flag.name;
            });
            var edit_column_data = editing ? '<td class="govuk-table__cell govuk-table__cell"><a id="edit-inclusive-flags" class="condition-edit" href="#" style="color:#1D70B8">Edit</a></td>' : ""

            rows.push(`
                <tr class="govuk-table__row">
                    <td class="govuk-table__cell govuk-table__cell">Applies to cases that contain selected flags</td>
                    <td class="govuk-table__cell govuk-table__cell">${flags.join(", ")}</td>
                    ${edit_column_data}
                    <td class="govuk-table__cell govuk-table__cell">
                        <a id="remove-inclusive-flags" class="condition-remove" href="#" style="color:#1D70B8">Remove</a>
                    </td>
                </tr>
            `);
        } else {
            var edit_column_data = editing ? '<td class="govuk-table__cell govuk-table__cell"><a id="edit-inclusive-flags" class="condition-edit" href="#" style="color:#1D70B8">Add</a></td>' : ""
            rows.push(`
                <tr class="govuk-table__row">
                    <td class="govuk-table__cell govuk-table__cell">Applies to cases that contain selected flags</td>
                    <td class="govuk-table__cell govuk-table__cell">None</td>
                    ${edit_column_data}
                    <td class="govuk-table__cell govuk-table__cell">
                        <a id="remove-inclusive-flags" class="condition-remove-none" href="#"></a>
                    </td>
                </tr>
            `);
        }

        if (conditions.flags_to_exclude.length) {
            var flags = conditions.flags_to_exclude.map(function (flag, index) {
                return flag.name;
            });

            var edit_column_data = editing ? '<td class="govuk-table__cell govuk-table__cell"><a id="edit-exclusive-flags" class="condition-edit" href="#" style="color:#1D70B8">Edit</a></td>' : ""
            rows.push(`
                <tr class="govuk-table__row">
                    <td class="govuk-table__cell govuk-table__cell">Applies to cases that do not contain selected flags</td>
                    <td class="govuk-table__cell govuk-table__cell">${flags.join(", ")}</td>
                    ${edit_column_data}
                    <td class="govuk-table__cell govuk-table__cell">
                        <a id="remove-exclusive-flags" class="condition-remove" href="#" style="color:#1D70B8">Remove</a>
                    </td>
                </tr>
            `);
        } else {
            var edit_column_data = editing ? '<td class="govuk-table__cell govuk-table__cell"><a id="edit-exclusive-flags" class="condition-edit" href="#" style="color:#1D70B8">Add</a></td>' : ""
            rows.push(`
                <tr class="govuk-table__row">
                    <td class="govuk-table__cell govuk-table__cell">Appies to cases that do not contain selected flags</td>
                    <td class="govuk-table__cell govuk-table__cell">None</td>
                    ${edit_column_data}
                    <td class="govuk-table__cell govuk-table__cell">
                        <a id="remove-exclusive-flags" class="condition-remove-none" href="#"></a>
                    </td>
                </tr>
            `);
        }

        var table = `
        <table class="govuk-table" id="results-table">
            ${header}
            <tbody class="govuk-table__body">${rows.join('')}</tbody>
        </table>
        `;

        $("#routing-rules-flags-details").html(table);
        $("#routing-rules-flags-details").show();

        editLinks = document.getElementsByClassName("condition-edit");
        removeLinks = document.getElementsByClassName("condition-remove");
        for (var i = 0; i < editLinks.length; i++) {
            editLinks[i].index = i;
            editLinks[i].addEventListener("click", editFlags, false);
        }
        for (var i = 0; i < removeLinks.length; i++) {
            removeLinks[i].index = i;
            removeLinks[i].addEventListener("click", removeFlags, false);
        }
    }

    function resetControls(editing) {
        $("#condition-label").text("Apply the routing rule to:").show();
        $(".govuk-radios").show();
        $(".lite-search__container").show();
        $(".govuk-checkboxes").show();
        $("#routing_rules_flags_condition-contain_selected_flags").prop("checked", false);
        $("#routing_rules_flags_condition-contain_selected_flags").prop("disabled", false);
        $("#routing_rules_flags_condition-doesnot_contain_selected_flags").prop("checked", false);
        $("#routing_rules_flags_condition-doesnot_contain_selected_flags").prop("disabled", false);
        $('a:contains("Add another condition")').show().text("Add another condition");
        $('a:contains("Save changes")').show().text("Save changes");
    }

    function updateFlagInputFields(conditions) {
        var includingIds = conditions.flags_to_include.map(function (flag) { return flag.id });
        var excludingIds = conditions.flags_to_exclude.map(function (flag) { return flag.id });

        $('input[name="flags_to_include"]').val(String(includingIds.join(",")));
        $('input[name="flags_to_exclude"]').val(String(excludingIds.join(",")));
    }

    function editFlags(event) {
        event.preventDefault();

        $("#condition-label").show();
        $(".govuk-radios").show();
        $(".govuk-checkboxes").show();
        $(".lite-search__container").show();
        if (event.target.id === "edit-inclusive-flags") {
            $("#condition-label").text("The routing rule will be applied to cases that contain your selected flags");
            $("#routing_rules_flags_condition-contain_selected_flags").prop("checked", true);
            $("#routing_rules_flags_condition-contain_selected_flags").prop("disabled", false);
            $("#routing_rules_flags_condition-doesnot_contain_selected_flags").prop("checked", false);
            $("#routing_rules_flags_condition-doesnot_contain_selected_flags").prop("disabled", true);

            setFlagsDisabledStatus(flagGroups.flags_to_exclude, true);
            setFlagsCheckedStatus(flagGroups.flags_to_include, true);
            if (flagGroups.flags_to_include.length) {
                showSideMenu();
            } else {
                hidesidemenu();
            }
        } else if (event.target.id === "edit-exclusive-flags") {
            $("#condition-label").text("The routing rule will be applied to cases that do not contain your selected flags");
            $("#routing_rules_flags_condition-doesnot_contain_selected_flags").prop("checked", true);
            $("#routing_rules_flags_condition-doesnot_contain_selected_flags").prop("disabled", false);
            $("#routing_rules_flags_condition-contain_selected_flags").prop("checked", false);
            $("#routing_rules_flags_condition-contain_selected_flags").prop("disabled", true);

            setFlagsDisabledStatus(flagGroups.flags_to_include, true);
            setFlagsCheckedStatus(flagGroups.flags_to_exclude, true);
            if (flagGroups.flags_to_exclude.length) {
                showSideMenu();
            } else {
                hidesidemenu();
            }
        }

        $(".govuk-radios").hide();
        $('a:contains("Add another condition")').show();
        $('a:contains("Add another condition")').text("Save changes");
        $('a:contains("Save changes")').show();
        $("#button-save_and_continue").hide();
    }

    function removeFlags(event) {
        event.preventDefault();
        var condition = getSelectedCondition();
        if (event.target.id === "remove-inclusive-flags") {
            if (condition === "contain_selected_flags") {
                setFlagsCheckedStatus(flagGroups.flags_to_include, false);
                hidesidemenu();
            } else if (condition === "doesnot_contain_selected_flags") {
                setFlagsCheckedStatus(flagGroups.flags_to_exclude, true);
                setFlagsDisabledStatus(flagGroups.flags_to_include, false);
            }
            flagGroups.flags_to_include = [];
        } else if (event.target.id === "remove-exclusive-flags") {
            if (condition === "doesnot_contain_selected_flags") {
                setFlagsCheckedStatus(flagGroups.flags_to_include, false);
                setFlagsDisabledStatus(flagGroups.flags_to_include, true);
                hidesidemenu();
            } else if (condition === "contain_selected_flags") {
                setFlagsDisabledStatus(flagGroups.flags_to_exclude, false);
            }
            flagGroups.flags_to_exclude = [];
        }
        updateFlagInputFields(flagGroups);
        renderTable(flagGroups);

        if (flagGroups.flags_to_include.length === 0 && flagGroups.flags_to_exclude.length === 0) {
            resetControls(editing);
        }
    }

    function showSideMenu() {
        $("#checkbox-counter").show().children().show();
    }

    function hidesidemenu() {
        $("#checkbox-counter").hide().children().hide();
    }

    function setFlagsCheckedStatus(flags, status) {
        $("input[type='checkbox']").prop("checked", false);
        var allFlags = $("input[type='checkbox']").map(function () {
            return this;
        }).toArray();


        flags.forEach(function (item, index) {
            allFlags.forEach(function (flag, i) {
                if (flag.value === item.id) {
                    $(flag).prop("checked", status).trigger("change");
                }
            });
        });
    }

    function setFlagsDisabledStatus(flags, status) {
        $("input[type='checkbox']").prop("disabled", false);
        var allFlags = $("input[type='checkbox']").map(function () {
            return this;
        }).toArray();


        flags.forEach(function (item, index) {
            allFlags.forEach(function (flag, i) {
                if (flag.value === item.id) {
                    $(flag).prop("disabled", status);
                }
            });
        });
    }

    function addFlagsToCondition(options) {
        var { condition, selectedFlags, append } = options;

        if (condition) {
            if (condition === "contain_selected_flags") {
                if (append) {
                    // add the flag only if it is not included already
                    var currentFlagIds = flagGroups.flags_to_include.map(flag => flag.id);
                    for (var i = 0; i < selectedFlags.length; i++) {
                        if (!currentFlagIds.includes(selectedFlags[i].id)) {
                            flagGroups.flags_to_include.push(selectedFlags[i]);
                        }
                    }
                } else {
                    flagGroups.flags_to_include = selectedFlags
                }
            }
            if (condition === "doesnot_contain_selected_flags") {
                if (append) {
                    // add the flag only if it is not included already
                    var currentFlagIds = flagGroups.flags_to_exclude.map(flag => flag.id);
                    for (var i = 0; i < selectedFlags.length; i++) {
                        if (!currentFlagIds.includes(selectedFlags[i].id)) {
                            flagGroups.flags_to_exclude.push(selectedFlags[i]);
                        }
                    }
                } else {
                    flagGroups.flags_to_exclude = selectedFlags
                }
            }
        }

        updateFlagInputFields(flagGroups);
        renderTable(flagGroups);
    }

    function getSelectedFlags() {
        var selectedFlags = $("input[type='checkbox']:checked").map(function () {
            var text = $(this).parent().find(".govuk-checkboxes__label").text();
            return { id: this.value, name: text };
        }).toArray();

        return selectedFlags;
    }

    function getSelectedCondition() {
        if ($('#routing_rules_flags_condition-contain_selected_flags').is(':checked')) {
            return "contain_selected_flags"
        } else if ($('#routing_rules_flags_condition-doesnot_contain_selected_flags').is(':checked')) {
            return "doesnot_contain_selected_flags"
        } else {
            return "none"
        }
    }

    $("#routing_rules_flags_condition-contain_selected_flags").change(function () {
        setFlagsDisabledStatus(flagGroups.flags_to_exclude, true);
        setFlagsCheckedStatus(flagGroups.flags_to_include, true);
    });

    $("#routing_rules_flags_condition-doesnot_contain_selected_flags").change(function () {
        setFlagsDisabledStatus(flagGroups.flags_to_include, true);
        setFlagsCheckedStatus(flagGroups.flags_to_exclude, true);
    });

    $('.lite-buttons-row').on('click', '#button-save_and_continue', function () {
        var condition = getSelectedCondition();
        var selectedFlags = getSelectedFlags();
        addFlagsToCondition({ "condition": condition, "selectedFlags": selectedFlags, "append": !editing });
    });

    $('a:contains("Add another condition")').click(function () {
        var condition = getSelectedCondition();
        var selectedFlags = getSelectedFlags();

        addFlagsToCondition({ "condition": condition, "selectedFlags": selectedFlags, "append": !editing });

        if (editing) {
            $("#condition-label").hide();
            $(".govuk-radios").hide();
            $(".govuk-checkboxes").hide();
            $(".lite-search__container").hide();
            $('a:contains("Save changes")').hide();
            $('a:contains("Add another condition")').hide();
            $("#button-save_and_continue").show();
            hidesidemenu();
        }

        if (!editing) {
            if (condition === "contain_selected_flags") {
                setFlagsCheckedStatus(flagGroups.flags_to_include, true);
            } else if (condition === "doesnot_contain_selected_flags") {
                setFlagsCheckedStatus(flagGroups.flags_to_exclude, true);
            }
        }

        // Clear the error if there is any.
        // It gets cleared automatically if either condition is selected and "Save and continue"
        // but if we are only saving changes the error is persistent in the UI so clear it here
        // till we are ready to submit
        if ($(".govuk-error-summary")[0] || $(".govuk-error-message")[0]) {
            var condition = getSelectedCondition();
            if (condition !== "none" && (flagGroups.flags_to_include.length || flagGroups.flags_to_exclude.length)) {
                $(".govuk-error-summary").hide().children().hide();
                $(".govuk-error-message").hide();
                $("#pane_routing_rules_flags_condition").removeClass("govuk-form-group--error");
            }
        }
    });

    $('a:contains("Save changes")').click(function () {
        var condition = getSelectedCondition();
        var selectedFlags = getSelectedFlags();
        addFlagsToCondition({ "condition": condition, "selectedFlags": selectedFlags, "append": false });

        if (editing) {
            $("#condition-label").hide();
            $(".govuk-radios").hide();
            $(".govuk-checkboxes").hide();
            $(".lite-search__container").hide();
            $('a:contains("Save changes")').hide();
        }
    });

    function setInitialState(editing) {
        flags_to_include = $('input[name="flags_to_include"]').val().split(",").filter(function (el) { return el; });
        flags_to_exclude = $('input[name="flags_to_exclude"]').val().split(",").filter(function (el) { return el; });

        if (flags_to_include.length === 0 && flags_to_exclude.length === 0) {
            resetControls(editing);
            return;
        }

        var allFlags = $("input[type='checkbox']").map(function () {
            return this;
        }).toArray();

        include_flags = [];
        exclude_flags = [];
        flags_to_include.forEach(function (item, index) {
            allFlags.forEach(function (flag, i) {
                if (flag.value === item) {
                    var text = $(flag).parent().find(".govuk-checkboxes__label").text();
                    include_flags.push({ id: item, name: text })
                }
            });
        });
        if (include_flags.length) {
            flagGroups.flags_to_include.push(...include_flags);
        }

        flags_to_exclude.forEach(function (item, index) {
            allFlags.forEach(function (flag, i) {
                if (flag.value === item) {
                    var text = $(flag).parent().find(".govuk-checkboxes__label").text();
                    exclude_flags.push({ id: item, name: text })
                }
            });
        });
        if (exclude_flags.length) {
            flagGroups.flags_to_exclude.push(...exclude_flags);
        }

        if (editing) {
            $("#condition-label").hide();
            $(".govuk-radios").hide();
            $(".govuk-checkboxes").hide();
            $(".lite-search__container").hide();
            $('a:contains("Add another condition")').hide();
        } else {
            var condition = getSelectedCondition();

            $("#condition-label").text("Apply the routing rule to:").show();
            if (condition === "contain_selected_flags") {
                setFlagsCheckedStatus(flagGroups.flags_to_include, true);
                setFlagsDisabledStatus(flagGroups.flags_to_exclude, true);
            } else if (condition === "doesnot_contain_selected_flags") {
                setFlagsCheckedStatus(flagGroups.flags_to_exclude, true);
                setFlagsDisabledStatus(flagGroups.flags_to_include, true);
            }
        }

        renderTable(flagGroups);

    }

    editing = $(".govuk-fieldset__heading").text().trim() == "Edit flags";

    setInitialState(editing);
})();
