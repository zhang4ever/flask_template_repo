import datetime
import time
import pandas as pd


class TimeUtils:

    STANDARD_DATE_FORMAT = '%Y-%m-%d'
    STANDARD_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    STANDARD_TIME_FORMAT_WITH_MILLS = '%Y-%m-%d %H:%M:%S.%f'
    UTC_TIME_FORMAT = '%Y-%m-%d %H:%M:%S+08:00'
    ISO_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
    ISO_UTC_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+08:00'

    @classmethod
    def str_to_date(cls, time_str: str):
        dt = cls.str_to_datetime(time_str)
        return cls.datetime_to_str(dt, cls.STANDARD_DATE_FORMAT)

    @classmethod
    def get_duration(cls, time1: str, time2: str):
        """
        获取两个时间之间的duration
        """
        dt1 = cls.str_to_datetime(time1)
        dt2 = cls.str_to_datetime(time2)
        return abs((dt1 - dt2).total_seconds())

    @classmethod
    def compare(cls, time1: str, time2: str) -> bool:
        """
        比较两个时间大小，如果 time1 > time2, 返回True，否则False

        """
        dt1 = cls.str_to_datetime(time1)
        dt2 = cls.str_to_datetime(time2)
        return (dt1 - dt2).total_seconds() > 0

    @classmethod
    def standard_time_to_iso(cls, time_str: str):
        if 'T' in time_str:
            return time_str
        return time_str.replace(' ', 'T')

    @classmethod
    def standard_time_to_iso_utc(cls, time_str: str):
        if time_str.endswith('+08:00'):
            return time_str
        return time_str.replace(' ', 'T') + '+08:00'

    @classmethod
    def standard_time_to_month(cls, time_str: str):
        return '-'.join(time_str.split('-')[:2])

    @classmethod
    def str_to_timestamp(cls, time_str, str_format=None):
        """
        将字符串格式的时间转换成时间戳
        """
        str_format = cls.STANDARD_TIME_FORMAT if str_format is None else str_format
        time_array = time.strptime(time_str, str_format)
        timestamp = time.mktime(time_array)
        return timestamp

    @classmethod
    def timestamp_to_str(cls, timestamp, str_format=None):
        """
        将时间戳转换成字符串格式的时间
        """
        str_format = cls.STANDARD_TIME_FORMAT if str_format is None else str_format
        time_local = time.localtime(timestamp)
        time_str = time.strftime(str_format, time_local)
        return time_str

    @classmethod
    def str_to_datetime(cls, time_str, str_format=None):
        """
        将字符串格式的时间转换成datetime类型
        """
        if 'T' in time_str:
            time_str = time_str.replace('T', ' ')
        if len(time_str.split(':')[-1]) > 2:
            fmt = cls.STANDARD_TIME_FORMAT_WITH_MILLS
        elif not str_format:
            fmt = cls.STANDARD_TIME_FORMAT
        else:
            fmt = str_format
        dt = datetime.datetime.strptime(time_str, fmt)

        return dt

    @classmethod
    def datetime_to_str(cls, dt, str_format=None):
        """
        将datetime类型的时间转换成字符串格式
        """
        str_format = cls.STANDARD_TIME_FORMAT if str_format is None else str_format
        time_str = dt.strftime(str_format)
        return time_str

    @classmethod
    def get_now_timestamp(cls):
        """
        当前时间的时间戳（毫秒）
        """
        return int(round(time.time()) * 1000)

    @classmethod
    def get_now_time(cls, str_format=None):
        """
        将当前时间转换成特定格式的字符串
        """
        str_format = cls.STANDARD_TIME_FORMAT if str_format is None else str_format
        now = datetime.datetime.now()
        time_str = now.strftime(str_format)
        return time_str

    @classmethod
    def add_time(cls, cur_time: str, hours: int = 0, minutes: int = 0, seconds: int = 0):
        date_time = cls.str_to_datetime(cur_time, cls.STANDARD_TIME_FORMAT)
        new_time = date_time + datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return cls.datetime_to_str(new_time)

    @classmethod
    def minus_time(cls, cur_time: str, hours: int = 0, minutes: int = 0, seconds: int = 0):
        date_time = cls.str_to_datetime(cur_time, cls.STANDARD_TIME_FORMAT)
        new_time = date_time + datetime.timedelta(hours=-hours, minutes=-minutes, seconds=-seconds)
        return cls.datetime_to_str(new_time)

    @classmethod
    def get_index_days(cls, start_time: str, end_time: str):
        """
        根据开始时间和结束时间，得到es查询时需要的index_days,
        example:
        	[2021-02-11, 2021-02-12...]
        """
        if '+08:00' in start_time:
            start_time = start_time.replace('+08:00', '')
        if '+08:00' in end_time:
            end_time = end_time.replace('+08:00', '')
        time_format = cls.STANDARD_TIME_FORMAT if ':' in start_time or ':' in end_time else cls.STANDARD_DATE_FORMAT
        start_time = start_time.replace('T', ' ') if 'T' in start_time else start_time
        end_time = end_time.replace('T', ' ') if 'T' in end_time else end_time
        start_time = cls.str_to_datetime(start_time, time_format)
        end_time = cls.str_to_datetime(end_time, time_format)
        index_days_list = [cls.datetime_to_str(
            dt=start_time+datetime.timedelta(days=i), str_format=cls.STANDARD_DATE_FORMAT)
            for i in range((end_time - start_time).days + 1)
        ]

        return index_days_list

    @classmethod
    def split_time_ranges(cls, from_time, to_time, frequency):
        """
        将一个时间段划分为多个连续的小时间段
        """
        from_time, to_time = pd.to_datetime(from_time), pd.to_datetime(to_time)
        time_range = list(pd.date_range(from_time, to_time, freq='%sS' % frequency))
        if to_time not in time_range:
            time_range.append(to_time)
        time_range = [item.strftime(cls.STANDARD_TIME_FORMAT) for item in time_range]
        time_ranges = []
        for item in time_range:
            f_time = item
            t_time = (cls.str_to_datetime(item, cls.STANDARD_TIME_FORMAT) + datetime.timedelta(seconds=frequency))
            if t_time >= to_time:
                t_time = to_time.strftime(cls.STANDARD_TIME_FORMAT)
                time_ranges.append((f_time, t_time))
                break
            time_ranges.append((f_time, t_time.strftime(cls.STANDARD_TIME_FORMAT)))
        return time_ranges
