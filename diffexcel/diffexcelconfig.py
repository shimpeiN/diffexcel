#メッセージ定義
message_001 = "ファイルを選択してください"
message_002 = "ファイルが存在しません"
message_003 = "選択したファイルに同一シート名のシートが存在しません"
message_004 = "完了しました"
message_005 = "Excelファイルを選択してください"
message_006 = "選択したファイルに差分箇所はありませんでした"
message_007 = "比較対象シートを選択してください"
message_008 = "※全シート比較は同一シート名のシートが比較対象になります"
execel_extension = [".xls",".xlsx",".xlsm"]

#プログラム名
PROGRAM_NAME = 'DiffExcel'
FIRST_TEXTBOX_LABEL = '１番目のファイル'    #テキストボックス１ラベル（入力用ウインドウ）
SECOND_TEXTBOX_LABEL = '２番目のファイル'   #テキストボックス２ラベル（入力用ウインドウ）
RADIO_LABEL_ALL = "全シート比較"
RADIO_LABEL_SELECT = "シートを選択して比較"
NODIFF_MSGLABEL = "比較対象シート"
CELLADDR_COL = "セル番地"
SHEETNAME_COL = "シート名"
FILENAME_COL = "ファイル名"

ALLSHEET_MODE = 0
SELECTSHEET_MODE = 1

#入力用ウィンドウ
INPUTBOX_X = 500            #ウィンドウ幅（入力用ウインドウ）
INPUTBOX_Y = 200            #ウィンドウ高さ（入力用ウインドウ）
INPUTBOX_MINIMUM_X = 500    #ウィンドウ最小幅（入力用ウインドウ）
TEXTBOX_WIDTH = 55          #テキストボックスサイズ（入力用ウインドウ）
RADIO_PAD_X = 15            #ラジオパディング（入力用ウインドウ）
INPUTDLG_MSG_PADX = 10      #メッセージ用ラベルパディングX（入力用ウインドウ）
INPUTDLG_MSG_PADY = 10      #メッセージ用ラベルパディングX（入力用ウインドウ）
INPUTDLG_TEXTFRAME_PADX = 8   #テキストボックス用フレームパディングX（入力用ウインドウ）
INPUTTEXT_LABEL_PAD_X = 5   #テキストボックス用ラベルパディングX（入力用ウインドウ）
INPUTTEXT_TEXT_PAD_X = 5    #テキストボックス用テキストボックスパディングX（入力用ウインドウ）
INPUTTEXT_COMBO_PAD_X = 15    #テキストボックス用コンボボックスパディングX（入力用ウインドウ）
INPUTBOX_PAD_X = 25         #ウィンドウ幅調整用（入力用ウインドウ）

#結果ビュアー
RESULTVIEW_X = 1200     #ウィンドウ幅（結果ビュアー）
RESULTVIEW_Y = 500      #ウィンドウ高さ（結果ビュアー）
INDEX_WIDTH = 45        #インデックス列幅（結果ビュアー）
VIEW_PAD_X = 45         #ウインドウ幅調整用（結果ビュアー）
VIEW_PAD_Y = 80         #ウインドウ高さ調整用（結果ビュアー）
ROW_HEIGHT = 18         #列高さ（結果ビュアー）
VIEW_COL_PAD = 15       #ヘッダーパディング（結果ビュアー）
VIEW_FONT_SIZE = 9      #フォントサイズ（結果ビュアー）

#メッセージウィンドウ
MSGDIALOG_X = 300           #ウィンドウ幅（メッセージウインドウ）
MSGDIALOG_Y = 120           #ウィンドウ高さ（メッセージウインドウ）
NODIFFMSGDIALOG_X = 500     #ウィンドウ幅（メッセージウインドウ）
MSGDLG_BUTTON_PADY = 25     #ボタンパディングY（メッセージウインドウ）
NODIFFMSGDIALOG_X = 400     #ウィンドウ幅（メッセージウインドウ）
NODIFFMSGDIALOG_Y = 170     #ウィンドウ高さ（メッセージウインドウ）
NODIFFMSGDLG_PADY = 15      #パディングY（メッセージウインドウ）