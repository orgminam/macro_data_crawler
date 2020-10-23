from database.manager import Session
from database.models import Master, ErrorHist, JobHist
import json


def get_last_date(id):
    """데이터가 최종적으로 기록된 일자를 조회"""

    sess = Session()
    return sess.query(Master).filter_by(id=id).first().last_date


def update_last_date(id, datestr):
    """데이터를 기록한 최종일자를 업데이트"""

    sess = Session()
    sess.query(Master).filter_by(id=id).update({"last_date": datestr})
    sess.commit()


def update_success_hist(id, params):
    """성공시 로그 기록"""

    job_hist = JobHist(id=id, params=params)
    sess = Session()
    sess.merge(job_hist)
    sess.commit()


def update_error_hist(id, reason, params, trace=None):
    """실패시 로그 기록"""
    sess = Session()
    err_hist = ErrorHist(id=id, reason=reason, params=params, trace=trace)
    sess.merge(err_hist)
    sess.commit()
