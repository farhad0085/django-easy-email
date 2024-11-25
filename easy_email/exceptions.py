class TemplateNotFound(Exception):
    """
    The exception used when a template does not exist.
    """

    def __init__(self, msg=None):
        if not msg:
            self.msg = "Template doesn't exists"
        super().__init__(msg)
