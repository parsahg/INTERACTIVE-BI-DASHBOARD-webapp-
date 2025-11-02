import pandas as pd

def load_data(file_path):
    sader1402 = pd.read_excel("/home/parsahg/Desktop/saderat1.xlsx", sheet_name='آمار صادرات 1402',skiprows=1) 
    sader1403 = pd.read_excel("/home/parsahg/Desktop/saderat1.xlsx", sheet_name='آمار صادرات 1403',skiprows=1)

    sader1402["سال"] = 1402
    sader1403["سال"] = 1403

    month_dict_1402 = {m: f"{m} 1402" for m in
        ['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']}
    month_dict_1403 = {m: f"{m} 1403" for m in
        ['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']}

    sader1402['ماه ارسال'] = sader1402['ماه ارسال'].map(month_dict_1402)
    sader1403['ماه ارسال'] = sader1403['ماه ارسال'].map(month_dict_1403)

    return sader1402, sader1403


def match_dataframes(sader1402, sader1403):
    matched = pd.DataFrame()
    common = list(set(sader1403.columns).intersection(set(sader1402.columns)))
    sader1402_common = sader1402[common].select_dtypes(include="number")
    sader1403_common = sader1403[common].select_dtypes(include="number")

    min_rows = min(len(sader1402_common), len(sader1403_common))
    substacted = sader1402_common.iloc[:min_rows] - sader1403_common.iloc[:min_rows]
    substacted = substacted.dropna(how="all")

    matched = substacted.copy()
    non_numeric = sader1403.select_dtypes(exclude="number").reindex(range(min_rows)).reset_index(drop=True)
    for col in non_numeric.columns:
        matched[col] = non_numeric[col]

    return matched
