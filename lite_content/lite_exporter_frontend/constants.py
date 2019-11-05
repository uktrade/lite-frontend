from conf.settings import env

PERMISSION_FINDER_LINK = '<a class="govuk-link" href="' + env('PERMISSIONS_FINDER_URL') + '">Permissions Finder</a>'

APPLICATION_GOODS_ADD_BACK = "Back to goods"
APPLICATION_GOODS_ADD_APPLICATION_DETAILS = "Details for good on application"
APPLICATION_GOODS_ADD_DOCUMENT_DESCRIPTION = "To finish creating the good, you must attach a document." \
                                             "\n\nWarning: Do not upload any document which is above " \
                                             "'official-sensitive' level\n\nMaximum size: 100MB per file"

APPLICATION_GOODS_CONTROL_CODE_REQUIRED_DESCRIPTION = 'If you don\'t know, please use' + PERMISSION_FINDER_LINK +  \
            'to find the appropriate ' 'code before adding the good to the application. You may need to create a good '\
            'from the goods list if you are still unsure'

GOODS_CREATE_CONTROL_CODE_REQUIRED_DESC = 'If you don\'t know you can use' + PERMISSION_FINDER_LINK
