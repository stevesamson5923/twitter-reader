import tweepy
from tweepy import OAuthHandler
import webbrowser
import time
from tkinter import *
from PIL import ImageTk, Image
import PIL 
import urllib.request
from datetime import datetime
def authenticate():
    consumer_key = 'H5Jla4zoZcNLtDiuR125fgPhR'
    consumer_secret = 'HWSbxGzQYgEhwOigJCrggYWzuGRKNcBX93CPXiyxi9RYYVrBhc'
    callback_uri = 'oob'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    redirect_url = auth.get_authorization_url() 
    #webbrowser.open(redirect_url)
    #print(redirect_url)
    access_token = '493298328-xZkQxyCSr5QkHN8VbGwBaY2SAZNyyH3X3yFrmr6N'
    access_secret_token = '3cPqkMk12ixa6GAfSly6W6KwuYdK0Uapw2KDZVEmP0wSI'
    auth.set_access_token(access_token,access_secret_token)
    api = tweepy.API(auth)
    #me = api.me()
    return api

root = Tk()
root.title('Charts')
root.geometry('1000x600')
root.resizable(0,0)
#root.tk.call('encoding', 'system', 'unicode')
hover_bg = '#613504'
leave_bg = '#fca503'

leftframe = Frame(root,width=150,bg='#fca503')
leftframe.pack(side=LEFT,expand=0,fill=BOTH)
rightframe = Frame(root,width=550,bg=hover_bg)
rightframe.pack(side=LEFT,expand=1,fill=BOTH)

me=None
api=None
if me:
    #print(me.screen_name)
    pass
else:
    api = authenticate()
    me = api.me()

flag_pressed_follow = False
flag_pressed_read = False
#print('Welcome'+me.screen_name)

def unpack_others():
    for a in rightframe.winfo_children():
        a.destroy() 

def hover(id):
    if id == 1:
        following.configure(bg=hover_bg)
    elif id == 2:
        Read_tweet.configure(bg=hover_bg)
    elif id == 3:
        search_tweet.configure(bg=hover_bg)
    
def leave(id):
    if id == 1 and not flag_pressed_follow:
        following.configure(bg=leave_bg)
    elif id == 2 and not flag_pressed_read:
        Read_tweet.configure(bg=leave_bg)
    elif id == 3:
        search_tweet.configure(bg=leave_bg)

def download_image(URL,count):
    with urllib.request.urlopen(URL) as url:
        with open('friend_photo_'+str(count)+'.jpg', 'wb') as f:
            f.write(url.read())

def download_image_read_tweets(URL,count):
    with urllib.request.urlopen(URL) as url:
        with open('tweet_photo_'+str(count)+'.jpg', 'wb') as f:
            f.write(url.read())

def download_user_image(URL):
    with urllib.request.urlopen(URL) as url:
        with open('profile_photo.jpg', 'wb') as f:
            f.write(url.read())

def display_following():
    global friend_frame
    count=1
    friend_frame = Frame(rightframe,bg=hover_bg,width=550,height=450)  
    friend_frame.pack(side='top',expand=1,fill='both')
    for index,friend in enumerate(me.friends()):
        #print(friend.screen_name)
        #print(friend.profile_image_url)
        download_image(friend.profile_image_url,count)
        
        friend_name = Label(rightframe,text=friend.screen_name,bg=hover_bg,fg='#fff')
        img = PIL.Image.open('friend_photo_'+str(count)+'.jpg')
        img = ImageTk.PhotoImage(img)
        #img = img.subsample(6,6)
        #profile_photo = Label(rightframe,text='Image',image=img)  
        canvas = Canvas(friend_frame,width=48,height=48,bg=hover_bg)
        canvas.image = img
        canvas.create_image(0,0,anchor='nw',image=img)
    
        canvas.grid(row=index,column=0,padx=20)
        
        username = Label(friend_frame,text=friend.screen_name,bg=hover_bg,fg='#fff',font=('Lucida Console',16))
        username.grid(row=index,column=1,padx=20,sticky='E')
        
        follow_unfollow_but(index,friend.screen_name)
        count = count + 1
            
def refresh_list():
    global friend_frame
    for a in friend_frame.winfo_children():
        a.destroy()
    friend_frame.destroy()
    display_following()
            
def follow_unfollow(friend_screen_name):
    #for friend in me.friends():
    #if friend.screen_name == friend_screen_name:
    api.destroy_friendship(friend_screen_name)
    refresh_list()
        
def change_but_text_on_enter(follow_but):
    follow_but.configure(text='Unfollow')
    follow_but.configure(bg=leave_bg)

def change_but_text_on_leave(follow_but):
    follow_but.configure(text='Following')
    follow_but.configure(bg=hover_bg)
    
def follow_unfollow_but(index, friend_screen_name):
    global friend_frame
    follow_but = Button(friend_frame,text='Following',font=('Helvetica',16),
                        bg=hover_bg,bd=2,fg='#fff',relief=GROOVE,command=lambda :follow_unfollow(friend_screen_name))
    follow_but.bind('<Enter>',lambda x: change_but_text_on_enter(follow_but))
    follow_but.bind('<Leave>',lambda x: change_but_text_on_leave(follow_but))
    follow_but.grid(row=index,column=2,padx=20)
    
        
def show_following():
    global flag_pressed_read
    global flag_pressed_follow
    flag_pressed_follow=True
    flag_pressed_read=False
    Read_tweet.configure(bg=leave_bg)
    following.configure(bg=hover_bg)
    
    unpack_others()
    
    api = authenticate()
    me = api.me()
    
    user_frame = Frame(rightframe,width=550,bg=hover_bg)    
    username = Label(user_frame,text='Welcome '+me.screen_name,bg=hover_bg,fg='#fff',font=('Chiller',20))
    
    URL=me.profile_image_url
    download_user_image(URL)
    
    #photo1 = PhotoImage(file = 'profile_photo.jpg')
    #photoimage1 = photo1.subsample(1, 1)
    img = PIL.Image.open('profile_photo.jpg')
    img = ImageTk.PhotoImage(img)
    #img = img.subsample(6,6)
    #profile_photo = Label(rightframe,text='Image',image=img)  
    canvas = Canvas(user_frame,width=48,height=48,bg=hover_bg)
    canvas.image = img
    canvas.create_image(0,0,anchor='nw',image=img)
    
    #profile_photo.configure(image=photoimage1)
    #profile_photo.grid(row=0,column=0)
    user_frame.pack(side='top',expand=0,fill='x')
    canvas.pack(side='right',anchor='ne',padx=(5,15),pady=15)
    username.pack(side='right',anchor='ne',pady=25)

    refresh_img = PIL.Image.open('refresh.png')
    refresh_img = ImageTk.PhotoImage(refresh_img)
    refresh_canvas = Canvas(user_frame,width=24,height=24,bg=hover_bg)
    refresh_canvas.image = refresh_img
    #refresh_canvas.create_image(0,0,anchor='nw',image=refresh_img)
    #refresh_canvas.pack(side='left',padx=20)
    but = Button(user_frame,image=refresh_img,bg=hover_bg,relief=FLAT,command=refresh_list)
    but.pack(side='left',padx=25)
    display_following()


def remove_unwanted_char(msg):
    char_list = [msg[j] for j in range(len(msg)) if ord(msg[j]) in range(65536)]
    tweet=''
    for j in char_list:
        tweet=tweet+j
    return tweet

#like_image_list = {}

class tweet_box:
    def __init__(self,msg,count):
        self.msg = msg
        self.count = count
        self.l = LabelFrame(rightframe,text=msg.user.screen_name,width=400,
                       height=100,bg=hover_bg,fg='#fff',font=('Dosis',16,'bold'))
        self.profile_img = PIL.Image.open('tweet_photo_'+str(self.count)+'.jpg')
        self.profile_img = ImageTk.PhotoImage(self.profile_img)
        self.profile_img_canvas = Canvas(self.l,width=48,height=48,bg=hover_bg)
        self.profile_img_canvas.image = self.profile_img
        #profile_img_canvas.create_image(0,0,anchor='nw',image=profile_img)
        self.profile_img_label = Label(self.l,image=self.profile_img,bg=hover_bg,relief=FLAT)
        self.tweet_after_process = remove_unwanted_char(self.msg.text)
        self.tweet_msg = Label(self.l,text=self.tweet_after_process,bg=hover_bg,fg='#fff',font=('Dosis',12))
        
        self.check_like_retweet()
        self.display_comp()
    
    def check_like_retweet(self):
        if self.msg.favorited:
            #print(self.msg.id)
            #print('already favorite')
            self.no = 1 #1 means convert to dislike
            like_img = PIL.Image.open('like.png')
            like_img = ImageTk.PhotoImage(like_img)
            like_img_canvas =  Canvas(self.l,width=24,height=24,bg=hover_bg)
            like_img_canvas.image = like_img
            #like_img_canvas.create_image(0,0,anchor='nw',image=like_img)
            self.like_image_label = Label(self.l, image=like_img,bg=hover_bg) 
            self.like_image_label.bind('<Button-1>',lambda a:self.like_unlike(self.msg.id)) #1 means dislike
            #self.like_image_list[msg.id] = like_image_label
        else:
            #print(self.msg.id)
            #print('Not favorite')
            self.no = 0 #0 means convert to like
            like_img = PIL.Image.open('unlike.png')
            like_img = ImageTk.PhotoImage(like_img)
            like_img_canvas =  Canvas(self.l,width=24,height=24,bg=hover_bg)
            like_img_canvas.image = like_img
            #like_img_canvas.create_image(0,0,anchor='nw',image=like_img)
            self.like_image_label = Label(self.l, image=like_img,bg=hover_bg) #0 means like
            self.like_image_label.bind('<Button-1>',lambda a:self.like_unlike(self.msg.id)) 
            #like_image_list[msg.id] = like_image_label
            
        
        if self.msg.retweeted:
            self.retweet_no  = 1 # 1 means to unretweet
            retweet_img = PIL.Image.open('retweet_done.png')
            retweet_img = ImageTk.PhotoImage(retweet_img)
            retweet_img_canvas =  Canvas(self.l,width=24,height=24,bg=hover_bg)
            retweet_img_canvas.image = retweet_img
            #retweet_img_canvas.create_image(0,0,anchor='nw',image=retweet_img)
            self.retweet_img_label = Label(self.l, image=retweet_img,bg=hover_bg)
            self.retweet_img_label.bind('<Button-1>',lambda a:self.re_unretweet(self.msg.id))
        else:
            self.retweet_no  = 0 #0 means to retweet
            retweet_img = PIL.Image.open('retweet_undone.png')
            retweet_img = ImageTk.PhotoImage(retweet_img)
            retweet_img_canvas =  Canvas(self.l,width=24,height=24,bg=hover_bg)
            retweet_img_canvas.image = retweet_img
            #retweet_img_canvas.create_image(0,0,anchor='nw',image=retweet_img)
            self.retweet_img_label = Label(self.l, image=retweet_img,bg=hover_bg)
            self.retweet_img_label.bind('<Button-1>',lambda a:self.re_unretweet(self.msg.id))
        
        time = self.msg.created_at
        self.tweet_time = time.strftime('%d/%m/%y')
        self.lb_time = Label(self.l,text = 'Tweeted on: '+self.tweet_time,bg=hover_bg,fg='#918a83')
        
    def display_comp(self):
        self.l.pack(side=TOP,pady=5,anchor= 'w',padx=15 )
        self.profile_img_label.grid(row=0,column=0,rowspan=2)
        self.tweet_msg.grid(row=0,column=1,rowspan=2,columnspan=4,padx=15)
        self.like_image_label.grid(row=2,column=1)
        self.retweet_img_label.grid(row=2,column=2)
        self.lb_time.grid(row=2,column=3)
    
    def re_unretweet(self,mid):
        if self.retweet_no == 1:
            #print('inside Already favorite',mid)
            api.unretweet(mid)
            retweet_img = PIL.Image.open('retweet_undone.png')
            retweet_img = ImageTk.PhotoImage(retweet_img)
            retweet_img_canvas =  Canvas(self.l,width=24,height=24,bg=hover_bg)
            retweet_img_canvas.image = retweet_img
            self.retweet_img_label.configure(image=retweet_img)
            self.retweet_no = 0
            #like_image_list[mid].configure(image=like_img)
        else:
            #print('inside Not favorite',mid)
            api.retweet(mid)
            retweet_img = PIL.Image.open('retweet_done.png')
            retweet_img = ImageTk.PhotoImage(retweet_img)
            retweet_img_canvas =  Canvas(self.l,width=24,height=24,bg=hover_bg)
            retweet_img_canvas.image = retweet_img
            self.retweet_img_label.configure(image=retweet_img)
            self.retweet_no = 1
            #like_image_list[mid].configure(image=like_img)
    
    
    def like_unlike(self,mid):
    #lobal like_image_label
    #print(mid)
        #for keys in like_image_list.keys():
            #if keys == mid:
        if self.no == 1:
            #print('inside Already favorite',mid)
            api.destroy_favorite(mid)
            like_img = PIL.Image.open('unlike.png')
            like_img = ImageTk.PhotoImage(like_img)
            like_img_canvas =  Canvas(self.l,width=24,height=24,bg=hover_bg)
            like_img_canvas.image = like_img
            self.like_image_label.configure(image=like_img)
            self.no = 0
            #like_image_list[mid].configure(image=like_img)
        else:
            #print('inside Not favorite',mid)
            api.create_favorite(mid)
            like_img = PIL.Image.open('like.png')
            like_img = ImageTk.PhotoImage(like_img)
            like_img_canvas =  Canvas(self.l,width=24,height=24,bg=hover_bg)
            like_img_canvas.image = like_img
            self.like_image_label.configure(image=like_img)
            self.no = 1
            #like_image_list[mid].configure(image=like_img)
    
def display_tweets(timeline):
    pass
def new_screen(last_count,my_timeline):
    unpack_others()
    start_count= last_count + 1
    for i, msg in enumerate(my_timeline):
        if i<=last_count:
            continue
        else:
            download_image_read_tweets(msg.user.profile_image_url,start_count)
            box = tweet_box(msg,start_count)
            start_count = start_count + 1
            if i - 4 == last_count:
                next_button = Button(rightframe,text='Next>>',bg=hover_bg,
                                 fg='#fff',relief=RAISED,font=('Timesnew Roman',14),
                                     command= lambda:new_screen(i,my_timeline))
                next_button.pack(side='right')
                prev_button = Button(rightframe,text='<<Prev',bg=hover_bg,
                                 fg='#fff',relief=RAISED,font=('Timesnew Roman',14),
                                     command=lambda:prev_screen(i+1,my_timeline))
                prev_button.pack(side='right',padx=20)
                return
def prev_screen(last_count,my_timeline):
    unpack_others()
    start_count= last_count - 8
    for i, msg in enumerate(my_timeline):
        if i<start_count:
            continue
        else:
            download_image_read_tweets(msg.user.profile_image_url,start_count)
            box = tweet_box(msg,start_count)
            start_count = start_count + 1
            if i - 3 == last_count - 8:
                next_button = Button(rightframe,text='Next>>',bg=hover_bg,
                                 fg='#fff',relief=RAISED,font=('Timesnew Roman',14),
                                     command= lambda:new_screen(i,my_timeline))
                next_button.pack(side='right')
                prev_button = Button(rightframe,text='<<Prev',bg=hover_bg,
                                 fg='#fff',relief=RAISED,font=('Timesnew Roman',14),
                                     command=lambda:prev_screen(i+1,my_timeline))
                prev_button.pack(side='right',padx=20)
                return
    
def read_tweet():
    global flag_pressed_read
    global flag_pressed_follow
    flag_pressed_read=True
    flag_pressed_follow=False
    Read_tweet.configure(bg=hover_bg)
    following.configure(bg=leave_bg)
    unpack_others()
    my_timeline = api.home_timeline()
    #display_tweets(my_timeline)
    count=0
    for i,msg in enumerate(my_timeline):
        download_image_read_tweets(msg.user.profile_image_url,count)
        box = tweet_box(msg,count)
        
        if i==3: # display only 4 tweets in a screen
            next_button = Button(rightframe,text='Next>>',bg=hover_bg,
                                 fg='#fff',relief=RAISED,font=('Timesnew Roman',14),command= lambda:new_screen(count,my_timeline))
            next_button.pack(side='right')
            prev_button = Button(rightframe,text='<<Prev',bg=hover_bg,
                                 fg='#fff',relief=RAISED,font=('Timesnew Roman',14),command=lambda:new_screen(count,my_timeline))
            prev_button.pack(side='right',padx=20)
            return
        count = count+1
    #for i in like_image_list.keys():
    #    print(i)
    
following = Button(leftframe,text='Show Following',width=15,bg='#fca503',
                   fg='#fff',font=('Bahnschrift Light SemiCondensed',16),relief=FLAT,command=show_following)
following.grid(row=0,column=0,pady=(15,0))
following.bind('<Enter>',lambda x:hover(1))
following.bind('<Leave>',lambda x:leave(1))

Read_tweet = Button(leftframe,text='Read Tweets',width=15,bg='#fca503',
                    fg='#fff',font=('Bahnschrift Light SemiCondensed',16),relief=FLAT,command=read_tweet)
Read_tweet.grid(row=1,column=0)
Read_tweet.bind('<Enter>',lambda x:hover(2))
Read_tweet.bind('<Leave>',lambda x:leave(2))

search_tweet = Button(leftframe,text='Search Tweets',width=15,bg='#fca503',fg='#fff',font=('Bahnschrift Light SemiCondensed',16),relief=FLAT)
search_tweet.grid(row=2,column=0)
search_tweet.bind('<Enter>',lambda x:hover(3))
search_tweet.bind('<Leave>',lambda x:leave(3))

#for i,wid in enumerate(leftframe.winfo_children()):    
#    #print(wid.winfo_class())
#    wid.bind('<Enter>',lambda x:hover(wid))
#    wid.bind('<Leave>',lambda x:leave(wid))

root.mainloop()