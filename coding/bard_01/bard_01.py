import xlwings as xw


def button_run():
    wb = xw.Book.caller()
    # wb.sheets[0].range("A1").value = "Hello xlwings!"     # for testing

    


# @xw.func
# def hello(name):
#     return "hello {0}".format(name)
