from flask import current_app
import elasticsearch


class Elastic(object):
    """
    A thin wrapper around `elasticsearch.Elasticsearch`
    """
    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        app.config.setdefault('ELASTICSEARCH_URL', 'http://localhost:9200/')

        # for backwards compatibility
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['elastic'] = elasticsearch.Elasticsearch(
            app.config['ELASTICSEARCH_URL'],
            **kwargs
        )

    def __getattr__(self, item):
        if 'elastic' not in current_app.extensions:
            raise Exception(
                'not initialised, did you forget to call init_app?')
        return getattr(current_app.extensions['elastic'], item)
