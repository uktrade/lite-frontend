(function () {
    var flagsConditions = [];

    function renderTable(conditions) {
        if (conditions && conditions.length === 0) {
            $("#routing-rules-flags-details").hide();
            return;
        }
        var header = `
            <thead class="govuk-table__head">
            <tr class="govuk-table__row">
                <th class="govuk-table__header" scope="col">Condition</th>
                <th class="govuk-table__header" scope="col">Flags</th>
                <th class="govuk-table__header" scope="col"></th>
            </tr>
        </thead>`

        var rows = conditions.map(function (row, index) {
            var condition_text = row.condition === "contain_selected_flags" ? "Cases including" : "Cases excluding";
            var flags = row.flags.map(function (flag) { return flag.name; });
            return `
                <tr class="govuk-table__row">
                    <td class="govuk-table__cell govuk-table__cell">${condition_text}</td>
                    <td class="govuk-table__cell govuk-table__cell">${flags.join(", ")}</td>
                    <td class="govuk-table__cell govuk-table__cell">
                        <a class="condition-remove" href="#">Remove</a>
                    </td>
                </tr>
            `;
        });

        var table = `
        <table class="govuk-table" id="results-table">
            ${header}
            <tbody class="govuk-table__body">${rows}</tbody>
        </table>
        `;

        $("#routing-rules-flags-details").html(table);
        $("#routing-rules-flags-details").show();

        removeLinks = document.getElementsByClassName("condition-remove");
        for (var i = 0; i < removeLinks.length; i++) {
            removeLinks[i].index = i;
            removeLinks[i].addEventListener("click", removeFlags, false);
        }
    }

    function updateFlagInputFields(conditions) {
        var includingIds = getFlagIds("contain_selected_flags", conditions)
        var excludingIds = getFlagIds("doesnot_contain_selected_flags", conditions)

        $('input[name="flags_to_include"]').val(String(includingIds.join(",")));
        $('input[name="flags_to_exclude"]').val(String(excludingIds.join(",")));
    }

    function removeFlags(event) {
        event.preventDefault();
        flagsConditions.splice(event.currentTarget.index, 1);

        updateFlagInputFields(flagsConditions);
        renderTable(flagsConditions);
    }

    function getFlagIds(condition, flags) {
        var filtered = flags.filter(function (flag) { return flag.condition === condition; })
        var allIds = filtered.map(function (item) { return item.ids; })
        return allIds;
    }

    function addConditionWithSelectedFlags() {
        // get all the selected flags
        var selectedFlags = $("input[type='checkbox']:checked").map(function () {
            var text = $(this).parent().find(".govuk-checkboxes__label").text();
            return { id: this.value, name: text };
        }).toArray();

        var condition = $('input[name="routing_rules_flags_condition"]:checked').val();
        if (condition) {
            var flag_ids = selectedFlags.map(function (flag) { return flag.id; });
            flagsConditions.push({ condition: condition, flags: selectedFlags, ids: flag_ids.join(",") });
        }
        updateFlagInputFields(flagsConditions);

        if (selectedFlags.length) {
            renderTable(flagsConditions);
        }
    }

    $('.lite-buttons-row').on('click', '#button-save_and_continue', function(){
        addConditionWithSelectedFlags()
    });

    $('a:contains("Add another condition")').click(function () {
        addConditionWithSelectedFlags()
    });

    // pre-populate selected flags in case of editing the rule
    function prePopulateFlags() {
        var allFlags = $("input[type='checkbox']").map(function () {
            return this;
        }).toArray();

        flags_to_include = $('input[name="flags_to_include"]').val().split(",");
        flags_to_exclude = $('input[name="flags_to_exclude"]').val().split(",");

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
            flagsConditions.push({ condition: "contain_selected_flags", flags: include_flags, ids: flags_to_include.join(",") })
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
            flagsConditions.push({ condition: "doesnot_contain_selected_flags", flags: exclude_flags, ids: flags_to_exclude.join(",") })
        }

        renderTable(flagsConditions);
    }

    prePopulateFlags();
})();