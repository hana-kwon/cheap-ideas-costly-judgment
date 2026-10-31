# ============================================================
# START DATE   : 2026-10-25
# CODE RUN DATE: 2026-10-25
# TIME TAKEN   : ~20 min
# DESCRIPTION  : Loaded automatically by every Python process an agent starts (via PYTHONPATH).
#                Logs each regression fit so "specifications actually estimated" is counted
#                from execution, not from the agent's own report. Used in the pilot and kept
#                on the path in every report-task session.
# INPUT FILES  : env ORGEVAL_LOG (path of the JSONL log)
# OUTPUT FILES : the JSONL log, one line per model fit
# ============================================================
# ★ IMPORTANT: must never break the agent's code. Every hook is wrapped in try/except.
# Limitation: fits done with numpy.linalg.lstsq, scipy.stats.linregress or hand-written
# algebra are not logged; transcripts are checked for those separately.
import json
import os
import time

_LOG = os.environ.get("ORGEVAL_LOG")


def _write(kind, model):
    try:
        names = list(getattr(model, "exog_names", None) or [])
        rec = {"ts": time.time(), "pid": os.getpid(), "kind": kind,
               "endog": str(getattr(model, "endog_names", "")),
               "exog": names, "nobs": int(getattr(model, "nobs", 0) or 0)}
        with open(_LOG, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    except Exception:
        pass


def _wrap(cls, kind):
    orig = cls.fit
    if getattr(orig, "_orgeval", False):
        return

    def fit(self, *a, **k):
        _write(kind, self)
        return orig(self, *a, **k)

    fit._orgeval = True
    cls.fit = fit


if _LOG:
    try:
        from statsmodels.regression import linear_model as _lm
        _wrap(_lm.RegressionModel, "sm_regression")
        from statsmodels.genmod import generalized_linear_model as _glm
        _wrap(_glm.GLM, "sm_glm")
        from statsmodels.regression import quantile_regression as _qr
        _wrap(_qr.QuantReg, "sm_quantreg")
        from statsmodels.discrete import discrete_model as _dm
        _wrap(_dm.DiscreteModel, "sm_discrete")
    except Exception:
        pass
    try:
        from sklearn import linear_model as _sk

        def _skwrap(cls):
            orig = cls.fit
            if getattr(orig, "_orgeval", False):
                return

            def fit(self, X, y, *a, **k):
                try:
                    names = list(getattr(X, "columns", []))
                    rec = {"ts": time.time(), "pid": os.getpid(), "kind": "sklearn_" + cls.__name__,
                           "endog": str(getattr(y, "name", "")), "exog": [str(c) for c in names],
                           "nobs": int(len(y))}
                    with open(_LOG, "a") as fh:
                        fh.write(json.dumps(rec) + "\n")
                except Exception:
                    pass
                return orig(self, X, y, *a, **k)

            fit._orgeval = True
            cls.fit = fit

        for _c in (_sk.LinearRegression, _sk.Ridge, _sk.Lasso):
            _skwrap(_c)
    except Exception:
        pass
