from CTkMessagebox import CTkMessagebox
import customtkinter
from CTkListbox import *
from tkinter import ttk,IntVar
import string
from pass_module import Password
import sqlite3
import pyperclip
import qrcode
import matplotlib.pyplot as plt
import re

    
FONT_TYPE = "meiryo"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.fonts = (FONT_TYPE, 12)
        self.bold_fonts = (FONT_TYPE, 12, "bold")
        self.title("Pass&Go!")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_width = screen_width/2 - 650/2
        center_height = screen_height/2 - 470/2
        self.geometry(f"650x470+{int(center_width)}+{int(center_height)}")

        # ここから表示系
        self.tabview = customtkinter.CTkTabview(self,width=250,border_width=1, command= self.tab_click)
        self.tabview.grid(row=0,column=0, padx=18, pady=4, sticky="n",ipady = 0,rowspan = 2)
        gen_tab = self.tabview.add('Generate')
        regi_tab = self.tabview.add('Register')
        search_tab = self.tabview.add('Search')

        # 生成モード
        # サイト名入力
        self.label_site = customtkinter.CTkLabel(gen_tab, text='サイト名(必須)', font=self.fonts)
        self.label_site.grid(row=0,column=0, padx=15, pady=0, sticky="sw")
        self.sitename = customtkinter.CTkEntry(gen_tab, width=200, font=self.fonts)
        self.sitename.grid(row=1,column=0, padx=15, pady=0, sticky="n")

        # ユーザー名入力
        self.label_user = customtkinter.CTkLabel(gen_tab, text='\nユーザー名', font=self.fonts)
        self.label_user.grid(row=2,column=0, padx=15, pady=0, sticky="sw")
        self.username = customtkinter.CTkEntry(gen_tab, width=200, font=self.fonts)
        self.username.grid(row=3,column=0, padx=15, pady=0, sticky="n")

        # 記号入力
        self.label_kigou = customtkinter.CTkLabel(gen_tab, text='\n使用する記号', font=self.fonts)
        self.label_kigou.grid(row=4,column=0, padx=15, pady=0, sticky="w")
        self.kigou = customtkinter.CTkEntry(gen_tab, width=200, font=self.fonts,)
        self.kigou.grid(row=5,column=0, padx=15, pady=0, sticky="n")

        # 桁数入力
        self.label_len = customtkinter.CTkLabel(gen_tab, text='\n桁数(必須)',font=self.fonts)
        self.label_len.grid(row=6,column=0, padx=15, pady=0, sticky="w")
        validate_length = self.register(self.validate_length)
        self.length = customtkinter.CTkEntry(gen_tab, width=200,font=self.fonts, validate="key",validatecommand=(validate_length, "%P"))
        self.length.grid(row=7,column=0, padx=15, pady=0, sticky="n")

        # 生成ボタン
        self.gen_button = customtkinter.CTkButton(gen_tab, text="生成", command=self.gen_pass_command,font=self.bold_fonts, width=150)
        self.gen_button.grid(row=8, column=0, padx=0, pady=20, sticky="s")

        # 登録モード
        # サイト名入力
        self.regi_site_label = customtkinter.CTkLabel(regi_tab, text='サイト名(必須)', font=self.fonts)
        self.regi_site_label.grid(row=0,column=0, padx=15, pady=0, sticky="sw")
        self.regi_sitename = customtkinter.CTkEntry(regi_tab, width=200, font=self.fonts)
        self.regi_sitename.grid(row=1,column=0, padx=15, pady=0, sticky="n")

        # ユーザー名入力
        self.regi_user_label = customtkinter.CTkLabel(regi_tab, text='\nユーザー名', font=self.fonts)
        self.regi_user_label.grid(row=2,column=0, padx=15, pady=0, sticky="sw")
        self.regi_username = customtkinter.CTkEntry(regi_tab, width=200, font=self.fonts)
        self.regi_username.grid(row=3,column=0, padx=15, pady=0, sticky="n")

        # パスワード入力
        self.regi_pass_label = customtkinter.CTkLabel(regi_tab, text='\nパスワード(必須)', font=self.fonts)
        self.regi_pass_label.grid(row=4,column=0, padx=15, pady=0, sticky="w")
        validate_regi_pass = self.register(self.validate_regi_pass)
        self.regi_pass = customtkinter.CTkEntry(regi_tab, width=200, font=self.fonts, validate="key",validatecommand=(validate_regi_pass, "%P"))
        self.regi_pass.grid(row=5,column=0, padx=15, pady=0, sticky="n")

        # 登録ボタン
        self.regi_button = customtkinter.CTkButton(regi_tab, text="登録", command=self.regi_pass_command,font=self.bold_fonts, width=150)
        self.regi_button.grid(row=8, column=0, padx=0, pady=20, sticky="s")

        # 検索モード
        # サイト検索テキストボックス
        self.search_site_label = customtkinter.CTkLabel(search_tab, text='サイト名', font=self.fonts)
        self.search_site_label.grid(row=0,column=0, padx=15, pady=0, sticky="sw")
        self.search_site_entry = customtkinter.CTkEntry(search_tab, width=200, font=self.fonts)
        self.search_site_entry.grid(row=1,column=0, padx=15, pady=0, sticky="n")

        # ユーザー検索テキストボックス
        self.search_user_label = customtkinter.CTkLabel(search_tab, text='\nユーザー名', font=self.fonts)
        self.search_user_label.grid(row=2,column=0, padx=15, pady=0, sticky="sw")
        self.search_username_entry = customtkinter.CTkEntry(search_tab, width=200, font=self.fonts)
        self.search_username_entry.grid(row=3,column=0, padx=15, pady=0, sticky="n")

        # 検索ボタン
        self.search_button = customtkinter.CTkButton(search_tab, text="検索", command=self.show_view_command, font=self.bold_fonts, width=150)
        self.search_button.grid(row=4, column=0, padx=0, pady=20, sticky="s")

        # リスト表示
        self.show_db_command()

        # 抽出ボタン
        self.ext_button = customtkinter.CTkButton(self, text="コピー", command = self.ext_pass_command, font=self.bold_fonts, width=100)
        self.ext_button.grid(row=1, column=2, padx=7, pady=0, sticky="wn")

        # 削除ボタン
        self.del_button = customtkinter.CTkButton(self, text="削除", command=self.del_pass_command, font=self.bold_fonts, width=100)
        self.del_button.grid(row=1, column=2, padx=7, pady=0, sticky="n")

        # QRボタン
        self.del_button = customtkinter.CTkButton(self, text="QR", command=self.qr_command, font=self.bold_fonts, width=100)
        self.del_button.grid(row=1, column=2, padx=7, pady=0, sticky="en")
        

    # リストの枠表示
    def show_list(self):
        self.listbox = ttk.Treeview(self, columns=('サイト名','ユーザー名'), show="headings", selectmode='browse',height=15)
        style = ttk.Style()
        style.configure('Treeview.Heading',font = (FONT_TYPE,12))
        style.configure('Treeview',font = (FONT_TYPE,12),rowheight=30)
        self.listbox.tag_configure('oddrow', background='#EEE')
        self.listbox.column('サイト名',width=210,anchor = 'c')
        self.listbox.column('ユーザー名',width=210,anchor = 'c')
        self.listbox.heading("#0", text="ID")
        self.listbox.heading('サイト名', text='サイト名', command=self.sort_sitename_command) 
        self.listbox.heading('ユーザー名', text='ユーザー名', command=self.sort_username_command) 
        self.listbox.grid(row=0, column=2, padx=5,pady=29, sticky="n")

    # 生成関数呼び出しと規制
    def gen_pass_command(self):
        sitename = self.sitename.get()
        username = self.username.get()
        kigou = self.kigou.get()
        length = self.length.get()
        self.conn = sqlite3.connect('pass.db')
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT * FROM passwords')
        self.cur.execute('SELECT COUNT(*) FROM passwords WHERE site = ? AND username = ?',(sitename,username))
        count = self.cur.fetchone()[0]

        # 入力を消す用
        def delete_entry(self):
            self.sitename.delete(first_index=0,last_index=len(sitename))
            self.username.delete(first_index=0,last_index=len(username))
            self.kigou.delete(first_index=0,last_index=len(kigou))
            self.length.delete(first_index=0,last_index=len(length))

        # 入力規制と実行
        if not sitename and not length:
            CTkMessagebox(self, title='Error' ,message="サイト名と桁数を入力してください",
                  icon="cancel", option_1="閉じる",justify='center',wraplength=300, font=self.fonts)
        elif not sitename:
            CTkMessagebox(self, title='Error' ,message="サイト名を入力してください",
                  icon="cancel", option_1="閉じる",justify='center',wraplength=300, font=self.fonts)
        elif not length:
            CTkMessagebox(self, title='Error' ,message="桁数を入力してください",
                  icon="cancel", option_1="閉じる",justify='center',wraplength=300, font=self.fonts)
        elif not all(char in string.punctuation for char in kigou):
            CTkMessagebox(self, title='Error' ,message="記号のみを入力してください",
                icon="cancel", option_1="閉じる",justify='center',wraplength=300, font=self.fonts)
        elif int(length) < len(kigou):
            CTkMessagebox(self, title='Error' ,message="記号を桁数より少なくしてください",
                  icon="cancel", option_1="閉じる",justify='center',wraplength=300, font=self.fonts)
        elif count != 0:
            msg = CTkMessagebox(self, title='Overwrite' ,message=f"登録済みです\nサイト名:{sitename} \nユーザー名:{username}\n上書きしますか？",
                  icon="question", option_1="Yes",option_2="No",justify='center',wraplength=300, font=self.fonts)
            response = msg.get()
            if response=="Yes":
                pw = Password(site=sitename,username=username,length=int(length),kigou=kigou, responece=response)
                pw.gen_pass()
                msg = CTkMessagebox(self, title='Success' ,message="上書きしました\nパスワードをクリップボードにコピーしますか?",
                  icon="check", option_1="Yes",option_2="No",justify='center',wraplength=350, font=self.fonts) 
                response = msg.get() 
                if response == 'Yes':
                    pyperclip.copy(pw.return_pass())
                    delete_entry(self)
                else:
                    delete_entry(self)
                self.show_db_command()
                
        else:
            pw = Password(site=sitename,username=username,length=int(length),kigou=kigou)
            pw.gen_pass()
            msg = CTkMessagebox(self, title='Success' ,message="パスワードを生成しました\nパスワードをクリップボードにコピーしますか？",
                  icon="check", option_1="Yes",option_2="No", justify='center',wraplength=350, font=self.fonts)
            response = msg.get()
            if response == 'Yes':
                pyperclip.copy(pw.return_pass())
                delete_entry(self)
            else:
                delete_entry(self)
            self.show_db_command()


    def regi_pass_command(self):
        sitename = self.regi_sitename.get()
        username = self.regi_username.get()
        regi_pass = self.regi_pass.get()
        self.conn = sqlite3.connect('pass.db')
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT * FROM passwords')
        self.cur.execute('SELECT COUNT(*) FROM passwords WHERE site = ? AND username = ?',(sitename,username))
        count = self.cur.fetchone()[0]

        if not sitename and not regi_pass:
            CTkMessagebox(self, title='Error' ,message="サイト名とパスワードを入力してください",
                  icon="cancel", option_1="閉じる",justify='center',wraplength=300, font=self.fonts)
        elif not sitename:
            CTkMessagebox(self, title='Error' ,message="サイト名を入力してください",
                  icon="cancel", option_1="閉じる",justify='center',wraplength=300, font=self.fonts)
        elif not regi_pass:
            CTkMessagebox(self, title='Error' ,message="パスワードを入力してください",
                    icon="cancel", option_1="閉じる",justify='center',wraplength=300, font=self.fonts)
        elif count != 0:
            msg = CTkMessagebox(self, title='Overwrite' ,message=f"登録済みです\nサイト名:{sitename} \nユーザー名:{username}\n上書きしますか？",
                  icon="question", option_1="Yes",option_2="No",justify='center',wraplength=300, font=self.fonts)
            response = msg.get()
            if response=="Yes":
                pw = Password(site=sitename, username=username,regi_pass=regi_pass, responece=response)
                pw.register_pass()
                CTkMessagebox(self, title='Success' ,message="パスワードを登録しました",
                  icon="check", option_1="閉じる",justify='center',wraplength=350, font=self.fonts) 
                self.regi_sitename.delete(first_index=0,last_index=len(sitename))
                self.regi_username.delete(first_index=0,last_index=len(username))
                self.regi_pass.delete(first_index=0,last_index=len(regi_pass))
                self.show_db_command()
        else:
            pw = Password(site=sitename, username=username,regi_pass=regi_pass)
            pw.register_pass()
            msg = CTkMessagebox(self, title='Success' ,message="パスワードを登録しました",
                    icon="check", option_1="閉じる",justify='center',wraplength=300, font=self.fonts)
            response = msg.get()
            if response == '閉じる':
                self.regi_sitename.delete(first_index=0,last_index=len(sitename))
                self.regi_username.delete(first_index=0,last_index=len(username))
                self.regi_pass.delete(first_index=0,last_index=len(regi_pass))
            self.show_db_command()
            


    # データベース表示用
    def show_db_command(self):
        self.show_list()
        pw = Password()
        try:
            sites,usernames = pw.show_db()
        except TypeError:
            pass
        else:
            for self.index,(self.site,username) in enumerate(zip(sites,usernames)):
                if self.index %2:
                    self.listbox.insert(parent='', index='end',values=(self.site,username))
                else:
                    self.listbox.insert(parent='', index='end',values=(self.site,username),tags='oddrow')

    # ソート用
    def show_sort(self):
        self.show_list()
        pw = Password()
        sites,usernames = pw.show_sort()
        for self.index,(self.site,username) in enumerate(zip(sites,usernames)):
            if self.index %2:
                self.listbox.insert(parent='', index='end',values=(self.site,username))
            else:
                self.listbox.insert(parent='', index='end',values=(self.site,username),tags='oddrow')

    # サイト名でソート
    def sort_sitename_command(self):
        pw = Password()
        pw.sort_sitename()
        self.show_sort()

    # ユーザー名でソート
    def sort_username_command(self):
        pw = Password()
        pw.sort_username()
        self.show_sort()

    # リスト選択
    def _select_list(self):
        select_item = self.listbox.selection()
        for item in select_item:
            select_values = self.listbox.item(item, 'values')
            self.ext_sitename,self.ext_username = select_values
            return self.ext_sitename,self.ext_username
        
    # 抽出関数呼び出し  
    def ext_pass_command(self):
        # 選択した行を取得してext_passを実行する
        self._select_list()
        try:
            pw = Password(site=self.ext_sitename,username=self.ext_username)
            pw.ext_pass()
        except UnboundLocalError:
            pass
        except AttributeError:
            pass
        except TypeError:
            pass
        else:
            CTkMessagebox(self, title='Success' ,message="パスワードをクリップボードにコピーしました",
                  icon="check", option_1="閉じる",justify='center',wraplength=350, font=self.fonts)
            self.show_db_command()
            self.ext_sitename = None
            
            
    # 削除関数呼び出し
    def del_pass_command(self):
        try:
            self._select_list()
            pw = Password(site=self.ext_sitename,username=self.ext_username)
            if self.ext_sitename is None:
                raise UnboundLocalError
        except UnboundLocalError:
            pass
        except AttributeError:
            pass
        else:
            msg = CTkMessagebox(self, title='Delete' ,message=f"削除します\nサイト名:{self.ext_sitename} \nユーザー名:{self.ext_username}\n本当によろしいですか？",
                  icon="question", option_1="Yes",option_2="No",justify='center',wraplength=300, font=self.fonts)
            response = msg.get()
            if response=="Yes":
                pw.del_pass()
                CTkMessagebox(self, title='Success' ,message="削除しました",
                  icon="check", option_1="閉じる",justify='center',wraplength=350, font=self.fonts)
                self.show_db_command()
                self.ext_sitename = None

        # QR表示用
    def qr_command(self):
        self._select_list()
        try:
            pw = Password(site=self.ext_sitename,username=self.ext_username)
            pw.ext_pass()
        except UnboundLocalError:
            pass
        except AttributeError:
            pass
        except TypeError:
            pass
        else:
            e_pass = pw.ext_pass()
            e_pass_qr = qrcode.make(e_pass)
            plt.imshow(e_pass_qr, cmap='gray')
            plt.axis('off')
            plt.show()

    # サイト名とユーザー名で検索
    def search_site_user(self):
        sitename = self.search_site_entry.get()
        username = self.search_username_entry.get()
        pw = Password(site=sitename, username=username)
        pw.search_db_site_user()

    # 検索view表示用
    def show_view_command(self):
        self.search_site_user()
        self.show_list()
        pw = Password()
        # try:
        sites,usernames = pw.show_view()
        # except TypeError:
            # pass
        # else:
        for self.index,(self.site,username) in enumerate(zip(sites,usernames)):
            if self.index %2:
                self.listbox.insert(parent='', index='end',values=(self.site,username))
            else:
                self.listbox.insert(parent='', index='end',values=(self.site,username),tags='oddrow')
    
    # 桁数制限用
    def validate_length(self, text):
        return (text.isdigit() and len(text) <= 2 and text != '0') or text == ""
    
    # 既存パス制限用
    def validate_regi_pass(self, text):
        return (re.fullmatch(r'[a-zA-Z0-9!-/:-@[-`{-~]*', text) and len(text) <= 99) or text == ""
    
    # タブクリックしたときの表示切替用
    def tab_click(self):
        tab_name = self.tabview.get()
        sitename = self.sitename.get()
        username = self.username.get()
        kigou = self.kigou.get()
        length = self.length.get()
        search_site = self.search_site_entry.get()
        search_user = self.search_username_entry.get()

        if tab_name == 'Search':
            self.show_db_command()
            self.sitename.delete(first_index=0,last_index=len(sitename))
            self.username.delete(first_index=0,last_index=len(username))
            self.kigou.delete(first_index=0,last_index=len(kigou))
            self.length.delete(first_index=0,last_index=len(length))
            self.ext_sitename = None
        else:
            self.show_db_command()
            self.search_site_entry.delete(first_index=0,last_index=len(search_site))
            self.search_username_entry.delete(first_index=0,last_index=len(search_user))
            self.ext_sitename = None
    

app = App()
app.mainloop()