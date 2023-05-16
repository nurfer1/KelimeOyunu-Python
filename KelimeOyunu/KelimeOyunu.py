import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.messagebox as msgbox
from random import choice
from os.path import isfile, dirname, realpath, basename
from threading import Thread


class playerName(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.title("Lütfen İsminizi Girin!")

        # İsminizi giriniz etiketi
        self.static_label = tk.Label(self, text="İsminizi giriniz!", font=("Verdana", 25))
        self.static_label.pack()

        # İsim giriş kutusu
        self.entered_name = tk.StringVar()
        self.name_entry = tk.Entry(self, font=("Verdana", 25), textvariable=self.entered_name, width=25)
        self.name_entry.pack()
        self.name_entry.focus()

        # Onayla düğmesi
        self.confirm_button = tk.Button(self, text="Onayla", command=self.confirm_name, font=("Verdana", 25))
        self.confirm_button.pack()

        # Puan tablosu düğmesi
        self.score_button = tk.Button(self, text="Puan Tablosu", command=self.score_list, font=("Verdana", 20))
        self.score_button.pack()

        # İsim değişkeni ve diğer özellikler
        self.name = ""
        self.max_character = 20
        self.allowed_characters = [
            "A","B","C","Ç","D","E","F","G","Ğ","H","I","İ","J","K","L","M","N","O","Ö","P","R","S","Ş","T","U","Ü","V","Y","Z",
            "a","b","c","ç","d","e","f","g","ğ","h","ı","i","j","k","l","m","n","o","ö","p","r","s","ş","t","u","ü","v","y","z"," "
        ]

        # İsim giriş kutusunda karakter sayısını kontrol etmek için izleme işlevi
        self.entered_name.trace("w", self.character_count_control)

        # Çıkış düğmesine basıldığında oyunu kapat
        self.protocol("WM_DELETE_WINDOW", self.exit_game)
    
    # Karakter sayısını kontrol eden işlev
    def character_count_control(self, *args):
        if len(self.entered_name.get()) != 0:
             # İsim, maksimum karakter sayısını aştığında gereksiz karakterleri kaldır
            if len(self.entered_name.get()) > self.max_character:
                self.entered_name.set(self.entered_name.get()[:-1])
            
            if not (self.entered_name.get()[-1] in self.allowed_characters):
                self.entered_name.set(self.entered_name.get()[:-1])

    def confirm_name(self, *args):
        if len(self.entered_name.get()) < 3:
            msgbox.showerror("Hata","İsimdeki karakter sayısı en az 3 olmalı.")
            return None
        for i in self.entered_name.get():
            if not (i in self.allowed_characters):
                msgbox.showerror("Hata","Geçersiz karakter girdiniz.\nLütfen türkçe karakterler kullanın")
                self.entered_name.set("")
                return None
        if len(self.entered_name.get()) > self.max_character:
            msgbox.showerror("Hata","İsim çok uzun.")
            self.entered_name.set("")
            return None
        self.name = self.entered_name.get()
        self.destroy()
     # Puan tablosunu gösteren işlev
    def score_list(self, *args):
        if args == ():
            if not isfile("puanlar.txt"):
                with open("puanlar.txt","w",encoding="utf-8") as f:
                    f.write("İsim,Puan,Kalan Süre,Soru Paketi\n")
            
        show_score = scoreBoard()
        show_score.focus_force()
        show_score.mainloop()
    # Oyundan çıkış işlevi    
    def exit_game(self):
        raise SystemExit

import tkinter as tk
from threading import Thread

class kelimeOyunu(tk.Tk):
    def __init__(self, name):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.title("Kelime Oyunu")
        self.bind("<Return>", self.benjamin_fonksiyon)
        self.bind("<space>", lambda *args: Thread(target=self.give_letter).start())
        self.bind("<Control-n>", self.new_questions)
        self.bind("<Control-p>", self.game_end)

        # Soru etiketi
        self.question_label = tk.Message(self, text="Soru", font=("Verdana", 15), width=600)
        self.question_label.grid(row=0, column=0, columnspan=3, sticky="we")

        # Kelime etiketi
        self.word_label = tk.Label(self, text="KELİME", font=("Times", 35), width=13)
        self.word_label.grid(row=1, column=0, columnspan=2, rowspan=2)

        # Kalan süre etiketi
        self.time_label_static = tk.Label(self, text="Kalan Süre", font=("Verdana", 14))
        self.time_label_static.grid(row=1, column=2)

        # Kalan süre label
        self.time_label = tk.Label(self, text=" ", font=("Verdana", 25))
        self.time_label.grid(row=2, column=2)

        # Harf alayım düğmesi
        self.letter_request_button = tk.Button(self, text="Harf Alayım", command=lambda: Thread(target=self.give_letter).start(), state="disabled", font=("Verdana", 25))
        self.letter_request_button.grid(row=3, column=0, columnspan=2, sticky="we")

        # Başla düğmesi
        self.benjamin_button = tk.Button(self, text="Başla", command=self.benjamin_fonksiyon, font=("Verdana", 25), width=13)
        self.benjamin_button.grid(row=3, column=2)

        # Cevap giriş kutusu
        self.guess_text = tk.Entry(self, state="disabled", font=("Verdana", 25))
        self.guess_text.grid(row=4, column=0, rowspan=2, sticky="we")

        # Cevap düğmesi
        self.guess_button = tk.Button(self, text="Cevap Ver", command=self.benjamin_fonksiyon, state="disabled", bg="green", fg="white", font=("Verdana", 25))
        self.guess_button.grid(row=4, column=1, rowspan=2, sticky="we")

        # Düşünme süresi etiketi
        self.think_time_label_static = tk.Label(self, text=" ", font=("Verdana", 14))
        self.think_time_label_static.grid(row=4, column=2)

        # Düşünme süresi label
        self.think_time_label = tk.Label(self, text=" ", font=("Verdana", 25))
        self.think_time_label.grid(row=5, column=2)

        # Puan etiketi
        self.score_label = tk.Label(self, text="Puan: 0", font=("Verdana", 25))
        self.score_label.grid(row=6, column=0, columnspan=3)

        # Oyunu kapatma işlev
        self.protocol("WM_DELETE_WINDOW", self.exit_game)
        self.animated_letters = "ASHYTUCOZK"

        self.player_name = name
        self.game_resume = False
        self.stop = True
        self.give_letter_and_benjamin_function_locked = False
        self.useless_locked = False
        self.special_situation = False
        self.ara = True
        self.total_second = 240
        self.remaining_time = 0
        self.elapsed_time = 0
        self.question_number = 0
        self.score = 0
        self.correct_answer = " "
        self.letters_received = []   #alınan harfler
        self.back_count(self.total_second)
        self.focus_force()
        if not isfile("veri"):
            with open("veri","w",encoding="utf-8") as f:
                pass
            self.last_file = ''
            self.new_questions()
        else:
            with open("veri",encoding="utf-8") as f:
                self.last_file = f.read()
            try:
                with open(self.last_file,encoding="utf-8") as f:
                    self.questions = f.readlines()
                    if self.file_verify():
                        msgbox.showerror("Hata","Seçilen soru dosyasının formatı uygun değil")
                        self.new_questions()
            except FileNotFoundError:
                msgbox.showerror("Hata","Süreler yüklenirken beklenmedik bir hata oluştu")
                self.last_file = ''
                self.new_questions()

    def back_count(self, local_remaining_time = None):
        if local_remaining_time is not None:
            self.remaining_time = local_remaining_time
        
        if self.special_situation:
            # Özel durum varsa (ör. süre dolduysa), oyunu sonlandır
            self.special_situation = False
            self.game_end()
        
        if self.remaining_time <= 0:
             # Süre dolduysa
            self.time_label.configure(text="Zaman doldu!")
            self.time_stop("Süre Bitti")
        else:
            # Süre hala dolmadıysa
            self.time_label.configure(text="{dk}:{sn:02d}".format(dk=(int(self.remaining_time//60)), sn=(int(self.remaining_time%60))))
            self.remaining_time -= 0.1
            if not self.stop:
                # Oyun durmamışsa, 0.1 saniye sonra geri sayımı güncelle
                self.after(100, self.back_count)

    def forward_count(self, bastan_basla=False):
        if self.ara:
            # Ara durumdaysa fonksiyondan çık
            return None

        if bastan_basla:
            # Başa dönme durumu ise, geçen süreyi sıfırla ve düşünme süresi etiketini başlangıç haline getir
            self.elapsed_time = 0
            self.think_time_label.configure(fg="black")
            self.think_time_label_static.configure(text="Düşünme Süresi")

        if self.elapsed_time >= 10:
            # Geçen süre 10 saniyeyi aştıysa düşünme süresi etiketinin rengini kırmızı yap
            self.think_time_label.configure(fg="red")

        if self.elapsed_time >= 20:
            # Geçen süre 20 saniyeyi aştıysa yanlış cevap işlemlerini yap ve fonksiyondan çık
            self.not_correct()
            return None

        self.think_time_label.configure(text="{0}".format(int(self.elapsed_time)))
        self.elapsed_time += 0.1
        if self.stop:
            # Oyun durmamışsa, 0.1 saniye sonra ileri sayımı güncelle
            self.after(100, self.forward_count)


    def time_stop(self, neden = "Yeni Soru"):
        self.stop = True
        self.ara = False
        self.forward_count(True)
        self.benjamin_button.configure(text=neden, state="disabled")
        self.guess_text.configure(state="normal")
        self.guess_text.focus()
        self.guess_button.configure(state="normal")
        self.letter_request_button.configure(state="disabled")
        self.score_label['text'] += " ({0})".format(list(self.word_label['text']).count("•") * 100)

    def benjamin_fonksiyon(self, *args):
        if self.give_letter_and_benjamin_function_locked:
            return None
        else:
            self.game_resume = True
            if self.benjamin_button['state'] == 'normal':
                if self.stop:
                    self.stop = False
                    self.back_count()
                    self.benjamin_button.configure(text="Durdur")
                    self.letter_request_button.configure(state="normal")
                    self.letters_received = []
                    self.question_label.configure(text=str(self.question_number+1) + ". " + self.questions[(self.question_number*2)][:-1])
                    self.correct_answer = self.questions[((self.question_number*2)+1)][:-1]
                    self.word_label.configure(text="•"*len(self.correct_answer))
                    self.question_number += 1
                else:
                    if self.question_number == 14:
                        self.time_stop("Son Soru")
                    else:
                        self.time_stop()
            elif self.benjamin_button['state'] == 'disabled':
                if self.guess_text.get().replace("i","İ").upper() == self.correct_answer:
                    self.guess_text.delete(0, "end")
                    self.correct()
                else:
                    self.guess_text.delete(0, "end")
                    def useless():
                        if self.useless_locked:
                            return None
                        else:
                            self.useless_locked = True
                            for _ in range(2):
                                self.guess_text.configure(background="red")
                                self.guess_text.update_idletasks()
                                self.after(100)
                                self.guess_text.configure(background="white")
                                self.guess_text.update_idletasks()
                                self.after(100)
                            self.useless_locked = False
                    Thread(target=useless).start()

    def give_letter(self, *args):  #HARF VER
        if self.give_letter_and_benjamin_function_locked:
            return None
        else:
            if self.letter_request_button['state'] == 'normal':
                self.give_letter_and_benjamin_function_locked = True
                gerekList = []
                for indx, letter in enumerate(self.word_label['text']):
                    if letter == "•":
                        gerekList.append(indx)
                letter_received = choice(gerekList)
                self.letters_received.append(letter_received) #ALINAN HARFLERE ALINAN HARFİ EKLEME
                for i in self.animated_letters:
                    memory = list(self.word_label['text'])
                    memory[letter_received] = i
                    memory = ''.join(memory)
                    self.word_label.configure(text=memory)
                    self.word_label.update_idletasks()
                    self.after(100)
                memory = list(self.word_label['text'])
                memory[letter_received] = self.correct_answer[letter_received]
                memory = ''.join(memory)
                self.word_label.configure(text=memory)
                if memory == self.correct_answer:
                    self.stop = True
                    if self.remaining_time > 0 and self.question_number != 14:
                        self.benjamin_button.configure(text="Yeni Soru", state="normal")
                        self.letter_request_button.configure(state="disabled")
                    elif self.question_number == 14:
                        self.benjamin_button.configure(text="Soru Bitti", state="disabled")
                        self.letter_request_button.configure(state="disabled")
                        self.game_resume = False
                        self.special_situation = True
                self.give_letter_and_benjamin_function_locked = False
            elif self.letter_request_button['state'] == 'disabled':
                return None

    def correct(self, situation = True):
        if self.remaining_time > 0 and self.question_number != 14:
            self.benjamin_button.configure(state="normal")
        self.guess_text.configure(state="disabled")
        self.guess_button.configure(state="disabled")
        if situation: #durum
            self.score += list(self.word_label['text']).count("•") * 100
        else:
            self.score -= list(self.word_label['text']).count("•") * 100
        self.ara = True
        memory = list(self.word_label['text'])
        gerekList = []
        for indx, letter in enumerate(memory):
            if letter == "•":
                gerekList.append(indx)
        for j in self.animated_letters:
            memory = list(self.word_label['text'])
            for i in gerekList:
                memory[i] = j
            memory = ''.join(memory)
            self.word_label.configure(text=memory)
            self.word_label.update_idletasks()
            self.after(100)
        self.word_label.configure(text=self.correct_answer)
        self.score_label.configure(text="Puan: {0}".format(self.score))
        self.think_time_label.configure(text=" ")
        self.think_time_label_static.configure(text=" ")
        if self.benjamin_button['state'] == 'disabled':
            self.game_resume = False
            self.game_end()

    def not_correct(self):
        self.correct(False)
    
    def file_verify(self):
        return len(self.questions) != 29 or self.questions[-1] != "SORU DOSYASI"

    def new_questions(self, *args):
        if not self.game_resume:
            file_path = dirname(realpath(__file__))
            new_file = fdialog.askopenfilename(filetypes=[("Soru Dosyaları","*.soru")], initialdir=file_path, title="Soru dosyası seç...")
            if new_file == '':
                if self.last_file == '':
                    msgbox.showerror("Hata","Sorular yüklenirken beklenmedik hata oluştu")
                    raise SystemExit
                return None
            self.last_file = new_file
            with open(self.last_file,encoding="utf-8") as f:
                self.questions = f.readlines()
            if self.file_verify():
                msgbox.showerror("Hata","Soru dosyası formatı uygun değil")
                raise SystemExit
            with open("veri", "w", encoding="utf-8") as f:
                f.write(self.last_file)
            self.stop = True
            self.ara = True
            self.elapsed_time = 0
            self.question_number = 0
            self.score = 0
            self.correct_answer = " "
            self.letters_received = []              #alınan harfler
            self.question_label.configure(text="Soru")
            self.word_label.configure(text="KELİME")
            self.think_time_label.configure(text=" ")  #düşünme süresi
            self.think_time_label_static.configure(text=" ")
            self.score_label.configure(text="Puan: 0")
            self.letter_request_button.configure(state="disabled")  #harf alayım butonu
            self.guess_text.configure(state="disabled")   #tahmin girişi
            self.guess_button.configure(state="disabled") #tahmin butonu
            self.benjamin_button.configure(state="normal", text="Başla")
            self.back_count(self.total_second) #geriye sayma
        else:
            msgbox.showerror("Hata","Oyun devam ederken soru paketi açılamaz")

    def exit_game(self):
        if self.game_resume:
            msgbox.showerror("Hata","Oyun hala devam ediyor!")
        else:
            raise SystemExit

    def game_end(self, *args):
        if args == ():
            if not isfile("puanlar.txt"):
                with open("puanlar.txt","w",encoding="utf-8") as f:
                    f.write("İsim,Puan,Kalan Süre,Soru Paketi\n")
            
            with open("puanlar.txt","a",encoding="utf-8") as f:
                f.write("{isim},{puan},{sure},{dosya}\n".format(isim=self.player_name, puan=self.score, sure=int(self.remaining_time), dosya=basename(self.last_file)))
        
        show_score = scoreBoard()
        show_score.focus_force()
        show_score.mainloop()

##puanTablosu
class scoreBoard(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.title("Puan Tablosu")
        self.bind("<Return>", lambda x: self.destroy())
        self.title_label = tk.Label(self, text="Puan Tablosu", font=("Verdana ",25))
        self.label_list = []
        self.column_label1 = tk.Label(self, text="İsim", font=("Verdana ",14))
        self.column_label2 = tk.Label(self, text="Puan", font=("Verdana ",14))
        self.column_label3 = tk.Label(self, text="Kalan Süre", font=("Verdana ",14))
        for i in range(30):
            self.label_list.append(tk.Label(self, text="", font=("Verdana ",14)))
        self.close_button = tk.Button(self, text="Kapat", command=self.destroy)
        self.title_label.grid(row=0, column=0, columnspan=3)
        self.column_label1.grid(row=1, column=0, sticky="w")
        self.column_label2.grid(row=1, column=1, sticky="w")
        self.column_label3.grid(row=1, column=2, sticky="w")
        for i in range(10):
            self.label_list[i].grid(row=i+2,column=0, sticky="w")
        for i in range(10,20):
            self.label_list[i].grid(row=i-8,column=1, sticky="w")
        for i in range(20,30):
            self.label_list[i].grid(row=i-18,column=2, sticky="w")
        self.close_button.grid(row=12,column=0, columnspan=3)
        self.score_list = []
        self.score_load()
    
    def score_load(self):
        if isfile("puanlar.txt"):
            with open("puanlar.txt",encoding="utf-8") as f:
                self.score_list = f.readlines()
            del self.score_list[0]
            for i in range(len(self.score_list)):
                self.score_list[i] = self.score_list[i].split(",")
            self.score_list = sorted(sorted(self.score_list, key=lambda neslis: int(neslis[2]), reverse = True), key=lambda neslis: int(neslis[1]), reverse = True)
            for i in range(10):
                try:
                    self.label_list[i]['text'] = "{0}. {1}".format(i+1, self.score_list[i][0])
                except IndexError:
                    break
            for i in range(10,20):
                try:
                    self.label_list[i]['text'] = "{0}".format(self.score_list[i-10][1])
                except IndexError:
                    break
            for i in range(20,30):
                try:
                    self.label_list[i]['text'] = "{0} saniye".format(self.score_list[i-20][2])
                except IndexError:
                    break
        else:
            msgbox.showerror("Hata","Şimdilik puan alan olmamış :(")
            self.destroy()

if __name__ == "__main__":
    get_name = playerName()
    get_name.mainloop()
    game = kelimeOyunu(get_name.name)
    game.mainloop()
