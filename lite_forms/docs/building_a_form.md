# Building a form

```
Form(
    title=strings.WHICH_EXPORT_LICENCE_DO_YOU_WANT_TITLE,
    description=strings.WHICH_EXPORT_LICENCE_DO_YOU_WANT_DESCRIPTION,
    questions=[
        RadioButtons(
            name="application_type",
            options=[
                Option(
                    key=STANDARD_LICENCE,
                    value=strings.STANDARD_LICENCE,
                    description=strings.STANDARD_LICENCE_DESCRIPTION,
                ),
                Option(
                    key=OPEN_LICENCE,
                    value=strings.OPEN_LICENCE,
                    description=strings.OPEN_LICENCE_DESCRIPTION,
                ),
            ],
        ),
        DetailComponent(strings.HELP_WITH_CHOOSING_A_LICENCE, strings.HELP_WITH_CHOOSING_A_LICENCE_CONTENT),
    ],
    default_button_name=strings.CONTINUE,
),
```
