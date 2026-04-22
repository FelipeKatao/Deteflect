__all__ = ["NLPFacade"]


def __getattr__(name: str):
    if name == "NLPFacade":
        from .facade import NLPFacade as _NLPFacade
        globals()["NLPFacade"] = _NLPFacade
        return _NLPFacade
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
