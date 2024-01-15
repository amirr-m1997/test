import os
import tkinter as tk
import pandas as pd
from persiantools.jdatetime import JalaliDate
from tkinter import messagebox
from pandastable import Table
def calculate_earning(result_label):
    global existing_df
    global without_bime1
    hours_worked_text = entry1.get()
    hourly_rate_text = entry2.get()

    if not hours_worked_text or not hourly_rate_text:
        messagebox.showerror("هشدار", "لطفاً ابتدا همه فیلدها را پر کنید")
        return
    if not (hours_worked_text.replace('.', '', 1).isdigit() and hourly_rate_text.replace('.', '', 1).isdigit()):
        messagebox.showerror("هشدار", "لطفاً فقط مقادیر عددی معتبر وارد کنید")
        return

    # تبديل ساعت ب دقيقه
    def convert_hours_to_minutes(hours_minutes):
        hours = int(hours_minutes)
        minutes = round((hours_minutes - hours) * 100)
        total_minutes = hours * 60 + minutes
        return total_minutes

    minutes_worked = float(hours_worked_text)
    minutes_worked = convert_hours_to_minutes(minutes_worked)
    # تبديل حقوق هر ساعت كاري ب دقيقه
    hourly_rate = float(hourly_rate_text)
    hourly_rate = hourly_rate / 60
    daily_earning = minutes_worked * hourly_rate
    without_bime1 = daily_earning * 0.93

    def convert_minutes_to_hours(minutes):
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return "{}.{}".format(hours, remaining_minutes)

    hours_worked = convert_minutes_to_hours(minutes_worked)

    # hours_worked = float(hours_worked_text)
    now = JalaliDate.today()
    if now.day == 21:
        messagebox.showerror("هشدار",
                             "لطفاً ابتدا فایل اکسل قبلی را براي جلوگيري از پاك شدن اطلاعات قبلي به یک پوشه دیگر انتقال دهید زيرا اضافه کاری ها هر ماه تا 20 ام محاسبه میشود و از 20ام به بعد به ماه بعد موكول ميشود همچنين اگر انتقال داده اید این پیام را نادیده بگیرید")
        # ایجاد فایل اکسل جدید با نام جدید
        file_name = f'{now.year}_EzafeKari.xlsx'

        # ساخت یک DataFrame جدید برای اطلاعات روز جدید
        data = {'روز هفته': [], 'تاریخ': [], 'ساعات کاری': [],
                'مبلغ هر ساعت': [], 'مجموع درآمد همان روز': [],
                'مجموع روزها': [], 'مجموع ساعت ها': [], 'مجموع درآمد': [],
                'دريافتي خالص امروز': [] ,'دريافتي بعد از كسر بيمه': []}
        existing_df = pd.DataFrame(data)
    if now.day >= 21 and now.day <= 30:
        messagebox.showerror("هشدار",
                             "لطفاً ابتدا فایل اکسل قبلی را براي جلوگيري از پاك شدن اطلاعات قبلي به یک پوشه دیگر انتقال دهید زيرا اضافه کاری ها هر ماه تا 20 ام محاسبه میشود و از 20ام به بعد به ماه بعد موكول ميشود همچنين اگر انتقال داده اید این پیام را نادیده بگیرید")
    if not existing_df.empty:

        total_earning = existing_df['مجموع درآمد'].iloc[-1] + daily_earning

        # تبديل دقيقه ب ساعت
        time_parts  = str(existing_df['مجموع ساعت ها'].iloc[-1]).split('.')
        hours = time_parts [0]
        minutes = time_parts [1] if len(time_parts ) > 1 else '00'
        total_minutes = int(hours) * 60 + int(minutes)
        total_minutes += minutes_worked
        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60
        total_hours = float(f"{total_hours}.{remaining_minutes}")

        daily_worked_sum = existing_df['مجموع روزها'].iloc[-1] + 1
        without_bime1=without_bime1
        print(
            without_bime1
        )
        print('----------',existing_df['دريافتي بعد از كسر بيمه'].iloc[-1])
        # without_bime = str(existing_df['دريافتي بعد از كسر بيمه'].iloc[-1])+without_bime1
        without_bime = str(existing_df['دريافتي بعد از كسر بيمه'].iloc[-1] + without_bime1)
    else:

        total_earning = daily_earning
        total_hours = hours_worked
        daily_worked_sum = 1
        without_bime = daily_earning * 0.93
    now = JalaliDate.today().to_gregorian()
    jalali_date = JalaliDate.to_jalali(year=now.year, month=now.month, day=now.day)
    day_of_week = jalali_date.strftime('%A')
    date = jalali_date.strftime('%Y/%m/%d')
    day_of_week_en = {
        'Shanbeh': 'شنبه',
        'Yekshanbeh': 'یکشنبه',
        'Doshanbeh': 'دوشنبه',
        'Seshanbeh': 'سه‌شنبه',
        'Chaharshanbeh': 'چهارشنبه',
        'Panjshanbeh': 'پنج‌شنبه',
        'Jomeh': 'جمعه',
    }
    day_of_week = day_of_week_en[day_of_week]
    result = messagebox.askyesno("هشدار", "آیا از ارسال اطلاعات اطمینان دارید؟")

    if result == True:
        new_row = pd.DataFrame(
            {'روز هفته': [day_of_week], 'تاریخ': [date], 'ساعات کاری': [hours_worked],
             'مبلغ هر ساعت': [hourly_rate_text],
             'مجموع درآمد همان روز': [daily_earning], 'مجموع روزها': [daily_worked_sum],
             'مجموع ساعت ها': [total_hours],
             'مجموع درآمد': [total_earning], 'دريافتي بعد از كسر بيمه': [without_bime],'دريافتي خالص امروز':[without_bime1]})
        now = JalaliDate.today()
        existing_df = pd.concat([existing_df, new_row], ignore_index=True)
        existing_df.to_excel(f'{now.year}_EzafeKari.xlsx', index=False)
        result_text = f"امروز: {day_of_week}\nتاریخ: {date}\nساعات کاری: {hours_worked}\nمجموع روزها: {daily_worked_sum}\nمجموع ساعت ها: {total_hours}\n  دريافتي خالص امروز: {without_bime1}\n "

        result_label.config(text=" ...در حال ذخیره و ارسال اطلاعات درخواستی" "\n", fg="green")
        root.after(1000, lambda: result_label.config(text=result_text, fg="black"))
        result_label.after(4000, lambda: button1.config(state=tk.NORMAL))
        button1.config(state=tk.DISABLED)


# pypy -m ensurepip pypy -m pip install package_name

def show_table():
    if not existing_df.empty:
        # ایجاد پنجره جدید برای نمایش جدول
        table_window = tk.Toplevel(root)
        table_window.title("نمایش جدول")
        table_window.geometry("800x400")

        # ایجاد جدول با استفاده از PandasTable
        table = Table(table_window, dataframe=existing_df)
        table.show()
    else:
        messagebox.showerror("هشدار", "!هیچ داده‌ای برای نمایش وجود ندارد")
        # result_label.config(fg="red", text=".هیچ داده‌ای موجود نیست")


now = JalaliDate.today()
file_name = f'{now.year}_EzafeKari.xlsx'
if not os.path.isfile(file_name):
    data = {'روز هفته': [], 'تاریخ': [], 'ساعات کاری': [], 'مبلغ هر ساعت': [], 'مجموع درآمد همان روز': [],
            'مجموع روزها': [], 'مجموع ساعت ها': [], 'مجموع درآمد': [],'دريافتي خالص امروز' : [], 'دريافتي بعد از كسر بيمه': []}
    existing_df = pd.DataFrame(data)
else:
    existing_df = pd.read_excel(file_name)

root = tk.Tk()
root.title("محاسبه درآمد")

root.geometry("400x300")
root.resizable(False, False)

label1 = tk.Label(root, text=" : لطفاً تعداد ساعات کاری را وارد کنید ")
label1.pack()
entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text=": لطفاً مبلغ هر ساعت کار را وارد کنید ")
label2.pack()
entry2 = tk.Entry(root)
entry2.pack()

button2 = tk.Button(root, text="نمایش کل اطلاعات تا به امروز", command=show_table)
button2.pack()

button1 = tk.Button(root, text="محاسبه و ذخیره اطلاعات امروز", command=lambda: calculate_earning(result_label))
button1.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
