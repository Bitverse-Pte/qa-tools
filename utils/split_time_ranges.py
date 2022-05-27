import datetime
import pandas as pd

class split_time_ranges:
    # from_time开始时间，to_time结束时间，frequency间隔时间,返回字符间隔
    def split_time_rangesStr(from_time, to_time, frequency):
        from_time, to_time = pd.to_datetime(from_time), pd.to_datetime(to_time)
        time_range = list(pd.date_range(from_time, to_time, freq='%sS' % frequency))
        if to_time not in time_range:
            time_range.append(to_time)
        time_range = [item.strftime("%Y-%m-%d %H:%M:%S") for item in time_range]
        time_ranges = []
        for item in time_range:
            f_time = item
            t_time = (datetime.datetime.strptime(item, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=frequency))
            if t_time >= to_time:
                t_time = to_time.strftime("%Y-%m-%d %H:%M:%S")
                time_ranges.append([f_time, t_time])
                break
            time_ranges.append([f_time, t_time.strftime("%Y-%m-%d %H:%M:%S")])
        return time_ranges

    # from_time开始时间，to_time结束时间，frequency间隔时间，返回时间戳
    def split_time_rangesLong(from_time, to_time, frequency):
        from_time, to_time = pd.to_datetime(from_time), pd.to_datetime(to_time)
        time_range = list(pd.date_range(from_time, to_time, freq='%sS' % frequency))
        if to_time not in time_range:
            time_range.append(to_time.timestamp())
        time_ranges = []
        for item in time_range:
            f_time = item
            t_time = (datetime.datetime.strptime(item, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=frequency))
            if t_time >= to_time:
                # t_time = to_time.strftime("%Y-%m-%d %H:%M:%S")
                # time_ranges.append([f_time, t_time])
                break
            time_ranges.append([f_time, t_time.timestamp()])
        return time_ranges


if __name__ == '__main__':
    splitTime=split_time_ranges
    from_time = '2019-10-01 10:20:45'
    to_time = '2019-10-01 10:50:45'
    frequency = 60 * 10

    time_ranges = splitTime.split_time_rangesStr(from_time, to_time, frequency)
    print(time_ranges)
    for time in time_ranges:
        print(time[0])
