import dialogclass as dlog
import diffexcelproc as dex
import sys
import diffexcelconfig as config



if __name__ == "__main__":
    #ウインドウダイアログ初期化
    fileinputdialog = dlog.InputFileDialog(config.INPUTBOX_X, config.INPUTBOX_Y, config.PROGRAM_NAME)
    #ウインドウ表示
    fileinputdialog.display_dialog()

    if fileinputdialog.fileflg:
        #ファイルフラグTrueの場合
        #Excel差分比較処理系クラス初期化
        diffexcel = dex.DiffExcelProc(fileinputdialog.first_filepath, fileinputdialog.second_filepath)
        file_check = diffexcel.get_file_data()
    else:
        #ファイルフラグFalseの場合、プログラム終了(「×」押下時対応)
        sys.exit(0)

    #全シート比較モード
    if file_check and fileinputdialog.selectedmode == config.ALLSHEET_MODE:
        #ファイル存在フラグTrueの場合
        if diffexcel.get_sheet_name():
            #同一シート名シート存在フラグtrueの場合
            #差分抽出処理
            if diffexcel.output_diff(config.ALLSHEET_MODE) != 0:
                #差分結果有りの場合、結果ビュアー表示
                csvview = dlog.ResultViewer(config.RESULTVIEW_X, config.RESULTVIEW_Y, config.PROGRAM_NAME)
                csvview.show_result(diffexcel.diff_list)
                csvview.show_dialog()
                sys.exit(0)
            else:
                #差分結果無しの場合、メッセージ表示
                msgdialog = dlog.NoDiffMessageDialog( config.NODIFFMSGDIALOG_X, config.NODIFFMSGDIALOG_Y, config.PROGRAM_NAME, config.message_006, config.message_008, diffexcel.sheet_names)
                sys.exit(0)
        else:
            #同一シート名シート存在フラグFalse
            #エラーメッセージ表示し、プログラム終了
            msgdialog = dlog.MessageDialog(config.MSGDIALOG_X,config.MSGDIALOG_Y,config.PROGRAM_NAME, config.message_003)
            sys.exit(0)
    #シート選択比較モード
    elif file_check and fileinputdialog.selectedmode == config.SELECTSHEET_MODE:
        #シート選択ダイアログを表示
        sheetinputdialog = dlog.InputSheetDialog(config.INPUTBOX_X, config.INPUTBOX_Y, config.PROGRAM_NAME, diffexcel.first_filename,diffexcel.first_sheetnames, diffexcel.second_filename,diffexcel.second_sheetnames)
        sheetinputdialog.display_dialog()
        #シート選択有りの場合、比較処理
        if sheetinputdialog.sheetchek:
            #差分抽出処理
            if diffexcel.output_diff(config.SELECTSHEET_MODE , sheetinputdialog.first_selectedsheet, sheetinputdialog.second_selectedsheet) != 0:
                #差分結果有りの場合、結果ビュアー表示
                csvview = dlog.ResultViewer(config.RESULTVIEW_X, config.RESULTVIEW_Y, config.PROGRAM_NAME)
                csvview.show_result(diffexcel.diff_list)
                csvview.show_dialog()
                sys.exit(0)
            else:
                #差分結果無しの場合、メッセージ表示
                msgdialog = dlog.MessageDialog(config.MSGDIALOG_X,config.MSGDIALOG_Y,config.PROGRAM_NAME, config.message_006)
                sys.exit(0)
        #シート選択無しの場合、処理終了（×押下対応）
        else:
            sys.exit(0)
    else:
        #ファイル存在フラグFalseの場合
        #エラーメッセージ表示し、プログラム終了
        msgdialog = dlog.MessageDialog(config.MSGDIALOG_X,config.MSGDIALOG_Y, config.PROGRAM_NAME,config.message_002)
        sys.exit(0)



