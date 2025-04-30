class BaseManifest:
    urls = None


class BaseCaseworkerUrls:

    @classmethod
    def get_detail_view_url(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_notes_and_timeline_url(cls, **kwargs):
        raise NotImplementedError


class BaseExporterUrls:

    @classmethod
    def get_application_detail_url(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_application_task_list_url(cls, **kwargs):
        raise NotImplementedError
