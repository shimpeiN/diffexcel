import tkinter
import tkinter.ttk as ttk
from tkinterdnd2 import *
import itertools
from tkinter import font
import unicodedata
import os
import diffexcelconfig as config

#入力用テキストボックスクラス
class InputTextBox:
    #コンストラクタ
    def __init__(self,frame,name):
        #ラベル定義
        self.lb = tkinter.Label(frame,text=name)
        self.lb.grid(row=0, column=0, padx=config.INPUTTEXT_LABEL_PAD_X, sticky=tkinter.W)
        #テキストボックス定義
        self.var = tkinter.StringVar(frame)
        self.txt = tkinter.Entry(frame,width=config.TEXTBOX_WIDTH, textvar=self.var)
        self.txt.grid(row=0, column=1, padx=config.INPUTTEXT_TEXT_PAD_X, sticky=tkinter.EW)
        frame.grid_columnconfigure(1, weight=1)
        #テキストボックスドロップ定義
        self.txt.drop_target_register(True,DND_FILES)
        self.txt.dnd_bind('<<Drop>>', self.drop)

    # ドロップイベント
    def drop(self,event):
        input_string = event.data
        #先頭末尾の{}を削除
        input_string=input_string.lstrip("{")
        input_string=input_string.rstrip("}")
        self.var.set(input_string)

#入力用コンボボックスボックスクラス
class InputConboBox:
    #コンストラクタ
    def __init__(self,frame,name,sheets):
        #スタイル設定
        self.style = ttk.Style()
        self.labelfont = font.Font(frame, family="Yu Gothic UI",size=config.VIEW_FONT_SIZE)
        #ラベル定義
        self.lb = tkinter.Label(frame,text=name,font=self.labelfont)
        self.lb.grid(row=0, column=0, padx=config.INPUTTEXT_LABEL_PAD_X, sticky=tkinter.W)
        #テキストボックス定義
        self.variable = tkinter.StringVar()
        self.combo=ttk.Combobox(frame,values=sheets,textvariable=self.variable,state="readonly")
        self.combo.grid(row=1, column=0, padx=config.INPUTTEXT_COMBO_PAD_X, sticky=tkinter.EW)
        frame.grid_columnconfigure(0, weight=1)

    def get_value(self):
        return self.combo.get()

class RadioButtonClass:
    #コンストラクタ
    def __init__(self, frame):
        # ラジオボタンの値
        self.radio_value = tkinter.IntVar(value = config.ALLSHEET_MODE) 

        # ラジオボタンの作成
        radio0 = tkinter.Radiobutton(frame, 
                           text = config.RADIO_LABEL_ALL,       # ラジオボタンの表示名
                           command = self.radio_click,          # クリックされたときに呼ばれるメソッド
                           variable = self.radio_value,         # 選択の状態を設定する
                           value = config.ALLSHEET_MODE         # ラジオボタンに割り付ける値の設定
                           )

        radio1 = tkinter.Radiobutton(frame, 
                           text = config.RADIO_LABEL_SELECT,    # ラジオボタンの表示名
                           command = self.radio_click,          # クリックされたときに呼ばれるメソッド
                           variable = self.radio_value,         # 選択の状態を設定する
                           value = config.SELECTSHEET_MODE      # ラジオボタンに割り付ける値の設定
                           )

        # 配置
        radio0.grid(row=0, column=0, padx=config.RADIO_PAD_X)
        radio1.grid(row=0, column=1, padx=config.RADIO_PAD_X)

        self.value = self.radio_value.get()

    def radio_click(self):
        # ラジオボタンの値を取得
        self.value = self.radio_value.get()

#入力用ウィンドウクラス
class InputFileDialog:
    #コンストラクタ
    def __init__(self, xsize, ysize, name):
        # Tkクラス生成
        self.root = TkinterDnD.Tk()
        # 画面サイズ
        self.root.geometry(str(xsize) + "x" + str(ysize))
        # 画面タイトル
        self.root.title(name)
        #ウインドウサイズ固定
        self.root.resizable(width=True, height=False)
        self.root.minsize(width=config.INPUTBOX_MINIMUM_X, height=ysize)
        
        #ラベル
        self.errlb = tkinter.Label(self.root,text="")
        self.errlb.pack(anchor=tkinter.W, padx=config.INPUTDLG_MSG_PADX, pady=config.INPUTDLG_MSG_PADY)
        #フレーム定義
        self.firstinputbox_frame = tkinter.Frame(self.root)
        self.firstinputbox_frame.pack(fill=tkinter.BOTH, expand=True, padx=config.INPUTDLG_TEXTFRAME_PADX)
        self.secondinputbox_frame = tkinter.Frame(self.root)
        self.secondinputbox_frame.pack(fill=tkinter.BOTH, expand=True, padx=config.INPUTDLG_TEXTFRAME_PADX)
        self.radiobutton_frame = tkinter.Frame(self.root)
        self.radiobutton_frame.pack(fill=tkinter.BOTH, expand=True, padx=config.INPUTDLG_TEXTFRAME_PADX)
        # ボタン作成
        self.btn = tkinter.Button(self.root, text='実行', command=self.btn_click)
        self.btn.pack(expand=True, anchor=tkinter.N)
        
        #テキストボックス１
        self.first_txtbox = InputTextBox(self.firstinputbox_frame, config.FIRST_TEXTBOX_LABEL)
        #テキストボックス２
        self.second_txtbox = InputTextBox(self.secondinputbox_frame, config.SECOND_TEXTBOX_LABEL)
        
        self.radiobox = RadioButtonClass(self.radiobutton_frame)
        self.selectedmode = self.radiobox.value

        #ファイルチェックフラグ
        self.fileflg = False

    # ボタンクリックイベント
    def btn_click(self):
        #メッセージ初期化
        self.display_errmessage("")

        #ファイルパス取得
        self.first_filepath = self.first_txtbox.txt.get()
        self.second_filepath = self.second_txtbox.txt.get()
        
        #拡張子取得
        self.first_extension=os.path.splitext(self.first_filepath)
        self.second_extension=os.path.splitext(self.second_filepath)


        #ファイルパスチェック
        if len(self.first_filepath) == 0 or len(self.second_filepath) == 0 :
            #メッセージ表示
            self.display_errmessage(config.message_001)
            #ファイルチェックフラグをFalse
            self.fileflg = False
            return
        
        #拡張子チェック
        if self.first_extension[1] not in config.execel_extension or self.second_extension[1] not in config.execel_extension:
            self.display_errmessage(config.message_005)
            #ファイルチェックフラグをFalse
            self.fileflg = False
            return

        #「/」を「\\」に置換
        self.first_filepath = '\\'.join(self.first_filepath.split('/'))
        self.second_filepath= '\\'.join(self.second_filepath.split('/'))
        
        #選択モード取得
        self.selectedmode = self.radiobox.value
        #ファイルチェックフラグをTrue
        self.fileflg = True
        #ウインドウを閉じる
        self.root.destroy()

    # ウィンドウ表示
    def display_dialog(self):
        self.root.mainloop()

     #ウインドウを閉じる
    def close_dialog(self):
        self.root.destroy()

    #メッセージラベル表示
    def display_errmessage(self, msg):
        self.errlb["text"] = msg

#シート入力用ウィンドウクラス
class InputSheetDialog:
    #コンストラクタ
    def __init__(self, xsize, ysize, name, first_filename, first_sheets, second_filename, second_sheets):
        # Tkクラス生成
        self.root = TkinterDnD.Tk()
        # 画面サイズ
        self.root.geometry(str(xsize) + "x" + str(ysize))
        # 画面タイトル
        self.root.title(name)
        #ウインドウサイズ固定
        self.root.resizable(width=True, height=False)
        self.root.minsize(width=config.INPUTBOX_MINIMUM_X, height=ysize)
        
        #ラベル
        self.errlb = tkinter.Label(self.root,text=config.message_007)
        self.errlb.pack(anchor=tkinter.W, padx=config.INPUTDLG_MSG_PADX, pady=config.INPUTDLG_MSG_PADY)
        #フレーム定義
        self.firstinputbox_frame = tkinter.Frame(self.root)
        self.firstinputbox_frame.pack(fill=tkinter.BOTH, expand=True, padx=config.INPUTDLG_TEXTFRAME_PADX)
        self.secondinputbox_frame = tkinter.Frame(self.root)
        self.secondinputbox_frame.pack(fill=tkinter.BOTH, expand=True, padx=config.INPUTDLG_TEXTFRAME_PADX)
       
        # ボタン作成
        self.btn = tkinter.Button(self.root, text='実行', command=self.btn_click)
        self.btn.pack(expand=True, anchor=tkinter.N)
        
        #コンボボックス１
        first_labelname = config.FIRST_TEXTBOX_LABEL + "：" + first_filename
        self.first_combobox = InputConboBox(self.firstinputbox_frame, first_labelname, first_sheets)
        #コンボボックス２
        second_labelname = config.SECOND_TEXTBOX_LABEL + "：" + second_filename
        self.second_combobox = InputConboBox(self.secondinputbox_frame, second_labelname, second_sheets)

        #ファイル名ラベルがウインドウサイズより大きくなった場合、ウインドウをリサイズ
        first_labelsize = self.first_combobox.labelfont.measure(first_labelname)
        second_labelsize = self.second_combobox.labelfont.measure(second_labelname)
        max_labelsize = first_labelsize if  first_labelsize > second_labelsize else second_labelsize
        if max_labelsize + 2 * config.INPUTTEXT_LABEL_PAD_X + config.INPUTBOX_PAD_X> xsize:
            # 画面サイズ
            self.root.geometry(str(max_labelsize + 2 * config.INPUTTEXT_LABEL_PAD_X + + config.INPUTBOX_PAD_X) + "x" + str(ysize))

        self.first_selectedsheet = ''
        self.second_selectedsheet = ''
        
        #ファイルチェックフラグ
        self.sheetchek = False

    # ボタンクリックイベント
    def btn_click(self):
        
        #シート名取得
        self.first_selectedsheet = self.first_combobox.get_value()
        self.second_selectedsheet = self.second_combobox.get_value()
        
        if len(self.first_selectedsheet) == 0 or len(self.second_selectedsheet) == 0:
             self.sheetchek = False
             return 

        #ファイルチェックフラグをTrue
        self.sheetchek = True
        #ウインドウを閉じる
        self.root.destroy()

    # ウィンドウ表示
    def display_dialog(self):
        self.root.mainloop()

     #ウインドウを閉じる
    def close_dialog(self):
        self.root.destroy()

    #メッセージラベル表示
    def display_errmessage(self, msg):
        self.errlb["text"] = msg

#メッセージウィンドウクラス
class MessageDialog:
    def __init__(self, xsize, ysize, name, msg):
        # Tkクラス生成
        self.root = TkinterDnD.Tk()
        # 画面サイズ
        self.root.geometry(str(xsize) + "x" + str(ysize))
        # 画面タイトル
        self.root.title(name)
        #ウインドウサイズ固定
        self.root.resizable(width=False, height=False)
        #フレーム定義
        self.frame = tkinter.Frame(self.root)
        self.frame.pack(fill=tkinter.BOTH, expand=True)

        #メッセージラベル
        self.lb = tkinter.Label(self.frame,text=msg)
        #self.lb.place(x=25, y=35)
        self.lb.pack(pady=config.MSGDLG_BUTTON_PADY)

        # ボタン作成
        self.btn = tkinter.Button(self.frame, text='閉じる', command=self.btn_click)
        #self.btn.place(x=120, y=80)
        self.btn.pack(anchor=tkinter.CENTER)

        self.root.mainloop()

    # ボタンクリックイベント
    def btn_click(self):
        #ウインドウを閉じる
        self.root.destroy()

#差分なしメッセージウィンドウクラス
class NoDiffMessageDialog:
    def __init__(self, xsize, ysize, name, msg1,msg2, sheetlist ):
        # Tkクラス生成
        self.root = TkinterDnD.Tk()
        # 画面サイズ
        self.root.geometry(str(xsize) + "x" + str(ysize))
        # 画面タイトル
        self.root.title(name)
        #ウインドウサイズ固定
        self.root.resizable(width=True, height=False)
        
        #メッセージラベル
        self.msglb1 = tkinter.Label(self.root,text=msg1)
        self.msglb1.pack(anchor=tkinter.W, padx= config.INPUTTEXT_COMBO_PAD_X, pady=config.NODIFFMSGDLG_PADY)
        #メッセージラベル
        self.msglb2 = tkinter.Label(self.root,text=msg2)
        self.msglb2.pack(anchor=tkinter.W, padx= config.INPUTTEXT_COMBO_PAD_X)
        #フレーム定義
        self.frame = tkinter.Frame(self.root)
        self.frame.pack(fill=tkinter.BOTH, expand=True, pady=config.NODIFFMSGDLG_PADY)

        self.lb = tkinter.Label(self.frame,text=config.NODIFF_MSGLABEL)
        self.lb.grid(row=0, column=0, padx=config.INPUTTEXT_COMBO_PAD_X, sticky=tkinter.W)
        self.variable = tkinter.StringVar()
        self.combo=ttk.Combobox(self.frame,values=sheetlist,textvariable=self.variable,state="readonly")
        self.combo.grid(row=0, column=1, padx=config.INPUTTEXT_TEXT_PAD_X, sticky=tkinter.EW)
        self.frame.grid_columnconfigure(1, weight=1)
        self.combo.set(sheetlist[0])
    
        # ボタン作成
        self.btn = tkinter.Button(self.root, text='閉じる', command=self.btn_click)
        #self.btn.place(x=120, y=80)
        #self.btn.grid(row=2,column=0,columnspan=2, pady=10)
        self.btn.pack(expand=True, anchor=tkinter.N)

        self.root.mainloop()

    # ボタンクリックイベント
    def btn_click(self):
        #ウインドウを閉じる
        self.root.destroy()

class ResultViewer:
    def __init__(self, xsize, ysize, name):
        #ウインドウサイズ
        self.xsize=xsize
        self.ysize=ysize
        # Tkクラス生成
        self.root = TkinterDnD.Tk()
        # 画面サイズ
        self.root.geometry(str(self.xsize) + "x" + str(self.ysize))
        # 画面タイトル
        self.root.title(name)

        # widget配置のフレームを作成
        self.frame = tkinter.Frame(self.root)
        self.frame.pack(fill=tkinter.BOTH, expand=True, padx=5, pady=5)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        #スタイル設定
        self.style = ttk.Style()
        self.headdingfont = font.Font(self.root, family="Yu Gothic UI",size=config.VIEW_FONT_SIZE)
        self.style.configure("Treeview.Heading", font=self.headdingfont)
        self.style.configure("Treeview", font=self.headdingfont)
        # CSVファイルの内容を表示するTreeviewを作成
        self.tree = ttk.Treeview(self.frame)
        self.tree.column('#0', width=config.INDEX_WIDTH, stretch=tkinter.NO, anchor=tkinter.E)
        self.tree.heading('#0', text='\n\n')
        self.tree.grid(row=0, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

        # X軸スクロールバー
        hscrollbar = tkinter.Scrollbar(self.frame, orient=tkinter.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=lambda f, l: hscrollbar.set(f, l))
        hscrollbar.grid(row=1, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

        # Y軸スクロールバー
        vscrollbar = tkinter.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vscrollbar.set)
        vscrollbar.grid(row=0, column=1, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

    #結果表示
    def show_result(self , data):

        # 列番号をTreeviewに追加する
        self.tree['column'] = data[0]

        #背景色設定
        self.tree.tag_configure("even", background="LightCyan") 

        # 列のヘッダーを更新する
        headertotal = 0
        for i in range(len(data[0])):
            
            #改行削除して、カラムサイズ取得
            col_width = self.headdingfont.measure(max(data[0][i].split('\n'), key=lambda x:self.len_count(str(x))))
            col_width = col_width + config.VIEW_COL_PAD
            self.tree.column(data[0][i], width=col_width, anchor=tkinter.E)
            self.tree.heading(data[0][i], text=data[0][i])
            header_width = self.tree.column(self.tree['columns'][i], width=None)

            rows = [x[i] for x in data]
            #改行含む場合、改行区切りで最大長を取得
            for j, row in enumerate(rows):
                #rows[j] = max(str(row).split("\n") ,key=lambda x:self.len_count(str(x)))
                rows[j] = max(str(row).split("\n") ,key=lambda x:self.headdingfont.measure(str(x)))
            #最大長セルを取得
            #max_str = max(rows, key=lambda x:self.len_count(str(x)))
            max_str = max(rows, key=lambda x:self.headdingfont.measure(str(x)))
            #最大長セルとカラムのサイズ比較し、入れ替え
            max_width = self.headdingfont.measure(max_str) + config.VIEW_COL_PAD
            if max_width > header_width:
                self.tree.column(self.tree['columns'][i], width=max_width)
                headertotal = max_width + headertotal
            else:
                headertotal = header_width + headertotal


        #平坦化
        cells = [s for s in itertools.chain.from_iterable(data[1:]) if type(s) is str]
        #改行最も多い要素を取り出し
        longest_cell = max(cells, key=lambda x:0 if x is None else x.count("\n"))
        #改行分列高さを調整
        max_row_lines = longest_cell.count("\n") + 1
        self.style.configure("Treeview", rowheight = config.ROW_HEIGHT * max_row_lines)
        
        # 行番号及びCSVの内容を表示する
        rowstotal = 0
        for i, row in enumerate(data[1:]):          
            #列高さをリスト化
            if rowstotal < self.ysize:
                rowstotal = rowstotal + max_row_lines * config.ROW_HEIGHT  
            view_tags = [] 
            if i % 2 == 0:
                view_tags.append("even")
            self.tree.insert('', 'end', text=i+1, values=row, tags=view_tags)
        
        #ウインドウサイズ調整
        view_xsize = self.xsize if headertotal + config.INDEX_WIDTH + config.VIEW_PAD_X > self.xsize else headertotal + config.INDEX_WIDTH + config.VIEW_PAD_X 
        view_ysize = rowstotal + config.VIEW_PAD_Y 
        self.root.geometry(str(view_xsize) + "x" + str(view_ysize))

    #ウインドウ表示
    def show_dialog(self):
        self.root.mainloop()
    
    #文字列カウント（全角２カウント：半角１カウント）
    def len_count(self,text):
        count = 0
        for c in text:
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 2
            else:
                count += 1
        return count


        
        
