import sys
import main_window
import error_dialog
import pass_dialog
import help_dialog

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import re

tab_char = " "*4
class Log:
    def __init__(self):
        self.log = ''

    def insert(self, info):
        self.log += f'{info}\n'

    def __str__(self):
        return '='*60 + '\n' + self.log + '='*60 + '\n'

    def __repr__(self):
        return self.__str__()

    def text(self):
        return '='*60 + '\n' + self.log + '='*60 + '\n'


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 实例化主窗口
    MainWindow = QMainWindow()
    ui = main_window.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowIcon(QIcon('./ico1.ico'))
    MainWindow.setWindowTitle("“参考文献格式”检测")

    # 实例化 error_Dialog 窗口
    error_Dialog = QDialog()
    ui_error_dialog = error_dialog.Ui_Dialog()
    ui_error_dialog.setupUi(error_Dialog)
    error_Dialog.setWindowIcon(QIcon('./ico1.ico'))
    error_Dialog.setWindowTitle("检测不通过")
    error_Dialog.setWindowFlags(Qt.WindowCloseButtonHint)

    # 实例化 pass_Dialog 窗口
    pass_Dialog = QDialog()
    ui_pass_dialog = pass_dialog.Ui_Dialog()
    ui_pass_dialog.setupUi(pass_Dialog)
    pass_Dialog.setWindowIcon(QIcon('./ico1.ico'))
    pass_Dialog.setWindowTitle("检测通过")
    pass_Dialog.setWindowFlags(Qt.WindowCloseButtonHint)

    # 实例化 help_Dialog 窗口
    help_Dialog = QDialog()
    ui_help_dialog = help_dialog.Ui_Dialog()
    ui_help_dialog.setupUi(help_Dialog)
    help_Dialog.setWindowIcon(QIcon('./ico1.ico'))
    help_Dialog.setWindowTitle("help")
    help_Dialog.setWindowFlags(Qt.WindowCloseButtonHint)


    def check_button_click():
        input_text = ui.textEdit.toPlainText()
        log, error_flag = check(input_text)
        if error_flag:
            ui_error_dialog.textBrowser.setText(log)
            error_Dialog.show()
        else:
            pass_Dialog.show()

    def check(input_text):

        references = [text for text in input_text.split('\n') if text != '']
        if references == []:
            cur_log = Log()
            error_flag = True
            cur_log.insert(f'{tab_char}未检测到参考文献')
            check_log = cur_log.text()
            return check_log, error_flag

        check_log = f'检测到{len(references)}个参考文献\n'
        error_flag = False

        for index, reference in enumerate(references):
                # 检测是否有+号
                cur_log = Log()
                cur_log.insert(f'第{index+1}个参考文献：\n{tab_char}{reference}\n检测结果：')
                if '+' not in reference:
                    error_flag = True
                    cur_log.insert(f'{tab_char}未检测到 + 号')
                    check_log += cur_log.text()
                    continue

                # 检测参考文献是否可以正常划分，划分后的数量是否符合要求
                parts = reference.split('+')
                if len(parts) == 6:
                    code_author, use, method, publication, year, title = parts
                else:
                    error_flag = True
                    cur_log.insert(f'{tab_char}参考文献解析失败，格式错误，请用以下格式命名：\n{tab_char}有无代码有无重要作者+用途+方法+期刊或会议小写缩写+年份后两位+标题')
                    check_log += cur_log.text()
                    continue

                # 检测 代码 部分
                if len(code_author) != 2:
                    error_flag = True
                    cur_log.insert(f'{tab_char}代码以及重要作者 部分格式错误，代码部分用 0 或 1 表示，重要作者用 A 或 B 表示，例如：有代码有重要作者，则为 1A')
                    check_log += cur_log.text()
                    continue


                try:
                    if int(code_author[0]) not in [0, 1]:
                        error_flag = True
                        cur_log.insert(f'{tab_char}代码 部分格式错误，有无代码，用 0 或 1 表示')
                        check_log += cur_log.text()
                        continue
                except ValueError:
                    error_flag = True
                    cur_log.insert(f'{tab_char}代码 部分格式错误，有无代码，用 0 或 1 表示')
                    check_log += cur_log.text()
                    continue

                if code_author[1] not in ['A', 'B']:
                    error_flag = True
                    cur_log.insert(f'{tab_char}重要作者 部分格式错误，有重要作者，用 A, 否则用 B 表示')
                    check_log += cur_log.text()
                    continue

                # 检测 用途 部分
                _use = use.split('、')
                if '' in _use:
                    error_flag = True
                    cur_log.insert(f'{tab_char}用途 有多余的中文顿号 或者 中文顿号结尾')
                    check_log += cur_log.text()
                    continue
                for cur_use in _use:
                    if re.match('[\u4e00-\u9fa5]+$', cur_use):
                        pass
                    else:
                        error_flag = True
                        cur_log.insert(f'{tab_char}用途 部分请使用中文表述')
                        check_log += cur_log.text()
                        continue

                # 检测 方法 部分
                _method = method.split('、')
                if '' in _method:
                    error_flag = True
                    cur_log.insert(f'{tab_char}方法 有多余的中文顿号 或者 中文顿号结尾')
                    check_log += cur_log.text()
                    continue
                for cur_method in _method:
                    if re.match('[\u4e00-\u9fa5]+$', cur_method):
                        pass
                    else:
                        error_flag = True
                        cur_log.insert(f'{tab_char}方法 部分请使用中文表述')
                        check_log += cur_log.text()
                        continue

                # 检测 刊物 部分
                if re.match('[a-z ]+$', publication):
                    pass
                else:
                    error_flag = True
                    cur_log.insert(f'{tab_char}期刊或会议 部分请使用英文小写')
                    check_log += cur_log.text()
                    continue

                # 检测 年份 部分
                try:
                    _ = int(year)
                    if len(year) != 2:
                        error_flag = True
                        cur_log.insert(f'{tab_char}年份 错误，请输入年份后两位，例如： 19')
                        check_log += cur_log.text()
                        continue
                except ValueError:
                    error_flag = True
                    cur_log.insert(f'{tab_char}年份 错误，请输入年份后两位，例如：19')
                    check_log += cur_log.text()
                    continue


        return check_log, error_flag

    def help_button_click():
        help_Dialog.show()


    ui.pushButton.clicked.connect(check_button_click)
    ui.pushButton_2.clicked.connect(help_button_click)

    # 显示
    MainWindow.show()
    sys.exit(app.exec_())