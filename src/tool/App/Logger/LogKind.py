from Utils.Wrap import Wrap

class LogKind(Wrap):
    KIND_SUCCESS = 'success'
    KIND_ERROR = 'error'
    KIND_DEPRECATED = 'deprecated'
    KIND_MESSAGE = 'message'
    KIND_HIGHLIGHT = 'highlight'

    kind: str
