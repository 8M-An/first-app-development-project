from flask import Flask, request
from flask import render_template,redirect,url_for
from flask import current_app as app
from application.models import Users,Decks,Cards,Globalcards
from application.database import db
import datetime
import random

#signup
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    if request.method=='POST':
        uname=request.form.get('uname')
        psw=request.form.get('psw')
        check_user=Users.query.filter(Users.username==uname).first()
        if check_user:
            return render_template('uname_exists.html')
        check_user1=Users.query.filter(Users.password==psw).first()
        if check_user1:
            k=1
            return render_template('psw_exists.html',key=k)
        user=Users(username=uname,password=psw)
        db.session.add(user)
        db.session.commit()
        user1=Users.query.filter(Users.username==uname,Users.password==psw).first()
        user_id1=user1.user_id

        deck=Decks(deck_name='Hindi',user_id=user_id1)
        db.session.add(deck)
        db.session.commit()
        gcards=Globalcards.query.filter(Globalcards.gdeck_name==deck.deck_name).all()
        for i in gcards:
            card=Cards(deck_id=deck.deck_id,front=i.gfront,back=i.gback,difficulty=i.gdifficulty)
            db.session.add(card)
            db.session.commit()
        deck1=Decks(deck_name='Telugu',user_id=user_id1)
        db.session.add(deck1)
        db.session.commit()
        gcards1=Globalcards.query.filter(Globalcards.gdeck_name==deck1.deck_name).all()
        for i in gcards1:
            card1=Cards(deck_id=deck1.deck_id,front=i.gfront,back=i.gback,difficulty=i.gdifficulty)
            db.session.add(card1)
            db.session.commit()
        return redirect(url_for('dashboard',user_id=user_id1))


#user login
@app.route('/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        username=request.form.get('uname')
        password=request.form.get('psw')
        user=Users.query.filter(Users.username==username,Users.password==password).first()
        if user:
            user_id1=user.user_id
            return redirect(url_for('dashboard',user_id=user_id1))
        else:
            ykey=0
            user_uname=Users.query.filter(Users.username==username).first()
            user_psw=Users.query.filter(Users.password==password).first()
            if user_uname:
                ykey=1
                return render_template('loginfail.html',key=ykey)
            elif user_psw:
                ykey=2
                return render_template('loginfail.html',key=ykey)
            else:
                ykey=3
                return render_template('loginfail.html',key=ykey)

#forgot password
@app.route('/login/reset',methods=['GET','POST'])
def reset_password():
    if request.method=='GET':
        return render_template('forgot_password.html')
    if request.method=='POST':
        uname=request.form.get('uname')
        user=Users.query.filter(Users.username==uname).first()
        if user:
            userid=user.user_id
            path='/login/reset/{0}'.format(userid)
            return redirect(path)
        else:
            return render_template('no_user.html',username=uname)

@app.route('/login/reset/<int:user_id>',methods=['GET','POST'])
def new_password(user_id):
    if request.method=='GET':
        return render_template('forgot_password1.html',userid=user_id)
    if request.method=='POST':
        new_psw=request.form.get('psw')
        check_user1=Users.query.filter(Users.password==new_psw).first()
        if check_user1:
            k=2
            return render_template('psw_exists.html',key=k,userid=user_id)
        user=Users.query.filter(Users.user_id==user_id).first()
        user.password=new_psw
        db.session.commit()
        path='/dashboard/{0}'.format(user.user_id)
        return render_template('changed_password.html')


#dashboard
@app.route('/dashboard/<int:user_id>',methods=['GET','POST'])
def dashboard(user_id):
    info=Decks.query.filter(Decks.user_id==user_id).all()
    user=Users.query.filter(Users.user_id==user_id).first()
    return render_template('dashboard.html',info=info,userid2=user_id,name=user.username)

#change deck name
@app.route('/dashboard/<int:user_id>/<int:deck_id>/change/name', methods=['GET','POST'])
def change_name(user_id,deck_id):
    if request.method=='GET':
        deck=Decks.query.filter(Decks.deck_id==deck_id).first()
        return render_template('change_name.html',deck=deck)
    if request.method=='POST':
        deck_name=request.form.get('deck_name')
        deck=Decks.query.filter(Decks.deck_id==deck_id).first()
        if deck_name is not None:
            deck.deck_name=deck_name
            db.session.commit()
            path='/dashboard/{0}'.format(user_id)
            return redirect(path)
        else:
            return('change_name.html')

#global variables
card=[]
key=1
answers={}

#deck_review
@app.route('/dashboard/<int:user_id>/<int:deck_id>', methods=['GET'])
def deck(user_id,deck_id):
    global card
    global key
    if key==1:
        card.clear()
        card1=Cards.query.filter(Cards.deck_id==deck_id).all()
        cardh=[]
        cardm=[]
        carde=[]
        cardn=[]
        for i in card1:
            if i.difficulty=='Hard':
                cardh.append(i)
                random.shuffle(cardh)
        card.extend(cardh)

        for i in card1:
            if i.difficulty=='Medium':
                cardm.append(i)
                random.shuffle(cardm)

        card.extend(cardm)
        for i in card1:
            if i.difficulty=='Easy':
                carde.append(i)
                random.shuffle(carde)

        card.extend(carde)
        for i in card1:
            if i not in card:
                cardn.append(i)
                random.shuffle(cardn)
        card.extend(cardn)


    if card!=[]:
        k=card[0]
        app.logger.info(card)
        deck=Decks.query.filter(Decks.deck_id==deck_id).first()
        if len(card)==1:
            key3=1
        else:
            key3=2
        return render_template('quiz.html',i=k,user_id=user_id,deck_id=deck_id,deck_name=deck.deck_name,key=key3)
    else:
        return render_template('empty.html',userid=user_id,deckid=deck_id)


#quiz continuation
@app.route('/dashboard/<int:user_id>/<int:deck_id>/<int:fc_id>',methods=['GET','POST'])
def deck2(user_id,deck_id,fc_id):
    global card
    global key
    if request.method=='POST':
        key=0
        a={}
        a[fc_id]=request.form.get('ans')
        d=request.form.get('difficulty')
        new_card=Cards.query.filter(Cards.fc_id==fc_id).first()
        if d is not None:
            new_card.difficulty=d
        db.session.commit()
        if card!=[]:
            card.pop(0)
        app.logger.info(card)
        answers.update(a)
        app.logger.info(answers)
        if card!=[]:
            path='/dashboard/{0}/{1}'.format(user_id,deck_id)
            return redirect(path)
        else:
            right=0
            total=0
            score=0
            key=1
            check_cards=Cards.query.filter(Cards.deck_id==deck_id).all()
            for i in check_cards:
                total+=1
                if i.fc_id in answers:
                    i1=i.back.lower()
                    i2=answers[i.fc_id].lower()
                    app.logger.info(i1,i2)
                    if i2==i1:
                        right+=1
            score1=(right/total)*100
            score=round(score1,2)
            reviewed=datetime.datetime.now()
            deck=Decks.query.filter(Decks.deck_id==deck_id).first()
            deck.Score=score
            deck.last_reviewed=reviewed
            db.session.commit()
            qa=[]
            cardo=Cards.query.filter(Cards.deck_id==deck_id).all()
            app.logger.info(cardo)
            for i in cardo:
                for j in answers:
                    if j==i.fc_id:
                        qa.append([i,answers[j]])
            return render_template('result.html',total=total,score=score,right=right,userid=user_id, qa=qa)

#create deck
@app.route('/dashboard/<int:user_id>/create',methods=['GET','POST'])
def create(user_id):
    if request.method=='GET':
        return render_template('create.html',userid=user_id)
    if request.method=='POST':
        deckname=request.form.get('deck_name')
        d=Decks(deck_name=deckname,user_id=user_id)
        db.session.add(d)
        db.session.commit()
        path='/dashboard/{0}'.format(user_id)
        return redirect(path)

#update deck
@app.route('/dashboard/<int:user_id>/<int:deck_id>/update', methods=['GET','POST'])
def update(user_id,deck_id):
    if request.method=='GET':
        return render_template('updateoptions.html',userid=user_id,deckid=deck_id)

#update deck continuation
@app.route('/dashboard/<int:user_id>/<int:deck_id>/add/cards', methods=['GET','POST'])
def addcards(user_id,deck_id):
    if request.method=='GET':
        return render_template('newcard.html',userid=user_id,deckid=deck_id)
    if request.method=='POST':
        front=request.form.get('front')
        back=request.form.get('back')
        difficulty=request.form.get('difficulty')
        card=Cards(front=front,back=back,deck_id=deck_id,difficulty=difficulty)
        db.session.add(card)
        db.session.commit()
        deck=Decks.query.filter(Decks.deck_id==deck_id).first()
        deck_name=deck.deck_name
        deck_id=deck.deck_id
        return render_template('added_card_successfully.html',userid=user_id,deck_name=deck_name,deckid=deck_id)

#update continuation: editing existing cards
@app.route('/dashboard/<int:user_id>/<int:deck_id>/choose/card', methods=['GET','POST'])
def choosecard(user_id,deck_id):
    if request.method=='GET':
        cards=Cards.query.filter(Cards.deck_id==deck_id).all()
        return render_template('choosecardtoedit.html',userid=user_id,deckid=deck_id,cards=cards)

@app.route('/dashboard/<int:user_id>/<int:deck_id>/<int:fc_id>/edit/card', methods=['GET','POST'])
def edit_card(user_id,deck_id,fc_id):
    if request.method=='GET':
        card=Cards.query.filter(Cards.fc_id==fc_id).first()
        return render_template('editcard.html',deckid=deck_id,fcid=fc_id,front=card.front,back=card.back,userid=user_id)
    if request.method=='POST':
        front=request.form.get('front')
        back=request.form.get('back')
        difficulty=request.form.get('difficulty')
        card=Cards.query.filter(Cards.fc_id==fc_id).first()
        card.front=front
        card.back=back
        card.difficulty=difficulty
        db.session.commit()
        path='/dashboard/{0}/{1}/choose/card'.format(user_id,deck_id)
        return redirect(path)

#update continuation:remove card:confirmation
@app.route('/dashboard/<int:user_id>/<int:deck_id>/<int:fc_id>/delete/card/sure')
def are_you_sure_card(user_id,deck_id,fc_id):
    deck=Decks.query.filter(Decks.deck_id==deck_id).first()
    card=Cards.query.filter(Cards.fc_id==fc_id).first()
    return render_template('delete_card_sure.html',deck=deck,card=card)

#update continuation:remove card:delete
@app.route('/dashboard/<int:user_id>/<int:deck_id>/<int:fc_id>/delete/card')
def delete_card(user_id,deck_id,fc_id):
    if request.method=='GET':
        card=Cards.query.filter(Cards.fc_id==fc_id).first()
        db.session.delete(card)
        db.session.commit()
        path='/dashboard/{0}/{1}/choose/card'.format(user_id,deck_id)
        return redirect(path)

#remove deck:confirmation
@app.route('/dashboard/<int:user_id>/<int:deck_id>/delete/sure')
def are_you_sure(user_id,deck_id):
    deck=Decks.query.filter(Decks.deck_id==deck_id).first()
    return render_template('delete_deck_sure.html',deck=deck)

#remove deck continuation:delete
@app.route('/dashboard/<int:user_id>/<int:deck_id>/delete')
def delete_deck(user_id,deck_id):
    flashcard=Cards.query.filter(Cards.deck_id==deck_id).all()
    for i in flashcard:
        db.session.delete(i)
        db.session.commit()
    deck=Decks.query.filter(Decks.deck_id==deck_id).first()
    db.session.delete(deck)
    db.session.commit()
    path='/dashboard/{0}'.format(user_id)
    return redirect(path)

#display all cards
@app.route('/dashboard/<int:user_id>/<int:deck_id>/show/cards')
def show_cards(user_id,deck_id):
    deck=Decks.query.filter(Decks.deck_id==deck_id).first()
    cards=Cards.query.filter(Cards.deck_id==deck_id).all()
    return render_template('show_cards.html',cards=cards,deck=deck)
